# 4단계: 2. Mapless Navigation을 위한 강화학습 모델/알고리즘 설계 및 구현

## 실험 환경 조건 및 설계
- 가장 단순한 DQN 구조의 강화학습 모델 실험에서 시작하여 점진적으로 좀 더 다양하고 복잡한 강화학습 모델 구조를 실험할 예정
- 본 연구는 시뮬레이션 환경이 아니라, 실세계의 환경을 기반으로 한 실험 중심의 연구임을 고려해야 한다.
- 실제 주행 중 실시간으로 DQN을 학습시킬 때는 이동체 또는 장애물에 물리적 손상이 발생할 수 있는 위험이 있으므로, 이러한 위험을 최소화하기 위해 다음과 같이 몇가지 조건을 설정하여 실험한다.

  1. 초기에는 조속 + e-greedy 제한
  2. 약한 충격에도 즉시 정지할 수 있도록 순간 가속도 임계값을 낮게 설정
  3. 실험 단계에서 학습률을 매우 작게 설정하여 급격한 움직임 변화 방지
  4. "초기 학습 실험 --> 로그 수집 및 분석을 통한 DQN 수정  --> 재학습 실험" 과정을 반복하여 학습 최적화  

## 저사양 마이크로 프로세서 적응을 위한 설정

- 입력 데이터(이미지) 전처리 부분:
  1. 카메라로 촬영한 이미지 전체에서 관심 부분(area of interest, aoi)만 잘라내서 처리
  2. 3채널 RGB 이미지를 2채널의 Gray 이미지로 변환하여 처리

- 모델 구조 설계 부분:
  1. ...

## Overall Software Diagram

**1. Micro Computer(Rpi 5)**

  <img width="1245" height="603" alt="image" src="https://github.com/user-attachments/assets/7e9789fd-14ed-482e-804c-44abe86cde0e" />

<br>
<br>
<br>

**2. Micro Controller(Arduino Uno)**

  <img width="1208" height="498" alt="image" src="https://github.com/user-attachments/assets/d9394b8c-1f54-4d61-99bd-1413350a6701" />

