from django.urls import path, include
from . import views 
urlpatterns = [
    path('', views.getAngeschlosseneGereate),
    path('hmp4040_measure/',views.hmp4040_measure),
    path('auto_corrector_add_ch/',views.auto_corrector_add_ch),
    path('auto_corrector_remove_ch/',views.auto_corrector_remove_ch),
    path('channel_aktivieren/',views.channel_aktivieren) ,
    path('channel_deaktivieren/',views.channel_deaktivieren) ,
    path('out_aktivieren/',views.out_aktivieren) ,
    path('out_deaktivieren/',views.out_deaktivieren) ,
    path('start_saving_Data/',views.start_saving_Data) ,
    path('stop_saving_Data/',views.stop_saving_Data),
    path('set_power/',views.set_power),
    path('read_volt/',views.read_voltage),
    path('read_curr/',views.read_curr)
]
