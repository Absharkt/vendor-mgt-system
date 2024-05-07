from django.db import models

# Create your models here.

class Vendor(models.Model):
    name = models.CharField(max_length=20)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=20,unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)


    def update_on_time_delivery_rate(self):
        completed_orders = self.purchaseorder_set.filter(status='Completed')
        total_completed_orders = completed_orders.count()
        
        if total_completed_orders == 0:
            self.on_time_delivery_rate = 0
        else:
            on_time_orders = completed_orders.filter(delivery_date__lte=models.F('acknowledgment_date')).count()
            on_time_delivery_rate = (on_time_orders / total_completed_orders) * 100
            self.on_time_delivery_rate = on_time_delivery_rate
        
        self.save()

    def update_quality_rating_average(self):
        completed_purchase_orders = self.purchaseorder_set.filter(status='Completed')
        num_completed_orders = completed_purchase_orders.count()
        if num_completed_orders > 0:
            quality_rating_sum = completed_purchase_orders.aggregate(models.Sum('quality_rating'))['quality_rating__sum']
            average_quality_rating = quality_rating_sum / num_completed_orders
            self.quality_rating_avg = average_quality_rating
            self.save()


    def update_average_response_time(self):
        total_response_time = 0
        num_orders = 0
        for purchase_order in self.purchaseorder_set.filter(acknowledgment_date__isnull=False):
            if purchase_order.acknowledgment_date:
                response_time_hours = (purchase_order.acknowledgment_date - purchase_order.issue_date).total_seconds() / 3600
                total_response_time += response_time_hours
                num_orders += 1
        
        if num_orders > 0:
            average_response_time = total_response_time / num_orders
            self.average_response_time = average_response_time
            self.save()

    def update_fulfillment_rate(self):
        total_orders = self.purchaseorder_set.count()
        if total_orders == 0:
            self.fulfillment_rate = 0
        else:
            completed_orders = self.purchaseorder_set.filter(status='Completed').count()
            fulfillment_rate = (completed_orders / total_orders) * 100
            self.fulfillment_rate = fulfillment_rate
        self.save()


    def __str__(self):
        return self.name  
    

class PurchaseOrder(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    ]

    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=40,choices=STATUS_CHOICES)
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True)

    def save(self):
        super().save()
        if self.status == 'Completed' and self.quality_rating is not None:
            self.vendor.update_quality_rating_average()
            self.vendor.update_on_time_delivery_rate()

        if self.acknowledgment_date:
            self.vendor.update_average_response_time()

        self.vendor.update_fulfillment_rate()

    def __str__(self):
        return f'{self.vendor.name}:{self.po_number}'


