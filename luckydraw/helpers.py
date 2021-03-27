
import string
import random
# from .models import Tickets


def generate_random_string(N):
    result  = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = N))
    # if Tickets.objects.filter(ticket = result).first():
    #     generate_random_string(N)
        
    return result


