from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.db.models import Avg


def category_image_directory_path(instance: "Category", filename: str) -> str:
    return "categories/category_{pk}/{filename}".format(
        pk=instance.pk, filename=filename
    )


class Category(models.Model):
    class Meta:
        verbose_name_plural = "Categories"

    title = models.CharField(max_length=128)
    active = models.BooleanField(default=False)
    image = models.ImageField(
        null=True, blank=True, upload_to=category_image_directory_path
    )

    def __str__(self):
        return self.title

    def serialize(self):
        return {
            "id": self.pk,
            "title": self.title,
            "image": {"src": self.image.url, "alt": "Image alt string"},
            "subcategories": [],
        }


def product_image_directory_path(instance: "Product", filename: str) -> str:
    return "products/product_{pk}/{filename}".format(pk=instance.pk, filename=filename)


class Product(models.Model):
    name = models.CharField(max_length=256)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    image = models.ImageField(
        null=True, blank=True, upload_to=product_image_directory_path
    )
    description = models.TextField(default="")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_reviews(self):
        reviews_list = list(Review.objects.filter(product_id=self.pk).values())
        return reviews_list

    def get_rating(self):
        avg_rating = Review.objects.filter(product_id=self.pk).aggregate(Avg("rate"))
        return avg_rating["rate__avg"]

    def serialize(self):
        if self.image:
            return {
                "id": self.pk,
                "category": self.category.pk,
                "description": self.description,
                "price": self.price,
                "count": self.stock,
                "title": self.name,
                "images": [
                    {
                        "src": self.image.url,
                        "alt": "hello alt",
                    }
                ],
                "reviews": self.get_reviews(),
                "rating": self.get_rating(),
            }
        else:
            return {
                "id": self.pk,
                "category": self.category.pk,
                "description": self.description,
                "price": self.price,
                "count": self.stock,
                "title": self.name,
                "images": [
                    {
                        "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                        "alt": "hello alt",
                    }
                ],
                "reviews": self.get_reviews(),
                "rating": self.get_rating(),
            }


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    author = models.CharField(max_length=128)
    email = models.EmailField(null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    RATING_CHOICES = ((1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5"))
    rate = models.IntegerField(choices=RATING_CHOICES)
    date = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    total = models.DecimalField(decimal_places=2, default=0.00, max_digits=100)


class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(CartItem, blank=True)
    ordered = models.BooleanField(default=False)
    session_key = models.CharField(max_length=40, null=True)

    def serialize(self):
        cart_items = self.products.all()
        data = []
        for cart in cart_items:
            product = Product.objects.get(pk=cart.product_id)
            json_data = product.serialize()
            json_data["count"] = cart.count
            json_data["price"] = product.price
            data.append(json_data)

        return data


class Order(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    delivery_type = models.CharField(max_length=128)
    payment_type = models.CharField(max_length=128)
    total_cost = models.DecimalField(decimal_places=2, default=0.00, max_digits=100)
    status = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    address = models.CharField(max_length=512)
    products = models.JSONField(null=True, blank=True, encoder=DjangoJSONEncoder)
    payment_info = models.JSONField(null=True, blank=True, encoder=DjangoJSONEncoder)

    def serialize(self, request):
        # current_cart = Cart.objects.get(ordered=False, user=request.user).serialize()
        # total = sum(product["price"] for product in current_cart)
        data = {
            "id": self.pk,
            "createdAt": self.created_at,
            "fullName": self.name,
            "email": self.email,
            "phone": self.phone,
            "deliveryType": self.delivery_type,
            "paymentType": self.payment_type,
            "totalCost": self.total_cost,
            "status": self.status,
            "city": self.city,
            "address": self.address,
            "products": self.products,
        }

        return data
