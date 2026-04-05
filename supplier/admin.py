from django.contrib import admin

from supplier.models import Supplier, SupplierDocument


class DocumentInline(admin.TabularInline):
    model = SupplierDocument


class SupplierDocumentAdmin(admin.ModelAdmin):
    model = SupplierDocument
    fields = ['document', 'id_supplier', 'name', 'number', 'issued_date', 'expiry_date', 'is_valid', 'notes']
    list_display = ('name', 'number', 'issued_date', 'expiry_date', 'is_valid', 'notes')


class SupplierAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'legal_entity', 'inn', 'created_at', 'updated_at', 'kpp', 'contact_person',
                    'email', 'phone', 'bank_name')
    list_filter = ('legal_entity', 'created_at', 'bank_name')
    fields = ('short_name', 'legal_entity', 'user', 'inn', 'kpp', 'contact_person',
              'email', 'phone', 'bank_name')
    inlines = [DocumentInline]
    search_fields = ('short_name', 'legal_entity', 'bank_name')


admin.site.register(Supplier, SupplierAdmin)
admin.site.register(SupplierDocument, SupplierDocumentAdmin)
