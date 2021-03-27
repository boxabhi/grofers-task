from django.contrib import admin


from .models import *  


admin.site.register(Tickets)
admin.site.register(GameParticipants)
admin.site.register(LuckyDraws)
admin.site.register(Prizes)
admin.site.register(LuckyDrawWinners)