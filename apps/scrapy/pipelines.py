import os
import re
import django
import asyncio
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()
import requests
from decimal import Decimal
from django.db.models import Q, Avg, F
from asgiref.sync import sync_to_async
from django.core.files.base import ContentFile
from apps.product.models import Product, ProductCategory


def classify_category(description):
    text = description.lower()
    if re.search(r"\b(rice|arroz)\b", text):
        return ProductCategory.CategoryNames.RICE
    if re.search(r"\b(beans?|feij[aã]o)\b", text):
        return ProductCategory.CategoryNames.BEANS
    return None


def extract_weight_kg(description):
    text = description.lower()
    match = re.search(r"(\d+(?:[.,]\d+)?)\s*(kg|g)", text)
    if not match:
        return None
    value = Decimal(match.group(1).replace(",", "."))
    unit = match.group(2)
    if unit == "g":
        return value / 1000
    return value


def download_image(item):
    try:
        response = requests.get(item["image"], timeout=10)
        response.raise_for_status()
        ext = item["image"].split("?")[0].rsplit(".", 1)[-1]
        return ext, response.content
    except Exception:
        return None, None


class EverydayBrazilPipeline:

    def open_spider(self, spider):
        self.items = []
        self.categories = {}

    async def process_item(self, item, spider):
        self.items.append(item)
        return item

    async def close_spider(self, spider):
        if not self.items:
            return

        # Carrega todas as categorias do banco
        self.categories = await sync_to_async(
            lambda: {category.name: category for category in ProductCategory.objects.all()}
        )()

        # Filtra os produtos que ja existem no banco
        filters = Q()
        for item in self.items:
            filters |= Q(description=item["description"], brand=item["brand"])

        existing = await sync_to_async(
            lambda: set(Product.objects.filter(filters).values_list("description", "brand"))
        )()

        new_items = [item for item in self.items if (item["description"], item["brand"]) not in existing]

        if not new_items:
            return

        # Baixa imagens em paralelo
        image_results = await asyncio.gather(
            *(asyncio.to_thread(download_image, item) for item in new_items)
        )

        # Cria produtos
        products = []
        for item, (ext, img_content) in zip(new_items, image_results):
            category_name = classify_category(item["description"])
            product = Product(
                description=item["description"],
                brand=item["brand"],
                price=item["price"],
                weight_kg=extract_weight_kg(item["description"]),
                category=self.categories.get(category_name),
            )
            if img_content:
                await sync_to_async(product.image.save)(
                    f"{item['description'][:30]}.{ext}",
                    ContentFile(img_content),
                    save=False,
                )
            products.append(product)

        await sync_to_async(Product.objects.bulk_create)(products)

        # Calcula preço medio por kg
        for category_name in (ProductCategory.CategoryNames.RICE, ProductCategory.CategoryNames.BEANS):
            avg = await sync_to_async(
                lambda name=category_name: Product.objects
                .filter(category__name=name, weight_kg__isnull=False)
                .aggregate(avg=Avg(F("price") / F("weight_kg")))["avg"]
            )()

            if avg is not None:
                await sync_to_async(
                    lambda name=category_name, val=avg: ProductCategory.objects
                    .filter(name=name)
                    .update(average_price_kg=round(val, 2))
                )()
