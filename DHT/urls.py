from django.urls import path
from . import views
from . import api
from django.contrib.auth import views as auth_views

urlpatterns=[
    path("api/",api.dhtser,name='json'),
    path("api/post", api.dhtser, name='json'),

    path('', views.login_user,name='login'),
    path('logout', views.logout_user, name='logout'),
 #   path('home',views.table,name='table'),
    path('home', views.home, name='home'),

    path('chartHum', views.chartHum, name='chartHum'),
    path('chartTemp', views.chartTemp, name='chartTemp'),
    path('chartHum_jour',views.chart_Hum_jour,name='chartHumJ'),
    path('chartTemp_jour',views.chart_Temp_jour,name='chartTempJ'),
    path('chartTemp_semaine',views.chart_Temp_semaine,name='chartTempS'),
    path('chartHum_semaine',views.chart_Hum_semaine,name='chartHumS'),
    path('chartTemp_mois',views.chart_Temp_mois,name='chartTempM'),
    path('chartHum_mois',views.chart_Hum_mois,name='chartHumM'),

    path('download_csv/', views.download_csv, name='csv'),
    path('csv_semaine',views.csv_semaine,name='csvS'),
    path('csv_mois',views.csv_mois,name='csvM'),
    path('csv_jour',views.csv_jour,name='csvJ'),

    path('gestion_incidents/', views.gestion, name='gestion_incidents'),
    path('archive_incidents/', views.archive, name='archive_incidents'),
]