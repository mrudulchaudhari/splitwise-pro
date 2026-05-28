from django.db import models
from django.conf import settings
# Create your models here.

class Group(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_groups"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class GroupMember(models.Model):
    ROLE_CHOICES = (
    ("admin", "ADMIN"),
    ("member", "MEMBER")
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="group_memberships"
    )

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name = "members"
    )

    role = models.CharField(
        max_length=20,
        choices = ROLE_CHOICES,
        default = "member"
    )

    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "group")

    def __str__(self):
        return f"{self.user.email} -> {self.group.name}"
