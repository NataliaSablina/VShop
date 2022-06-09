# Generated by Django 4.0.3 on 2022-05-08 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('expire_date', models.DateField(verbose_name='Expire Data')),
                ('sailing_percent', models.IntegerField(verbose_name='Sailing Percent')),
                ('highlight', models.TextField(verbose_name='Highlight')),
                ('creation', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Creation')),
                ('review', models.IntegerField(verbose_name='Views')),
            ],
            options={
                'verbose_name': 'PromoCode',
                'verbose_name_plural': 'PromoCode',
                'ordering': ['creation'],
            },
        ),
    ]