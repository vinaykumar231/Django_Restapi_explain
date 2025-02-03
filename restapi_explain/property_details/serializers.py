from rest_framework import serializers
from .models import PropertyDetails

class PropertyDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyDetails
        fields = '__all__'  # Include all fields in the model
