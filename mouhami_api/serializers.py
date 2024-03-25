from rest_framework import serializers
from .models import Lawyer,Language, Review,Specialities,Booked,Customer

class LawyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lawyer
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'





class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'



class SpecialitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialities
        fields = '__all__'

class BookedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booked
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)

    class Meta:
        model = Review
        fields = '__all__'