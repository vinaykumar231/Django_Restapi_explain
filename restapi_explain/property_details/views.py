import os
import uuid
import shutil
from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from property_data.models import Property
from user.models import AriyanspropertiesUser
from .models import PropertyDetails
from .serializers import PropertyDetailsSerializer
from werkzeug.utils import secure_filename


# Configure file upload folder and allowed extensions
UPLOAD_FOLDER = "static/images"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def save_upload_file(upload_file):
    if not upload_file or not allowed_file(upload_file.name):  # use .name instead of .filename
        return None

    try:
        filename = secure_filename(upload_file.name)  # secure the file name
        unique_filename = f"{uuid.uuid4()}_{filename}"  # Create a unique filename
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Ensure the directory exists

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)  # use .file instead of the stream

        return file_path.replace("\\", "/")  # Normalize the path for storage

    except Exception as e:
        print(f"Error saving file: {str(e)}")
        return None



@api_view(['POST'])
def add_property_details(request):
    try:
        # Extract form data
        property_code = request.POST.get("property_code")
        rate_buy = request.POST.get("rate_buy")
        rate_lease = request.POST.get("rate_lease")
        floor = request.POST.get("floor")
        unit_no = request.POST.get("unit_no")
        wing = request.POST.get("wing")
        car_parking = request.POST.get("car_parking")
        remarks = request.POST.get("remarks")
        edit_date = request.POST.get("edit_date")
        user_id = request.POST.get("user_id")

        # Handle file upload
        image_file = request.FILES.get("property_image")
        image_path = save_upload_file(image_file) if image_file else None

        # Get the related Property and AriyanspropertiesUser instances
        property_instance = Property.objects.get(property_code=property_code)  # Get the Property instance by property_code
        user_instance = AriyanspropertiesUser.objects.get(user_id=user_id)  # Get the User instance by user_id

        # Create a new PropertyDetails instance
        property_details = PropertyDetails(
            property_code=property_instance,
            rate_buy=rate_buy,
            rate_lease=rate_lease,
            floor=floor,
            unit_no=unit_no,
            wing=wing,
            car_parking=car_parking,
            remarks=remarks,
            edit_date=edit_date,
            user_id=user_instance,
            property_image_path=image_path,
        )

        property_details.save()

        return JsonResponse({"message": "Property details added successfully!"}, status=status.HTTP_201_CREATED)

    except Property.DoesNotExist:
        return JsonResponse({"error": "Property with given property_code does not exist."}, status=status.HTTP_400_BAD_REQUEST)
    except AriyanspropertiesUser.DoesNotExist:
        return JsonResponse({"error": "User with given user_id does not exist."}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
def get_property_details_by_id(request, id):
    try:
        # Get the PropertyDetails instance by ID
        property_details = PropertyDetails.objects.get(id=id)

        # Base URL to serve images (adjust based on your Django configuration)
        base_url = "http://192.168.29.85:8001/"

        property_detail = {
            "id": property_details.id,
            "property_code": property_details.property_code.property_code,
            "rate_buy": property_details.rate_buy,
            "rate_lease": property_details.rate_lease,
            "floor": property_details.floor,
            "unit_no": property_details.unit_no,
            "wing": property_details.wing,
            "car_parking": property_details.car_parking,
            "remarks": property_details.remarks,
            "edit_date": property_details.edit_date,
            "user_id": property_details.user_id.user_id,
            "property_image_url": f"{base_url}{property_details.property_image_path}",
        }

        return JsonResponse({"property_detail": property_detail}, status=status.HTTP_200_OK)

    except PropertyDetails.DoesNotExist:
        return JsonResponse({"error": "PropertyDetails with given ID does not exist."}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_property_details(request):
    try:
        property_details = PropertyDetails.objects.all()

        # Base URL to serve images (adjust based on your Django configuration)
        base_url = "http://192.168.29.85:8001/"

        property_details_list = [
            {
                "id": pd.id,
                "property_code": pd.property_code.property_code,  # Access property_code field from related Property model
                "rate_buy": pd.rate_buy,
                "rate_lease": pd.rate_lease,
                "floor": pd.floor,
                "unit_no": pd.unit_no,
                "wing": pd.wing,
                "car_parking": pd.car_parking,
                "remarks": pd.remarks,
                "edit_date": pd.edit_date,
                "user_id": pd.user_id.user_id,  # Access user_id field from related AriyanspropertiesUser model
                "property_image_url": f"{base_url}{pd.property_image_path}",  # Full image URL
            }
            for pd in property_details
        ]

        return JsonResponse({"property_details": property_details_list}, status=status.HTTP_200_OK)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT'])
def update_property_details(request, id):
    try:
        # Extract form data
        property_code = request.data.get("property_code")
        rate_buy = request.data.get("rate_buy")
        rate_lease = request.data.get("rate_lease")
        floor = request.data.get("floor")
        unit_no = request.data.get("unit_no")
        wing = request.data.get("wing")
        car_parking = request.data.get("car_parking")
        remarks = request.data.get("remarks")
        edit_date = request.data.get("edit_date")
        user_id = request.data.get("user_id")

        # Handle file upload
        image_file = request.FILES.get("property_image")
        image_path = save_upload_file(image_file) if image_file else None

        # Get the related Property and AriyanspropertiesUser instances
        property_instance = Property.objects.get(property_code=property_code)
        user_instance = AriyanspropertiesUser.objects.get(user_id=user_id)

        # Get the existing PropertyDetails instance by ID
        property_details = PropertyDetails.objects.get(id=id)

        # Update the fields
        property_details.property_code = property_instance
        property_details.rate_buy = rate_buy
        property_details.rate_lease = rate_lease
        property_details.floor = floor
        property_details.unit_no = unit_no
        property_details.wing = wing
        property_details.car_parking = car_parking
        property_details.remarks = remarks
        property_details.edit_date = edit_date
        property_details.user_id = user_instance
        property_details.property_image_path = image_path if image_path else property_details.property_image_path

        property_details.save()

        return JsonResponse({"message": "Property details updated successfully!"}, status=status.HTTP_200_OK)

    except PropertyDetails.DoesNotExist:
        return JsonResponse({"error": "PropertyDetails with given ID does not exist."}, status=status.HTTP_400_BAD_REQUEST)
    except Property.DoesNotExist:
        return JsonResponse({"error": "Property with given property_code does not exist."}, status=status.HTTP_400_BAD_REQUEST)
    except AriyanspropertiesUser.DoesNotExist:
        return JsonResponse({"error": "User with given user_id does not exist."}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['DELETE'])
def delete_property_details(request, id):
    try:
        # Get the PropertyDetails instance by ID
        property_details = PropertyDetails.objects.get(id=id)
        property_details.delete()

        return JsonResponse({"message": "Property details deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)

    except PropertyDetails.DoesNotExist:
        return JsonResponse({"error": "PropertyDetails with given ID does not exist."}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


