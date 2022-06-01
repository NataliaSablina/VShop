from django.db import models
from Categories.models import Category, Product


class PromoCode(models.Model):
    name = models.CharField(verbose_name='Name', max_length=200)
    expire_date = models.DateField(verbose_name='Expire Data')
    sailing_percent = models.IntegerField(verbose_name='Sailing Percent')
    highlight = models.TextField(verbose_name='Highlight')
    creation = models.DateTimeField(auto_now=False, auto_now_add=True, null=True, verbose_name='Creation')
    review = models.IntegerField(verbose_name="Views", null=True, blank=True)
    active = models.BooleanField(default=True, null=True, blank=True)
    photo = models.ImageField(upload_to='promos/%Y/%m/%d/', null=True, blank=True, verbose_name='Photo')
    terms_conditions = models.TextField(verbose_name="Terms&conditions", null=True, blank=True)

    class Meta:
        verbose_name = 'PromoCode'
        verbose_name_plural = 'PromoCode'
        ordering = ['creation']

    def __str__(self):
        return self.name
