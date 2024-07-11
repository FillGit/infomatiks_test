import globals

import signal
import shlex
import threading

import subprocess as sp
from subprocess import Popen

from ip_publisher import ip_mqtt_publisher
import paho.mqtt.client as mqtt
from typing import Dict, Union


received_messages = []


def on_message(client, userdata, message):
    mes = str(message.payload.decode('utf-8'))
    if not received_messages:
        received_messages.append(mes)
    if received_messages:
        if mes != received_messages[-1]:
            received_messages.append(mes)


def received_out(received_mes: str, p: Union[Popen, None],
                 last_mes: str = None) -> Popen:
    list_mes = received_mes.split('+')
    md = {'name': list_mes[0][0:4],
          'out_n': list_mes[4],
          'd_time': list_mes[-1]}
    if last_mes:
        list_last_mes = last_mes.split('+')
        last_md = {'d_time': list_last_mes[-1]}

    if not last_mes:
        return sp.Popen(shlex.split(get_gst_launch(md)), stdout=sp.PIPE)

    if md['d_time'] != last_md['d_time']:
        p.send_signal(signal.SIGINT)
        p.stdout.close()
        p.wait()
        return sp.Popen(shlex.split(get_gst_launch(md)), stdout=sp.PIPE)
    return p


def get_gst_launch(md: dict[str]) -> str:
    rtsp_url = 'rtsp://admin:admin@192.168.1.99:554/av0_0'
    gstreamer_exe = 'gst-launch-1.0'
    out_name = f"{md['name']}-{md['d_time'][-8:].replace(':', '_')}.mp4"
    gst_launch = f"{gstreamer_exe} rtspsrc location={rtsp_url} ! "
    gst_launch += "rtph264depay ! h264parse ! mp4mux ! "
    gst_launch += f"filesink location={md['out_n']}/{out_name} -e"
    return gst_launch


def ip_camera():
    mqttBroker = 'mqtt.eclipseprojects.io'
    client = mqtt.Client('video recorder')
    client.connect(mqttBroker)

    client.loop_start()
    client.subscribe("METADATA")
    client.on_message = on_message

    last_mes = None
    p = None

    while globals.flag:
        if received_messages and last_mes != received_messages[-1]:
            if not last_mes:
                p = received_out(received_messages[-1], p)
            else:
                p = received_out(received_messages[-1], p, last_mes)
            last_mes = received_messages[-1]
        else:
            continue

    p.send_signal(signal.SIGINT)
    p.stdout.close()
    p.wait()
    client.loop_stop()


if __name__ == "__main__":
    t1 = threading.Thread(target=ip_camera)
    t2 = threading.Thread(target=ip_mqtt_publisher)

    t1.start()
    t2.start()

    while True:
        m = input('Введите q и ENTER, для остановки процесса: ')
        if m == 'q':
            globals.flag = False
            break

    t1.join()
    t2.join()
