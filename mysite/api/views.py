from django.shortcuts import render
from django.http import JsonResponse
from random import randrange
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.core.paginator import Paginator

from accounts.models import Profile
from shopapp.filters import ProductFilter
from shopapp.models import Category, Product, Review, Cart, CartItem, Order

# from shopapp.serializers import ProductSerializer

User = get_user_model()


def banners(request):
    current_product = Product.objects.get(pk=3)
    data = [current_product.serialize()]
    print(data)
    return JsonResponse(data, safe=False)


def categories(request):
    data = list(Category.objects.values("id", "title", "image"))
    for dictionary in data:
        # dictionary["image"] = {
        #                 "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
        #                 "alt": "Image alt string"
        #             }
        dictionary["subcategories"] = []

    return JsonResponse(data, safe=False)


def catalog(request):
    all_products = Product.objects.all()
    # filterset = ProductFilter(request.GET, queryset=all_products)
    # print(filterset.qs)
    # print(request.GET)
    # if filterset.is_valid():
    #     all_products = filterset.qs
    if request.GET.get("filter[minPrice]"):
        all_products = all_products.filter(price__range=(request.GET.get("filter[minPrice]"), request.GET.get("filter[maxPrice]")))
    if request.GET.get("filter[name]"):
        all_products = all_products.filter(name__contains=request.GET.get("filter[name]"))
    if request.GET.get("sort"):
        all_products = all_products.order_by(request.GET.get("sort"))
    if request.GET.get("sortType") == "dec":
        all_products = all_products.order_by("-" + request.GET.get("sort"))
    products = [every_product.serialize() for every_product in list(all_products)]
    print(products)

    pages = Paginator(products, request.GET.get("limit"))
    current_page = request.GET.get("currentPage")
    data = {
        "items": pages.page(current_page).object_list,
        "currentPage": current_page,
        "lastPage": pages.num_pages
    }
    return JsonResponse(data)


def productsPopular(request):
    products = list(Product.objects.all())
    data = [product.serialize() for product in products if product.get_rating()]

    # for each_product in products:
    #     if each_product.get_rating():
    #         rating_data[each_product.pk] = len(each_product.get_reviews())
    # sorted_rating = sorted(rating_data.items(), key=lambda x: x[1], reverse=True)
    # id_list = [sorted_rating[0][0], sorted_rating[1][0], sorted_rating[2][0]]
    # print(id_list)

    return JsonResponse(data, safe=False)


def productsLimited(request):
    products = list(Product.objects.all())
    data = [product.serialize() for product in products if product.price > 5000]
    return JsonResponse(data, safe=False)


def sales(request):
    data = {
        'items': [
            {
                "id": 123,
                "price": 500.67,
                "salePrice": 200.67,
                "dateFrom": "05-08",
                "dateTo": "05-20",
                "title": "video card",
                "images": [
                    {
                        "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                        "alt": "hello alt",
                    }
                ],
            }
        ],
        'currentPage': randrange(1, 4),
        'lastPage': 3,
    }
    return JsonResponse(data)


def basket(request):
    if request.method == "GET":
        print('[GET] /api/basket/')
        if request.user.is_authenticated:
            cart = Cart.objects.get_or_create(user=request.user)
        else:
            cart = Cart.objects.get_or_create(session_key=request.session.session_key)
        data = cart[0].serialize()

        return JsonResponse(data, safe=False)

    elif (request.method == "POST"):
        body = json.loads(request.body)
        id = body['id']
        count = body['count']
        if request.user.is_authenticated:
            cart = Cart.objects.get_or_create(user=request.user)
            if cart[0].products.filter(product_id=id).exists():
                product_in_cart = cart[0].products.get(product_id=id)
                product_in_cart.count += int(count)
                product_in_cart.save()
            else:
                cart[0].products.add(CartItem.objects.create(user=request.user, product_id=id, count=count))
            data = cart[0].serialize()
        else:
            cart = Cart.objects.get_or_create(session_key=request.session.session_key)
            if cart[0].products.filter(product_id=id).exists():
                product_in_cart = cart[0].products.get(product_id=id)
                product_in_cart.count += int(count)
                product_in_cart.save()
            else:
                cart[0].products.add(CartItem.objects.create(user=None, product_id=id, count=count))
            data = cart[0].serialize()

        print('[POST] /api/basket/   |   id: {id}, count: {count}'.format(id=id, count=count))

        return JsonResponse(data, safe=False)

    elif (request.method == "DELETE"):
        body = json.loads(request.body)
        id = body['id']
        print('[DELETE] /api/basket/')
        if request.user.is_authenticated:
            cart = Cart.objects.get_or_create(user=request.user)
        else:
            cart = Cart.objects.get_or_create(session_key=request.session.session_key)
        product_in_cart = cart[0].products.get(product_id=id)
        product_in_cart.count -= 1
        if product_in_cart.count == 0:
            cart[0].products.get(product_id=id).delete()
        else:
            product_in_cart.save()
        data = cart[0].serialize()
        return JsonResponse(data, safe=False)


# def orders(request):
#     if (request.method == "POST"):
#         data = [
#             {
#                 "id": 123,
#                 "category": 55,
#                 "price": 500.67,
#                 "count": 12,
#                 "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
#                 "title": "video card",
#                 "description": "description of the product",
#                 "freeDelivery": True,
#                 "images": [
#                     {
#                         "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
#                         "alt": "hello alt",
#                     }
#                 ],
#                 "tags": [
#                     {
#                         "id": 0,
#                         "name": "Hello world"
#                     }
#                 ],
#                 "reviews": 5,
#                 "rating": 4.6
#             }
#         ]
#         return JsonResponse(data, safe=False)


def signIn(request):
    if request.method == "POST":
        body = json.loads(request.body)
        username = body['username']
        password = body['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=500)


def signUp(request):
    if request.method == "POST":
        body = json.loads(request.body)
        name = body["name"]
        username = body['username']
        password = body['password']
        User.objects.create_user(username=username, password=password, is_superuser=False, is_staff=False,
                                 is_active=True)
        user = authenticate(request, username=username, password=password)
        login(request=request, user=user)
        Profile.objects.create(user=user, name=name)
        return HttpResponse(status=200)


def signOut(request):
    logout(request)
    return HttpResponse(status=200)


def product(request, id):
    current_product = Product.objects.get(pk=id)
    data = current_product.serialize()
    print(data)
    # test = ProductSerializer(current_product)
    # test_data = test.data
    # print(test_data)
    # data["category"] = data["category_id"]
    # data["count"] = data["stock"]
    # data["title"] = data["name"]
    # data["images"] = []
    # data = {
    #     "id": 123,
    #     "category": 55,
    #     "price": 500.67,
    #     "count": 12,
    #     "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
    #     "title": "video card",
    #     "description": "description of the product",
    #     "fullDescription": "full description of the product",
    #     "freeDelivery": True,
    #     "images": [
    #         {
    #             "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
    #             "alt": "hello alt",
    #         }
    #     ],
    #     "tags": [
    #         {
    #             "id": 0,
    #             "name": "Hello world"
    #         }
    #     ],
    #     "reviews": [
    #         {
    #             "author": "Annoying Orange",
    #             "email": "no-reply@mail.ru",
    #             "text": "rewrewrwerewrwerwerewrwerwer",
    #             "rate": 4,
    #             "date": "2023-05-05 12:12"
    #         }
    #     ],
    #     "specifications": [
    #         {
    #             "name": "Size",
    #             "value": "XL"
    #         }
    #     ],
    #     "rating": 4.6
    # }
    return JsonResponse(data, safe=False)


def tags(request):
    data = [
        {"id": 0, "name": 'tag0'},
        {"id": 1, "name": 'tag1'},
        {"id": 2, "name": 'tag2'},
    ]
    return JsonResponse(data, safe=False)


def productReviews(request, id):
    if request.method == "POST":
        body = json.loads(request.body)
        print(body)
        Review.objects.create(
            author=body["author"],
            email=body["email"],
            text=body["text"],
            rate=int(body["rate"]),
            product_id=id,
            user_id=request.user.id
        )
    data = list(Review.objects.filter(product_id=id).values())

    return JsonResponse(data, safe=False)


def profile(request):
    user = request.user
    if (request.method == 'GET'):
        data = {
            "fullName": user.profile.name,
            "email": user.profile.email,
            "phone": user.profile.phone,
            "avatar": {
                "src": user.profile.avatar.url,
                "alt": "no image yet",
            }
        }
        return JsonResponse(data)

    elif (request.method == 'POST'):
        body = json.loads(request.body)
        data = {
            "fullName": body["fullName"],
            "email": body["email"],
            "phone": body["phone"],
            "avatar": {
                "src": body["avatar"],
                "alt": "hello alt",
            }
        }
        user.profile.name = data["fullName"]
        user.profile.email = data["email"]
        user.profile.phone = data["phone"]
        user.profile.save()
        return JsonResponse(data)

    return HttpResponse(status=500)


def profilePassword(request):
    return HttpResponse(status=200)


def orders(request):
    if (request.method == 'GET'):
        data = [my_order.serialize(request) for my_order in list(Order.objects.filter(user=request.user))]
        # data = [
        #     {
        #         "id": 123,
        #         "createdAt": "2023-05-05 12:12",
        #         "fullName": "Annoying Orange",
        #         "email": "no-reply@mail.ru",
        #         "phone": "88002000600",
        #         "deliveryType": "free",
        #         "paymentType": "online",
        #         "totalCost": 567.8,
        #         "status": "accepted",
        #         "city": "Moscow",
        #         "address": "red square 1",
        #         "products": [
        #             {
        #                 "id": 123,
        #                 "category": 55,
        #                 "price": 500.67,
        #                 "count": 12,
        #                 "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
        #                 "title": "video card",
        #                 "description": "description of the product",
        #                 "freeDelivery": True,
        #                 "images": [
        #                     {
        #                         "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
        #                         "alt": "Image alt string"
        #                     }
        #                 ],
        #                 "tags": [
        #                     {
        #                         "id": 12,
        #                         "name": "Gaming"
        #                     }
        #                 ],
        #                 "reviews": 5,
        #                 "rating": 4.6
        #             }
        #         ]
        #     },
        #     {
        #         "id": 123,
        #         "createdAt": "2023-05-05 12:12",
        #         "fullName": "Annoying Orange",
        #         "email": "no-reply@mail.ru",
        #         "phone": "88002000600",
        #         "deliveryType": "free",
        #         "paymentType": "online",
        #         "totalCost": 5555.8,
        #         "status": "accepted",
        #         "city": "Moscow",
        #         "address": "red square 1",
        #         "products": [
        #             {
        #                 "id": 123,
        #                 "category": 55,
        #                 "price": 500.67,
        #                 "count": 12,
        #                 "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
        #                 "title": "video card",
        #                 "description": "description of the product",
        #                 "freeDelivery": True,
        #                 "images": [
        #                     {
        #                         "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
        #                         "alt": "Image alt string"
        #                     }
        #                 ],
        #                 "tags": [
        #                     {
        #                         "id": 12,
        #                         "name": "Gaming"
        #                     }
        #                 ],
        #                 "reviews": 5,
        #                 "rating": 4.6
        #             }
        #         ]
        #     }
        # ]
        return JsonResponse(data, safe=False)

    elif (request.method == 'POST'):
        print("order sent")
        current_cart = Cart.objects.get(ordered=False, user=request.user).serialize()

        new_order = Order.objects.create(
            user=request.user,
            name=request.user.username,
            delivery_type="free",
            payment_type="online",
            total_cost=sum(cur_product["price"] for cur_product in current_cart),
            status="in progress",
            city="temp",
            address="temp",
            products=current_cart,
        )
        data = {
            "orderId": new_order.pk,
        }
        return JsonResponse(data)

    return HttpResponse(status=500)


def order(request, id):
    current_order = Order.objects.get(pk=id)
    if request.method == 'GET':
        data = current_order.serialize(request)
        # data = {
        #     "id": 123,
        #     "createdAt": "2023-05-05 12:12",
        #     "fullName": "Annoying Orange",
        #     "email": "no-reply@mail.ru",
        #     "phone": "88002000600",
        #     "deliveryType": "free",
        #     "paymentType": "online",
        #     "totalCost": 567.8,
        #     "status": "accepted",
        #     "city": "Moscow",
        #     "address": "red square 1",
        #     "products": [
        #         {
        #             "id": 123,
        #             "category": 55,
        #             "price": 500.67,
        #             "count": 12,
        #             "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
        #             "title": "video card",
        #             "description": "description of the product",
        #             "freeDelivery": True,
        #             "images": [
        #                 {
        #                     "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
        #                     "alt": "Image alt string"
        #                 }
        #             ],
        #             "tags": [
        #                 {
        #                     "id": 12,
        #                     "name": "Gaming"
        #                 }
        #             ],
        #             "reviews": 5,
        #             "rating": 4.6
        #         },
        #     ]
        # }
        return JsonResponse(data)

    elif request.method == 'POST':
        body = json.loads(request.body)
        current_order.name = body["fullName"]
        current_order.email = body["email"]
        current_order.phone = body["phone"]
        current_order.delivery_type = body["deliveryType"]
        current_order.city = body["city"]
        current_order.address = body["address"]
        current_order.payment_type = body["paymentType"]
        current_order.save()
        data = {"orderId": id}
        return JsonResponse(data)

    return HttpResponse(status=500)


def payment(request, id):
    if request.method == "POST":
        body = json.loads(request.body)
        current_order = Order.objects.get(pk=id)
        current_order.payment_info = {
            "name": body["name"],
            "card_number": body["number"],
            "exp_year": body["year"],
            "exp_month": body["month"],
            "cvc": body["code"],
        }
        current_order.save()
        if current_order.payment_info:
            current_order.status = "paid"
            current_order.save()
            Cart.objects.get(user=request.user).products.clear()
    return HttpResponse(status=200)


def avatar(request):
    if request.method == "POST":
        current_user = request.user
        current_user.profile.avatar = request.FILES["avatar"]
        current_user.profile.save()
        return HttpResponse(status=200)

