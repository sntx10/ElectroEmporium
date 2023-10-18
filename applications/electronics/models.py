from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    title = models.SlugField(primary_key=True, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)


class Electronic(models.Model):
    STATUS = (
        ('on_sale', 'on sale'),
        ('out_of_stock', 'out of stock')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='electronics')
    category = models.ForeignKey(Category, related_name='electronics', on_delete=models.CASCADE)
    title = models.CharField(max_length=88)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    amount = models.PositiveIntegerField(default=10)
    status = models.CharField(max_length=50, choices=STATUS, default='on_sale')
    orders_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Image(models.Model):
    electronic = models.ForeignKey(Electronic, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/')


class Characteristic(models.Model):
    electronic = models.OneToOneField(Electronic, on_delete=models.CASCADE, related_name='electronics')
    thickness = models.CharField(max_length=128, null=True, blank=True)
    display = models.CharField(max_length=128, null=True, blank=True)
    processor = models.CharField(max_length=128, null=True, blank=True)
    video = models.CharField(max_length=10, null=True, blank=True)
    memory = models.CharField(max_length=120, null=True, blank=True)
    size = models.CharField(max_length=128, null=True, blank=True)
    weight = models.CharField(max_length=128, null=True, blank=True)


class ParsedElectronic(models.Model):
    title = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)


class RecommendImages(models.Model):
    electronic_recommend = models.ForeignKey(ParsedElectronic, related_name='images', on_delete=models.CASCADE)
    image = models.TextField()
