from django.db import models

from authentication.models import CustomUser


class Supplier(models.Model):
    type_of_legal_entity = [
        ('ООО', 'ООО'),
        ('ИП', 'ИП'),
        ('АО', 'АО')
    ]
    name = models.CharField(max_length=60)
    short_name = models.CharField(max_length=20)
    legal_entity = models.CharField(max_length=4, choices=type_of_legal_entity)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    inn = models.CharField(max_length=12)
    kpp = models.CharField(max_length=9)
    contact_person = models.CharField(max_length=40)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    bank_name = models.CharField(max_length=60)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='supplier', null=True, blank=True)

    def __str__(self):
        return self.short_name


class SupplierDocument(models.Model):
    document = models.FileField(upload_to='Supplier_documents/%Y/%m/%d')
    id_supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=255,
        verbose_name='Название документа'
    )

    number = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Номер документа'
    )

    issued_date = models.DateField(
        null=True, blank=True,
        verbose_name='Дата выдачи'
    )

    expiry_date = models.DateField(
        null=True, blank=True,
        verbose_name='Срок действия'
    )

    is_valid = models.BooleanField(
        default=True,
        verbose_name='Действителен'
    )

    notes = models.TextField(
        blank=True,
        verbose_name='Примечания'
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Загружен'
    )

    def __str__(self):
        return self.name
