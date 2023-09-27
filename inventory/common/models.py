from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields
from .validators import *
from auditlog.registry import auditlog
from django.contrib.auth import get_user_model
User = get_user_model()

COMPANY_TYPE = (
    ("ART, PHOTOGRAPHY & CREATIVE SERVICES", "Art, Photography & Creative Services",),
    ("CONSTRUCTION & HOME IMPROVEMENT", "Construction & Home Improvement",),
    ("CONSULTING & PROFESSIONAL SERVICES", "Consulting & Professional Services",),
    ("FINANCIAL SERVICES & INSURANCE", "Financial Services & Insurance",),
    ("HAIR, SPA & AESTHETICS", "Hair, Spa & Aesthetics",),
    ("NON-PROFITS, ASSOCIATIONS & GROUPS", "Non-profits, Associations & Groups",),
    ("REAL ESTATE", "Real Estate",),
    ("RETAILERS, RESELLERS & SALES", "Retailers, Resellers & Sales",),
    ("WEB, TECH & MEDIA", "Web, Tech & Media",),
    ("OTHER: I MAKE OR SELL A PRODUCT", "Other: I make or sell a PRODUCT",),
    ("OTHER: I PROVIDE A SERVICE", "Other: I provide a SERVICE")
)

CUSTOMER_TYPE = (
    ("CUSTOMER", "Customer"),
    ("SUPPLIER", "Supplier"),
    ("INVESTOR", "Investor"),
    ("BORROWER", "Borrower"),
)

LANGUAGE_CHOICES = (
    ("EN", "EN"),
    ("BD", "BD"),
)

CURRENCY_CHOICES = (
    ("USD", "USD"),
    ("BDT", "BDT"),
)


class CompanyType(models.Model):
    company_type = models.CharField(max_length=100, choices=COMPANY_TYPE, blank=True, null=True)

    def __str__(self):
        return self.company_type

    class Meta:
        verbose_name = "Company Type"
        verbose_name_plural = _("Company Types")


auditlog.register(CompanyType)


class Company(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    company_type = models.ForeignKey(CompanyType, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = _('Companies')


auditlog.register(Company)


class CustomerType(models.Model):
    customer_type = models.CharField(max_length=255, choices=CUSTOMER_TYPE, blank=True, null=True)

    def __str__(self):
        return self.customer_type

    class Meta:
        verbose_name = 'Customer Type'
        verbose_name_plural = _('Customer Types')


auditlog.register(CustomerType)


class Customer(models.Model):
    first_name = models.CharField(max_length=255, null=True, validators=[alphanumeric])
    last_name = models.CharField(max_length=255, null=True, blank=True, validators=[alphanumeric])
    full_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=15, null=True, validators=[phone_regex, MinLengthValidator(11)])
    email = models.EmailField(blank=True, null=True, validators=[email_regex])
    customer_type = models.ForeignKey(CustomerType, on_delete=models.CASCADE, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,  null=True)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)
    total_due = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.first_name and self.last_name:
            self.full_name = str(self.first_name) + " " + str(self.last_name)

        if self.first_name and not self.last_name:
            self.full_name = str(self.first_name)

        if not self.first_name and self.last_name:
            self.full_name = str(self.last_name)

        super(Customer, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.full_name)


auditlog.register(Customer)


class Language(models.Model):
    name = models.CharField(max_length=50, unique=True, choices=LANGUAGE_CHOICES, null=True)
    logo = models.ImageField(upload_to='languages/', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')


auditlog.register(Language)


class Currency(models.Model):
    name = models.CharField(max_length=50, unique=True, choices=CURRENCY_CHOICES,  null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Currency')
        verbose_name_plural = _('Currencies')


auditlog.register(Currency)


class Faqs(TranslatableModel):
    translations = TranslatedFields(
        question=models.TextField(_("question"), max_length=150, blank=True, null=True),
        answer=models.TextField(_("answer"), max_length=555, blank=True, null=True)
    )
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return str(self.question)

    class Meta:
        verbose_name = _('FAQ')
        verbose_name_plural = _('FAQs')


auditlog.register(Faqs)



class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, blank=True, null=True)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, blank=True, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'User Preference'
        verbose_name_plural = 'User Preferences'


auditlog.register(UserPreference)


class CompanyUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Company User'
        verbose_name_plural = 'Company Users'


auditlog.register(CompanyUser)
