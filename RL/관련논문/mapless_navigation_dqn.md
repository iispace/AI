# 제목 

- [Mapless Navigation Based on DQN Cnsidering Moving Obstacles, and Training Time Reduction Algorithm](https://koreascience.kr/article/JAKO202111236685836.pdf)
- 이동 장애물을 고려한 DQN 기반 Mapless Navigation 및 학습 시간 단축 알고리즘
  
# 저자

- 윤범진(Beomjin Yoon), 유승열(Seungryeol Yoo)
- 한국정보통신학회논문지 Vol.25, No.3, pp.377-383, Mar. 2021

# Abstract

- 공장 물류창고, 서비스영역에서 유연한 물류이송을 위한 자율 이동형 모바일 로봇의 사용 증가
- SLAM(Simulaneous Localization and Mapping)을 수행하기 위해 많은 수작업 필요 => 개선된 모바일 로봇 자율 주행 필요성 커짐
- DQN 기반 고정 및 이동 장애물을 피해 최적의 경로로 주행하는 Mapless navigation 알고리즘 및 학습시간 단축 알고리즘 제안
  - 오랜 시간과 많은 수작업이 필요한 SLAM 생성 문제에 대한 대안으로, 강화학습 기반 자율주행 모델 생성
  - DQN은 trail and error를 기반으로 하기 때문에 학습 시간이 굉장히 길다는 문제가 있음. 이 문제의 완화를 위해 학습 시간 단축 알고리즘 제안 => Target size를 처음에는 크게 설정하고 하나의 에피소드가 종료될 때마다 점진적으로 크기를 줄여 나가면서 학습 시키는 방법 제안

 # Keywords:

- Reinforcement neural network, DQN, Mobile robot, Autonomous driving, Obstacle
- 강화학습, 딥러닝, 모바일 로봇, 자율주행, 장애물
  

# 용어 정리

|용어|설명|
|:-|:-|
|SLAM|Simulaneous Localization and Mapping<b>차량이나 로봇의 현재 위치 및 주변환경을 동시에 탐색하는 기술|
|오도메트리(Odometry)|로봇이 바퀴의 회전이나 카메라 등의 센서 데이터를 이용하여 자신의 상대적인 위치와 방향 변화를 추정하는 기술. 주행거리계<b> - 로봇이 이동한 경로(궤적)를 파악하는 핵심 기술|
|Visual Odometry|카메라를 통해 들어오는 비디오 스트림을 이용하여 로봇의 이동 궤적을 구하는 기술<b> - Monocular Visual Odometry<b> - Stereo Visual Odometry|


# 모바일 로봇 주행을 위한 일반적 처리 과정 및 문제점
- 처리 과정:
  - 주행 공간의 장애물 정보를 SLAM을 통해 map(cost map) 형태로 취득하여 위치 정보 동기화
  - LiDAR 및 Odometry 기반으로 목표지점까지의 경로 생성
  - 목표 지점으로 이동
- 문제점:
  - 환경이 바뀔 때마다 시간과 노력이 많이 투입되는 SLAM 기반 map을 다시 생성해야 함.
- 개선방향:
  - map에 의존하지 않고 센서 기반으로 장애물을 회피하는 자율주행 기법이 필요=> mapless navigation 연구 필요

# 실험 환경 구성
- ROS와 Turblebot3 Machine Learning 튜토리얼 패키지 기반 에피소드 시퀸스 및 알고리즘을 수정하여 시뮬레이션 구성
- GAZEBO 시뮬레이션 환경 사용
  - 시뮬레이션 구동 컴퓨터 사양: Intel Xeon E3-1270v5, RAM 16Gb, Geforce GTX1070 89Gb / Ubuntu 및 Keras
  - 에피소드 하나의 종료 기준:
    - 모바일 로봇이 목표 지점에 도착하거나
    - 벽, 장애물, 사람과 충돌하거나
    - 200초를 초과하여도 목표지점에 도착하지 못했을 때를 종료시점으로 함. 
  - 6m x 6m 크기 정사각형 벽 내부에 고정된 원통형 장애물 2개가 존재하는 가상 공간
  - 장애물 크기: 반지름 0.3m, 약 2m 간격을 두고 설치
    
    <img width="538" height="295" alt="image" src="https://github.com/user-attachments/assets/ee007fdf-ba32-41e7-9557-8986b1369fa6" />
    
    <img width="566" height="587" alt="image" src="https://github.com/user-attachments/assets/caaa1bb5-bc3c-4cae-aad0-c2aae8b544ed" />

    <img width="483" height="250" alt="image" src="https://github.com/user-attachments/assets/2061c184-2167-4897-86b0-ac003c319a34" />



# DQN 구성
- FCN과 dropout layer로 구성
- 입력:
  - 라이다 스캔 데이터: 12도 간격의 측정 거리
  - 로봇과 목표 지점 사이의 각도
  - 로봇과 목표 지점 사이의 거리
- dropout rate: 20%
- 입력층 및 은닉층 활성화 함수: ReLU
- 옵티마이저: RMSprop (Stochastic Gradient Descent 방식 중 하나)  

  <img width="388" height="200" alt="image" src="https://github.com/user-attachments/assets/58e2f9b8-7157-4e1e-a02a-899ac67264df" />

- 보상 함수

  - Goal reward: 목표 지점 도달했을 때의 보상
  - Collision reward: 장애물에 부딪혔을 때의 보상(패널티)
  - Human collision reward: 사람과 부딪혔을 때의 보상(패널티)
  - Driving reward: 매 시간 t에서 받는 보상으로, 목표와 로봇의 heading 방향에 따라 Heading reward 및 Distancce reward를 곱하여 계산
    - $\theta_{goal}(t)$ : 시간 t에서 Heading과 목표지점이 이루는 각도
    - $d_{goal}(t)$ : 로봇과 목표지점간의 거리
    - $d_{\in}  $ : 에피소드가 시작하였을 때 모바일 로봇과 목표지점간의 거리


  <img width="475" height="180" alt="image" src="https://github.com/user-attachments/assets/6f8919dd-09c3-41e6-ba23-488e7eb7f394" />
      
  <img width="475" height="150" alt="image" src="https://github.com/user-attachments/assets/7d6b624d-901c-4f4f-b6b5-0e56e066f06d" />
      
# 학습 시간 단축 조건 실험 결과

  <img width="409" height="175" alt="image" src="https://github.com/user-attachments/assets/da7dad44-11aa-4660-9748-ec4d85b23739" />

  <img width="396" height="300" alt="image" src="https://github.com/user-attachments/assets/56c95ef0-b53a-4b31-897a-165e6bfd87b6" />

# DQN 학습 완료 후 테스트 결과
- Mapless Navigation의 학습에 소요된 시간: 약 20시간
- 충돌하지 않고 목표 지점에 도착할 확률
  - Test-1: 로봇 주행 공간에 사람이 서 있을 때 (정지 장애물)
  - Test-2: 로봇 주행 공간에 사람이 걷고 있을 때 (이동 장애물)
  <img width="434" height="129" alt="image" src="https://github.com/user-attachments/assets/d781a8aa-0e7b-459f-8700-22c45dac4811" />

<hr>

### 내 연구와의 차별점:

|위 논문의 내용|나의 연구 방향|
|:-|:-|
|출발지점과 위치가 다른 목표 지점이 사전에 설정된 시나리오|목표 지점에 출발 지점과 같은 시나리오<b>(예) 출발한 시간으로부터 10분간 주변 정찰 후 출발지로 복귀|
|LiDAR 센서와 카메라 사용|RGB 단안 카메라만 사용|
|시뮬레이션 기반 연구|실제 환경 기반 연구|
