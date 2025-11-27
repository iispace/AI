# Rpi 5 <--> Arduino Uno UART 통신 (양방향 테스트)

### Rpi 5 파이썬 코드
```
import mycamera
import cv2
import threading
import serial 
import time 

ser = serial.Serial('/dev/ttyAMA2', 9600, timeout=1)  # UART2 (GPIO4-TX, GPIO5-RX)

def control_thread():
    while True:
        ser.write(b'G')
        print("G data sent to uno")
        time.sleep(1)   # 5초에 한 번씩 "HIGH" 신호 전송
        ser.write(b'0')
        print("0 data sent to uno")
        while ser.in_waiting > 0:
            #print(ser.readline().strip().decode("utf-8"))  # <== string을 받으면 병목 발생
            data = ser.read(1)  # 1byte 읽기   
            print("sensor data from Uno: ", int.from_bytes(data, 'big'))
        time.sleep(4)

def main():
    W, H = 640, 480
    # 카메라 객체 생성
    camera = mycamera.MyPiCamera(W, H)
    filepath = "/home/pi/ARserverance/video/train"
    i = 0

    try:
        while (camera.isOpened()):
            
            _, image = camera.read()
            image = cv2.flip(image, -1)
            cv2.imshow('Original image', image)

            height, _, _ = image.shape  # (480, 640, 3) => height: 480
            save_image = image[int(height/2):, :, :]
            cv2.imshow('Save image', save_image)

            # 이미지 파일로 저장
            cv2.imwrite("%s_%05d.png" % (filepath, i), save_image)
            i += 1
    
        cv2.destroyAllWindows()

    except KeyboardInterrupt:
        ser.close()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    task1 = threading.Thread(target=control_thread)
    task1.start()
    main()
    ser.close()

```


### Arduino 코드

```
// Rpi 5에서 시리얼 신호 받아 RC카 제어하고 Rpi 5로 센서값 전달하는 프로그램  

#include <Arduino.h>
#include <SoftwareSerial.h>

//SoftwareSerial btSerial(2,3);
SoftwareSerial rpiSerial(4,5); // RX, TX

#define Speed_L 11
#define LEFT_1 10    // left motor forward
#define LEFT_2 9     // left motor reverse
#define RIGHT_1 8    // right motor forward
#define RIGHT_2 7    // right motor reverse
#define Speed_R 6

#define CtrlLED 12   // Rpi 5로부터 시리얼 신호 받으면 동작하는 LED

char c;
int speed = 128;  // duty cycle: 50% i.e., 0.5
int sensor_value = 9;

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

  //Serial.println("....bluetooth test....");
  for (int i=0;i<5;i++){
    digitalWrite(CtrlLED, HIGH);
    delay(100);
    digitalWrite(CtrlLED, LOW);
    delay(100);
  }
}

void loop() {
  if(rpiSerial.available() > 0){
    delay(100);
    c = rpiSerial.read();
    Serial.println(c);

    if (c == 'B'){  // (후진) 
      analogWrite(Speed_L, speed);   // 11
      //LEFT_1 = HIGH 이고 LEFT_2 = LOW이면 두 핀 사이의 전압이 다르므로 전류가 흐르지만 방향이 반대. 즉, 왼쪽 모터가 역방향으로 회전함 
      digitalWrite(LEFT_1, HIGH);    // 10 
      digitalWrite(LEFT_2, LOW);    // 9
      //RIGHT_1 = HIGH 이고 RIGHT_2 = LOW이면 두 핀 사이의 전압이 다르므로 전류가 흐르지만 방향이 반대. 즉, 오른쪽 모터가 역방향으로 회전함 
      digitalWrite(RIGHT_1, HIGH);   // 8
      digitalWrite(RIGHT_2, LOW);   // 7
      analogWrite(Speed_R, speed);   // 6
    }
    else if (c == 'G'){  // (전진) 
      analogWrite(Speed_L, speed);   // 11
      digitalWrite(LEFT_1, LOW);    // 10 
      digitalWrite(LEFT_2, HIGH);    // 9
      digitalWrite(RIGHT_1, LOW);   // 8
      digitalWrite(RIGHT_2, HIGH);   // 7
      analogWrite(Speed_R, speed);   // 6
      digitalWrite(CtrlLED, HIGH);
    }
    else if (c == 'L'){  // (좌회전) 
      analogWrite(Speed_L, speed);   // 11
      digitalWrite(LEFT_1, LOW);    // 10 
      digitalWrite(LEFT_2, HIGH);    // 9
      digitalWrite(RIGHT_1, HIGH);   // 8
      digitalWrite(RIGHT_2, LOW);   // 7
      analogWrite(Speed_R, speed);   // 6
    }
    else if (c == 'R'){ // (우회전) 
      analogWrite(Speed_L, speed);   // 11
      digitalWrite(LEFT_1, HIGH);    // 10 
      digitalWrite(LEFT_2, LOW);    // 9
      digitalWrite(RIGHT_1, LOW);   // 8
      digitalWrite(RIGHT_2, HIGH);   // 7
      analogWrite(Speed_R, speed);   // 6
    }
    else if (c == '0'){
      analogWrite(Speed_L, 0);
      digitalWrite(LEFT_1, HIGH);    // 10 
      digitalWrite(LEFT_2, HIGH);    // 9
      digitalWrite(RIGHT_1, HIGH);   // 8
      digitalWrite(RIGHT_2, HIGH);   // 7
      analogWrite(Speed_R, 0);   // 6
      digitalWrite(CtrlLED, LOW);
    }
  }
  //rpiSerial.print("from Uno: ");    // string을 보내면 병목 현상이 생겨 간헐적 통신 장애 발생
  //rpiSerial.println(sensor_value);  // string을 보내면 병목 현상이 생겨 간헐적 통신 장애 발생
  rpiSerial.write(sensor_value);   
  delay(100);
}

```

### 테스트 

