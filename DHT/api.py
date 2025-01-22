from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Dht11, Incident
from .serializers import DHT11serialize
from twilio.rest import Client
from django.core.mail import send_mail
from threading import Timer
import os

# Initialize a global counter variable
person_counter = 0
incident_timers = {}

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

            latest_data = Dht11.objects.last()
            print(latest_data)

            #check for alerts
            if latest_data.temp > 30 or latest_data.hum > 70:
                #create a new incident in the database
                if not Incident.objects.filter(temp=latest_data.temp, hum=latest_data.hum, dt=latest_data.dt).exists():
                    Incident.objects.create(
                        temp=latest_data.temp,
                        hum=latest_data.hum,
                        dt=latest_data.dt
                    )

                    #sending an SMS to the first operator using TWILIO
                    account_sid = 'AC6f00dec70c539346716f6913131abfea'
                    auth_token = '8059437daadbd9eb29e41fc190e21c5e'
                    client = Client(account_sid, auth_token)

                    message = client.messages.create(
                    from_='whatsapp:+14155238886',
                    body='ALERTE : La temperature ou l humidité sur votre capteur depasse le seuil !, veuillez intervenir',
                    to='whatsapp:+212680272781'
                    )
                    print(f"Message SID: {message.sid}")

                    #send an email alert to operator 1#
                    subject = 'Alerte DHT'
                    email_message = (f'Il y a une alerte importante sur votre Capteur.'
                           f'Température est: {latest_data.temp}°C, Humidité: {latest_data.hum}%. '
                           f' Veuillez intervenir immédiatement pour vérifier et corriger cette situation.'
                    )
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = ['kaoutaraakki@gmail.com']
                    send_mail(subject, email_message, email_from, recipient_list)

                    # Fonction to notify two operators if incident is unresolved
                    def notify_two_operators():
                        unresolved_incident = Incident.objects.filter(id=latest_data.id, resolved=False).exists()
                        if unresolved_incident:
                            # we notify both operators

                            account_sid = 'AC6f00dec70c539346716f6913131abfea'
                            auth_token = '8059437daadbd9eb29e41fc190e21c5e'
                            client = Client(account_sid, auth_token)

                            message = client.messages.create(
                                from_='whatsapp:+14155238886',
                                body='ALERTE : La temperature ou l humidité sur votre capteur depasse le seuil !, veuillez intervenir',
                                to='whatsapp:+212680272781'
                            )
                            print(f"Message SID: {message.sid}")

                            account_sid = 'AC43db42b0fd06d2546c9ab922348acf66'
                            auth_token = '700ac47d548105f618703f0100e958cc'
                            client = Client(account_sid, auth_token)

                            message = client.messages.create(
                                from_='whatsapp:+14155238886',
                                body='ALERTE : La temperature ou l humidité sur votre capteur depasse le seuil !, veuillez intervenir',
                                to='whatsapp:+212639732792'
                            )
                            print(f"Message SID: {message.sid}")

                            # Send email alert to both operators
                            recipient_list = ['kaoutaraakki@gmail.com', 'bentayaa.maryam@gmail.com']
                            send_mail(subject, email_message, email_from, recipient_list)
                            print("Alerte envoyé aux deux opérateurs.")

                    # start a timer ( 20 minutes )
                    timer = Timer(1200, notify_two_operators)
                    timer.start()
                    incident_timers[latest_data.id] = timer

            return Response(serial.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
