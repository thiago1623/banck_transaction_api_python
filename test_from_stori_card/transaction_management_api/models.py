# pylint: disable=missing-module-docstring
from django.db import models


class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    transaction = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.id}, {self.transaction}'

    class Meta:
        db_table = 'transactions'
