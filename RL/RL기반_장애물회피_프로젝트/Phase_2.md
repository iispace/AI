# 2 단계: Raspberry Pi 5 부분


### 0. Python 가상환경 생성
  
  - Raspberry Pi 5 OS인 bookworm은 이미 설치된 상태임
      
  - Raspberry Pi 5 홈 폴더 하위에 작업 폴더 생성
        
  - 작업 폴더 하위에 가상환경을 설치할 "env" 폴더 생성
        
  - env 폴더에 가상환경 생성 및 활성화
    - 작업 폴더에서 터미널 열고 아래 명령 실행
      - ``` python -m venv env ```
      - ``` source env/bin/activate ```

        <img width="744" height="189" alt="image" src="https://github.com/user-attachments/assets/6dc84b55-b82d-43a9-af90-128cea1b99f1" />


  - 현재 작업 중인 terminal에서 가상환경에 필요한 라이브러리 계속 추가 설치
    - ``` pip install --upgrade pip ```
    - ``` pip install numpy matplotlib opencv-python torch torchvision ```
    - picamera2"를 설치하기 위해 ```pip install picamera2```를 실행했을 때, libcap headers 설치가 필요하다는 오류 메시지가 나오면 다음과 같이 apt로 libcap-dev를 설치한 후 다시 시도했더니 설치됨.

       <img width="847" height="34" alt="image" src="https://github.com/user-attachments/assets/3d6a511e-3ecd-4830-b6e3-6106a132ba8a" />

    - 설치 확인
      ```
      python - <<EOF
      import sys, numpy, cv2, torch
      print("Python:", sys.version)
      print("NumPy:", numpy.__version__)
      print("OpenCV:", cv2.__version__)
      print("Torch:", torch.__version__)
      EOF
        ```

      - 설치된 라이브러리 중 picamera2를 확인하기 위해 가상환경 내에서 python을 실행한 후 ```from picamera2 import Picamera2 ```를 했을 때 libcamera 모듈이 없다는 오류 발생. => Rpi 5 OS에 기본으로 설치된 Python 환경에서 해당 라이브러리를 복사한 후 현재 사용중인 가상환경의 라이브러리 폴더에 붙여 넣어서 해결.
        
        - Rpi 5 OS 기본 Python 환경의 라이브러리 경로: /usr/lib/python3/dist-packages
        - 프로젝트 가상환경 라이브러리 경로: {프로젝트 폴더}/env/lib/pythonX/site-packages (=> pythonX에서 X는 python의 version)

      - libcamera 모듈을 붙여넣기 한 후에 가상환경의 python에서 ```from picamera2 import Picamera2 ```을 다시 실행하니, 이번에는 pykms 모듈 없음 오류 발생. => libcamera 모듈을 복사해서 붙여넣기한 것처럼 같은 방법으로 pykms 모듈을 붙여넣기하여 해결.
     
      - ``` pip install gpiozero ```
        
<hr>

### 1. UPS 장치 연결

  - 포고 핀(Pogo pin) 연결 방식의 UPS 모듈이므로 Raspberry Pi 5 하단에 직접 적층하여 연결
    
    <img width="182" height="144" alt="image" src="https://github.com/user-attachments/assets/0a8a995c-08ce-43a9-9471-5c2f1ad4bda3" />
    <img width="223" height="144" alt="image" src="https://github.com/user-attachments/assets/86fd045e-0bd7-4202-840f-768e4a8de1c5" />


<hr>

### 2. Display 장치 연결

  - 케이블 연결
    
  - Display 테스트


<hr>

### 3. 카메라 연결

  - Raspberry Pi 5 CAM/DISP 1 connector에 카메라 케이블 연결
    
    <img width="174" height="127" alt="image" src="https://github.com/user-attachments/assets/756bde61-8948-4c7e-97be-a962247ca1ca" />
    <img width="145" height="127" alt="image" src="https://github.com/user-attachments/assets/ad4396f7-10ca-45ae-8d1c-1cb7ee8060b6" />

  
      
  - 카메라 테스트


<hr>
