from django.urls import path

from megaMan.views.frcBOMView import frcBOMView


urlpatterns = [
        path('pdf/frc_bom/<str:pk>/',
             frcBOMView.as_view(),
             name= 'frc-bom')
]