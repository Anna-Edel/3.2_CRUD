from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from stocks_products.logistic.models import Product, Stock
from stocks_products.logistic.serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # при необходимости добавьте параметры фильтрации
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description']


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    # при необходимости добавьте параметры фильтрации
    filter_backends = [SearchFilter]
    filterset_fields = ['products',]
    search_fields = ['products__title', 'products__description',]


