from django.contrib import admin
from mainapp.models import Category,Product,Order,Tag,OldOrders,ProductTags , ProductKNN ,Comment
# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(ProductTags)
admin.site.register(Tag)
admin.site.register(OldOrders)
admin.site.register(ProductKNN)
admin.site.register(Comment)

