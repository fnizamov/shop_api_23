from rest_framework import serializers
from .models import Product, ProductImage, Category

from apps.review.serializers import CommentSerializer

class ProductSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Product
        fields = '__all__'

    def validate_price(self, price):
        if price < 0:
            raise serializers.ValidationError('цена не может быть отрицательной')
        return price

    def validate_quantity(self, quantity):
        if quantity < 0:
            raise serializers.ValidationError('количество не может быть отрицательной')
        return quantity

    def validate(self, attrs):
        user = self.context['request'].user
        attrs['user'] = user
        return attrs

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        rep['comments_count'] = instance.comments.all().count()
        return rep

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('image', 'title', 'price', 'in_stock', 'slug')


    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['comments_count'] = instance.comments.all().count()
        return rep

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'