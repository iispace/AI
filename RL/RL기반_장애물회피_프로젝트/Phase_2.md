# 2 단계: Raspberry Pi 5 Python 가상환경 설정


### 1. Python 가상환경 생성
 
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
    - ``` pip install numpy matplotlib opencv-python torch torchvision gpiozero lgpio pyserial ```
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
     


### 2. VSCode 열고 python interpretor 선택  

  - 아래와 같이 ``` code . ``` 명령을 실행하여 VSCode 열기
    
    <img width="430" height="45" alt="image" src="https://github.com/user-attachments/assets/63559396-d8e6-449a-ba88-8640b925a24d" />

  - 아래 그림에서 VSCode 하단 오른쪽 코너에 노란색 사각형으로 표시한 부분을 클릭하여 현재 프로젝트를 위해 생성한 가상환경 선택

    <img width="492" height="250" alt="image" src="https://github.com/user-attachments/assets/b5459fdb-f9d6-47e2-9f6e-1e4912f201db" />

<hr>

### [※] Rpi 5 부팅시 특정 Python 스크립트 자동 실행 방법 

 - nano와 같은 편집기로 Rpi 5의 default autostart 파일을 열고 자동 실행할 파이썬 스크립트를 등록하면 됨
   
   - default autostart 파일 열기: ``` sudo nano /etc/xdg/lxsession/DXDE-pi/autostart ```
   - 파일 끝에 추가할 내용: ``` lxterminal -e sudo {python3} /home/pi/{프로젝트폴더}/{실행할_파이썬_스크립트.py} ```
     - 위 명령어에서 {python3} 부분에는 실행할 파이썬 스크립트를 작성할 때 사용한 가상환경의 경로와 함께 지정
   - 내용 추가 후에는 Ctrl+X를 누르고 Save modified buffer?라는 질문에 y를 입력한 후 [엔터]키를 치면 변경 내용이 저장되고 nano 편집기가 종료됨
