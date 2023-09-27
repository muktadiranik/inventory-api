from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from inventory.common.models import UserPreference, CompanyUser
from inventory.users.forms import UserAdminChangeForm, UserAdminCreationForm

User = get_user_model()


class UserPreferenceTabluarInline(admin.TabularInline):
    model = UserPreference
    extra = 1


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    readonly_fields = ["date_joined"]
    fieldsets = (
        (None, {'fields': ('email', "password", )}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', "phone", "image")}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', "is_owner", "is_editor", 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', "phone",  "groups"),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_superuser', "created_by")
    list_filter = ('is_active', 'groups')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)
    inlines = [UserPreferenceTabluarInline, ]

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            a = CompanyUser.objects.filter(user=request.user)
            print(a)
            return super().get_queryset(request).filter(created_by=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_superuser:
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        else:
            if db_field.name == "created_by":
                kwargs["queryset"] = User.objects.filter(email=request.user)
            return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change) -> None:
        obj.created_by = request.user
        return super().save_model(request, obj, form, change)
