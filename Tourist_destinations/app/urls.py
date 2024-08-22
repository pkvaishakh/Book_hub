from django.urls import path,include
from .views import *
from . import views

urlpatterns = [
    path('create/',DestinationCreateView.as_view(),name='create_destination_view'),
    path('detail/<int:pk>/',DestinationDetail.as_view(),name='destination_datail'),
    path('update/<int:pk>/',UpdateDestinationView.as_view(),name='update_destination'),
    path('delete/<int:pk>/',DeleteDestination.as_view(),name='delete_destination'),
    path('search/<str:place_name>/',SearchDestination.as_view(),name='search_destination'),


    path('create_destination/',views.create_destination,name='create_destination'),
    path('update_destination/<int:id>/',views.update_destination,name='update_destination'),
    path('delete_destination/<int:id>/',views.delete_destination,name='delete_destination'),
    path('view_details/<int:id>/',views.view_details,name='view_details'),
    path('',views.index,name='index'),
]