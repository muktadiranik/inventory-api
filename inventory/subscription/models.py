from django.db import models
from django.contrib.auth import get_user_model
from auditlog.registry import auditlog

User = get_user_model()


class Plan(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    discount = models.IntegerField(blank=True,
                                   null=True, help_text="Discount in percentage")
    duration = models.IntegerField(blank=True, null=True)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.discount:
            self.price = self.price - (self.price * self.discount / 100)
        super(Plan, self).save(*args, **kwargs)


auditlog.register(Plan)


class PlanDetails(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)


auditlog.register(PlanDetails)


class Subscriber(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)


auditlog.register(Subscriber)
