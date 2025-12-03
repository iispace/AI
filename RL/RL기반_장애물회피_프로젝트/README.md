# 강화학습 기반 장애물 회피 자율 주행 시스템 제작

## 프로젝트 진행 단계

1. 이동체를 RC Car로 제작하여 아두이노 제어와 모터 구동 상태 등을 확인
2. Raspberry Pi 5 하드웨어 구성: 카메라 연결 및 테스트, Display 장치 연결 및 테스트, UPS 전원 연결
3. 이동체 제어보드인 아두이노와 Raspberry Pi 5 사이의 UART 통신 구현 및 테스트
4. 강화학습 모델 설계 및 구현
5. 이동체에서 RC 기능 제거 후 강화학습 모델 탑재
6. 이동체 주행 환경에서 강화학습 진행


## 재료

[materials](https://github.com/iispace/AI/blob/main/RL/RL%EA%B8%B0%EB%B0%98_%EC%9E%A5%EC%95%A0%EB%AC%BC%ED%9A%8C%ED%94%BC_%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/materials.md)

<br>


## 최종 하드웨어 구성도(안)

 <img width="1020" height="400" alt="image" src="https://github.com/user-attachments/assets/fd408eb5-31a2-4b51-a05f-e66eb2a8a8c1" />

  - [Rpi 5 3D model step file](https://www.elecrow.com/blog/download-the-raspberry-pi-5-3d-design-stp-file-for-free-from-elecrow.html)
  - [Rpi 5 Active Cooler 3D model step file](https://www.printables.com/model/858776-raspberry-pi-active-cooler/files)
  - [Arduino Uno 3D model step file](https://www.printables.com/model/358867-arduino-uno-3d-model-stp/remixes)

    <img width="476" height="400" alt="image" src="https://github.com/user-attachments/assets/4f5ab685-6078-4db1-be15-954d1fb50b60" />

<hr>

### [1단계: RC Car 제작을 통한 모터 드라이버 동작 확인](https://github.com/iispace/AI/blob/main/RL/RL%EA%B8%B0%EB%B0%98_%EC%9E%A5%EC%95%A0%EB%AC%BC%ED%9A%8C%ED%94%BC_%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/Phase_1.md)



### [2단계: Raspberry Pi 5에 Python 가상환경 설정](https://github.com/iispace/AI/blob/main/RL/RL%EA%B8%B0%EB%B0%98_%EC%9E%A5%EC%95%A0%EB%AC%BC%ED%9A%8C%ED%94%BC_%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/Phase_2.md)

 
### [3단계] Rpi 5 <-> Arduino Uno 통신, Rpi 5 전원, 카메라 + Arduino 가속도 센서 

  - [Arduino <-> Raspberry Pi 5 UART 통신 및 카메라 테스트](https://github.com/iispace/AI/blob/main/RL/RL%EA%B8%B0%EB%B0%98_%EC%9E%A5%EC%95%A0%EB%AC%BC%ED%9A%8C%ED%94%BC_%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/Phase_3_1.md)
  - [Rpi 5 Power Supply & Display](https://github.com/iispace/AI/blob/main/RL/RL%EA%B8%B0%EB%B0%98_%EC%9E%A5%EC%95%A0%EB%AC%BC%ED%9A%8C%ED%94%BC_%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/Phase_3_2.md)
  - [Arduino 가속도 센서](https://github.com/iispace/AI/blob/main/RL/RL%EA%B8%B0%EB%B0%98_%EC%9E%A5%EC%95%A0%EB%AC%BC%ED%9A%8C%ED%94%BC_%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/Phase_3_3.md)

### [4단계] 강화학습 모델 연구

 - [선행 연구 고찰](https://github.com/iispace/AI/blob/main/RL/RL%EA%B8%B0%EB%B0%98_%EC%9E%A5%EC%95%A0%EB%AC%BC%ED%9A%8C%ED%94%BC_%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/Phase_4_1.md)
 - [강화학습 모델 설계 및 구현](#)


### [5단계: 이동체 강화학습 모델 탑재 및 학습](#)


### [6단계: 장애물 회피 자율주행 테스트](#)

