import globals
import paho.mqtt.client as mqtt
import string
import time

from datetime import datetime
from random import choice, uniform


def generate_random_string(length: int) -> str:
    sym = string.ascii_letters + string.digits
    return ''.join(choice(sym) for i in range(length))


def ip_mqtt_publisher():
    mqttBroker = 'mqtt.eclipseprojects.io'
    client = mqtt.Client('IP-camera')
    client.connect(mqttBroker)

    randsyms = generate_random_string(8)
    randnum = choice(['11a', '12b', '13c'])
    d_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    n = 0
    out_n = 'out1'
    while globals.flag:
        randcoordinatex = uniform(56.52400, 56.52900)
        randcoordinatey = uniform(85.06000, 85.08500)
        res = f'{randsyms}+{randnum}+{randcoordinatex}+{randcoordinatey}+{out_n}+{d_time}'
        client.publish('METADATA', res)
        time.sleep(10)
        n += 1
        if n == 6:
            n = 0
            d_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if out_n == 'out1':
                out_n = 'out2'
            else:
                out_n = 'out1'
