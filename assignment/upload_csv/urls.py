from typing import final
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import upload_csv,view_data,filter_data,check
app_name = 'upload_csv'
urlpatterns = [
    path('',upload_csv,name="upload-view"),
    path('view/',view_data,name="view-data"),
    # path('filterdata/',filter_data,name='filter_data'),
    path('check/',check,name="check")

]