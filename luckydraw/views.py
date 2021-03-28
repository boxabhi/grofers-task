from django.shortcuts import render
from .models import *
# Create your views here.


def home(request):
    
    context = {}
    
    if request.user.is_authenticated:
        context['lucky_draw_objs'] = LuckyDraws.objects.all()
        context['ticke_obj'] = Tickets.objects.filter(user=request.user , is_ticket_used = False).first() 
        
    
    
    return render(request , 'home.html' , context)

def winnners(request):
    return render(request , 'winners.html')