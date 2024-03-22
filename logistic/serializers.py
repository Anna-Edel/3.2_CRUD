from rest_framework import serializers

from stocks_products.logistic.models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields =['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['produkt', 'quantity', 'price']



class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)
    class Meta:
        model = Stock
        fields = ['id' ,'address', 'products']

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = super().create(validated_data)

        # здесь вам надо заполнить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions
        for sp in positions:
            StockProduct.objects.create(stock=stock, product=sp['product'], price=sp['price'], quantity = sp['quantity'])
        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)

        # здесь вам надо обновить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions
        for sp in positions:
            # StockProduct.objects.update_or_create(stock=stock, product=sp['product'], price=sp['price'], quantity = sp['quantity'])
            StockProduct.objects.update_or_create(stock=stock, product=sp['product'], defaults={'price': 'price', 'quantity':'quantity'})
        return stock
