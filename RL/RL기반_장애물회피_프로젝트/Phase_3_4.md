# Raspberry Pi 5의 파이썬 프로그램 동작 Hold/Resume 토글 스위치 추가

## 결선도


<img width="540" height="300" alt="image" src="https://github.com/user-attachments/assets/7ceeebb8-894f-4208-8fea-33bade3ca871" />
<img width="684" height="400" alt="image" src="https://github.com/user-attachments/assets/183f94e6-dd1f-4d33-8b72-74761104f0e5" />



## Rpi 5 Code

```
from typing import List
from gpiozero import Button, DigitalOutputDevice, PWMOutputDevice, TonalBuzzer, LED 

import carserve_camera
import cv2
import threading
import serial 
import time, sys, os

import random 

# 실행 상태 플래그
thread_running = True
stop_event = threading.Event() # 종료 이벤트

LED_Blue = LED(17)  # Rpi 5 Ready/Collision/Hold Indicator
Hold_Btn = Button(23, pull_up=True)

def uart_task():
    global thread_running
    global gSensorValue
    global gCtrlData
    global gPrev_action
    
    try:
        ser = serial.Serial('/dev/ttyAMA2', 9600, timeout=0.1)  # UART2 (GPIO4-TX, GPIO5-RX)

        # 버퍼 초기화
        ser.reset_input_buffer()
        time.sleep(0.1)

        while not stop_event.is_set():
            if thread_running:
                if gCtrlData != '-1':
                    ser.write(gCtrlData.encode())
                    gPrev_action = gCtrlData  # 이전 action 값을 보존하기 위해 변수에 저장
                    time.sleep(0.1)  
                    print(f"data sent to uno: {gCtrlData}")
                    gCtrlData = '-1'
                while ser.in_waiting > 0:
                    gCtrlData = '-1'  # 충돌 감지 신호 수신 즉시 모터 제어 신호 초기화하여 전송되지 않도록 함.
                    gSensorValue = ser.read(1).strip().decode('utf-8', errors='ignore') # 1byte 읽어서 문자로 변환
                    led_blinking(0.05, 10)   # 50ms 간격으로 10번 깜박임


                #time.sleep(0.1)
            else:
                time.sleep(0.01)
    except Exception as e:
        print(f"Exception arose in uart_task: {e}")
    finally:
        ser.close()

def toggle_running():
    global thread_running
    thread_running = not thread_running
    if thread_running:
        LED_Blue.off()
        led_blinking(0.1, 2)
        print("... Program resummed ...")
    else:
        LED_Blue.on()
        print("--- Program hold ...")
        #led_blinking(0.1, 2)


def led_blinking(ts:float, cnt=10):
    for i in range(cnt):
        LED_Blue.on()
        time.sleep(ts)
        LED_Blue.off()
        time.sleep(ts)


def main():

    global thread_running        
    global gCtrlData 
    global gSensorValue
    global gPrev_action

    gCtrlData = '-1'   
    #gSensorValue = '-1'.encode()
    gSensorValue = None
    chars = ['G', 'B', 'L', 'R', '0']
    gPrev_action = '0'  # 직전 제어 값 저장 변수

    Hold_Btn.when_pressed = toggle_running 

    task1  = threading.Thread(target=uart_task, daemon=True)
    task1.start()

    # Camera 객체 생성       
    W, H = 640, 480
    camera = carserve_camera.Carserve_PiCamera(W, H)
    filepath = "/home/pi/{프로젝트_폴더}/video/train"
    i = 0

    # Rpi 5 ready indication
    led_blinking(0.1, 10)

    try:
        while not stop_event.is_set():
            while (camera.isOpened()) and thread_running:
                
                # 이미지 촬영 및 화면 출력
                _, image = camera.read()
                image = cv2.flip(image, -1)
                cv2.imshow('Original image', image)

                height, _, _ = image.shape  # (480, 640, 3) => height: 480
                save_image = image[int(height/2):, :, :]
                cv2.imshow('Save image', save_image)

                # 이미지 파일로 저장
                cv2.imwrite("%s_%05d.png" % (filepath, i), save_image)
                i += 1
                time.sleep(1)  # 1초마다 반복

                # 이미지 전처리 부분
                # ..... <코드 구현하기> ....

                # 제어 데이터 값 갱신 (강화학습 모델 처리 및 출력 데이터<action> 생성 부분)
                gCtrlData = random.choice(chars) 
                                      

                # 아두이노에서 수신한 센서 값 출력(충돌 신호 수신)
                #print("sensor data from Uno: ", int.from_bytes(gSensorValue, 'big', signed=True)) 
                if gSensorValue is not None:
                    print("sensor data from Uno: ",gSensorValue) 
                    # 충돌 발생 시그널 받았을 때 처리해야 할 일 여기에 구현
                    # .... <강화학습 모델에서 사용하는 상태 변수와 보상값 갱신하는 코드 구현하기> .... 
                    time.sleep(2.0)  # 충돌 감지 신호 수신 후 3초 동안 대기 (아두이노 쪽에서도 같은 시간 동안 대기함)  <== 이 부분은 강화학습 적용할 때 수정하기 !!!
                    gSensorValue = None
                


            cv2.destroyAllWindows()

    except KeyboardInterrupt:
        print("Keyboard Interrupt arose")
        cv2.destroyAllWindows()
        stop_event.set()
        task1.join()      # 서브 스레드가 종료될 때까지 기다림
        print("All threads stopped.")



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Program ended")

```

<br>

## Arduino Uno 코드

```
// 시리얼 통신으로 Rpi 5에서 제어 신호 받아 이동체를 제어하고 Rpi 5로 충돌 감지 이벤트 전달 프로그램  

#include <Arduino.h>
#include <SoftwareSerial.h>
#include <Wire.h>

// --------------- Rpi 5 Serial --------------- //
SoftwareSerial rpiSerial(4,5); // RX, TX

// ------------ Motor Control Pins ------------ //
#define Speed_L 11
#define LEFT_1 10    // left motor forward
#define LEFT_2 9     // left motor reverse
#define RIGHT_1 8    // right motor forward
#define RIGHT_2 7    // right motor reverse
#define Speed_R 6

#define CtrlLED 12   // Rpi 5로부터 시리얼 신호 받으면 동작하는 LED

// -------------------- MPU-6050-- ------------------- //
const int interruptPin = 2; // MPU-6050 인터럽트 핀 연결 (Arduino D2)
const int MPU = 0x68;   // I2C address of the MPU-6050
volatile bool collisionDetected = false; // 인터럽트 발생 플래그



// --------------------- Variables -------------------- //
char c = '\0';    // default control command to stop motor
int speed = 128;   // duty cycle: 25% i.e., 0.25
//int sensor_value = -2;  // This value will be 1 and sent to Rpi 5 when Collision is detected

void led_blinking();
void motorStop();
void wakeUpMPU6050() ;
void enableCollisionDetection(uint8_t, uint8_t);


// ----------- ISR (Interrupt Service Routine) ----------- //
void collisionISR() {
  collisionDetected = true;
  
} 

// -------------------- Setup & Loop ------------------- //
void setup() {
  rpiSerial.begin(9600);
  Serial.begin(9600);
  delay(20);

  // Motor control pins
  pinMode(Speed_L, OUTPUT);  // 11
  pinMode(LEFT_1, OUTPUT);   // 10
  pinMode(LEFT_2, OUTPUT);   // 9
  pinMode(RIGHT_1, OUTPUT);  // 8
  pinMode(RIGHT_2, OUTPUT);  // 7
  pinMode(Speed_R, OUTPUT);  // 6

  pinMode(CtrlLED, OUTPUT);


  // ----------------------- MPU-6050 Init ---------------------- //
  Wire.begin();
  wakeUpMPU6050();
  //enableCollisionDetection(2, 20); // threshold = 2 LSB = (2 / 16384 ≈ 0.12 mg), duration=20 samples(≈ 20 * 0.125 ms = 2.5 ms)
  enableCollisionDetection(1, 20); // threshold = 1 LSB = (1 / 16384 ≈ 0.06 mg), duration=20 samples(≈ 20 * 0.125 ms = 2.5 ms)

   // 아두이노가 준비 되었음을 알리기 위한 깜박임(Arduino Ready Indicator)
  for (int i=0;i<10;i++){
    digitalWrite(CtrlLED, HIGH);
    delay(100);
    digitalWrite(CtrlLED, LOW);
    delay(100);
  }
}


void loop() {
  // ---------------- 충돌 인터럽트 처리 ---------------- //
  if(collisionDetected){
    //sensor_value = 1; // 충돌 감지 시 센서 값 1로 설정
    for (int i=0; i<5; i++) { 
      rpiSerial.write('Y');   // 충돌 감지 신호를 Rpi 5로 5번 전송 (통신 실패할 경우를 대비하여...) 
      Serial.println("===== Collision detected! Sent to Rpi 5: Y ===== ");
      delay(10);
    }
    motorStop();
    c='\0';
    //sensor_value = -2; // 기본 센서 값으로 복귀
    led_blinking();
    rpiSerial.flush();  // 차량이 멈춘 후 Rpi 5로부터 오는 잔여 데이터 제거
    delay(3000); // 충돌 후 3초간 대기 후 다시 루프 진행
    collisionDetected = false; // 플래그 리셋
  } 

  // --------------- Rpi 5의 제어 신호 처리 ---------------- //
  if(rpiSerial.available() > 0){
    delay(10);
    c = rpiSerial.read();
    Serial.print("Received command from Rpi 5: ");
    Serial.println(c);
    

    if (c == 'B'){  // (후진) 
      analogWrite(Speed_L, speed);   // 11
      digitalWrite(LEFT_1, HIGH);    // 10 
      digitalWrite(LEFT_2, LOW);    // 9
      digitalWrite(RIGHT_1, HIGH);   // 8
      digitalWrite(RIGHT_2, LOW);   // 7
      analogWrite(Speed_R, speed);   // 6
      digitalWrite(CtrlLED, HIGH);
      c = '\0';  // 명령어 처리 후 초기화
    }
    else if (c == 'G'){  // (전진) 
      analogWrite(Speed_L, speed);   // 11
      digitalWrite(LEFT_1, LOW);    // 10 
      digitalWrite(LEFT_2, HIGH);    // 9
      digitalWrite(RIGHT_1, LOW);   // 8
      digitalWrite(RIGHT_2, HIGH);   // 7
      analogWrite(Speed_R, speed);   // 6
      digitalWrite(CtrlLED, HIGH);
      c = '\0';  // 명령어 처리 후 초기화
    }
    else if (c == 'L'){  // (좌회전) 
      analogWrite(Speed_L, speed);   // 11
      digitalWrite(LEFT_1, LOW);    // 10 
      digitalWrite(LEFT_2, HIGH);    // 9
      digitalWrite(RIGHT_1, HIGH);   // 8
      digitalWrite(RIGHT_2, LOW);   // 7
      analogWrite(Speed_R, speed);   // 6
      digitalWrite(CtrlLED, HIGH);
      c = '\0';  // 명령어 처리 후 초기화
    }
    else if (c == 'R'){ // (우회전) 
      analogWrite(Speed_L, speed);   // 11
      digitalWrite(LEFT_1, HIGH);    // 10 
      digitalWrite(LEFT_2, LOW);    // 9
      digitalWrite(RIGHT_1, LOW);   // 8
      digitalWrite(RIGHT_2, HIGH);   // 7
      analogWrite(Speed_R, speed);   // 6
      digitalWrite(CtrlLED, HIGH);
      c = '\0';  // 명령어 처리 후 초기화
    }
    else if (c == '0'){
      motorStop();
      c = '\0';  // 명령어 처리 후 초기화
    }
  }
  else {
    // Rpi 5로부터 제어 신호를 받지 못하면 모터 정지
    motorStop();
    c = '\0';  // 명령어 처리 후 초기화
    Serial.println("No command received from Rpi 5. Stopping motors.");
  }
  // 센서 값 랜덤하게 갱신 (통신 테스트용)
  //sensor_value = random(-10, 20);
  //rpiSerial.write(sensor_value);
  //Serial.print("Sent to Rpi 5: ");
  //Serial.println(sensor_value);
  //sensor_value = -2;
  delay(1000);
}

// 충돌 감지를 알리는 LED 깜박임 함수
void led_blinking(){
  for (int i=0;i<10;i++){
    digitalWrite(CtrlLED, HIGH);
    delay(50);
    digitalWrite(CtrlLED, LOW);
    delay(50);
  }
}

void motorStop(){
  analogWrite(Speed_L, 0);
  digitalWrite(LEFT_1, HIGH);    // 10 
  digitalWrite(LEFT_2, HIGH);    // 9
  digitalWrite(RIGHT_1, HIGH);   // 8
  digitalWrite(RIGHT_2, HIGH);   // 7
  analogWrite(Speed_R, 0);   // 6
  digitalWrite(CtrlLED, LOW);
}

void wakeUpMPU6050() {
  Wire.beginTransmission(MPU);
  Wire.write(0x6B);  // PWR_MGMT_1 register
  Wire.write(0);     // set to zero (wakes up the MPU-6050)
  Wire.endTransmission(true);
}

void enableCollisionDetection(uint8_t threshold, uint8_t duration) {
  // Motion Detection Threshold 설정 (Register 0x1F)
  Wire.beginTransmission(MPU);
  Wire.write(0x1F);  // MOT_THR register
  Wire.write(threshold);    // threshold 값 (필요시 조정, 단위: LSB): 1 LSB = (1 / 16384) * 1000 ≈ 0.061 g, so threshold=4이면 4 * 0.061 g = 0.24 g
  Wire.endTransmission(true);

  // Motion Detection Duration 설정 (Register 0x20)
  Wire.beginTransmission(MPU);
  Wire.write(0x20);  // MOT_DUR register
  Wire.write(duration);    // duration 값 (필요시 조정, 단위: samples): 1 sample = 1/8 kHz = 0.125 ms, so duration=20이면 20 * 0.125 ms = 2.5 ms
  Wire.endTransmission(true);

  Wire.beginTransmission(MPU);
  Wire.write(0x38);  // INT_ENABLE register
  Wire.write(0x40);  // MOT_EN 비트 활성화
  Wire.endTransmission(true);

  pinMode(interruptPin, INPUT);
  attachInterrupt(digitalPinToInterrupt(interruptPin), collisionISR, RISING);
  delay(20);

  Serial.println("\nACCELEROMETER(LSB)\tTEMP\tGYROSCOPE(LSB)");
  Serial.println("ax\tay\taz\tT\tgx\tgy\tgz");
  delay(20);
}

```

## 테스트 결과

  <img width="800" height="400" alt="image" src="https://github.com/user-attachments/assets/80cb2f1c-fa63-4862-ba4c-a5fd807dbdd4" />

