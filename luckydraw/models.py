from django.db import models

from django.contrib.auth.models import User
from .helpers import *
from datetime import datetime, timedelta
# Create your models here.






class Tickets(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    ticket = models.CharField(max_length=100)
    is_ticket_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username + ' ' + self.ticket
    
    
    def get_or_create_ticket(self ,user):
        try:
            ticket_obj = Tickets.objects.filter(user = user , is_ticket_used = False).first()
            if ticket_obj:
                return ticket_obj
            ticket_code = generate_random_string(7)
            ticket_obj =Tickets.objects.create(ticket=ticket_code , user = user)
            return ticket_obj
        
        except Exception as e:
            print(e)
        return None
    

class Prizes(models.Model):
    prize_name = models.CharField(max_length=100)
    prize_date = models.DateField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    
    def __str__(self):
        return self.prize_name

    
class LuckyDraws(models.Model):
    lucky_draw_name = models.CharField(max_length=100)
    lucky_draw_timings = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    prize = models.ManyToManyField(Prizes)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.lucky_draw_name
    
    def get_active_lucky_draws(self):
        try:
            lucky_draw_objs = LuckyDraws.objects.filter(is_active=True)
            result = []
            for lucky_draw_obj in lucky_draw_objs:
                prizes = []
                for pize_obj in lucky_draw_obj.prize.all():
                    prizes.append({
                        'prize_name' : pize_obj.prize_name,
                        'prize_date' : pize_obj.prize_date
                    })    
                
                result.append({
                    'lucky_draw_name' : lucky_draw_obj.lucky_draw_name,
                    'lucky_draw_timings' : lucky_draw_obj.lucky_draw_timings,
                    'is_active' : lucky_draw_obj.is_active,
                    'prizes' : prizes,
                })
                    
                return result
        
        except Exception as e: 
            print(e)    
        
            return []    
        
        
        
    
        

class LuckyDrawWinners(models.Model):
    ticket = models.ForeignKey(Tickets , on_delete=models.SET_NULL , null=True , blank=True)
    prize = models.ForeignKey(Prizes , on_delete=models.SET_NULL , null=True , blank=True)
    lucky_draw = models.ForeignKey(LuckyDraws , on_delete=models.SET_NULL , null=True , blank=True)        
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.ticket.user.username  + " won " + self.prize.prize_name
    
    def get_winners(days = 7):
        result = []
        try:
            winner_objs = LuckyDrawWinners.objects.filter(created_at__gte=datetime.now()-timedelta(days=7 ))
            for winner_obj in winner_objs:
                result.append({
                  'lucky_draw_name' : winner_obj.lucky_draw.lucky_draw_name,
                  'ticket' : winner_obj.ticket.ticket,
                  'user' : winner_obj.ticket.user.username,
                  'winning_date' : str(winner_obj.created_at)     
                })
                    
                
        except Exception as e: 
            print(e)
            
            
        return result

class GameParticipants(models.Model):
    lucky_draw = models.ForeignKey(LuckyDraws , on_delete=models.SET_NULL , null=True , blank=True)
    ticket = models.ForeignKey(Tickets , on_delete=models.SET_NULL , null=True , blank=True)
    is_won = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.ticket.ticket + " " + self.ticket.user.username
    