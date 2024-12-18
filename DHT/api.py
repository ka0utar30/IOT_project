from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Dht11
from .serializers import DHT11serialize


# Initialize a global counter variable
person_counter = 0


@api_view(["GET", "POST"])
def dhtser(request):
    global person_counter

    if request.method == "GET":
        all = Dht11.objects.all()
        data_ser = DHT11serialize(all, many=True) # Les données sont sérialisées en JSON
        return Response(data_ser.data)

    elif request.method == "POST":
        serial = DHT11serialize(data=request.data)

        if serial.is_valid():
            serial.save()
            derniere_temperature = Dht11.objects.last().temp
            print(derniere_temperature)

            return Response(serial.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
