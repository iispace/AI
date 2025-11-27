# 3단계: Arduino <-> Raspberry Pi 5 UART 통신

### Raspberry Pi 5 (이하 Rpi 5)와 Arduino Uno 간 시리얼 통신 설정:

  - Rpi 5: UART2 추가 및 활성화 ('/dev/ttyAMA2') 및 GPIO핀 확인 --> GPIO4(TX), GPIO5(RX)핀
  - Arduino Uno: SoftwareSerial()로 D4(RX), D5(TX)핀을 시리얼 통신 핀으로 사용.
  - 자세한 방법은 [Arduino와 Raspberry Pi 5의 UART(Serial) 통신](https://github.com/iispace/Arduino_Learning_Tutorials/tree/main/UART/ArduinoUno_Rpi5) 참조

<hr>

### 코드

##### Rpi 5 파이썬 코드

  ```
  import mycamera
  import cv2
  import threading
  import serial 
  import time 
  
  ser = serial.Serial('/dev/ttyAMA2', 9600, timeout=1)  # UART2 (GPIO4-TX, GPIO5-RX)

  // Rpi 5가 보낸 제어 신호로 Arduino Uno에 연결된 모터 구동 및 LED 점등 테스트
  def control_thread():
      while True:
          ser.write(b'G')
          print("G data sent to uno")
          time.sleep(1)   # 5초에 한 번씩 "HIGH" 신호 전송
          ser.write(b'0')
          print("0 data sent to uno")
          time.sleep(5)

  // 카메라 테스트            
  def main():
      W, H = 640, 480
      # 카메라 객체 생성
      camera = mycamera.MyPiCamera(W, H)
      filepath = "/home/pi/MyProject/video/train"
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


##### Arduino 코드

  ```
  // Rpi 5에서 받은 시리얼 통신 신호로 RC카 제어 테스트 <2025-11-27>
  
  #include <Arduino.h>
  #include <SoftwareSerial.h>
  
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
  
    //Serial.println("....Arduino Ready....");
    for (int i=0;i<5;i++){
      digitalWrite(CtrlLED, HIGH);
      delay(100);
      digitalWrite(CtrlLED, LOW);
      delay(100);
    }
  }
  
  void loop() {
    if(rpiSerial.available()){
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
        //LEFT_1 = HIGH 이고 LEFT_2 = HIGH 이면 두 핀 사이의 전압 차이가 없어 전류가 흐르지 않음. 즉, 왼쪽 모터 정지 
        digitalWrite(LEFT_1, HIGH);    // 10 
        digitalWrite(LEFT_2, HIGH);    // 9
        //RIGHT_1=HIGH, RIGHT_2=HIGH 이면 두 핀 사이의 전압 차이가 없어 전류가 흐르지 않음. 즉, 오른쪽 모터 정지
        digitalWrite(RIGHT_1, HIGH);   // 8
        digitalWrite(RIGHT_2, HIGH);   // 7
        analogWrite(Speed_R, 0);   // 6
        digitalWrite(CtrlLED, LOW);
      }
    }
  
  }

  ```
