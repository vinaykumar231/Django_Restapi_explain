from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import AriyanspropertiesUser
from .serializers import RegisterSerializer, LoginSerializer
from auth.auth_handler import signJWT  # Ensure JWT function exists

@api_view(['POST'])
def register(request):
    """API for User Registration"""
    # Extract data from request
    user_name = request.data.get('user_name')
    email = request.data.get('user_email')
    password = request.data.get('user_password')
    user_type = request.data.get('user_type')
    phone_no = request.data.get('phone_no')

    # Validate required fields
    if not all([user_name, email, password, user_type, phone_no]):
        return Response({'detail': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if email already exists
    if AriyanspropertiesUser.objects.filter(user_email=email).exists():
        return Response({'detail': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

    # Validate email format
    if not AriyanspropertiesUser.validate_email(email):
        return Response({'detail': 'Invalid email format'}, status=status.HTTP_400_BAD_REQUEST)

    # Validate phone number format
    if not AriyanspropertiesUser.validate_phone_number(phone_no):
        return Response({'detail': 'Phone number must be 10 digits'}, status=status.HTTP_400_BAD_REQUEST)

    # Validate password length
    if not AriyanspropertiesUser.validate_password(password):
        return Response({'detail': 'Password must be at least 8 characters'}, status=status.HTTP_400_BAD_REQUEST)

    # Hash the password before storing it
    hashed_password = make_password(password)

    # Create new user and save to the database
    user = AriyanspropertiesUser(
        user_name=user_name,
        user_email=email,
        user_password=hashed_password,
        user_type=user_type,
        phone_no=phone_no
    )
    user.save()

    # Generate JWT token
    token, exp = signJWT(user.user_id, user.user_type)

    # Return response with user details and token
    return Response({
        'token': token,
        'exp': exp,
        'user_id': user.user_id,
        'user_name': user.user_name,
        'user_email': user.user_email,
        'user_type': user.user_type,
        'created_on': user.created_on,
        'phone_no': user.phone_no,
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login(request):
    """API for User Login"""
    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():
        validated_data = serializer.validated_data
        email = validated_data['email']
        password = validated_data['password']

        # Fetch user (404 if not found)
        user = get_object_or_404(AriyanspropertiesUser, user_email=email)

        # Validate password (checking against the hashed password in DB)
        if check_password(password, user.user_password):
            token, exp = signJWT(user.user_id, user.user_type)

            return Response({
                'token': token,
                'exp': exp,
                'user_id': user.user_id,
                'user_name': user.user_name,
                'user_email': user.user_email,
                'user_type': user.user_type,
                'created_on': user.created_on,
                'phone_no': user.phone_no,
            }, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
