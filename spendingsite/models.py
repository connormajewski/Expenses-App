from django.db import models

class Transaction(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateField()
    description = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    category = models.CharField(max_length=32)
    year = models.IntegerField(default=0)
    month = models.IntegerField(default=0)
    day = models.IntegerField(default=0)

    def __str__(self):
        return f"DATE: {self.date}\nDESC: {self.description}\nPRICE: {self.price}\nCATEGORY: {self.category}\n"
