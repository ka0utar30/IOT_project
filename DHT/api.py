from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Dht11
from .serializers import DHT11serialize
from twilio.rest import Client
from django.core.mail import send_mail



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
            if derniere_temperature < 10 :
                account_sid = 'AC6f00dec70c539346716f6913131abfea'
                auth_token = '8059437daadbd9eb29e41fc190e21c5e'
                client = Client(account_sid, auth_token)

                message = client.messages.create(
                    from_='whatsapp:+14155238886',
                    body='ALERTE : La temperature sur votre capteur depasse le seuil.',
                    to='whatsapp:+212680272781'
                )
                print(message.sid)
                ######
                subject = 'Alerte DHT'
                message = (f'Il y a une alerte importante sur votre Capteur, la température est: {Dht11.objects.last().temp} et dépasse le seuil.'
                           f' Veuillez intervenir immédiatement pour vérifier et corriger cette situation.')
                email_from = settings.EMAIL_HOST_USER
                recipient_list = ['kaoutaraakki@gmail.com']
                send_mail(subject, message, email_from, recipient_list)


            return Response(serial.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
