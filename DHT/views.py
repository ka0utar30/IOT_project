
import datetime
from django.utils import timezone
from django.shortcuts import render
from .models import Dht11, Incident, ArchivedIncident
from django.db.models import Count, Q
from django.shortcuts import render
from django.http import HttpResponse
import csv
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now, localtime
from django.db.models import Max, Min


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticating the user
        user = authenticate(request, username=username, password=password)
        # Checking if authentication is successful
        if user is not None:
            login(request, user)
            return redirect("/home")
        else:
            return render(request, 'login.html', {'error': 'Nom d’utilisateur ou mot de passe incorrect. Veuillez réessayer.'})

    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/')

@login_required
def home(request):
    # the current time and date
    current_datetime = localtime()
    formatted_date = current_datetime.strftime('%b-%d-%Y')
    formatted_time = current_datetime.strftime('%H:%M')

    aujourd_hui = current_datetime.date()

    # Fetch the latest record
    derniere_ligne = Dht11.objects.last()

    # Calculer le temps écoulé depuis la dernière capture
    if derniere_ligne and derniere_ligne.dt:
        time_difference = current_datetime - derniere_ligne.dt
        minutes_elapsed = int(time_difference.total_seconds() // 60)
    else:
        minutes_elapsed = 'N/A'

    valeurs = {
        'temp': derniere_ligne.temp if derniere_ligne else 'N/A',
        'hum': derniere_ligne.hum if derniere_ligne else 'N/A',
        'last_temp_time': minutes_elapsed,
        'last_hum_time': minutes_elapsed,
        'temp_max': 'N/A',
        'temp_min': 'N/A',
        'hum_max': 'N/A',
        'hum_min': 'N/A',
        'current_date': formatted_date,
        'current_time': formatted_time,
    }

    # Daily stats
    donnees_du_jour = Dht11.objects.filter(dt__date=aujourd_hui)
    if donnees_du_jour.exists():
        daily_stats = donnees_du_jour.aggregate(
            temp_max=Max('temp'),
            temp_min=Min('temp'),
            hum_max=Max('hum'),
            hum_min=Min('hum'),
        )
        valeurs.update(daily_stats)

    # Weekly stats
    start_date = aujourd_hui - datetime.timedelta(days=6)
    weekly_records = Dht11.objects.filter(dt__date__range=(start_date, aujourd_hui))

    weekly_data = []
    for i in range(7):
        date_check = start_date + datetime.timedelta(days=i)
        day_data = weekly_records.filter(dt__date=date_check)
        if day_data.exists():
            stats = day_data.aggregate(
                temp_high=Max('temp'),
                temp_low=Min('temp'),
                hum_high=Max('hum'),
                hum_low=Min('hum'),
            )
            weekly_data.append({'name': date_check.strftime('%a').upper(), **stats})
        else:
            weekly_data.append({
                'name': date_check.strftime('%a').upper(),
                'temp_high': 'N/A',
                'temp_low': 'N/A',
                'hum_high': 'N/A',
                'hum_low': 'N/A',
            })
    return render(request, 'home.html', {'valeurs': valeurs, 'weekly_data': weekly_data})



#@login_required
#def table(request):
 #   derniere_ligne = Dht11.objects.last()
  #  derniere_date = Dht11.objects.last().dt
   # delta_temps = timezone.now() - derniere_date
    #difference_minutes = delta_temps.seconds // 60
#    temps_ecoule = ' il y a ' + str(difference_minutes) + ' min'
 #   if difference_minutes > 60:
  #      temps_ecoule = 'il y ' + str(difference_minutes // 60) + 'h' + str(difference_minutes % 60) + 'min'
   # valeurs = {'date': temps_ecoule, 'id': derniere_ligne.id, 'temp': derniere_ligne.temp, 'hum': derniere_ligne.hum}
    #return render(request, 'table.html', {'valeurs': valeurs})


@login_required
def download_csv(request):
    model_values = Dht11.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="dht.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'temp', 'hum', 'dt'])
    liste = model_values.values_list('id', 'temp', 'hum', 'dt')
    for row in liste:
        writer.writerow(row)
    return response

#####Affichage csv####
@login_required
def csv_jour(request):
    now = timezone.now()
    last_24_hours = now - timezone.timedelta(hours=24)
    model_values = Dht11.objects.filter(dt__range=(last_24_hours, now))
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="dhtJOUR.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'temp', 'hum', 'dt'])
    liste = model_values.values_list('id', 'temp', 'hum', 'dt')
    for row in liste:
        writer.writerow(row)
    return response


@login_required
def csv_semaine(request):
    date_debut_semaine = timezone.now().date() - datetime.timedelta(days=7)
    print(datetime.timedelta(days=7))
    print(date_debut_semaine)
    model_values =  Dht11.objects.filter(dt__gte=date_debut_semaine)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="dhtSEMAINE.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'temp', 'hum', 'dt'])
    liste = model_values.values_list('id', 'temp', 'hum', 'dt')
    for row in liste:
        writer.writerow(row)
    return response

@login_required
def csv_mois(request):
    dht = Dht11.objects.all()
    date_debut_semaine = timezone.now().date() - datetime.timedelta(days=30)
    print(datetime.timedelta(days=30))
    print(date_debut_semaine)
    model_values =  Dht11.objects.filter(dt__gte=date_debut_semaine)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="dhtMOIS.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'temp', 'hum', 'dt'])
    liste = model_values.values_list('id', 'temp', 'hum', 'dt')
    for row in liste:
        writer.writerow(row)
    return response


####AffichageHum####

@login_required
def chartHum(request):
    tab=Dht11.objects.all()
    s={'tab':tab}
    return render(request,'chartHum.html',s)

@login_required
def chart_Hum_jour(request):
    now = timezone.now()
# Récupérer l'heure il y a 24 heures
    last_24_hours = now - timezone.timedelta(hours=24)
# Récupérer tous les objets de Module créés au cours des 24 dernières
    tab= Dht11.objects.filter(dt__range=(last_24_hours, now))
    s = {'tab': tab}
    return render(request, 'chartHum.html', s)

@login_required
def chart_Hum_semaine(request):
    dht = Dht11.objects.all()
    date_debut_semaine = timezone.now().date() - datetime.timedelta(days=7)
    print(datetime.timedelta(days=7))
    print(date_debut_semaine)
    tab = Dht11.objects.filter(dt__gte=date_debut_semaine)
    s = {'tab': tab}
    return render(request, 'chartHum.html', s)

@login_required
def chart_Hum_mois(request):
    dht = Dht11.objects.all()
    date_debut_semaine = timezone.now().date() - datetime.timedelta(days=30)
    print(datetime.timedelta(days=30))
    print(date_debut_semaine)
    tab= Dht11.objects.filter(dt__gte=date_debut_semaine)
    s = {'tab': tab}
    return render(request, 'chartHum.html', s)


#####AffichageTemperature#####

@login_required
def chartTemp(request):
    tab=Dht11.objects.all()
    s={'tab':tab}
    return render(request,'chartTemp.html',s)

@login_required
def chart_Temp_jour(request):
    now = timezone.now()
# Récupérer l'heure il y a 24 heures
    last_24_hours = now - timezone.timedelta(hours=24)
# Récupérer tous les objets de Module créés au cours des 24 dernières
    tab= Dht11.objects.filter(dt__range=(last_24_hours, now))
    s = {'tab': tab}
    return render(request, 'chartTemp.html', s)

@login_required
def chart_Temp_semaine(request):
    dht = Dht11.objects.all()
    date_debut_semaine = timezone.now().date() - datetime.timedelta(days=7)
    print(datetime.timedelta(days=7))
    print(date_debut_semaine)
    tab = Dht11.objects.filter(dt__gte=date_debut_semaine)
    s = {'tab': tab}
    return render(request, 'chartTemp.html', s)

@login_required
def chart_Temp_mois(request):
    dht = Dht11.objects.all()
    date_debut_semaine = timezone.now().date() - datetime.timedelta(days=30)
    print(datetime.timedelta(days=30))
    print(date_debut_semaine)
    tab= Dht11.objects.filter(dt__gte=date_debut_semaine)
    s = {'tab': tab}
    return render(request, 'chartTemp.html', s)

@login_required
def gestion(request):

    if request.method == 'POST':
        incident_id = request.POST.get('incident_id')
        if incident_id:
            try:
                incident = Incident.objects.get(id=incident_id)
                incident.resolved = True
                incident.save()
                #Archiver the resolved alerts
                ArchivedIncident.objects.create(
                    temp=incident.temp,
                    hum=incident.hum,
                    dt=incident.dt
                )
                return redirect('gestion_incidents')
            except Incident.DoesNotExist:
                pass

    unresolved_incidents = Incident.objects.filter(resolved=False).order_by('-dt')

    formatted_alerts = [
        {
            'id': incident.id,
            'temp': incident.temp,
            'hum': incident.hum,
            'date': incident.dt.strftime('%b-%d-%Y'),
            'time': incident.dt.strftime('%H:%M'),
        }
        for incident in unresolved_incidents
    ]
    context = {
        'alerts' : formatted_alerts
    }

    return render(request, 'gestion.html', context)

@login_required
def archive(request):
    archived_incidents = ArchivedIncident.objects.order_by('-archived_at')

    formatted_archives = [
        {
            'id':archive.id,
            'temp': archive.temp,
            'hum': archive.hum,
            'date': archive.dt.strftime('%b-%d-%Y'),
            'time': archive.dt.strftime('%H:%M'),
            'archived_at': archive.archived_at.strftime('%b-%d-%Y %H:%M'),
        }
        for archive in archived_incidents
    ]
    context = {
        'archives': formatted_archives
    }
    return render(request, 'archive.html', context)