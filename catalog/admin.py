from django.contrib import admin

from catalog.models import AutoParts, Subcategories, GlobalCategory, ModelCar, AutoPartImage


class Sub(admin.StackedInline):
    model = Subcategories


class GlobaleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_active')
    list_filter = ('name', 'description', 'is_active', 'created_at', 'updated_at')
    fields = ['name', 'description', 'is_active']
    inlines = [
        Sub
    ]


class SubAdmin(admin.ModelAdmin):
    list_display = ('name', 'global_category', 'created_at', 'updated_at', 'is_active')
    list_filter = ('name', 'global_category', 'created_at', 'updated_at', 'is_active')
    fields = ['name', 'global_category', 'is_active']


class CarAdmin(admin.ModelAdmin):
    list_display = ('brand_car', 'model', 'generation', 'created_at', 'updated_at', 'fuel_tank', 'body_type')
    list_filter = ('brand_car', 'model', 'generation', 'updated_at', 'fuel_tank', 'body_type')
    fields = ('brand_car', 'model', 'generation', 'fuel_tank', 'body_type', 'year_start', 'year_end')


class AutoPartsAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'cost_price', 'selling_price', 'quantity', 'subcategory', 'is_available',
                    'created_at', 'supplier',
                    'updated_at')
    list_filter = ('brand', 'cost_price', 'is_available', 'created_at', 'updated_at',
                   'quantity')
    fields = ('name', 'brand', 'cost_price', 'selling_price', 'subcategory', 'quantity', 'is_available',
              'documents', 'supplier', 'warranty', 'condition', 'features')
    search_fields = ('name', 'supplier')


class AutoPartImageAdmin(admin.ModelAdmin):
    list_display = ('image', 'auto_part')
    fields = ('image', 'auto_part')
    list_filter = ('auto_part',)


admin.site.register(Subcategories, SubAdmin)
admin.site.register(GlobalCategory, GlobaleAdmin)
admin.site.register(ModelCar, CarAdmin)
admin.site.register(AutoParts, AutoPartsAdmin)
admin.site.register(AutoPartImage, AutoPartImageAdmin)