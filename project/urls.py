from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('csv_file', views.CsvFileView.as_view(), name='csv_file'),
    path('json_file', views.JsonFileView.as_view(), name='json_file'),
    path('xml_file', views.XmlFileView.as_view(), name='xml_file'),
    path('csv_data', views.CsvDataView.as_view(), name='csv_data'),
    path('json_data', views.JsonDataView.as_view(), name='json_data'),
    path('xml_data', views.XmlDataView.as_view(), name='xml_data'),
    path('show_details', views.ShowDetailsView.as_view(), name='show_details'),

]