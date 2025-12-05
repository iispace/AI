# 강화학습 기반 장애물 회피 자율 주행 시스템 연구

## 프로젝트 진행 단계

1. 이동체를 RC Car로 제작하여 아두이노 제어와 모터 구동 상태 등을 확인 후 RC 기능(블루투스 조종 기능) 제거
2. Rpi 5에 Python 가상 환경 설정
3. 하드웨어 구현
   
   3.1. 이동체 제어보드인 아두이노와 Raspberry Pi 5 사이의 UART 통신 및 카메라 테스트<br>
   3.2. Raspberry Pi 5 전원 공급 장치 연결<br>
   3.3. Arduino Uno 3축 가속도 센서 설치<br>
   3.4. Raspberry Pi 5 프로그램 동작 On/Off 버튼 추가<br>
   
5. 강화학습 모델 설계 및 구현
6. 강화학습 모델 탑재 및 학습
7. 장애물 회피 자율 주행 테스트


## 재료

[materials](https://github.com/iispace/AI/blob/main/RL/RL%EA%B8%B0%EB%B0%98_%EC%9E%A5%EC%95%A0%EB%AC%BC%ED%9A%8C%ED%94%BC_%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/materials.md)

<br>


## 하드웨어 모형

 <img width="1056" height="400" alt="image" src="https://github.com/user-attachments/assets/85f72427-f718-4344-b512-90ff58b525d2" />

  - [Rpi 5 3D model step file](https://www.elecrow.com/blog/download-the-raspberry-pi-5-3d-design-stp-file-for-free-from-elecrow.html)
  - [Rpi 5 Active Cooler 3D model step file](https://www.printables.com/model/858776-raspberry-pi-active-cooler/files)
  - [Arduino Uno 3D model step file](https://www.printables.com/model/358867-arduino-uno-3d-model-stp/remixes)

    <img width="580" height="400" alt="image" src="https://github.com/user-attachments/assets/2d615726-43fd-4e32-a77a-2a6d35f452b5" />


<hr>

### [1단계: RC Car 제작을 통한 모터 드라이버 구동 및 제어 동작 확인](https://github.com/iispace/AI/blob/main/RL/RL%EA%B8%B0%EB%B0%98_%EC%9E%A5%EC%95%A0%EB%AC%BC%ED%9A%8C%ED%94%BC_%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/Phase_1.md)



### [2단계: Raspberry Pi 5에 Python 가상환경 설정](https://github.com/iispace/AI/blob/main/RL/RL%EA%B8%B0%EB%B0%98_%EC%9E%A5%EC%95%A0%EB%AC%BC%ED%9A%8C%ED%94%BC_%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/Phase_2.md)

 
### [3단계] 하드웨어 구현 

  - [Arduino <-> Raspberry Pi 5 UART 통신 및 카메라 테스트](https://github.com/iispace/AI/blob/main/RL/RL%EA%B8%B0%EB%B0%98_%EC%9E%A5%EC%95%A0%EB%AC%BC%ED%9A%8C%ED%94%BC_%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/Phase_3_1.md)
  - [Rpi 5 Power Supply & Display](https://github.com/iispace/AI/blob/main/RL/RL%EA%B8%B0%EB%B0%98_%EC%9E%A5%EC%95%A0%EB%AC%BC%ED%9A%8C%ED%94%BC_%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/Phase_3_2.md)
  - [Arduino 가속도 센서](https://github.com/iispace/AI/blob/main/RL/RL%EA%B8%B0%EB%B0%98_%EC%9E%A5%EC%95%A0%EB%AC%BC%ED%9A%8C%ED%94%BC_%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/Phase_3_3.md)
  - [Rpi 5 프로그램 동작 On/Off 버튼 추가](https://github.com/iispace/AI/blob/main/RL/RL%EA%B8%B0%EB%B0%98_%EC%9E%A5%EC%95%A0%EB%AC%BC%ED%9A%8C%ED%94%BC_%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/Phase_3_4.md)

### [4단계] 강화학습 모델 연구

 - [선행 연구 고찰](https://github.com/iispace/AI/tree/main/RL/%EA%B4%80%EB%A0%A8%EB%85%BC%EB%AC%B8)
 - [강화학습 모델 설계 및 구현](https://github.com/iispace/AI/blob/main/RL/RL%EA%B8%B0%EB%B0%98_%EC%9E%A5%EC%95%A0%EB%AC%BC%ED%9A%8C%ED%94%BC_%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/Phase_4_1.md)


### [5단계: 이동체 강화학습 모델 탑재 및 학습](#)


### [6단계: 장애물 회피 자율주행 테스트](#)

