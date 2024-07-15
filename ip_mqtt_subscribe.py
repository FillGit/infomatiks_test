import globals

import signal
import shlex
import threading

import subprocess as sp
from subprocess import Popen

from ip_mqtt_publisher import ip_mqtt_publisher
import paho.mqtt.client as mqtt
from typing import Union

from database import engine, Base
from operations.models import Operation
from sqlalchemy.orm import Session


session = Session(bind=engine)
received_messages = []


def on_message(client, userdata, message):
    mes = str(message.payload.decode('utf-8'))
    if not received_messages:
        received_messages.append(mes)
    if received_messages:
        if mes != received_messages[-1]:
            received_messages.append(mes)


def db_read(session, received_mes):
    list_mes = received_mes.split('+')
    md = {'name': list_mes[0],
          'flight_number': list_mes[1],
          'coordinatex': list_mes[2],
          'coordinatey': list_mes[3],
          'out_n': list_mes[4],
          'coordinates_time': list_mes[5],
          'out_time': list_mes[-1]}
    name_time = f"{md['name'][0:4]}-{md['out_time'][-8:].replace(':', '_')}"
    session.add(Operation(
        name=md['name'],
        flight_number=md['flight_number'],
        coordinatex=md['coordinatex'],
        coordinatey=md['coordinatey'],
        out_n=md['out_n'],
        out_time=md['out_time'],
        coordinates_time=md['coordinates_time'],
        name_time=name_time))
    session.commit()


def get_popen(rtsp_url: str, received_mes: str,
              p: Union[Popen, None], last_mes: str = None) -> Popen:
    list_mes = received_mes.split('+')
    md = {'name': list_mes[0][0:4],
          'out_n': list_mes[4],
          'out_time': list_mes[-1]}
    if last_mes:
        list_last_mes = last_mes.split('+')
        last_md = {'out_time': list_last_mes[-1]}

    if not last_mes:
        return sp.Popen(shlex.split(get_gst_launch(rtsp_url, md)),
                        stdout=sp.PIPE, stderr=sp.PIPE)

    if md['out_time'] != last_md['out_time']:
        p.send_signal(signal.SIGINT)
        p.stdout.close()
        p.wait()
        return sp.Popen(shlex.split(get_gst_launch(rtsp_url, md)),
                        stdout=sp.PIPE, stderr=sp.PIPE)
    return p


def get_gst_launch(rtsp_url: str, md: dict[str]) -> str:
    with open('rtsp_url.txt', 'w+', encoding='utf-8') as f:
        f.truncate(0)
        f.write(rtsp_url)

    gstreamer_exe = 'gst-launch-1.0'
    name_time = f"{md['name']}-{md['out_time'][-8:].replace(':', '_')}.mp4"
    gst_launch = f"{gstreamer_exe} rtspsrc location={rtsp_url} ! "
    gst_launch += "rtph264depay ! h264parse ! mp4mux ! "
    gst_launch += f"filesink location=out/{md['out_n']}/{name_time} -e"
    return gst_launch


def ip_mqtt_camera(session: Session, rtsp_url: str):
    Base.metadata.create_all(bind=engine)

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
            db_read(session, received_messages[-1])
            if not last_mes:
                p = get_popen(rtsp_url, received_messages[-1], p)
            else:
                p = get_popen(rtsp_url, received_messages[-1], p, last_mes)
            last_mes = received_messages[-1]
        else:
            continue

    p.send_signal(signal.SIGINT)
    p.stdout.close()
    p.wait()
    client.loop_stop()


def correct_rtsp_url(rtsp_url):
    gstreamer_exe = 'gst-launch-1.0'
    gst_launch = f"{gstreamer_exe} rtspsrc location={rtsp_url} "
    p = sp.Popen(shlex.split(gst_launch), stdout=sp.PIPE, stderr=sp.PIPE)
    res = p.communicate()
    error = res[1].decode()
    p.stdout.close()
    p.wait()
    if "ERROR: pipeline doesn't want to preroll.\n" == error[-41:]:
        print('Вы неправильно указали rtsp_url')
        return False
    return True


if __name__ == "__main__":
    # rtsp://admin:admin@192.168.1.99:554/av0_0
    rtsp_url = input('Введите свой rtsp_url: ')

    if correct_rtsp_url(rtsp_url):
        t1 = threading.Thread(target=ip_mqtt_camera, args=(session,
                                                           rtsp_url,))
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
