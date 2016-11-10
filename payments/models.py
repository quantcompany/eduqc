from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=4, default=0, validators=[MinValueValidator(0), MaxValueValidator(1)])

    def __str__(self):
        return '%s (%.2f%%)' % (self.code, self.discount * 100)
