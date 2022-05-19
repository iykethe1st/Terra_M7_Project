from django.contrib import admin

from .models import Category, Product, ProductImage, ProductReview, Subject

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductReview)
admin.site.register(Subject)