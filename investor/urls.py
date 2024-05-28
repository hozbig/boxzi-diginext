from django.urls import path
from . import views

app_name = "investor"
urlpatterns = [
    path("dashboard/", views.InvestorDashboard.as_view(), name="dashboard"),
    path("funds/management/", views.FundsManagements.as_view(), name="funds-management"),
    path("funds/<str:uuid>/update/", views.UpdateFund.as_view(), name="update-fund"),
    path("funds/<str:uuid>/delete/", views.delete_fund, name="delete-fund"),
    path("roads/list/", views.RoadList.as_view(), name="roads"),
    path("roads/<str:uuid>/investment/", views.RoadInvestment.as_view(), name="road-investment"),
    path("products/list/", views.ProductList.as_view(), name="product-list"),
    path("products/<str:uuid>/investment/", views.ProductInvestment.as_view(), name="product-investment"),
]