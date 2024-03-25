import datetime
from django.http import JsonResponse,HttpResponseNotAllowed
from django.shortcuts import redirect
from account.models import User
from .models import Lawyer
from mouhami_api.models import Language, Lawyer, Specialities, Customer,Booked,Review
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
import random
from .serializers import BookedSerializer, LawyerSerializer,ReviewSerializer,CustomerSerializer
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg



@api_view(['POST'])
def lawyerData(request):
    
    with open('mouhami_api/cabinets.json', 'r', encoding='utf-8') as json_file:
        cabinets_data = json.load(json_file)
    all_languages=[]
    if request.method == 'POST':
        Language.objects.create(name='arabic')
        Language.objects.create(name='french')
        Language.objects.create(name='english')
        for data in cabinets_data:
            specialities_data = data.get('categories', [])
            for language in Language.objects.all():
                all_languages.append(language)

            num_languages_to_select = random.randint(1, min(2, len(Language.objects.all())))
            languages_data = random.sample(all_languages, num_languages_to_select)
            language_instances = []
            for lang in languages_data:
                
                language_instance= Language.objects.get(name=lang.name)
                language_instances.append(language_instance)

            speciality_instances = []
            for speciality_name in specialities_data:
                speciality_instance, created = Specialities.objects.get_or_create(name=speciality_name)
                speciality_instances.append(speciality_instance)

            lawyer_data = {
                'name': f"{data.get('name', '')} {data.get('fname', '')}",
                'email': data.get('email', ''),
                'phone': data.get('phone', ''),
                'photo': data.get('avocat_image', ''),
                'location': data.get('address', ''),
                'lng': data.get('longitude', 0.0),
                'lat': data.get('latitude', 0.0),
                'rating': data.get('rating', 0.0),
            }

            lawyer_instance = Lawyer.objects.create(**lawyer_data)
            lawyer_instance.languages.set(language_instances)
            lawyer_instance.specialities.set(speciality_instances)

        return Response({"data inserted to the database successfully!!"})
    

@api_view(['GET'])
def customerDetail(request, id):
    if request.method == 'GET':
        try:
            # Retrieve Customer object by id
            user=User.objects.get(pk=id)
            customer = Customer.objects.get(user=user)
            
            # Serialize the Customer object
            serializer = CustomerSerializer(customer)

            # Return serialized data as a response
            return Response(serializer.data)
        except Customer.DoesNotExist:
            return JsonResponse({"error": "Customer not found"}, status=404)
    return JsonResponse({"error": "Invalid request method"}, status=400)


@api_view(['POST'])
def searchLawyer(request):
    if request.method == 'POST':
        print("this is lawyer ",request.data)
        # Retrieve search parameters from request data
        name = request.data.get('lawyerName', '')
        wilaya = request.data.get('wilaya', '')
        langue = request.data.get('language', '')
        categories_str = request.data.get('specialities', '')  # Receive as comma-separated string
        categories = [category.strip() for category in categories_str.split(',') if category.strip()]
        
        # Initialize queryset with all lawyers
        lawyer_list = Lawyer.objects.all()
        # Filter Lawyer objects based on search parameters
        lawyer_list = lawyer_list.filter(
            Q(name__icontains=name) &
            Q(languages__name__icontains=langue)
        )

        # Check if wilaya is "Alger"
        if wilaya.lower() == 'alger':
            # Exclude lawyers located in "Algérie" (Algiers)
            lawyer_list = lawyer_list.exclude(location__icontains='Algérie')
        else:
            # Filter lawyers based on the provided wilaya
            lawyer_list = lawyer_list.filter(location__icontains=wilaya)

        # Filter Lawyer objects by each category using the "and" condition
        for category in categories:
            lawyer_list = lawyer_list.filter(specialities__name=category)

        # Serialize the queryset of Lawyer objects
        serializer = LawyerSerializer(lawyer_list.distinct(), many=True)
        print(serializer.data)
        # Return serialized data as a response
        return Response(serializer.data)





@api_view(['GET'])
def lawyerDetail(request, id):
    try:
        # Retrieve Lawyer object by id
        lawyer = Lawyer.objects.get(id=id)
    except Lawyer.DoesNotExist:
        try:
            user = User.objects.get(pk=id)
            lawyer = Lawyer.objects.get(user=user)
        except (User.DoesNotExist, Lawyer.DoesNotExist):
            return JsonResponse({"error": "User or Lawyer not found"}, status=404)

    reviews = Review.objects.filter(lawyer=lawyer)

    # Calculate average rating
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']

    # Serialize the Lawyer object
    lawyer_data = LawyerSerializer(lawyer).data

    # Add average rating to the serialized data
    lawyer_data['average_rating'] = average_rating
    return Response(lawyer_data)


@api_view(['POST'])
def insertLawyer(request):
    if request.method == 'POST':
        data = request.data['lawyerData']

        # Get user instance
        print(data['id'])
        user = User.objects.get(id=data['id'])

        # Create or get language instances
        languages = [Language.objects.get_or_create(name=lang)[0] for lang in data['language']]

        # Create or get specialities instances
        specialities = [Specialities.objects.get_or_create(name=spec)[0] for spec in data['specialities']]
        Lawyer.objects.filter(user=user).delete()
        # Create lawyer instance
        lawyer = Lawyer.objects.create(
            user=user,
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            photo="https://avocatalgerien.com/wp-content/themes/vantage/images/no-thumb.jpg",
            location=data['location'],
            lng=data['lng'],
            lat=data['lat'],
            rating=data['rating']
        )

        # Add languages and specialities to lawyer
        lawyer.languages.set(languages)
        lawyer.specialities.set(specialities)
        redirect('http://localhost:3000/my-account')
        return JsonResponse({"message": "Data inserted to the database successfully!!"}) 
    return JsonResponse({"error": "Invalid request method"}, status=400)




@api_view(['POST'])
def insertCustomer(request):
    if request.method == 'POST':
        print(request.data)
        data = request.data['customerData']

        # Get user instance
        print(data['id'])
        user = User.objects.get(id=data['id'])
        Customer.objects.filter(user=user).delete()
        
        # Create lawyer instance
        Customer.objects.create(
            user=user,
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            photo="https://avocatalgerien.com/wp-content/themes/vantage/images/no-thumb.jpg",
            location=data['location'],
            
        )

        return JsonResponse({"message": "Data inserted to the database successfully!!"}) 
    return JsonResponse({"error": "Invalid request method"}, status=400)


@api_view(['POST'])
def makeBooking(request):
    if request.method == 'POST':
        data = request.data
        print(data)

        try:
            lawyer = Lawyer.objects.get(pk=data['lawyer_id'])
            customer =  User.objects.get(pk=data['customer_id'])
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Lawyer or Customer does not exist"}, status=400)


        Booked.objects.create(
            lawyer=lawyer,
            customer=customer,
            time_from=data['time_from'],
            time_to=data['time_to'],
            date=data['date'],
        )

        return JsonResponse({"message": "Data inserted to the database successfully!!"})
    return JsonResponse({"error": "Invalid request method"}, status=400)
@api_view(['POST'])
def makeReview(request):
    if request.method == 'POST':
        print(request.data)
        print("enfiendw")
        data = request.data
        try:
            lawyer = Lawyer.objects.get(pk=data['lawyer_id'])
            customer = User.objects.get(pk=data['customer_id'])
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Lawyer or Customer does not exist"}, status=400)
        print(Review.objects.filter(lawyer=lawyer, customer=customer).exists())
        if Review.objects.filter(lawyer=lawyer, customer=customer).exists():
            return JsonResponse({"error": "You have already reviewed this lawyer"},status=400)
       
        try:
            Review.objects.create(
                lawyer=lawyer,
                customer=customer,
                rating=data['rating'],
                comment=data['comment'],
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

        return JsonResponse({"message": "Review inserted to the database successfully!!"})
    

@api_view(['GET'])
def seeBooking(request, id):  # Add 'id' parameter here
    if request.method == 'GET':
        try:
            customer = User.objects.get(pk=id)  # Use 'id' instead of 'customer_id'
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Customer does not exist"}, status=400)

        bookings = Booked.objects.filter(customer=customer)

        serializer = BookedSerializer(bookings, many=True)

        return Response(serializer.data)
    return JsonResponse({"error": "Invalid request method"}, status=400)
@api_view(['GET'])
def seeMissions(request, id):
    if request.method == 'GET':
        try:
            user = User.objects.get(pk=id)
            print(f"User: {user}")  # Add logging
            lawyer=Lawyer.objects.get(user=user)
            print(f"Lawyer: {lawyer}")  # Add logging
        except ObjectDoesNotExist as e:
            print(f"Error: {e}")  # Add logging
            return JsonResponse({"error": "Lawyer does not exist"}, status=400)
       
        bookings = Booked.objects.filter(lawyer=lawyer)

        serializer = BookedSerializer(bookings, many=True)
        
        print(f"Bookings: {bookings}")  # Add logging

        print(f"Serializer: {serializer.data}")
        return Response(serializer.data)
    return JsonResponse({"error": "Invalid request method"}, status=400)


@api_view(['GET'])
def Reviews(request, id):
    if request.method == 'GET':
        try:
            lawyer = Lawyer.objects.get(pk=id)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Lawyer does not exist"}, status=400)
        reviews = Review.objects.filter(lawyer=lawyer)
        serializer = ReviewSerializer(reviews, many=True)
        serialized_data = serializer.data
        return Response(serialized_data)
    return JsonResponse({"error": "Invalid request method"}, status=400)



from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Booked
from .serializers import BookedSerializer
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_booking(request, booking_id):
    try:
        booking = Booked.objects.get(id=booking_id)
        print(booking)
    except Booked.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        print(request.data)
        serializer = BookedSerializer(booking, data=request.data, partial=True)
        print("ser",serializer)
        if serializer.is_valid():
            print(serializer.validated_data)  # Access validated data instead of serializer.data
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_mission(request, mission_id):
    try:
        mission = Booked.objects.get(id=mission_id)
    except Booked.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = BookedSerializer(mission, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def delete_booking(request, bookingId):
    if request.method == 'DELETE':
        try:
            booking = Booked.objects.get(id=bookingId)
            booking.delete()
            return JsonResponse({'status': 'success'}, status=200)
        except Booked.DoesNotExist:
            return JsonResponse({'error': 'Booking not found'}, status=404)
    else:
        return HttpResponseNotAllowed(['DELETE'])