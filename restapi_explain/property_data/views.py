from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from auth.auth_bearer import admin_required
from .models import Property
from .serializers import PropertySerializer
from rest_framework.permissions import IsAuthenticated  # Add this if user authentication is needed

# Create Property
@api_view(['POST'])
@admin_required
def create_property(request):
    """API to create a new property"""
    if request.method == 'POST':
        # Ensure user_id is part of the request data
        if 'user_id' not in request.data:
            return Response({'detail': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Proceed to serialize and save the property
        serializer = PropertySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save the new property
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Get All Properties with user name
@api_view(['GET'])
def get_all_properties(request):
    """API to get all properties with user name"""
    properties = Property.objects.all().select_related('user_id')  # Join the User model with Property model
    
    # Serialize the data and include user_name from the User model
    property_list = []
    for property in properties:
        property_data = {
            "property_code": property.property_code,
            "building": property.building,
            "address2": property.address2,
            "city": property.city,
            "area": property.area,
            "pin": property.pin,
            "des_code": property.des_code,
            "lease_code": property.lease_code,
            "status_code": property.status_code,
            "usp": property.usp,
            "company": property.company,
            "contact_person1": property.contact_person1,
            "contact_person2": property.contact_person2,
            "contact_person3": property.contact_person3,
            "c_status": property.c_status,
            "property_type": property.property_type,
            "user_name": property.user_id.user_name,  # Accessing the user_name based on user_id
            "phone_no": property.user_id.phone_no,
            "user_email": property.user_id.user_email,
        }
        property_list.append(property_data)
    
    return Response(property_list, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_property_by_id(request, property_code):
    """API to get a property by its property_code along with user_name"""
    try:
        # Fetch the property with the given property_code and join with user_id
        property = Property.objects.get(property_code=property_code)
    except Property.DoesNotExist:
        return Response({'detail': 'Property not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Prepare the response data
    property_data = {
        "property_code": property.property_code,
        "building": property.building,
        "address2": property.address2,
        "city": property.city,
        "area": property.area,
        "pin": property.pin,
        "des_code": property.des_code,
        "lease_code": property.lease_code,
        "status_code": property.status_code,
        "usp": property.usp,
        "company": property.company,
        "contact_person1": property.contact_person1,
        "contact_person2": property.contact_person2,
        "contact_person3": property.contact_person3,
        "c_status": property.c_status,
        "property_type": property.property_type,
        "user_name": property.user_id.user_name,  # Accessing the user_name based on user_id
        "phone_no": property.user_id.phone_no,
        "user_email": property.user_id.user_email,
    }

    return Response(property_data, status=status.HTTP_200_OK)


# Update Property
@api_view(['PUT'])
def update_property(request, property_code):
    """API to update a property"""
    try:
        property = Property.objects.get(property_code=property_code)
    except Property.DoesNotExist:
        return Response({'detail': 'Property not found'}, status=status.HTTP_404_NOT_FOUND)

    # Allow partial updates
    serializer = PropertySerializer(property, data=request.data, partial=True)  # partial=True for partial update
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Delete Property
@api_view(['DELETE'])
def delete_property(request, property_code):
    """API to delete a property"""
    try:
        property = Property.objects.get(property_code=property_code)
    except Property.DoesNotExist:
        return Response({'detail': 'Property not found'}, status=status.HTTP_404_NOT_FOUND)
    
    property.delete()
    return Response({'detail': 'Property deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
