from django.db import models

from supplier.models import Supplier


class GlobalCategory(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'


class Subcategories(models.Model):
    name = models.CharField(max_length=60)
    global_category = models.ForeignKey(GlobalCategory, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ModelCar(models.Model):
    brand_car = models.CharField(max_length=60)
    model = models.CharField(max_length=60)
    generation = models.CharField(max_length=60)
    year_start = models.IntegerField()
    year_end = models.IntegerField()
    body_type = models.CharField(max_length=60)
    engine = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    fuel_tank = models.IntegerField()

    def __str__(self):
        return f'{self.brand_car} {self.model}'


class AutoParts(models.Model):
    name = models.CharField(max_length=60)
    brand = models.CharField(max_length=60)
    subcategory = models.ForeignKey(Subcategories, on_delete=models.CASCADE, blank=True, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    cost_price = models.DecimalField(max_digits=6, decimal_places=2)
    selling_price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    features = models.TextField()
    short_description = models.TextField()
    documents = models.FileField(upload_to='documents/', blank=True, null=True)
    warranty = models.CharField(max_length=20)
    condition = models.CharField(max_length=20)
    image = models.ImageField(upload_to='auto_parts/%Y/%m/%d/', blank=True, null=True)
    cars = models.ManyToManyField(ModelCar, blank=True, related_name='parts')

    def __str__(self):
        return self.name


class AutoPartImage(models.Model):
    auto_part = models.ForeignKey(
        'AutoParts',
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Товар'
    )
    image = models.ImageField(
        upload_to='auto_parts/%Y/%m/%d/'
    )
