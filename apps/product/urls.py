from django.urls import path
from apps.product import views, api


urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("api/products", api.ProductsListView.as_view(), name="products"),
    path("api/scrape", api.ScrapeView.as_view(), name="scrape"),
]
