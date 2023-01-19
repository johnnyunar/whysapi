from django.contrib import admin

from core.models import (
    AttributeName,
    AttributeValue,
    Attribute,
    Product,
    ProductAttribute,
    Image,
    ProductImage,
    Catalog,
)


@admin.register(AttributeName)
class AttributeNameAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "display")


@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ("value",)


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ("name", "value")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "currency", "is_published")


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ("product", "attribute")


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("name", "url")


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "image")


@admin.register(Catalog)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("name",)
