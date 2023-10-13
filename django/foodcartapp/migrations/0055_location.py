# Generated by Django 3.2.15 on 2023-02-28 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0054_auto_20230221_1150'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200, unique=True, verbose_name='Адрес')),
                ('lon', models.FloatField(verbose_name='Долгота')),
                ('lat', models.FloatField(verbose_name='Широта')),
                ('updated_at', models.DateTimeField(db_index=True, verbose_name='Обновлено')),
            ],
            options={
                'verbose_name': 'координаты локации',
                'verbose_name_plural': 'координат локаций',
            },
        ),
    ]
