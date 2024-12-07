from django.urls import path
from . import views
from . import api
urlpatterns=[
    path('', views.home ),
    path('api',api.Dlist,name='json'),
    path("api/post", api.Dlist, name='json'),
    path('download_csv/', views.download_csv, name='download_csv'),
    path('index/',views.table,name='table'),
    path('myChart/',views.graphique,name='myChart'),
    path('chart-temp/', views.my_chart_temp_view, name='myChartTemp'),
    path('chart-hum/', views.my_chart_hum_view, name='myChartHum'),
    path('chart-data/', views.chart_data, name='chart-data'),
    path('chart-data-jour/', views.chart_data_jour, name='chart-data-jour'),
    path('chart-data-semaine/', views.chart_data_semaine, name='chart-data-semaine'),
    path('chart-data-mois/', views.chart_data_mois, name='chart-data-mois'),
    path('home/', views.home, name='home'),
    path('table/',views.table,name='table'),
]