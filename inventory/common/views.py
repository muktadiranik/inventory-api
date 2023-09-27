from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import filters
from rest_framework import permissions
from .serializers import *
from .models import *
from django.db.models import Q


# Create your views here.


class SimpleCustomerViewSet(ModelViewSet):
    serializer_class = SimpleCustomerSerializer

    def get_queryset(self):

        return Customer.objects.filter(Q(company=self.kwargs["company_pk"]) & Q(customer_type__customer_type="CUSTOMER")).order_by('-id')[0:5]

    http_method_names = ["get"]


class SimpleSupplierViewSet(ModelViewSet):
    serializer_class = SimpleCustomerSerializer

    def get_queryset(self):
        return Customer.objects.filter(Q(company=self.kwargs["company_pk"]) & Q(customer_type__customer_type="SUPPLIER")).order_by('-id')[0:5]

    http_method_names = ["get"]


class SimpleBorrowerViewSet(ModelViewSet):
    serializer_class = SimpleCustomerSerializer

    def get_queryset(self):
        return Customer.objects.filter(Q(company=self.kwargs["company_pk"]) & Q(customer_type__customer_type="BORROWER")).order_by('-id')[0:5]

    http_method_names = ["get"]


class SimpleInvestorViewSet(ModelViewSet):
    serializer_class = SimpleCustomerSerializer

    def get_queryset(self):
        return Customer.objects.filter(Q(company=self.kwargs["company_pk"]) & Q(customer_type__customer_type="INVESTOR")).order_by('-id')[0:5]

    http_method_names = ["get"]


class CompanyViewSet(ModelViewSet):
    serializer_class = CompanySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Company.objects.all()
        if self.request.user.is_owner:
            return Company.objects.filter(owner=self.request.user.id)
        elif self.request.user.is_editor:
            company_instance = CompanyUser.objects.get(
                user=self.request.user.id)
            return Company.objects.filter(pk=company_instance.company.id)

    def get_serializer_context(self):
        return {"user_id": self.request.user.id, "request": self.request}


class CustomerTypeViewSet(ModelViewSet):
    serializer_class = CustomerTypeSerializer

    permission_classes = [AllowAny]

    def get_queryset(self):
        return CustomerType.objects.all()

    http_method_names = ["get"]


class CustomerViewSet(ModelViewSet):
    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateCustomerSerializer
        return CustomerSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ["customer_type__customer_type"]

    def get_queryset(self):
        return Customer.objects.filter(company=self.kwargs["company_pk"])

    def get_serializer_context(self):
        return {"company_id": self.kwargs["company_pk"], "request": self.request}


class UserPreferenceViewSet(ModelViewSet):
    def get_queryset(self):
        return UserPreference.objects.filter(user=self.request.user.id)

    serializer_class = UserPreferenceSerializer

    def get_serializer_context(self):
        return {"user_id": self.request.user.id}

    @action(detail=False, methods=["GET", "PUT"])
    def me(self, request):
        user_pref = UserPreference.objects.get(user=request.user)
        if request.method == "GET":
            serializer = UserPreferenceSerializer(user_pref, many=False)
            return Response(serializer.data)
        if request.method == "PUT":
            serializer = UserPreferenceSerializer(user_pref, many=False)
            user_pref.company = Company.objects.get(id=request.data["company"])
            user_pref.language = Language.objects.get(
                id=request.data["language"])
            user_pref.currency = Currency.objects.get(
                id=request.data["currency"])
            user_pref.save()
            return Response(serializer.data)


class CompanyTypeViewSet(ModelViewSet):
    serializer_class = CompanyTypeSerializer

    permission_classes = [AllowAny]

    def get_queryset(self):
        return CompanyType.objects.all()

    http_method_names = ["get"]


class LanguageViewSet(ModelViewSet):
    serializer_class = LanguageSerializer
    permission_classes = [AllowAny]
    queryset = Language.objects.all()
    http_method_names = ["get"]


class CurrencyViewSet(ModelViewSet):
    serializer_class = CurrencySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Currency.objects.all()


class FaqViewSet(ModelViewSet):
    serializer_class = FAQSerializer
    permission_classes = [AllowAny]
    http_method_names = ["get"]

    def get_queryset(self):
        return Faqs.objects.all().order_by("id")
          


class EditorViewSet(ModelViewSet):
    def get_queryset(self):
        company = Company.objects.get(pk=self.kwargs["company_pk"])
        return User.objects.prefetch_related("companyuser_set").filter(companyuser__company=company).filter(companyuser__user__is_editor=True)

    def get_serializer_class(self):
        if self.request.method == "PUT":
            return UpdateEditorSerializer
        return EditorSerializer

    serializer_class = EditorSerializer
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        return {"company_id": self.kwargs["company_pk"], "request": self.request}


# dashboard viewset
