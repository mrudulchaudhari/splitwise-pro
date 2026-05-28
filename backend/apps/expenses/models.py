from django.db import models
from django.conf import settings

from .constants import SplitType
# Create your models here.

class Expense(models.Model):
    title = models.CharField(max_length=255)
    amount = models.DecimalField(
        max_digits=12, decimal_places=2
    )
    split_type = models.CharField(
        max_length=20,
        choices = SplitType.choices
    )

    paid_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="paid_expenses"
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name = "created_expense"
    )

    group = models.ForeignKey(
        "groups.Group",
        on_delete=models.CASCADE,
        null=True,
        blank= True,
        related_name = "expenses"
    )

    class Meta:
        indexes = [
            models.Index(fields=["group"]),
            models.Index(fields=["paid_by"]),
            models.Index(fields=["created_at"]),
        ]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ExpenseParticipant(models.Model):
    expense = models.ForeignKey(
        Expense,
        on_delete=models.CASCADE,
        related_name="participants"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="expense_participation"
    )

    owed_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    class Meta:
        unique_together = ("expense", "user")