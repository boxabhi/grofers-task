from django.urls import path

from .views_api import *

urlpatterns = [
    
    path('get-ticket/' , GetTicketView),
    path('get-lucky-draws/' , GetLuckyDraws),
    path('get-winners/' , GetWinnners),
    path('participate-in-game/' , ParticipateInGame),
    path('compute-winners/' , ComputeWinners),
    path('login/' , Login)
]
