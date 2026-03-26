import os
import sys
import subprocess
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from apps.product.models import Product
from apps.product.serializers import ProductSerializer
env = os.environ.copy()
env["PYTHONPATH"] = str(settings.BASE_DIR)
env["DJANGO_SETTINGS_MODULE"] = "core.settings"


class ProductsListView(APIView):

    def get(self, request):
        products = Product.objects.select_related("category").order_by("-id")
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ScrapeView(APIView):

    def post(self, request):
        suffix = request.data.get("url", "").strip()
        if not suffix:
            return Response({
                "detail": "URL não informada",
                "detail_type": "error",
            }, status=status.HTTP_400_BAD_REQUEST)

        process = subprocess.Popen(
            [sys.executable, "-m", "scrapy", "crawl", "everydaybrazil", "-a", f"suffix={suffix}"],
            cwd=settings.BASE_DIR / "apps" / "scrapy",
            env=env,
        )
        process.wait(timeout=120)

        return Response({
            "detail": "Scraping concluído",
            "detail_type": "success",
        }, status=status.HTTP_200_OK)
