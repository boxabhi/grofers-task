from django.shortcuts import render , redirect
from .models import *
from django.contrib.auth import logout
# Create your views here.


def home(request):
    
    context = {}
    
    if request.user.is_authenticated:
        context['lucky_draw_objs'] = LuckyDraws.objects.all()
        context['ticke_obj'] = Tickets.objects.filter(user=request.user , is_ticket_used = False).first() 
        
    
    
    return render(request , 'home.html' , context)

def winnners(request):
    return render(request , 'winners.html')


def logout_view(request):
    logout(request)
    return redirect('/')