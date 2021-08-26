from django.db import models
from shop.submodels.general import TimeStampModel

class Order(TimeStampModel):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length = 250)
    postal_code = models.CharField(max_length = 20)
    city = models.CharField(max_length=100)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())