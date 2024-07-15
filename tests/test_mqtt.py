import globals
import os
import shlex
import subprocess as sp
import time
import threading

from ip_mqtt_publisher import ip_mqtt_publisher
from ip_mqtt_subscribe import correct_rtsp_url, get_gst_launch, get_popen
from hamcrest import assert_that, is_, has_length
import paho.mqtt.client as mqtt
from subprocess import Popen

RTSP_URL_CORRECT = 'rtsp://rtspstream:0be18a5171bcc7d6db04a09cd4260432@zephyr.rtsp.stream/movie'
received_messages = []


def on_message(client, userdata, message):
    received_messages.append(str(message.payload.decode('utf-8')))


def mqtt_subscribe():
    mqttBroker = 'mqtt.eclipseprojects.io'
    client = mqtt.Client('video recorder')
    client.connect(mqttBroker)

    client.loop_start()
    client.subscribe("METADATA")
    while globals.flag:
        client.on_message = on_message

    client.loop_stop()


def test_ip_mqtt_publisher(session):
    t1 = threading.Thread(target=ip_mqtt_publisher)
    t2 = threading.Thread(target=mqtt_subscribe)
    t1.start()
    t2.start()
    time.sleep(11)
    globals.flag = False
    t1.join()
    t2.join()

    res = received_messages[0].split('+')
    print(received_messages[0])
    assert_that(res[0], has_length(8))
    assert_that(res[1], has_length(3))
    assert_that(res[4], is_('out1'))
    assert_that(res, has_length(7))


def test_correct_rtsp_url():
    assert_that(
        correct_rtsp_url('rtsp://localhost:8000/av0_0'), is_(False))
    assert_that(correct_rtsp_url(RTSP_URL_CORRECT), is_(True))


def test_get_gst_launch():
    md = {
        'name': 'qwer1234',
        'out_time': '2022-01-10 10:11:12',
        'out_n': 'out1'
    }
    assert_that(get_gst_launch(RTSP_URL_CORRECT, md),
                is_('gst-launch-1.0 rtspsrc location=rtsp://rtspstream:0be18a5171bcc7d6db04a09cd4260432@zephyr.rtsp.stream/movie ! rtph264depay ! h264parse ! mp4mux ! filesink location=out/out1/qwer1234-10_11_12.mp4 -e'))


def test_get_popen():
    p = None
    received_mes = 'ZBGuW95J+13c+56.52699988947395+85.07500201495604+out1+2024-07-15 22:48:12.041929+2024-07-15 22:48:12'
    last_mes = 'ZBGuW95J+13c+56.52802974320799+85.07654604907547+out1+2024-07-15 22:53:08.519887+2024-07-15 22:52:58'

    assert_that(get_popen(RTSP_URL_CORRECT, received_mes, p, received_mes),
                is_(None))
    assert_that(get_popen(RTSP_URL_CORRECT, received_mes, p), is_(Popen))

    p = sp.Popen(
        shlex.split('gst-launch-1.0 rtspsrc location=rtsp://rtspstream:0be18a5171bcc7d6db04a09cd4260432@zephyr.rtsp.stream/movie ! rtph264depay ! h264parse ! mp4mux ! filesink location=out/out1/qwer1234-10_11_12.mp4 -e'),
        stdout=sp.PIPE, stderr=sp.PIPE)

    assert_that(get_popen(RTSP_URL_CORRECT, received_mes, p, last_mes),
                is_(Popen))
    time.sleep(10)
    os.remove('out/out1/ZBGu-22_48_12.mp4')
