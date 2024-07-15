import shlex
import subprocess as sp

from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends

from database import get_db

from operations.models import Operation


router = APIRouter(
    prefix="/v1",
    tags=["Operation"]
)


@router.get('/metadata_video_fragments/{name_time}')
def get_metadata_video_fragments(name_time: str,
                                 db: Session = Depends(get_db)):
    return db.query(
        Operation).filter(Operation.name_time.like(name_time + "%")).all()


def get_gst_launch(rtsp_url) -> str:
    gstreamer_exe = 'gst-launch-1.0'
    gst_launch = f"{gstreamer_exe} rtspsrc location={rtsp_url} "
    gst_launch += "latency=10 ! queue ! rtph264depay ! h264parse ! "
    gst_launch += "avdec_h264 ! videoconvert ! videoscale ! "
    gst_launch += "video/x-raw,width=1280,height=720 ! ximagesink"
    return gst_launch


@router.get('/video')
def get_video():
    try:
        with open('rtsp_url.txt', 'r', encoding='utf-8') as f:
            rtsp_url = f.readlines()[0]
    except Exception:
        return ['нужен файл rtsp_url.txt, запустите ip_mqtt_subscribe.py']

    p = sp.Popen(shlex.split(get_gst_launch(rtsp_url)), stdout=sp.PIPE)
    while True:
        if not p.stdout.read():
            break

    p.stdout.close()
    p.wait()
    return []


@router.get('/emulation_server')
def get_emulation_server():
    sp.call(["xdg-open", "out"])
    return []
