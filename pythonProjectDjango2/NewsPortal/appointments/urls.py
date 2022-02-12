from django.urls import path
from .views import *


urlpatterns = [

    path('', AppointmentView.as_view(), name='make_appointment'),
    # path('appoint/', AppointView.as_view(), name='test'),

]







# подписка на рассылку на статью
# path('add_subscribe_t/', add_subscribe_t, name='add_subscribe_t'),
# path('del_subscribe_t/', del_subscribe_t, name='del_subscribe_t'),