from django.db import models
from user.models import AriyanspropertiesUser
from property_data.models import Property

class PropertyDetails(models.Model):
    property_code =models.ForeignKey(Property, on_delete=models.CASCADE, to_field='property_code', related_name="property_details", null=True)
    property_image_path = models.CharField(max_length=250)  # Corrected Column definition
    rate_buy = models.FloatField()
    rate_lease = models.FloatField()
    floor = models.IntegerField()
    unit_no = models.CharField(max_length=50)
    wing = models.CharField(max_length=50)
    car_parking = models.CharField(max_length=50)
    remarks = models.TextField()
    edit_date = models.DateTimeField(auto_now=True)  # auto_now=True for auto-updating on modification
    user_id = models.ForeignKey(AriyanspropertiesUser, on_delete=models.CASCADE, to_field='user_id', related_name="property_details", null=True)
    
    class Meta:
        db_table = 'property_details'  # Define the custom table name
    
