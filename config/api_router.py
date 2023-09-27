from django.conf import settings
from rest_framework_nested import routers
from django.urls import path, include
from inventory.subscription.views import *
from inventory.accounting.views import *
from inventory.common.views import *
from inventory.users.views import *
from hr.views import *

# DashboardSuppliersViewSet, SupplierViewSet
from inventory.users.api.views import *


if settings.DEBUG:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()


router.register("users", UserViewSet)
router.register("groups", GroupViewSet)
router.register("plans", PlanViewSet)
router.register("subscribers", SubscriberViewSet)
router.register("companies", CompanyViewSet, basename="company")
router.register("customer-types", CustomerTypeViewSet, basename="customer-type")
router.register("chartofaccounts", ChartOfAccountViewSet, basename="chartofaccount")
router.register("user-preferences", UserPreferenceViewSet, basename="user-preference")
router.register("company-types", CompanyTypeViewSet, basename="company-type")
router.register("languages", LanguageViewSet, basename="language")
router.register("currencies", CurrencyViewSet, basename="currency")
router.register("faqs", FaqViewSet, basename="faq")


# accounting router
company_router = routers.NestedSimpleRouter(router, "companies", lookup="company")
# api/companies/{company_pk}/transactions/{transaction_pk}/
company_router.register("transactions", TransactionViewSet, basename="company-transactions")
# api/companies/{company_pk}/customers/{customer_pk}/
company_router.register("customers", CustomerViewSet, basename="company-customers")

"""
api/companies/{company_pk}/latest-customers/
api/companies/{company_pk}/latest-suppliers/
api/companies/{company_pk}/latest-borrowers/
api/companies/{company_pk}/latest-borrowers/

"""

company_router.register("products", ProductViewSet, basename="product")
# api/companies/{company_pk}/products/{products_pk}/
company_router.register("product-categories", ProductCategoryViewSet, basename="product-category")
# api/companies/{company_pk}/product-category/{product-category_pk}/


company_router.register("latest-customers", SimpleCustomerViewSet, basename="company-latest-customers")
company_router.register("latest-suppliers", SimpleSupplierViewSet, basename="company-latest-suppliers")
company_router.register("latest-borrowers", SimpleBorrowerViewSet, basename="company-latest-borrowers")
company_router.register("latest-investors", SimpleInvestorViewSet, basename="company-latest-investors")
#
company_router.register("profite-loss", ProfiteLossViewSet, basename="profite-loss")
# dashboard transaction updates endpoint
company_router.register("dashboard-transactions", DashboardTransactionViewSet,
                        basename="company-dashboard-transactions")
#
# plotting data rendering endpioints
company_router.register("plots", PlotViewSet, basename="plot")
# editor for company endpoint
company_router.register("editors", EditorViewSet, basename="company-editors")


# Hr router
router.register("employees", EmployeeViewSet, basename="employee")
router.register("departments", DepartmentViewSet, basename="department")
router.register("applications", JobApplicationViewSet, basename="job-application")
router.register("leaves", LeaveViewSet, basename="leave")
router.register('attendances', AttendanceViewSet, basename='attendance')
router.register('departments', DepartmentViewSet, basename='department')
router.register('job-position', JobPositionViewSet, basename='job-position')
router.register('payrolls', PayrollViewSet, basename='payroll')
router.register("job-circulars", JobCircularViewSet, basename="job-circular")

employee_router = routers.NestedSimpleRouter(router, "employees", lookup="employee")

employee_router.register("private-info", EmployeePrivateInfoViewSet, basename="employee-private-info")
# api/employee/{employee_pk}/private-info/{private-info_pk}/

"""
department_router = routers.NestedSimpleRouter(router, "departments", lookup="department")
department_router.register("positions", JobPositionViewSet, basename="job-position")
api/department/{department_pk}/positions/{position_pk}/

"""

app_name = "api"

urlpatterns = [
    path("", include(router.urls)),
    path("", include(company_router.urls)),
    path("", include(employee_router.urls)),
]
