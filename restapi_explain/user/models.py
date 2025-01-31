from django.db import models
from django.utils import timezone
import re

class AriyanspropertiesUser(models.Model):
    # Fields
    user_id = models.AutoField(primary_key=True)  # AutoIncrement is default in Django
    user_name = models.CharField(max_length=255)
    user_email = models.EmailField(unique=True)
    user_password = models.CharField(max_length=255)
    user_type = models.CharField(max_length=100)
    phone_no = models.BigIntegerField()  # Django's equivalent of BIGINT
    created_on = models.DateTimeField(default=timezone.now)  # Default to current time

    # Meta options to specify table name and other Django settings
    class Meta:
        db_table = 'users'

    @staticmethod
    def validate_email(email):
        """
        Validates the email format. Django already performs email validation, but you can customize it if needed.
        """
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(email_pattern, email)

    @staticmethod
    def validate_password(password):
        """
        Validates if the password meets the minimum length requirement. 
        You can extend this validation for complexity as per your requirements.
        """
        return len(password) >= 8  # Can be extended to include other complexity requirements

    @staticmethod
    def validate_phone_number(phone_number):
        """
        Validates if the phone number is a valid 10-digit number.
        You can extend this to handle different formats (with country code, etc.).
        """
        phone_pattern = r"^\d{10}$"
        return re.match(phone_pattern, phone_number)
