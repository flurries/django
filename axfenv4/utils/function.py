
import random
from datetime import datetime

def random_titck():
    s = ''
    a = '123456789qwertyuiopasdfghjklzxcvbnmQAZWSXEDCRFVTGBYHNUJMIKOLP'
    for _ in range(20):
        s += random.choice(a)
    return s


def get_order():
    num = ''
    number = '0123456789'
    for _ in range(20):
        num += random.choice(number)
    num = num + datetime.now().strftime("%Y%m%d%H%M%S")
    return num
