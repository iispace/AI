# Rpi 5 <--> Arduino Uno UART 통신 (양방향 통신과 Thread 간 데이터 접근 테스트)

  - 카메라가 켜져 있는 동안 1초에 한번씩 제어 데이터 값을 갱신하고, 아두이노에서 수신한 센서 값을 화면에 출력함.
  - Thread로 동작하는 serial_thread()에서는 제어 데이터를 아두이노에 보내고, 아두이노에서 보내온 센서 값을 받는다.

### Rpi 5 파이썬 코드

```
import mycamera
import cv2
import threading
import serial 
import time 

import random 

ser = serial.Serial('/dev/ttyAMA2', 9600, timeout=0.1)  # UART2 (GPIO4-TX, GPIO5-RX)

gCtrlData = '-1'
gSensorValue = '-1'.encode()
chars = ['G', 'B', 'L', 'R', '0']

def serial_thread():
    global gSensorValue

    while True:
        ser.write(gCtrlData.encode())
        print(f"data sent to uno: {gCtrlData}")
        time.sleep(0.5)    
        while ser.in_waiting > 0:
            gSensorValue = ser.read(1) # 1byte 읽기
        time.sleep(0.5)
            


def main():
    global gCtrlData 

    W, H = 640, 480
    # 카메라 객체 생성
    camera = mycamera.MyPiCamera(W, H)
    filepath = "/home/pi/{프로젝트폴더}/video/train"
    i = 0


    try:
        while (camera.isOpened()):
            # 제어 데이터 값 갱신 
            gCtrlData = random.choice(chars)
            # 아두이노에서 수신한 센서 값 출력
            print("sensor data from Uno: ", int.from_bytes(gSensorValue, 'big'))

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

        cv2.destroyAllWindows()

    except KeyboardInterrupt:
        ser.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    task1 = threading.Thread(target=serial_thread)
    task1.start()
    main()
    ser.close()
    
```

### 아두이노 코드

```
// 시리얼 통신으로 Rpi 5에서 제어 신호 받아 이동체를 제어하고 Rpi 5로 센서값 전달하는 프로그램 

#include <Arduino.h>
#include <SoftwareSerial.h>

SoftwareSerial rpiSerial(4,5); // RX, TX

#define Speed_L 11
#define LEFT_1 10    // left motor forward
#define LEFT_2 9     // left motor reverse
#define RIGHT_1 8    // right motor forward
#define RIGHT_2 7    // right motor reverse
#define Speed_R 6

#define CtrlLED 12   // Rpi 5로부터 제어 신호 받으면 동작하는 LED

char c;
int speed = 128;  // duty cycle: 50% i.e., 0.5
int sensor_value = -1;

void setup() {
  rpiSerial.begin(9600);
  Serial.begin(9600);
  delay(20);

  pinMode(Speed_L, OUTPUT);  // 11
  pinMode(LEFT_1, OUTPUT);   // 10
  pinMode(LEFT_2, OUTPUT);   // 9
  pinMode(RIGHT_1, OUTPUT);  // 8
  pinMode(RIGHT_2, OUTPUT);  // 7
  pinMode(Speed_R, OUTPUT);  // 6

  pinMode(CtrlLED, OUTPUT);

  // 아두이노가 준비 되었음을 알리기 위한 깜박임
  for (int i=0;i<5;i++){
    digitalWrite(CtrlLED, HIGH);
    delay(100);
    digitalWrite(CtrlLED, LOW);
    delay(100);
  }
}

void loop() {
  if(rpiSerial.available() > 0){
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
      analogWrite(Speed_L, 0);
      digitalWrite(LEFT_1, HIGH);    // 10 
      digitalWrite(LEFT_2, HIGH);    // 9
      digitalWrite(RIGHT_1, HIGH);   // 8
      digitalWrite(RIGHT_2, HIGH);   // 7
      analogWrite(Speed_R, 0);   // 6
      digitalWrite(CtrlLED, LOW);
      c = '\0';  // 명령어 처리 후 초기화
    }
  }
  else {
    // Rpi 5로부터 제어 신호를 받지 못하면 모터 정지
    analogWrite(Speed_L, 0);
    digitalWrite(LEFT_1, HIGH);    // 10 
    digitalWrite(LEFT_2, HIGH);    // 9
    digitalWrite(RIGHT_1, HIGH);   // 8
    digitalWrite(RIGHT_2, HIGH);   // 7
    analogWrite(Speed_R, 0);       // 6
    digitalWrite(CtrlLED, LOW);
    Serial.println("No command received from Rpi 5. Stopping motors.");
  }
  // 센서 값 랜덤하게 갱신
  sensor_value = random(0, 10);
  // Rpi 5에 센서 값 전송
  rpiSerial.write(sensor_value);
  Serial.print("Sent to Rpi 5: ");
  Serial.println(sensor_value);
  sensor_value = -1; // 전송 후 초기화
  delay(1000);
}

```


### 테스트



https://github.com/user-attachments/assets/931c0243-4dc0-42db-a2ec-bec8d906d086

