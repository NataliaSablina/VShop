from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from country.models import City
from User.models import User


class Category(models.Model):
    name = models.CharField(verbose_name='Name', max_length=150, db_index=True)
    creation_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Creation Time')
    changing_time = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Changing Time')
    city = models.ManyToManyField(City, verbose_name='City', related_name='city')
    photo = models.ImageField(upload_to='categories/%Y/%m/%d/', null=True, blank=True)
    active = models.BooleanField(default=True, null=True, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['creation_time']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(verbose_name='Name', max_length=150, db_index=True)
    price = models.FloatField(verbose_name='Price')
    creation = models.DateTimeField(auto_now=False, auto_now_add=True, null=True, verbose_name='Creation')
    changing = models.DateTimeField(auto_now=True, auto_now_add=False, null=True, verbose_name='Changing')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Category',
                                 related_name="product_category")
    promo_code = models.ForeignKey('promocode.PromoCode', on_delete=models.SET_NULL, verbose_name='Promo Code',
                                   null=True, blank=True, related_name="product_promo")
    review = models.IntegerField(verbose_name="Views", default=0)
    product_details = models.TextField(verbose_name='Product Details')
    delivery = models.ForeignKey('DeliveryType', on_delete=models.SET_DEFAULT, default='Free')
    active = models.BooleanField(default=True, null=True, blank=True)
    photo = models.ImageField(upload_to='products/%Y/%m/%d/', null=True, blank=True, verbose_name='Photo')

    def count_average_rating(self):
        pass

    @property
    def like_amount(self):
        return len(self.upr.filter(like=True))

    @property
    def views_amount(self):
        return len(self.upr.filter(view=True))

    # def counter(self):
    #     self.review += 1
    #     return self.review

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['creation']

    def __str__(self):
        return self.name


class Mark(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name='Product')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    creation = models.DateTimeField(auto_now=False, auto_now_add=True, null=True, verbose_name='Creation')
    value = models.PositiveSmallIntegerField(validators=[MaxValueValidator(100), MinValueValidator(1)],
                                             verbose_name='Mark')

    class Meta:
        verbose_name = 'Mark'
        verbose_name_plural = 'Marks'
        ordering = ['creation']


class ProductPhoto(models.Model):
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', null=True, blank=True, verbose_name='Photo')
    product = models.ManyToManyField(Product, verbose_name='Product', null=True, blank=True, related_name='products')
    creation = models.DateTimeField(auto_now=False, auto_now_add=True, null=True, verbose_name='Creation')

    class Meta:
        verbose_name = 'ProductPhoto'
        verbose_name_plural = 'ProductPhotos'
        ordering = ['creation']


class UserProductRelation(models.Model):
    RATE_CHOICES = (
        (1, 'Ok'),
        (2, 'Fine'),
        (3, 'Good'),
        (4, 'Amazing'),
        (5, 'Incredible'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='upr')
    like = models.BooleanField(default=False)
    in_bookmarks = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, default=RATE_CHOICES[4][0])
    view = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}:{self.product.name}, RATE {self.rate}'


class DeliveryType(models.Model):
    name = models.CharField(max_length=50, verbose_name='Delivery')

    class Meta:
        verbose_name = 'DeliveryType'
        verbose_name_plural = 'DeliveryTypes'

    def __str__(self):
        return self.name


class CommentProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comment', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    content = models.TextField(verbose_name="Text")
    date = models.DateTimeField(auto_now=False, auto_now_add=True, null=True, verbose_name='Comment Date')
    comment = models.ForeignKey('CommentProduct', on_delete=models.CASCADE, verbose_name='Parent Comment', blank=True, null=True)

    @property
    def like_amount(self):
        return len(self.comment_product.filter(like=True))


class UserCommentRelation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    comment = models.ForeignKey(CommentProduct, on_delete=models.CASCADE, related_name='comment_product')
    like = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}:{self.comment.product}'



