# 실제 환경에서의 강화학습 기반 장애물 회피 자율 주행 시스템 연구

## 기존 강화학습 관련 연구의 문제점

1. 대부분의 강화학습 연구는 물리 기반 시뮬레이터에 지나치게 의존적이어서 실제 환경과 시뮬레이션 결과 사이에 차이가 발생할 수 밖에 없는 한계가 있음. 많은 논문들이 시뮬레이터에서의 성능 향상만을 보여주고 있으므로 실제 환경에서의 검증이 부족함.
2. 강화학습의 성능은 보상 설계에 크게 좌우되는데, 작위적으로 설계된 시뮬레이션 환경에 맞춰진 보상 함수를 사용하는 기존의 연구는 보상 함수를 일반화하지 못함. 강화학습의 특성 상 보상 함수가 바뀌면 왼전히 다른 정책이 되므로, 시뮬레이션에서 우수한 성능을 보인 강화학습 모델이 실제 환경에는 제대로 적응하지 못할 가능성이 높음.
4. 고정된 MDP(Markov Decision Process) 조건에서 실험된 강화학습 에이전트는 훈련된 환경에서만 잘 작동하고, 환경이 조금만 달라져도 성능이 급락할 수 있음 (환경 노이즈에 매우 민감)
5. 대규모 연산 자원 의존: 더 큰 환경과 더 많은 파라미터에 의존하는 강화학습 기법 연구는 거대한 연산량을 필요로하는데, 이는 새로운 연구자에게 진입 장벽이 되고 있음.

## 연구 필요성 

1. 시뮬레이터의 불확실성을 벗어날 수 있도록 실제 환경 데이터를 기반으로 한 강화학습 연구 필요
2. 보상 함수의 일반화를 위해 보상 자동 생성 기법 연구 필요
3. Non-stationary MDP 학습 또는 정책의 구조가 아니라 학습되는 표현(representation)에 대한 일반화 연구 필요
4. 경량화된 강화학습 알고리즘 설계 연구 필요


## 연구 목적

1. 단안 카메라를 통해 실제 환경의 데이터를 2D image 형태로 입력 데이터로 수집하고, 이를 기반으로 입력 데이터의 노이즈와 물리적 오차를 학습 가능한 파라미터로 포함하되, 경량화된 강화학습 모델 설계(연산량의 상한을 설정하는 방안 연구하여 설계에 적용). 
2. 보상 함수의 일반화를 위해 보상의 분포를 추정하는 inverse RL 형태 시도
3. Monocular Camera를 설치한 Micro Computer(Raspberry Pi 5)와 Micro Controller (Arduino Uno) 기반의 non-holonomic mobile vehicle(named 'Carserverance')을 제작하고, 설계한 강화학습 모델을 탑재하여 실제 환경에서 스스로 장애물을 회피하며 이동할 수 있도록 학습 진행
4. 기준 시간 동안 carserverance가 스스로 이동하며 장애물을 얼마나 정확하게 회피하는 지를 측정하여 Baseline model과의 차이 비교
5. 모델이 생성한 representation과 출력의 관계를 분석하여 설계한 모델이 어떤 상태에서 어떤 행동을 선택하는지 이유를 설명할 수 있는 단서 추적
6. (추가 연구 목표) 물리적 안전성과 소프트웨어적 안전성 추가


## 재료

[materials](https://github.com/iispace/AI/blob/main/RL/RL%EA%B8%B0%EB%B0%98_%EC%9E%A5%EC%95%A0%EB%AC%BC%ED%9A%8C%ED%94%BC_%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/materials.md)

<br>


## 하드웨어 모형

 <img width="1575" height="627" alt="image" src="https://github.com/user-attachments/assets/66450e69-a835-4291-94ad-e4802750971b" />

  - [Rpi 5 3D model step file](https://www.elecrow.com/blog/download-the-raspberry-pi-5-3d-design-stp-file-for-free-from-elecrow.html)
  - [Rpi 5 Active Cooler 3D model step file](https://www.printables.com/model/858776-raspberry-pi-active-cooler/files)
  - [Arduino Uno 3D model step file](https://www.printables.com/model/358867-arduino-uno-3d-model-stp/remixes)

    <img width="580" height="400" alt="image" src="https://github.com/user-attachments/assets/2d615726-43fd-4e32-a77a-2a6d35f452b5" />


<hr>

## 연구 진행 단계

### [1단계: RC Car 제작을 통한 모터 드라이버 구동 및 제어 동작 확인](https://github.com/iispace/AI/blob/main/RL/RL%EA%B8%B0%EB%B0%98_%EC%9E%A5%EC%95%A0%EB%AC%BC%ED%9A%8C%ED%94%BC_%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/Phase_1.md)



### [2단계: Raspberry Pi 5에 Python 가상환경 설정](https://github.com/iispace/AI/blob/main/RL/RL%EA%B8%B0%EB%B0%98_%EC%9E%A5%EC%95%A0%EB%AC%BC%ED%9A%8C%ED%94%BC_%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/Phase_2.md)

 
### [3단계] 하드웨어 구현 

  - [Arduino <-> Raspberry Pi 5 UART 통신 및 카메라 테스트](https://github.com/iispace/AI/blob/main/RL/RL%EA%B8%B0%EB%B0%98_%EC%9E%A5%EC%95%A0%EB%AC%BC%ED%9A%8C%ED%94%BC_%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/Phase_3_1.md)
  - [Rpi 5 Power Supply & Display](https://github.com/iispace/AI/blob/main/RL/RL%EA%B8%B0%EB%B0%98_%EC%9E%A5%EC%95%A0%EB%AC%BC%ED%9A%8C%ED%94%BC_%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/Phase_3_2.md)
  - [Arduino 가속도 센서](https://github.com/iispace/AI/blob/main/RL/RL%EA%B8%B0%EB%B0%98_%EC%9E%A5%EC%95%A0%EB%AC%BC%ED%9A%8C%ED%94%BC_%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/Phase_3_3.md)
  - [Rpi 5 프로그램 Hold/Resume Hold/Resume 토글 스위치 추가](https://github.com/iispace/AI/blob/main/RL/RL%EA%B8%B0%EB%B0%98_%EC%9E%A5%EC%95%A0%EB%AC%BC%ED%9A%8C%ED%94%BC_%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/Phase_3_4.md)

### [4단계] 강화학습 모델 연구

 - [선행 연구 고찰](https://github.com/iispace/AI/tree/main/RL/%EA%B4%80%EB%A0%A8%EB%85%BC%EB%AC%B8)
 - [강화학습 모델 설계 및 구현](https://github.com/iispace/AI/blob/main/RL/RL%EA%B8%B0%EB%B0%98_%EC%9E%A5%EC%95%A0%EB%AC%BC%ED%9A%8C%ED%94%BC_%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/Phase_4_1.md)


### [5단계: 이동체 강화학습 모델 탑재 및 학습](#)


### [6단계: 장애물 회피 자율주행 테스트](#)

  - Baseline 성능 측정
  - 연구 모델 성능 측정
  - 측정 성능 비교

### [7단계: Representation과 출력 간 상관관계 분석](#)

