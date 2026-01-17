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
     
     <img width="912" height="432" alt="image" src="https://github.com/user-attachments/assets/54766f14-06e7-413b-b0cb-e2202418d5c8" />


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


## Baseline Code (DQN)

```
import cv2
import serial
import time 
import random
import numpy as np
from collections import deque 

import torch 
import torch.nn as nn 
import torch.optim as optim 
import torch.nn.functional as F

from picamera2 import Picamera2 # required for camera module v3, Raspberry Pi에서 기본으로 제공되는 라이브러리
import numpy as np 

class PiCamera_DQN():
    def __init__(self, width, height):
        self.cap = Picamera2()

        self.width = width
        self.height = height 
        self.is_open = True 

        try:
            self.config = self.cap.create_video_configuration(main={"format": "RGB888", "size": (width, height)})
            self.cap.align_configuration(self.config)
            self.cap.configure(self.config)

            self.cap.start()
        except:
            self.is_open=False
        return 
    
    def read(self, dst=None):
        # allocate blank image to avoid returning a "None"
        if dst is None:
            dst = np.empty((self.height, self.width, 3), dtype=np.uint8)
        
        if self.is_open:
            dst = self.cap.capture_array()  # 카메라로부터 이미지를 캡쳐하여 Numpy 배열 형태로 변환하는 함수

        # dst is either blank or the previously captured image at this point 
        return self.is_open, dst 
    
    def isOpened(self):
        return self.is_open
    
    def release(self):
        if self.is_open:
            self.cap.close()
        self.is_open = False
        return
    

class DQN(nn.Module):
    def __init__(self, input_dim=1, action_dim=4):  # grayscale image를 처리하므로 input_dim=1
        super(DQN, self).__init__()

        self.conv1 = nn.Conv2d(input_dim, 32, kernel_size=8, stride=4)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=4, stride=2)
        self.conv3 = nn.Conv2d(64, 64, kernel_size=3, stride=1)

        self.fc1 = nn.Linear(64*7*7, 512)
        self.fc2 = nn.Linear(512, action_dim)

    def forward(self,x):
        print(f"x.shape before conv layer: {x.shape}")
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        print(f"x.shape after conv layer: {x.shape}")

        x = x.view(x.size(0), -1)  # fc layer에 입력으로 넣기 위해서 1차원 구조로 reshape
        print(f"x.shape for fc layer input: {x.shape}")

        x = F.relu(self.fc1(x))
        out = self.fc2(x)

        return out
        

class ReplayBuffer:
    def __init__(self, capacity=50000):
        self.buffer = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done ))

    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        state, action, reward, next_state, done = zip(*batch) 
        return state, action, reward, next_state, done 

    def __len__(self):
        return len(self.buffer)


class DQNAgent:
    def __init__(self, learning_rate=1e-4):
        self.learning_rate = learning_rate
        self.action_dim = 4 # action_dim = {Go staight, Turn Left, Turn Right, Go backward}
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.policy_net = DQN(input_dim=1, action_dim=4).to(self.device)
        self.target_net = DQN(input_dim=1, action_dim=4).to(self.device)
        self.target_net.load_state_dict(self.policy_net.state_dict())

        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=self.learning_rate)
        self.memory = ReplayBuffer()

        self.gamma = 0.99
        self.epsilon = 1.0
        self.epsilon_min = 0.05
        self.epsilon_decay = 0.995

    def select_action(self, state):
        # state: grayscale image
        if random.random() < self.epsilon:
            return random.randint(0, 3) # {0,1,2,3} 중 임의의 값 하나 생성
        
        with torch.no_grad():
            q = self.policy_net(torch.FloatTensor(state).to(self.device))
            return q.argmax().item()

    def train(self, batch_size=32):
        if len(self.memory) < batch_size:
            return 
        
        states, actions, rewards, next_states, dones = self.memory.sample(batch_size)        

        states = torch.FloatTensor(states).to(self.device)
        next_states = torch.FloatTensor(next_states).to(self.device)
        actions = torch.LongTensor(actions).to(self.device)
        rewards = torch.FloatTensor(rewards).to(self.device)
        dones = torch.FloatTensor(dones).to(self.device)

        q_values = self.policy_net(states).gather(1, actions.unsqueeze(1)).squeeze()
        next_q = self.target_net(next_states).max(1)[0]
        target = rewards + self.gamma * next_q * (1 - dones)

        loss = F.mse_loss(q_values, target.detach())
        self.optimizer.zero_grad() 
        loss.backward()
        self.optimizer.step()

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


def camera_get_state():
    _, frame = camera.read()
    frame = cv2.flip(frame, -1)  # flipCode = -1 => 이미지를 상하좌우로 반전
    #print(f"frame.shape:{frame.shape}")
    height, _, _ = frame.shape  # (480, 640, 3) => height: 480
    #cv2.imshow("DQN_camera", frame)
    #if cv2.waitKey(1) == ord('q'):
    #    break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # shape changed to (H, W) from (H, W, C)
    aoi_image = gray[int(height/2):,:]  # aoi: area of interest
    normalized = aoi_image / 255.0

    # 이미지 파일로 저장
    cv2.imwrite("%s_%05d.png" % (filepath, i), aoi_image)
    #cv2.imwrite("%s_%05d_full.png" % (filepath, i), gray)

if __name__ == "__main__":
    W = 640
    H = 480
    camera = PiCamera_DQN(W, H)
    filepath = "/home/pi/Carserverance/video_dqn/dqn"
    i = 0

    agent = DQNAgent()

    # dqn 코드 테스트할 때 아두이노와의 통신에서 받은 센서 값을 대신하기 위해 아래와 같이 임시로 충돌에 대한 모의 값을 저장하여 사용함.
    arduino_collision_data = []
    for k in range(100):
        value = random.randint(0,1)  # 0: 충돌 아님, 1: 충돌
        arduino_collision_data.append(value)
    
    # 이동체 출발 후 5분 동안 정찰 하는 임무를 하나의 에피소드로 설정하기 위해 출발 시간 저장
    start_time = time.time() 
    MAX_TIME = 300 # 5분
    

    while camera.isOpened():
        ######################################################################
        # ##########   DQN call 해서 처리 결과를 얻는 코드가 들어갈 부분   ##########
        ######################################################################
        state = camera_get_state()

        while time.time() - start_time < MAX_TIME:
            action = agent.select_action(state)
            print(f"action value to be sent to Arduino: {action}")
            time.sleep(0.2)
            collision = bool(arduino_collision_data[i])
            print(f"collision: {collision}")
            reward = -100 if collision else 0.1
            done = collision 
            i += 1
            next_state = camera_get_state()
            agent.memory.push(state, action, reward, next_state, done)

            agent.train()

            state = next_state

            if done: 
                break

            

    cv2.destroyAllWindows()


```
