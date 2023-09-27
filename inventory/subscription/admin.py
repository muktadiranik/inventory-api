from django.contrib import admin
from .models import Plan, PlanDetails, Subscriber
from django.contrib.auth import get_user_model

User = get_user_model()


class PlanDetailsTabularInline(admin.TabularInline):
    model = PlanDetails
    extra = 1
    fields = ["description"]


class PlanAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "price",
        "discount",
        "duration",
        "active",
        "created_at"
    ]

    search_fields = ["title", "price"]
    inlines = [PlanDetailsTabularInline]
    ordering = ('id',)


class SubscriberAdmin(admin.ModelAdmin):
    list_display_links = ["user"]
    list_display = ["plan", "user", "active", "created_at"]
    search_fields = ["plan__title", "user__email"]
    list_filter = ["plan", "created_at"]
    ordering = ('id',)

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(is_superuser=False)
        return super().formfield_for_dbfield(db_field, **kwargs)


admin.site.register(Plan, PlanAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
