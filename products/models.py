from django.db import models


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
 
    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=254)
    description = models.TextField()
    available_quantity = models.IntegerField(default=20)
    sold = models.IntegerField(default=0)
    reserved = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(null=True, blank=True)
    euro_shipping = models.BooleanField(default=True)
    l = models.IntegerField(default=20)
    h = models.IntegerField(default=20)
    w = models.IntegerField(default=20)
    weight = models.IntegerField(default=20)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

