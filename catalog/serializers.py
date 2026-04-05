from rest_framework import serializers

from catalog.models import AutoParts, GlobalCategory, Subcategories, ModelCar, AutoPartImage


class ModelCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelCar
        fields = ('brand_car',)


class AutoPartImageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('image',)
        model = AutoPartImage


class AutoPartsSerializer(serializers.ModelSerializer):
    images = AutoPartImageSerializer(many=True, read_only=True)
    upload_images = serializers.ListField(
        required=False,
        child=serializers.ImageField(max_length=None, use_url=True),
        write_only=True)
    cars = serializers.PrimaryKeyRelatedField(write_only=True, many=True, queryset=ModelCar.objects.all())

    car_s = ModelCarSerializer(many=True, read_only=True, source='cars')

    class Meta:
        fields = [
            'id',
            'name',
            'brand',
            'subcategory',
            'supplier',
            'cars',
            'cost_price',
            'selling_price',
            'quantity',
            'features',
            'short_description',
            'documents',
            'warranty',
            'condition',
            'image',
            'upload_images',
            'images',
            'car_s'
        ]
        model = AutoParts


class AutoPartsPaginationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoParts
        fields = ['id', 'name', 'brand', 'selling_price', 'quantity', 'short_description', 'warranty', 'condition']


class GlobalCategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id','name', 'description', 'image')
        model = GlobalCategory


class SubcategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name','id')
        model = Subcategories
