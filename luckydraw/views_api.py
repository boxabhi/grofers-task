from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from django.contrib.auth import authenticate, login


class Login(APIView):
    def post(self, request):
        response = {}
        response['status_code'] = 500
        response['status_message'] = 'Something went wrong'
        try:
            data = request.data
            
            user_obj,_ = User.objects.get_or_create(username=data.get('username'))
            
            login( request , user_obj)
            response['status_code'] = 200
            response['status_message'] = 'Login'
        except Exception as e:
            print(e)
            
        return Response(response)

Login = Login.as_view()       
    

class GetTicketView(APIView):
    
    def get(self , request):
        response = {}
        response['status_code'] = 500
        response['status_message'] = 'Something went wrong'
        try:
            ticket_class_obj = Tickets() # get_or_create_ticket()
            ticket_obj = ticket_class_obj.get_or_create_ticket(request.user)
            
            if ticket_obj is None:
                raise Exception('Something went wrong')
        
            payload = {}
            
            payload['ticket'] = ticket_obj.ticket
            payload['is_ticket_used'] = ticket_obj.is_ticket_used
            payload['user'] = ticket_obj.user.username
            payload['created_at'] = str(ticket_obj.created_at)
            
            response['data'] = payload
            response['status_code'] = 200
            response['status_message'] = 'Your raffle tickets now you can participate'
            
            
        except Exception as e:
            print(e)

        return Response(response)
GetTicketView = GetTicketView.as_view()



class GetLuckyDraws(APIView):
    
    def get(self, request):
        response = {}
        response['status_code'] = 500
        response['status_message'] = 'Something went wrong'
        
        try:
            lucky_draw_class = LuckyDraws()
            lucky_draw_payload = lucky_draw_class.get_active_lucky_draws()
            
            
            if len(lucky_draw_payload) == 0:
                response['status_code'] = 300
                response['status_message'] = 'No lucky draw running'
                return Response(response)
            
            response['status_code'] = 200
            response['status_message'] = 'All lucky draws'
            response['data'] = lucky_draw_payload
        
        except Exception as e:
            print(e) 
            
        return Response(response)
        
GetLuckyDraws = GetLuckyDraws.as_view()





class GetWinnners(APIView):
    def get(self , request):
        response = {}
        response['status_code'] = 500
        response['status_message'] = 'Something went wrong'
        try:
            lucky_draw_winners_class = LuckyDrawWinners()
            winners_objs = lucky_draw_winners_class.get_winners()

            response['status_code'] = 200
            response['status_message'] = 'Game winners'
            
            response['data'] = winners_objs
            
        except Exception as e: 
            print(e)
        
        return Response(response)  
    
GetWinnners = GetWinnners.as_view()




class ComputeWinners(APIView):
    def post(self , request):
        response = {}
        response['status_code'] = 500
        response['status_message'] = 'Something went wrong'
        
        try:
            data = request.data
                        
            lucky_draw_id =  data.get('lucky_draw_id') 
            current_date = data.get('current_date')
            
            # Validation checks for lucky_draw_id,current_date
            
            if lucky_draw_id is None:
                response['status_message'] = 'lucky_draw_id is required'
                raise Exception('lucky_draw_id is required')
            
            if current_date is None:
                response['status_message'] = 'current_date is required'
                raise Exception('current_date is required')
                


            

            
            lucky_draw_obj = None
            
            # Getting Lucky draw obj
            
            try:
                lucky_draw_obj = LuckyDraws.objects.get(id = lucky_draw_id)
            except Exception as e:
                print('Invalid lucky draw id')
                
            
            if lucky_draw_obj is None:
                raise Exception('lucky_draw_obj is None')
            
            
            # Getting all game participant for the Lucky draw
            
            game_participants_objs  = GameParticipants.objects.filter(lucky_draw = lucky_draw_obj )
            

            
            if len(game_participants_objs) == 0:
                response['status_code'] = 300
                response['status_message'] = f'No game participants found for lucky draw **{lucky_draw_obj.lucky_draw_name}**'
                raise Exception('No game participants found')
                
                
            
            
            # Getting random object for game winner
            lucky_draw_winner = random.choice(game_participants_objs)
            
            # Valid date format Check
            try:
                current_date = datetime.strptime(current_date, "%Y-%m-%d").date()
            except Exception as e:
                response['status_message'] = f"{current_date} value has an invalid date format. It must be in YYYY-MM-DD format."
                print('Invalid date format')
            
            # Getting prize obj
            prize_obj = lucky_draw_obj.prize.filter(prize_date=current_date).first()
            
            if prize_obj is None:
                response['status_message'] = f"No lucky draw found on this date **{current_date} **"
                raise Exception(f'No lucky draw found on this date **{current_date} **')
            
            
            # Checking is winner already declared for this Lucky draw
            if prize_obj.is_winner_calculated:
                response['status_code'] = 300
                response['status_message'] = f'Winner is already declared for **{lucky_draw_obj.lucky_draw_name}** date **{current_date}**'
                raise Exception('Luckt draw already declared')
                
            
            if prize_obj is None:
                response['status_message'] = 'No lucky draw found on date'
                raise Exception('No lucky draw found on date ')                
                
        
            # Creating Lucky Draw Winner 
            lucky_draw_winner_obj = LuckyDrawWinners.objects.create(
                prize = prize_obj,
                lucky_draw = lucky_draw_obj,
                ticket = lucky_draw_winner.ticket
            )
            
            lucky_draw_winner.is_won = True
            prize_obj.is_winner_calculated = True
            prize_obj.save()
            
            payload = {}
            response['status_code'] = 200
            response['status_message'] = 'Winner computed successfully'
            
            payload['winner'] = lucky_draw_winner.ticket.user.username
            payload['prize'] = prize_obj.prize_name
            payload['ticket'] = lucky_draw_winner.ticket.ticket
            response['data'] = payload
        except Exception as e:
            print(e)
            
        return Response(response)
    
ComputeWinners = ComputeWinners.as_view()




class ParticipateInGame(APIView):
    
    def post(self , request):
        response = {}
        response['status_code'] = 500
        response['status_message'] = 'Something went wrong'
        
        try:
            data = request.data
            user_obj = None
            ticket_id = data.get('ticket_id')
            lucky_draw_id = data.get('lucky_draw_id')
            
            
            # Getting user object if user is authenticated or getting via json response
            
            if request.user.is_authenticated:
                user_obj = request.user
            else:
                user_id = data.get('user_id')
                if user_id is None:
                    response['status_message'] = 'user_id is required'
                    raise Exception('user_id is required')
                try:
                    user_obj = User.objects.get(id = user_id) 
                except Exception as e:
                    response['status_message'] = 'user does not exist'
                    return Response(response)
                    
                    
            # Validation checks for ticket_id and lucky_draw_id
            if ticket_id is None:
                response['status_message'] = 'ticket_id is required'
                raise Exception('ticket_id is required')
            
            if lucky_draw_id is None:
                response['status_message'] = 'lucky_draw_id is required'
                raise Exception('lucky_draw_id is required')

                
            lucky_draw_obj = LuckyDraws.objects.get(id = lucky_draw_id)
            ticket_obj = Tickets.objects.get(id = ticket_id)
            
            # Checking is ticket already used in some other LuckyDraw
            if ticket_obj.is_ticket_used:
                response['status_code'] = 300
                response['status_message'] = 'sorry this ticket is already used'
                raise Exception('ticker already used')
            

            
            # Checking user has already participated in this lucky draw
            if GameParticipants.objects.filter(lucky_draw = lucky_draw_obj ,user = user_obj).first():
                response['status_code'] = 300
                response['status_message'] = 'You have already participated in this LuckyDraw'
                raise Exception('already participated')
            
            
            
            # Finally Creating Game Participant
            game_participant_objs =  GameParticipants.objects.create(
                lucky_draw= lucky_draw_obj,
                ticket=ticket_obj,
                user = user_obj
            )   
            
            ''' 
            After game participant is created setting ticket to True
            so that it can't be used in some other Lucky Draw
            '''
            ticket_obj.is_ticket_used = True
            ticket_obj.save()            
            response['status_code'] = 200
            response['status_message'] = 'You have successfully participated in Lucky draw'    
        except Exception as e:
            print(e)
        return Response(response)
        
        
ParticipateInGame= ParticipateInGame.as_view()