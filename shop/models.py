from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from home.models import ShopProfile


class Category(models.Model):
    name = models.CharField(max_length=200,db_index=True)
    slug = models.SlugField(max_length=250,db_index=True,unique=True)
    creator = models.ForeignKey(ShopProfile,related_name='mwenyewe',on_delete=models.CASCADE)
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',args=[self.slug])
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
    
class Product(models.Model):
    category = models.ForeignKey(Category,related_name='products',on_delete=models.CASCADE)
    shop = models.ForeignKey(ShopProfile,related_name='owner',on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=250, db_index=True,unique=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d',blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    old_cost = models.DecimalField(max_digits=10, decimal_places=2,blank=True,default=0)
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),) 
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)
    def product_detail(self):
        return reverse('shop:product_detail',args=[self.id, self.slug])
    def product_price(self):
        return reverse('shop:update_price',args=[self.id, self.slug])
    def product_update(self):
        return reverse('shop:update_product',args=[self.id, self.slug])
    def product_value(self):
        return str(self.stock * self.cost)
