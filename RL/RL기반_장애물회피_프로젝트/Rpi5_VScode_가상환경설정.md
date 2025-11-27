# Raspberry Pi 5(Rpi 5)에서 개인 프로젝트 진행을 위해 파이썬 가상환경 설치한 방법

**⚠️ 주의사항**

<img width="994" height="63" alt="image" src="https://github.com/user-attachments/assets/978f8b51-1d98-4a03-ae69-ab8ce9c47666" />

<hr>

- 인터넷에 흔히 알려진 바와 같이 ``` python -m venv --system-site-packages env ``` 이 명령어를 이용하여 가상환경을 생성하면 picamera2와 같이 Rpi 5에 기본적으로 설치되어 있는 주요 라이브러리들을 가상환경에서도 별다른 작업 없이 그대로 사용할 수 있다. 
- 그런데, 가상환경에서 opencv를 설치하기 위해 pip install opencv-python을 실행하면 opencv와 호환되는 버전의 numpy가 설치되지 못한 채 opencv가 설치된다.
- 이 상태에서 import cv2를 하면 numpy.dtype error가 발생했다. 이유인 즉, opencv에서 사용하는 numpy version이 현재 Rpi 5 OS에 설치되어 있는 기본 Python 환경에 포함된 numpy version보다 낮은데, 가상환경에서는 Rpi 5 OS에 있는 라이브러리를 삭제하거나 추가하지 못하기 때문에 opencv가 설치되는 과정에서 numpy version이 수정되지 못했던 것이다.
- Rpi 5 OS에 있는 기본 파이썬 환경의 numpy version을 건드리고 싶지는 않았기 때문에 다음과 같은 방법으로 Rpi 5 OS에 있는 python 환경과 독립적인 가상환경을 생성하고 필요한 라이브러리들은 다시 설치하거나 Rpi 5 OS에 있는 Python환경에서 직접 복사해 오는 방법으로 환경을 설정했다.


### 가상환경 생성

  - VSCode는 설치 되어 있는 것으로 본다.

    <img width="1133" height="235" alt="image" src="https://github.com/user-attachments/assets/99299cc5-2203-4196-a321-5c27ddb9b7c3" />

  - VSCode의 오른쪽 하단 구석에 Python Interpreter 선택하는 곳에서 위에서 생성한 가상환경이 제대로 선택되어 있는지 확인한다.
  - 이제, 필요한 라이브러리들을 설치할 수 있도록 VSCode에서 Terminal을 열고, ```source ./env/bin/activate ``` 명령어로 Terminal에서도 가상환경으로 진입한다.
  - 프로젝트에 필요한 주요 라이브러리 중 하나인 "opencv"를 설치하기 위해 ``` pip install opencv-python ```를 실행한다. 별다른 문제 없이 설치가 잘 된다.(numpy version도 호환되는 버전으로 맞춰진다.)
  - 다음으로, 또 다른 주요 라이브러리인 "picamera2"를 설치하기 위해 ``` pip install picamera2 ```를 실행한다. 그런데, 이번에는 설치가 되지 않고, libcap headers 설치가 필요하다는 오류 메시지가 나온다.
  - Rpi 5 OS terminal로 돌아가서 아래와 같이 실행하여 libcap headers를 설치한다.
    
    <img width="1248" height="52" alt="image" src="https://github.com/user-attachments/assets/cc4a4a39-67ed-4818-b0b4-1f13fca88952" />

  - 이제 다시 VSCode의 Terminal로 가서 ``` pip install picamera2 ```를 한 번 더 실행한다. 이번에는 어떤 warning이 보이기는 했으나(켑처를 못했음) 설치는 된 것 같다.
  - 그런데, 막상 python code로 ```from picamera2 import Picamer2```를 실행해 보면, libcamera module이 없다고 나온다.
  - libcamera module을 pip로 설치해 보려 하였으나, 설치 되지 않았다. (설치할 수 있는 버전이 없거나 그런 모듈이 없거나 뭐 그런 오류가 발생했었던 듯....)
  - 고민 끝에, Rpi 5 OS의 기본 Python 환경에 설치되어 있는 라이브러리를 찾아서 현재 사용하는 가상환경으로 복사해 오기로 했다.
    - Rpi 5 기본 Python 환경의 라이브러리들이 있는 경로로 가서 libcamera 폴더를 통째로 복사해서 현재 프로젝트의 가상환경 라이브러리 폴더에 붙여 넣었다.
      
      - Rpi 5 기본 Python 환경의 라이브러리들이 있는 경로: /usr/lib/python3/dist-packages
      - 프로젝트 가상환경 라이브러리 폴더: {프로젝트 폴더}/env/lib/pythonX/site-packages (=> pythonX에서 X는 python의 version)
  
  - 다시 VSCode에 돌아와서 python code로 ```from picamera2 import Picamer2```를 실행했더니 이번에는 libcamera가 아니라 또 다른 어떤 모듈이 없다고 나왔는데, 이번에도 libcamera 모듈을 복사해 온 것처럼 같은 방법으로 복사해 왔다.
  - 또 다시 VSCode에 돌아와서 ```from picamera2 import Picamer2```를 실행했더니, 이번에는 문제 없이 잘 실행되었다.

  - Rpi 5의 여러 GPIO핀들에도 접근하는 코드를 작성할 수 있도록 ```pip install gpiozero ```도 실행해 보았는데, gpiozero 모듈은 문제 없이 잘 설치가 되었다.
