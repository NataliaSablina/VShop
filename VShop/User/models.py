from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.safestring import mark_safe


class UserManager(BaseUserManager):
    def create_user(self, username, phone_number, email, photo=None, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            phone_number=phone_number,
            email=self.normalize_email(email),
            photo=photo,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, phone_number, email, photo=None, password=None):
        user = self.create_user(
            email=email,
            username=username,
            phone_number=phone_number,
            password=password,
            photo=photo,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, verbose_name='Name', null=True)
    phone_number = models.CharField(max_length=12, verbose_name='Phone Number', null=True)
    email = models.EmailField(unique=True, verbose_name='Email', null=True)
    password = models.CharField(max_length=100, verbose_name='Password', null=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()
    """USERNAME_FIELDS определяет уникальную идентификацию для модели пользователя — по электронной почте"""
    USERNAME_FIELD = 'email'
    """REQUIRED_FIELDS запрашивает поля, когда мы создаем суперпользователя с помощью команды createsuperuser.
     Он должен включать любое поле, для которого пустым является False."""
    REQUIRED_FIELDS = ['username', 'phone_number']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def get_avatar(self):
        if not self.photo:
            return '/static/images/user.png'
        return self.photo.url

    # method to create a fake table field in read only mode
    def avatar_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % self.get_avatar())

    avatar_tag.short_description = 'Avatar'
