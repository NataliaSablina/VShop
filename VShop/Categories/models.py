from django.db import models


class Categories(models.Model):
    name = models.CharField(verbose_name='Name', max_length=150, db_index=True)

    class Meta:
        verbose_name = 'Category'
        verbose_plural_name = 'Categories'

    def __str__(self):
        return self.name



