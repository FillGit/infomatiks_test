# infomatiks_test

Создание и конфигурация unit-файла для systemd, вы можете посмотреть в ветке infomatiks-3_systemctl. Но я рекомендую эту ветку:

Installation
------------
    
    sudo apt-get -y update
    
    sudo apt-get -y install libunwind-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-bad1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio
    
    python3 -m venv venv

    source venv/bin/activate

    pip install -r requirements.txt


Для того, чтобы начать процесс, вам нужно запустить:

    python ip_mqtt_subscribe.py

        Введите свой rtsp_url: (например rtsp://admin:admin@192.168.1.99:554/av0_0)

        потом появится

        Введите q и ENTER, для остановки процесса:


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


