from django.db import models
from PIL import Image
from django.core.files.storage import default_storage as storage
from PIL import Image, ImageOps


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
    category = models.ForeignKey('Category', null=True,
                                 blank=True, on_delete=models.SET_NULL)
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

    def save(self, *args, **kwargs):
        super(Product,self).save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image)
            print('ok')
            size = 500
            thumb = (500, 500)
            
            method = Image.ANTIALIAS
            img.thumbnail((size,size), method)
            new = ImageOps.fit(img, thumb, method)
            temp = storage.open(self.image.name, "wb")
            new.save(temp)
            print('ok2')
            img.close()
            super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name