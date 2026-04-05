from rest_framework import serializers

from supplier.models import Supplier


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(SupplierSerializer, self).__init__(many=many, *args, **kwargs)

    def validate_email(self, email):
        if Supplier.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email already exists')
        return email

    def validate_phone(self, phone):
        if Supplier.objects.filter(phone=phone).exists():
            raise serializers.ValidationError('Phone already exists')
        return phone

    def validate_inn(self, inn):
        if Supplier.objects.filter(inn=inn).exists():
            raise serializers.ValidationError('Inn already exists')
        return inn

    def validate_name(self, name):
        if Supplier.objects.filter(name=name).exists():
            raise serializers.ValidationError('Name already exists')
        return name

    def validate_short_name(self, short_name):
        if Supplier.objects.filter(short_name=short_name).exists():
            raise serializers.ValidationError('Short name already exists')
        return short_name

