from rest_framework.serializers import ModelSerializer
from .models import *

class VendorSerializer(ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['name','contact_details','address','vendor_code']


class PuchaseOrderSerializer(ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'


class VendorPerformanceSerializer(ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'