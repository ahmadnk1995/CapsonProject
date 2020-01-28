from django.db import models
from django.conf import settings
from django.contrib.auth.models import User,auth
from django.contrib.auth import get_user_model
import os
import sqlite3
import pandas as pd
import recommender

class Category(models.Model):
    image = models.ImageField()
    name = models.CharField(max_length=30)
    description = models.TextField()

    def __str__(self):
        return self.name

class Product(models.Model):
    image = models.ImageField()
    name = models.CharField(max_length=30)
    description = models.TextField()
    price = models.FloatField()
    rate = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    @property
    def neighbors(self):
        nei = ProductKNN.objects.filter(product=self).values_list('neighbor_id', flat=True)
        print(nei)
        print('\n\n')
        products = Product.objects.filter(id__in=nei)    
        return products
        

    def __str__(self):
        return self.name

class ProductKNN(models.Model):

    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    neighbor_id = models.IntegerField()

    @classmethod
    def fill(cls):
        for prod in Product.objects.all():
            neighbors = settings.REC.get(prod.id)
            print(neighbors)
            for nei_id in neighbors:
                obj = ProductKNN(product=prod, neighbor_id=nei_id)
                print('saving ', str(prod.id))
                if (nei_id!=None):
                    obj.save()


class Order(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    date=models.DateField()

    def __str__(self):
        return self.product.name

class Comment(models.Model):
    text=models.TextField()
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    date=models.DateField()

    def __str__(self):
        return self.product.name


class OldOrders(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    date=models.DateField()

    def __str__(self):
        return self.product.name

class Tag(models.Model):
    name=models.CharField(max_length=255)
    def __str__(self):
        return self.name


class ProductTags(models.Model):
    tag = models.ManyToManyField(Tag)
    product = models.OneToOneField(to='Product', primary_key=True, on_delete=models.CASCADE)


    def __str__(self):
        return str(self.pk)


