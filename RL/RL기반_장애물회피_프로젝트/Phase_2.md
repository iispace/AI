# 2 단계: Raspberry Pi 5 부분


### 0. Python 가상환경 생성
  
  - Raspberry Pi 5 OS인 bookworm은 이미 설치된 상태임
      
  - Raspberry Pi 5 홈 폴더 하위에 작업 폴더 생성:
    - 작업 폴더명: RL_CAR
        
  - 작업 폴더 하위에 가상환경을 설치할 "env" 폴더 생성
        
  - env 폴더에 가상환경 생성
    - 작업 폴더인 RL_CAR에서 터미널 열고 아래 명령 실행
      - ``` python -m venv --system-site-packages env   ```
    - 명령 실행 후 env 폴더에 가상환경이 설치되었는지 확인 : bin, include, lib 등의 폴더와 pyvenv.cfg 파일이 생성되었다면 OK

  - 가상환경에 필요한 라이브러리 추가 설치
    - pip install opencv-python
    - ...

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
