from bs4 import BeautifulSoup
import requests as http_requests
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.files.base import ContentFile
from apps.home.models import Product
from apps.home.serializers import ProductSerializer


class ProductsListView(APIView):

    def get(self, request):
        products = Product.objects.order_by("-id")
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ScrapeView(APIView):

    def post(self, request):
        suffix = request.data.get("url", "").strip()
        url = "https://www.everydaybrazil.com/en/collections/" + suffix

        try:
            response = http_requests.get(url, timeout=10)
            response.raise_for_status()
        except Exception as error:
            print(str(error))
            return Response({
                "detail": f"Erro ao acessar a url informada",
                "detail_type": "error",
            }, status=status.HTTP_400_BAD_REQUEST)

        soup = BeautifulSoup(response.text, "html.parser")
        products = soup.select("li.productgrid--item")

        new_products = []
        for product in products:
            try:
                image = f"https:{product.select_one("img.productitem--image-primary").get("src")}"
                description = product.select_one("h2.productitem--title a").get_text().strip()
                brand = product.select_one("span.productitem--vendor a").get_text().strip()
                price = float(product.select_one("div[data-price-container] span.money").get_text().replace("$", "").replace(",", ".").strip())
            except Exception as error:
                print(str(error))
                continue

            product = Product(description=description, brand=brand, price=price)

            try:
                img_response = http_requests.get(image, timeout=10)
                img_response.raise_for_status()
                ext = image.split("?")[0].rsplit(".", 1)[-1]
                product.image.save(
                    f"{description[:30]}.{ext}",
                    ContentFile(img_response.content),
                    save=False,
                )
            except Exception:
                print(str(error))
                continue

            new_products.append(product)

        Product.objects.bulk_create(new_products)
        return Response({
            "detail": f"Foram importados {len(new_products)} produtos",
            "detail_type": "success",
        }, status=status.HTTP_201_CREATED)
