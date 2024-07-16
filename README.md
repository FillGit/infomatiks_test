# infomatiks_test


Installation
------------
    
    sudo apt-get -y update
    
    sudo apt-get -y install libunwind-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-bad1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio
    
    sudo -H pip install paho-mqtt==1.6.1 SQLAlchemy==2.0.30 fastapi==0.111.0 uvicorn==0.29.0


Для того, чтобы начать процесс, вам нужно:

    в файле ip_mqtt_subscribe.service поменять, то что в закрытых скобка.
    Например:

        [Unit]
        Description="ip mqtt subscribe"

        [Service]
        User=dima
        Group=dime
        WorkingDirectory=/home/dima/infomatiks_test
        ExecStart=/usr/bin/python3 ip_mqtt_subscribe.py

        [Install]
        WantedBy=multi-user.target

    Добавте этот файл в /etc/systemd/system.

    в файле rtsp_url.txt. Например:
        
        rtsp://admin:admin@192.168.1.99:554/av0_0

    Запуск сервиса:

        sudo systemctl enable ip_mqtt_subscribe
        sudo systemctl start ip_mqtt_subscribe


Запуск infomatiks-API:
    
    uvicorn main:app --reload

    Здесь есть три эндпоинта:

        http://127.0.0.1:8000/v1/video - Эндпоинт для доступа к текущему
        видеопотоку в реальном времени.
        
        http://127.0.0.1:8000/v1/emulation_server - Эндпоинт для показа видеофрагментов на видеорегистратор.

        http://127.0.0.1:8000/v1/metadata_video_fragments/{name_time} - Эндпоинт для получения метаданных, связанных с видеофрагментами.

        name_time - это название видеофрагментов, например 3Y8I-17_48_54

        К примеру, за 10 секунд mqtt_publisher шлет сообщение:
        [{"name":"3Y8IqwtA",
          "coordinatex":"56.52896723732562",
          "out_n":"out1",
          "out_time":"2024-07-14 11:28:02",
          "coordinatey":"85.06633381996583",
          "flight_number":"13c",
          "id":18,
          "coordinates_time":"2024-07-14 11:28:02.734608",
          "name_time":"3Y8I-17_48_54"},
          .... ]

        Координаты GPS - coordinatex, coordinatey
        Номер рейса - flight_number
        Время начала видеофрагмента - out_time
        Время взятие координат - coordinates_time
