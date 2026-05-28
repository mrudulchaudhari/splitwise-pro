from django.db import models


class SplitType(models.TextChoices):
    EQUAL = "EQUAL", "Equal"
    PERCENTAGE = "PERCENTAGE", "Percentage"
    EXACT = "EXACT", "Exact"
