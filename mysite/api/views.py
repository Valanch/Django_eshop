from django.shortcuts import render
from django.http import JsonResponse
from random import randrange
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.http import HttpResponse

from accounts.models import Profile
from shopapp.models import Category, Product

User = get_user_model()


def banners(request):
    data = [
        {
            "id": "123",
            "category": 55,
            "price": 500.67,
            "count": 12,
            "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
            "title": "video card",
            "description": "description of the product",
            "freeDelivery": True,
            "images": [
                {
                    "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                    "alt": "any alt text",
                }
            ],
            "tags": [
                "string"
            ],
            "reviews": 5,
            "rating": 4.6
        },
    ]
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
    data = {
        "items": [
            {
                "id": 123,
                "category": 123,
                "price": 500.67,
                "count": 12,
                "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
                "title": "video card",
                "description": "description of the product",
                "freeDelivery": True,
                "images": [
                    {
                        "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                        "alt": "hello alt",
                    }
                ],
                "tags": [
                    {
                        "id": 0,
                        "name": "Hello world"
                    }
                ],
                "reviews": 5,
                "rating": 4.6
            }
        ],
        "currentPage": randrange(1, 4),
        "lastPage": 3
    }
    return JsonResponse(data)


def productsPopular(request):
    data = [
        {
            "id": "123",
            "category": 55,
            "price": 500.67,
            "count": 12,
            "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
            "title": "video card",
            "description": "description of the product",
            "freeDelivery": True,
            "images": [
                {
                    "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                    "alt": "hello alt",
                }
            ],
            "tags": [
                {
                    "id": 0,
                    "name": "Hello world"
                }
            ],
            "reviews": 5,
            "rating": 4.6
        }
    ]
    return JsonResponse(data, safe=False)


def productsLimited(request):
    data = [
        {
            "id": "123",
            "category": 55,
            "price": 500.67,
            "count": 12,
            "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
            "title": "video card",
            "description": "description of the product",
            "freeDelivery": True,
            "images": [
                {
                    "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                    "alt": "hello alt",
                }
            ],
            "tags": [
                {
                    "id": 0,
                    "name": "Hello world"
                }
            ],
            "reviews": 5,
            "rating": 4.6
        }
    ]
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
    if (request.method == "GET"):
        print('[GET] /api/basket/')
        data = [
            {
                "id": 123,
                "category": 55,
                "price": 500.67,
                "count": 12,
                "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
                "title": "video card",
                "description": "description of the product",
                "freeDelivery": True,
                "images": [
                    {
                        "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                        "alt": "hello alt",
                    }
                ],
                "tags": [
                    {
                        "id": 0,
                        "name": "Hello world"
                    }
                ],
                "reviews": 5,
                "rating": 4.6
            },
            {
                "id": 124,
                "category": 55,
                "price": 201.675,
                "count": 5,
                "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
                "title": "video card",
                "description": "description of the product",
                "freeDelivery": True,
                "images": [
                    {
                        "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                        "alt": "hello alt",
                    }
                ],
                "tags": [
                    {
                        "id": 0,
                        "name": "Hello world"
                    }
                ],
                "reviews": 5,
                "rating": 4.6
            }
        ]
        return JsonResponse(data, safe=False)

    elif (request.method == "POST"):
        body = json.loads(request.body)
        id = body['id']
        count = body['count']
        print('[POST] /api/basket/   |   id: {id}, count: {count}'.format(id=id, count=count))
        data = [
            {
                "id": id,
                "category": 55,
                "price": 500.67,
                "count": 13,
                "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
                "title": "video card",
                "description": "description of the product",
                "freeDelivery": True,
                "images": [
                    {
                        "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                        "alt": "hello alt",
                    }
                ],
                "tags": [
                    {
                        "id": 0,
                        "name": "Hello world"
                    }
                ],
                "reviews": 5,
                "rating": 4.6
            }
        ]
        return JsonResponse(data, safe=False)

    elif (request.method == "DELETE"):
        body = json.loads(request.body)
        id = body['id']
        print('[DELETE] /api/basket/')
        data = [
            {
                "id": id,
                "category": 55,
                "price": 500.67,
                "count": 11,
                "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
                "title": "video card",
                "description": "description of the product",
                "freeDelivery": True,
                "images": [
                    {
                        "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                        "alt": "hello alt",
                    }
                ],
                "tags": [
                    {
                        "id": 0,
                        "name": "Hello world"
                    }
                ],
                "reviews": 5,
                "rating": 4.6
            }
        ]
        return JsonResponse(data, safe=False)


def orders(request):
    if (request.method == "POST"):
        data = [
            {
                "id": 123,
                "category": 55,
                "price": 500.67,
                "count": 12,
                "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
                "title": "video card",
                "description": "description of the product",
                "freeDelivery": True,
                "images": [
                    {
                        "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                        "alt": "hello alt",
                    }
                ],
                "tags": [
                    {
                        "id": 0,
                        "name": "Hello world"
                    }
                ],
                "reviews": 5,
                "rating": 4.6
            }
        ]
        return JsonResponse(data, safe=False)


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
    if request.method == "GET":
        data = Product.objects.filter(id=id)
        print(data)
        data = {
            "id": 1,
            "category": 55,
            "price": 500.67,
            "count": 12,
            "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
            "title": "video card",
            "description": "description of the product",
            "fullDescription": "full description of the product",
            "freeDelivery": True,
            "images": [
                {
                    "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                    "alt": "hello alt",
                }
            ],
            "tags": [
                {
                    "id": 0,
                    "name": "Hello world"
                }
            ],
            "reviews": [
                {
                    "author": "Annoying Orange",
                    "email": "no-reply@mail.ru",
                    "text": "rewrewrwerewrwerwerewrwerwer",
                    "rate": 4,
                    "date": "2023-05-05 12:12"
                }
            ],
            "specifications": [
                {
                    "name": "Size",
                    "value": "XL"
                }
            ],
            "rating": 4.6
        }
        return JsonResponse(data)


def tags(request):
    data = [
        {"id": 0, "name": 'tag0'},
        {"id": 1, "name": 'tag1'},
        {"id": 2, "name": 'tag2'},
    ]
    return JsonResponse(data, safe=False)


def productReviews(request, id):
    data = [
        {
            "author": "Annoying Orange",
            "email": "no-reply@mail.ru",
            "text": "rewrewrwerewrwerwerewrwerwer",
            "rate": 4,
            "date": "2023-05-05 12:12"
        },
        {
            "author": "2Annoying Orange",
            "email": "no-reply@mail.ru",
            "text": "rewrewrwerewrwerwerewrwerwer",
            "rate": 5,
            "date": "2023-05-05 12:12"
        },
    ]
    return JsonResponse(data, safe=False)


def profile(request):
    user = request.user
    if (request.method == 'GET'):
        data = {
            "fullName": user.profile.name,
            "email": user.profile.email,
            "phone": user.profile.phone,
            "avatar": {
                "src": str(user.profile.avatar),
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
        data = [
            {
                "id": 123,
                "createdAt": "2023-05-05 12:12",
                "fullName": "Annoying Orange",
                "email": "no-reply@mail.ru",
                "phone": "88002000600",
                "deliveryType": "free",
                "paymentType": "online",
                "totalCost": 567.8,
                "status": "accepted",
                "city": "Moscow",
                "address": "red square 1",
                "products": [
                    {
                        "id": 123,
                        "category": 55,
                        "price": 500.67,
                        "count": 12,
                        "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
                        "title": "video card",
                        "description": "description of the product",
                        "freeDelivery": True,
                        "images": [
                            {
                                "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                                "alt": "Image alt string"
                            }
                        ],
                        "tags": [
                            {
                                "id": 12,
                                "name": "Gaming"
                            }
                        ],
                        "reviews": 5,
                        "rating": 4.6
                    }
                ]
            },
            {
                "id": 123,
                "createdAt": "2023-05-05 12:12",
                "fullName": "Annoying Orange",
                "email": "no-reply@mail.ru",
                "phone": "88002000600",
                "deliveryType": "free",
                "paymentType": "online",
                "totalCost": 567.8,
                "status": "accepted",
                "city": "Moscow",
                "address": "red square 1",
                "products": [
                    {
                        "id": 123,
                        "category": 55,
                        "price": 500.67,
                        "count": 12,
                        "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
                        "title": "video card",
                        "description": "description of the product",
                        "freeDelivery": True,
                        "images": [
                            {
                                "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                                "alt": "Image alt string"
                            }
                        ],
                        "tags": [
                            {
                                "id": 12,
                                "name": "Gaming"
                            }
                        ],
                        "reviews": 5,
                        "rating": 4.6
                    }
                ]
            }
        ]
        return JsonResponse(data, safe=False)

    elif (request.method == 'POST'):
        data = {
            "orderId": 123,
        }
        return JsonResponse(data)

    return HttpResponse(status=500)


def order(request, id):
    if (request.method == 'GET'):
        data = {
            "id": 123,
            "createdAt": "2023-05-05 12:12",
            "fullName": "Annoying Orange",
            "email": "no-reply@mail.ru",
            "phone": "88002000600",
            "deliveryType": "free",
            "paymentType": "online",
            "totalCost": 567.8,
            "status": "accepted",
            "city": "Moscow",
            "address": "red square 1",
            "products": [
                {
                    "id": 123,
                    "category": 55,
                    "price": 500.67,
                    "count": 12,
                    "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
                    "title": "video card",
                    "description": "description of the product",
                    "freeDelivery": True,
                    "images": [
                        {
                            "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                            "alt": "Image alt string"
                        }
                    ],
                    "tags": [
                        {
                            "id": 12,
                            "name": "Gaming"
                        }
                    ],
                    "reviews": 5,
                    "rating": 4.6
                },
            ]
        }
        return JsonResponse(data)

    elif (request.method == 'POST'):
        data = {"orderId": 123}
        return JsonResponse(data)

    return HttpResponse(status=500)


def payment(request, id):
    print('qweqwewqeqwe', id)
    return HttpResponse(status=200)


def avatar(request):
    if request.method == "POST":
        # 		print(request.FILES["avatar"])
        return HttpResponse(status=200)
