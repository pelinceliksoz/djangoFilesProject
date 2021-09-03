from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('csv_data', views.CsvDataView.as_view(), name='csv_data'),
    path('json_data', views.JsonDataView.as_view(), name='json_data'),
    path('xml_data', views.XmlDataView.as_view(), name='xml_data'),
    path('show_details/<str:uid>/<str:file_type>', views.ShowDetailsView.as_view(), name='show_details'),

]