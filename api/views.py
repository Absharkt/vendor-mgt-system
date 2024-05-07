from django.shortcuts import render
from api.models import Vendor,PurchaseOrder
from.serializers import *

from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.

@api_view(['GET','POST'])
def vendor_list_or_create(request):
    if request.method == 'POST':
        vendor = VendorSerializer(data=request.data)
        if vendor.is_valid():
            vendor.save()
            return Response({"message": "Vendor created successfully"}, status=201)
        else:
            return Response({"message": "Something went wrong"},status=400)
        
    if request.method == 'GET':
        all_vendors = Vendor.objects.all()
        serialized_vendors = VendorSerializer(all_vendors,many=True)
        return Response(serialized_vendors.data)
    

@api_view(['GET','PUT','DELETE'])
def get_vendor(request,id):
    if request.method == 'GET': 
        try:
            vendor = Vendor.objects.get(id = id)
            serialized_vendor = VendorSerializer(instance=vendor)
            return Response(serialized_vendor.data)
        except:
            return Response({"message":"Vendor not found"})
        
    if request.method == 'PUT':
        try:
            vendor = Vendor.objects.get(id = id)
            serialized_vendor = VendorSerializer(instance=vendor,data=request.data)
            if serialized_vendor.is_valid():
                serialized_vendor.save()
                return Response(serialized_vendor.data)

        except:
            return Response({"message":"Not found"})
        
    if request.method == 'DELETE':
        vendor = Vendor.objects.get(id = id)
        vendor.delete()
        return Response({"message": "Vendor deleted."})
    

@api_view(['GET','POST'])
def get_or_create_po(request):
    if request.method == 'POST':
        purchase_order = PuchaseOrderSerializer(data=request.data)
        if purchase_order.is_valid():
            purchase_order.save()
            return Response(purchase_order.data,status=201)
        else:
            return Response({"message": "Something went wrong"},status=400)
        
    if request.method == 'GET':
        purchase_order = PurchaseOrder.objects.all()
        serialzed_data = PuchaseOrderSerializer(purchase_order,many = True)
        if serialzed_data:
            return Response(serialzed_data.data)
        else:
            return Response("No Data found")
        

@api_view(['GET','PUT','DELETE'])
def purchase_orders(request,id):
    purchase_order = PurchaseOrder.objects.get(id = id)

    if request.method == 'GET':
        serialized_data = PuchaseOrderSerializer(purchase_order)
        if serialized_data:
            return Response(serialized_data.data)
        
    if request.method == 'PUT':
        serializer = PuchaseOrderSerializer(instance=purchase_order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    if request.method == 'DELETE':
        purchase_order.delete()
        return Response('Purchase order deleted', status=204)
    

@api_view(['GET'])
def vendor_performance(request, id):
    vendor =  Vendor.objects.get(id=id)
    serialized_data = VendorPerformanceSerializer(vendor)
    return Response(serialized_data.data)


