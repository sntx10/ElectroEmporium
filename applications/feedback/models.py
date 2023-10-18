from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from applications.electronics.models import Electronic

User = get_user_model()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    electronic = models.ForeignKey(Electronic, on_delete=models.CASCADE, related_name='likes')
    like = models.BooleanField(default=False)


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    electronic = models.ForeignKey(Electronic, on_delete=models.CASCADE, related_name='favorites')
    is_favorite = models.BooleanField(default=False)


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    electronic = models.ForeignKey(Electronic, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ], blank=True, null=True
    )


class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    electronic = models.ForeignKey(Electronic, on_delete=models.CASCADE, related_name='comments')