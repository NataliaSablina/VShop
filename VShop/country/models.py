from django.db import models


class Country(models.Model):
    name = models.CharField(verbose_name='Name', max_length=150, db_index=True)
    currency = models.ForeignKey('Currency', on_delete=models.SET_DEFAULT, default='USD')
    active = models.BooleanField(default=True, null=True, blank=True)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(verbose_name='Name', max_length=150, db_index=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Country', related_name='cities')
    active = models.BooleanField(default=True,null=True, blank=True)

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.name


class Currency(models.Model):
    name = models.CharField(verbose_name='Currency', max_length=10)
    active = models.BooleanField(default=True, null=True, blank=True)

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"

    def __str__(self):
        return self.name

