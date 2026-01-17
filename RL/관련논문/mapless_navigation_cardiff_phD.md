# 제목 

- [Deep reinforcement learning-based indoor mapless robot navigation](https://orca.cardiff.ac.uk/id/eprint/177917/1/Amended%20thesis.pdf)

# 저자

- Yan Gao (Cardiff University 박사학위논문, Sept.2024)

# Abstract

- 지도 없이 주변 센서 정보만으로 모바일 로봇이 장애물을 피하며 목적지까지 이동하는 **mapless navigation 문제를 Deep RL로 해결하는 연구**
- **계층적 강화학습 구조(HRL-Hierarchical Reinforcement Learning)를 도입해 장애물 회피 및 가치 기반 행동 선택을 향상**시킴으로써, 기존의 end-to-end DQN/DRL 기법보다 난이도 높은 환경에서도 견고하게 동작하도록 설계
  - Two different subgoal:
    - Predictive Neighbouring Space Scoring(PNSS): 예측 기반 인접 공간 평가(점수화)
    - Predictive Exploration Worthiness(PEW) : 예측 기반 탐사 타당성(탐사 가치)
      
- High-Level representation <= PNSS + PEW
- 이 논문은 로봇이 현재 위치에서 더 멀리 떨어진 장소까지 탐색할 수 있도록 하는 새로운 하위 목표(subgoal) 공간 배치를 제안함.
- HRL 기반의 지도 없는 내비게이션을 위해 새로운 보상함수와 신경망 구조를 개발함
  - 외재적 보상(Extrinsic reward): 로봇이 목표 위치로 이동하도록 유도하는 역할
  - 내재적 보상(Intrinsic reward): 새로움(novelty), 에피소드 기억(episode memory), 기억의 소멸(memory decaying)을 기반으로 계산되어, 에이전트가 자발적인 탐색을 수행할 수 있게 하는 역할. 즉, **로봇이 단순히 목표만 향하는 것이 아니라, 스스로 새로운 환경과 경로를 탐색**하도록 동기를 부여하는 역할
    - novelty(새로움): 새로운 상태나 환경을 경험할 때 보상
    - episode memory(에피소드 기억): 과거 경험을 기억하여 중복된 탐색을 줄임
    - memory decaying(기억 소멸): 시간이 지나면서 기억이 약해져 다시 탐색할 수 있도록 유도
- 제안된 신경망(NN) 구조는 에이전트의 기억력과 추론 능력을 향상시키기 위해 LSTM 네트워크를 포함하고 있음. ==> **에이전트가 과거 경험을 더 잘 활용하고, 복잡한 상황에서 더 논리적인 판단을 내릴 수 있도록 하기 위함**

- 로봇 위치 추정(robot localisation)을 위해 RGB-D 카메라 기반 [ORB-SLAM2](https://github.com/raulmur/ORB_SLAM2) 활용함
- 정책 학습을 용이하게 하기 위해, 지도 점(map points)의 공간적 분포를 기반으로 한 간결한 상태 표현(compact state representation)이 제안되었으며, 이를 통해 로봇은 신뢰할 수 있는 특징들이 존재하는 영역에 대한 인식을 향상시킴.

# 그림 목록

  - (a) Metric map, (b) Topological map -- 15
  - Overall visual SLAM framework   ----- 63
  - The overall framework with PNSS  ---- 73
  - An example of the predicted PNSS values -- 71
  - The PNSS model extracts features from the RGB image firstly --- 76
  - The overall framework with PEW ---- 84
  - An example of what the PEW model predicts --- 84
  - Network structure of the PEW model --- 88
  - Example environments for testing ---- 91
  - Three difference layouts we mainly focus on ... ----- 94
  - Examples of the robot being trapped by obstacles ---- 99
  - The overall framework. --- 129
  - Subgoal space ----- 131
  - Network structure of HL policy ---- 135
  - Experiment environments for testing ---- 139
  - An example in the test of scenario 1. ---- 149
  - The overall framework of ORB-SLAM2 ---- 167
  - Env 1: Aloha and two examples of the robot visual features --- 174
  - Env 2: Arona and two examples of the robot visual features ---- 181
  
 
# Mobile Robot 특징
  - 환경 인지(Environment perception)
  - 동적 의사 결정(Dynamic decision making)
  - 행동 제어(Behavioural control)

# Mobile Robot 활용 예시
  - 군용: 지뢰 제거(demining)나 정찰(reconnaissance)등 위험 임무 수행 등
  - 민간용: 무인 지상 차량 기반 창고 자동화, 무인 항공기 기반 전력선 검사 등
  - 기타: 도시 수색 및 구조, 재난 구호, 가정용 서비스 로봇(domestic service robots) 등

# 전통적인 모바일 로봇 내비게이션 시스템 구성 모듈:
  - A mapping and localiation module: 환경 지도 생성 후 지도 상에서의 현재 위치와 목표 지점 추정
  - A global path planner: 가능한 경로 생성
  - A local planner: Global planner가 제안한 일련의 경유지를 따라 이동
  ==> 결론적으로, 전통적 모바일 로봇 내비게이션 방식은 정확한 지도 생성에 크게 의존하는 방식 => 지도 기반 방식(map-based method)

# 전통적 모바일 로봇 내비게이션 방식인 map-based method의 문제점:
  - 지도 신뢰성 문제:
    - 지도 제작은 시간 및 노력 집약적 작업을 요구함
    - 지도 수정과 유지보수에 대한 장기 비용 높음
    - 지도 제작에 사용되는 센서의 고정밀도 필요

# Mapless navigation: 
  - 지도 없이 이동 로봇이 환경을 완전히 알지 못하고 부분적인 관측 정보만을 가지고도 충돌 없는 경로를 찾아내는 것



# 용어 정리

|용어|설명|
|:-|:-|
|SLAM|Simultaneous Localization and Mapping|
