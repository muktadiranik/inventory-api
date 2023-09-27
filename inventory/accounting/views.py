from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from django.db.models import Q
from .serializers import *
from .models import Transaction
User = get_user_model()


class TransactionViewSet(ModelViewSet):
    def get_serializer_class(self):
        if self.request.method != "GET":
            return CreateTransactionSerializer
        return TransactionSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Transaction.objects.all().order_by("-id")
        return Transaction.objects.filter(company_id=self.kwargs["company_pk"]).select_related("buyer_seller").select_related("product").order_by("-id")

    def get_serializer_context(self):
        return {"company_id": self.kwargs["company_pk"], "request": self.request}


class DashboardTransactionViewSet(ModelViewSet):
    def get_queryset(self):
        return Transaction.objects.filter(company_id=self.kwargs["company_pk"]).order_by("id").reverse()[0:1]

    serializer_class = DashboardTransactionSerializer
    http_method_names = ["get"]


class ChartOfAccountViewSet(ModelViewSet):
    serializer_class = ChartOfAccountSerializer

    def get_queryset(self):
        return ChartOfAccount.objects.all()


class PlotViewSet(ModelViewSet):
    def get_queryset(self):
        return Transaction.objects.filter(company_id=self.kwargs["company_pk"]).order_by("-id")

    serializer_class = PlotSerializer
    http_method_names = ["get"]


class ProfiteLossViewSet(ModelViewSet):
    def get_queryset(self):
        return Company.objects.filter(Q(owner=self.request.user.id) & Q(pk=self.kwargs["company_pk"])).prefetch_related("transaction_set")

    serializer_class = ProfiteLossSerializer
    http_method_names = ["get"]

    def get_serializer_context(self):
        return {"company_id": self.kwargs["company_pk"], "request": self.request}


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(company=self.kwargs["company_pk"]).order_by("id")

    def get_serializer_context(self):
        return {"company_id": self.kwargs["company_pk"], "request": self.request}


class ProductCategoryViewSet(ModelViewSet):
    serializer_class = ProductCategorySerializer

    def get_queryset(self):
        return ProductCategory.objects.filter(company=self.kwargs["company_pk"])

    def get_serializer_context(self):
        return {"company_id": self.kwargs["company_pk"], "request": self.request}
