from django.contrib import admin

from product.models import Category, Product, Images


# Register your models here.
class ProductImagesInline(admin.TabularInline):
    model = Images
    extra = 5
    readonly_fields = ['image_tag']

class CategoryAdmin(admin.ModelAdmin):
    # fields = ['title', 'status']
    list_display = ['title','status']
    list_filter = ['status']
admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    # fields = ['title', 'status']
    list_display = ['title', 'image_tag', 'status']
    list_filter = ['status','category']
    readonly_fields = ('image_tag',)
    inlines = [ProductImagesInline]
admin.site.register(Product, ProductAdmin)




# resimlerin adminde gösterilmesi için
class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title','product', 'image_tag']
    readonly_fields = ['image_tag']
admin.site.register(Images, ImagesAdmin)