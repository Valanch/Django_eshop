from django.db import models


def category_image_directory_path(instance: "Category", filename: str) -> str:
    return "categories/category_{pk}/{filename}".format(pk=instance.pk, filename=filename)


class Category(models.Model):
    class Meta:
        verbose_name_plural = "Categories"

    title = models.CharField(max_length=128)
    active = models.BooleanField(default=False)
    image = models.ImageField(null=True, blank=True, upload_to=category_image_directory_path)

    def __str__(self):
        return self.title


def product_image_directory_path(instance: "Product", filename: str) -> str:
    return "products/product_{pk}/{filename}".format(pk=instance.pk, filename=filename)


class Product(models.Model):
    name = models.CharField(max_length=256)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    image = models.ImageField(null=True, blank=True, upload_to=product_image_directory_path)
    description = models.TextField(default="")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock = models.IntegerField(default=0)

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
            ]
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
            ]
            }
