from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import Sum, F, OuterRef, Subquery
from location.models import Location


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItemQuerySet(models.QuerySet):
    def with_location(self):
        return self.filter(availability=True) \
        .values('product', 'restaurant__name', 'restaurant__address') \
        .annotate(lon=Subquery(Location.objects.filter(address=OuterRef('restaurant__address')).values('lon'))) \
        .annotate(lat=Subquery(Location.objects.filter(address=OuterRef('restaurant__address')).values('lat')))


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )
    objects = RestaurantMenuItemQuerySet.as_manager()

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class OrderQuerySet(models.QuerySet):
    def manager_orders_view(self):
        return self.prefetch_related('order_items', 'order_items__product') \
            .annotate(total=Sum(F('order_items__price') * F('order_items__quantity'))) \
            .annotate(lon=Subquery(Location.objects.filter(address=OuterRef('address')).values('lon'))) \
            .annotate(lat=Subquery(Location.objects.filter(address=OuterRef('address')).values('lat')))


class Order(models.Model):
    STATUS_CHOICES = [
        ('4_finish', 'Выполнен'),
        ('1_create', 'Необработан'),
        ('2_work', 'Передан в ресторан'),
        ('3_delivery', 'Передан курьерам'),
    ]
    PAYMENT_CHOICES = [
        ('not_set', '--------'),
        ('cash', 'Наличные'),
        ('card', 'Электронно'),
    ]
    status = models.CharField(
        'Статус заказа',
        max_length=11,
        choices=STATUS_CHOICES,
        default='create',
        db_index=True
    )
    payment_type = models.CharField(
        'Способ оплаты',
        max_length=7,
        choices=PAYMENT_CHOICES,
        db_index=True,
        default='not_set',
        blank=True
    )
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='orders',
        verbose_name="ресторан",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    firstname = models.CharField(
        'Имя',
        max_length=15
    )
    lastname = models.CharField(
        'Фамилия',
        max_length=30
    )
    address = models.CharField(
        'Адрес доставки',
        max_length=200
    )
    phonenumber = PhoneNumberField(
        region='RU',
        verbose_name='Номер телефона',
        db_index=True
    )
    comment = models.TextField(
        'Комментарий к заказу',
        blank=True
    )
    created_at = models.DateTimeField(
        verbose_name='Заказ создан',
        db_index=True,
        default=timezone.now
    )
    called_at = models.DateTimeField(
        verbose_name='Время звонка',
        db_index=True,
        blank=True,
        null=True
    )
    delivered_at = models.DateTimeField(
        verbose_name='Время доставки',
        db_index=True,
        blank=True,
        null=True
    )

    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'
        ordering = ['status']

    def __str__(self):
        return f'{self.get_status_display()} - {self.firstname} {self.lastname}, {self.address}, {self.phonenumber}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='order_items',
        verbose_name='заказ',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        related_name='order_items',
        verbose_name='товар',
        on_delete=models.PROTECT
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    quantity = models.IntegerField(
        'Количество',
        validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name = 'товар заказа'
        verbose_name_plural = 'товары заказа'
        unique_together = [
            ['order', 'product']
        ]

    def __str__(self):
        return f'Заказ: {self.order.pk} Продукт: {self.product.name}'
