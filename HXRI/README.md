# HXRI

## In windows

py -3 -m pip install mediapipe
py -3 -m pip install opencv-python==3.4.16.59
py -3 -m pip install mediapipe==0.10.3
py -3 -m pip install -U nep
py -3 -m  pip install pyzed
py -3 -m pip install wheel
py -3 setup.py sdist bdist_wheel
py -3 -m pip install dist/hxri-0.0.0.3.tar.gz

## In Linux/MacOS

python3 -m pip install mediapipe
python3 -m pip install opencv-python==3.4.16.59
python3 -m pip install mediapipe==0.10.3
python3 -m pip install -U nep
python3 -m pip install pyzed
python3 -m pip install wheel
python3 setup.py sdist bdist_wheel
python3 -m pip install dist/hxri-0.0.0.3.tar.gz
