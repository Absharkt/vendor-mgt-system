from django.urls import path
from api import views


urlpatterns = [
    # Vendors
    path('vendors',views.vendor_list_or_create),
    path('vendors/<int:id>/',views.get_vendor,name='get_vendor'),
    path('vendors/<int:id>/',views.get_vendor,name='update_vendor'),
    path('vendors/<int:id>/',views.get_vendor,name='delete_vendor'),

    # Purchase Orders
    path('purchase_orders/',views.get_or_create_po),
    path('get-po/<int:id>/',views.purchase_orders,name='get_po'),

    # vendor performance
    path('vendors/<int:id>/performance/',views.vendor_performance,name='vendor_performance')

]
