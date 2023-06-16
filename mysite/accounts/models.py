from django.contrib.auth.models import User
from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


def avatar_image_directory_path(instance: "Profile", filename: str) -> str:
    return "profiles/profile_{pk}/{filename}".format(pk=instance.pk, filename=filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=256)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True)
    avatar = models.ImageField(null=True, blank=True, upload_to=avatar_image_directory_path)
    email = models.EmailField(null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
