from django.db import models

from user.models import AriyanspropertiesUser

class Property(models.Model):
    property_code = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(AriyanspropertiesUser, on_delete=models.CASCADE, to_field='user_id', related_name="properties", null=True)
    building = models.CharField(max_length=100)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    area = models.CharField(max_length=100, blank=True, null=True)
    pin = models.CharField(max_length=10, blank=True, null=True)
    des_code = models.CharField(max_length=100, blank=True, null=True)
    lease_code = models.CharField(max_length=100, blank=True, null=True)
    status_code = models.CharField(max_length=100, blank=True, null=True)
    usp = models.CharField(max_length=255, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    contact_person1 = models.CharField(max_length=100, blank=True, null=True)
    contact_person2 = models.CharField(max_length=100, blank=True, null=True)
    contact_person3 = models.CharField(max_length=100, blank=True, null=True)
    c_status = models.CharField(max_length=100, blank=True, null=True)
    property_type = models.CharField(max_length=100, blank=True, null=True)

    # Meta options to specify table name and other Django settings
    class Meta:
        db_table = 'properties'
