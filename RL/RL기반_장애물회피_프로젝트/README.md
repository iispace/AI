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

 <img width="602" height="350" alt="image" src="https://github.com/user-attachments/assets/b8397133-7123-4830-956b-729bcffc675d" />
 <img width="280" height="350" alt="image" src="https://github.com/user-attachments/assets/73e1293d-6619-4772-8a25-7f97668f7650" />


<hr>

### [1단계: RC Car 제작](https://github.com/iispace/AI/blob/main/RL/RL%EA%B8%B0%EB%B0%98_%EC%9E%A5%EC%95%A0%EB%AC%BC%ED%9A%8C%ED%94%BC_%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/Phase_1.md)



### [2단계: Raspberry Pi 5 하드웨어 구성](https://github.com/iispace/AI/blob/main/RL/RL%EA%B8%B0%EB%B0%98_%EC%9E%A5%EC%95%A0%EB%AC%BC%ED%9A%8C%ED%94%BC_%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/Phase_2.md)

 
### [3단계] 통신, 디스플레이 및 Rpi 5 전원

  - [Arduino <-> Raspberry Pi 5 UART 통신 및 카메라 테스트](https://github.com/iispace/AI/blob/main/RL/RL%EA%B8%B0%EB%B0%98_%EC%9E%A5%EC%95%A0%EB%AC%BC%ED%9A%8C%ED%94%BC_%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/Phase_3_1.md)
  - [Rpi 5 Display & 전원]([#](https://github.com/iispace/AI/blob/main/RL/RL%EA%B8%B0%EB%B0%98_%EC%9E%A5%EC%95%A0%EB%AC%BC%ED%9A%8C%ED%94%BC_%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/Phase_3_2.md))


### [4단계] 강화학습 모델 연구

 - [선행 연구 고찰](https://github.com/iispace/AI/blob/main/RL/RL%EA%B8%B0%EB%B0%98_%EC%9E%A5%EC%95%A0%EB%AC%BC%ED%9A%8C%ED%94%BC_%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/Phase_4_1.md)
 - [강화학습 모델 설계 및 구현](#)


### [5단계: RC 기능 제거, 이동체 강화학습 모델 탑재 및 학습](#)


### [6단계: 장애물 회피 자율주행 테스트](#)

