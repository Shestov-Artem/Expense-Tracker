from django.db import models

# Create your models here.

# Создаем базу данных с расходами
class Expense(models.Model):
    category = models.CharField(max_length=100)
    amount = models.FloatField()

    def __str__(self):
        return f"{self.category}: {self.amount} ₽"
