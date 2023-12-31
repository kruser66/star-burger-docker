from django import forms
from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from foodcartapp.models import Product, Restaurant, Order, RestaurantMenuItem
from foodcartapp.geo_util import check_location, calculate_distance
from collections import Counter


class Login(forms.Form):
    username = forms.CharField(
        label='Логин', max_length=75, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Укажите имя пользователя'
        })
    )
    password = forms.CharField(
        label='Пароль', max_length=75, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = Login()
        return render(request, "login.html", context={
            'form': form
        })

    def post(self, request):
        form = Login(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_staff:  # FIXME replace with specific permission
                    return redirect("restaurateur:RestaurantView")
                return redirect("start_page")

        return render(request, "login.html", context={
            'form': form,
            'ivalid': True,
        })


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('restaurateur:login')


def is_manager(user):
    return user.is_staff  # FIXME replace with specific permission


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_products(request):
    restaurants = Restaurant.objects.order_by('name')
    products = Product.objects.prefetch_related('menu_items', 'category')

    products_with_restaurant_availability = []
    for product in products:
        availability = {item.restaurant_id: item.availability for item in product.menu_items.all()}
        ordered_availability = [availability.get(restaurant.id, False) for restaurant in restaurants]

        products_with_restaurant_availability.append(
            (product, ordered_availability)
        )

    return render(request, template_name="products_list.html", context={
        'products_with_restaurant_availability': products_with_restaurant_availability,
        'restaurants': restaurants,
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_restaurants(request):
    return render(request, template_name="restaurants_list.html", context={
        'restaurants': Restaurant.objects.all(),
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_orders(request):
    orders = Order.objects.manager_orders_view().exclude(status='4_finish').order_by('status', 'pk')
    restaurants = RestaurantMenuItem.objects.with_location()

    order_available_restaurants = {}
    for order in orders:
        lat, lon = check_location(order.lat, order.lon, order.address)

        # Ошибка определения адреса в заказе - выведется сообщение напротив заказа
        if not lat and not lon:
            order_available_restaurants[order.pk] = None
            continue

        # Поиск доступных ресторанов для каждой позиции И расчет расстояния до них
        product_available_rests = []
        for order_item in order.order_items.all():

            item_available_rests = [rest for rest in restaurants if rest['product'] == order_item.product.pk]
            for rest in item_available_rests:
                item_rests = (
                        rest['restaurant__name'],
                        calculate_distance(
                            (lat, lon),
                            check_location(rest['lat'], rest['lon'], rest['restaurant__address'])
                        )
                )

                product_available_rests.append(item_rests)

        # определяем рестораны, в котором могут приготовить все позиции заказа
        order_available_restaurants[order.pk] = [
            item[0] for item in Counter(product_available_rests).items() if item[1] == order.order_items.count()
        ]
        order_available_restaurants[order.pk] = sorted(order_available_restaurants[order.pk], key=lambda x: x[1])

    return render(
        request,
        template_name='order_items.html',
        context={
            'orders': orders,
            'restaurants': order_available_restaurants
        }
    )
