# 3단계: 1. Arduino <-> Raspberry Pi 5 UART 통신 및 카메라 테스트

### Raspberry Pi 5 (이하 Rpi 5)와 Arduino Uno 간 시리얼 통신 설정:

  - Rpi 5: UART2 추가 및 활성화 ('/dev/ttyAMA2') 및 GPIO핀 확인 --> GPIO4(TX), GPIO5(RX)핀
  - Arduino Uno: SoftwareSerial()로 D4(RX), D5(TX)핀을 시리얼 통신 핀으로 사용.
  - 자세한 방법은 [Arduino와 Raspberry Pi 5의 UART(Serial) 통신](https://github.com/iispace/Arduino_Learning_Tutorials/tree/main/UART/ArduinoUno_Rpi5) 참조

<hr>

### 카메라 연결

  - Raspberry Pi 5 CAM/DISP 1 connector에 카메라 케이블 연결
    
    <img width="174" height="127" alt="image" src="https://github.com/user-attachments/assets/756bde61-8948-4c7e-97be-a962247ca1ca" />
    <img width="145" height="127" alt="image" src="https://github.com/user-attachments/assets/ad4396f7-10ca-45ae-8d1c-1cb7ee8060b6" />

### Rpi 5 Camera Test

 - Camera streaming test(참고1):
 
   <img width="560" height="100" alt="image" src="https://github.com/user-attachments/assets/4977b8da-d260-4015-b11f-73df9e9a64c2" />
 
 - Camera still image test(참고1):

   <img width="375" height="300" alt="image" src="https://github.com/user-attachments/assets/106e5666-4b29-4749-b03d-436df09fa822" />

  - Thonny에서 Rpi 5 기본 Python 환경으로 카메라 테스트(참고2)
    - Thonny는 Rpi OS의 GUI 세션 안에서 실행되므로 PyQt5가 설치되어 있는 파이썬 환경을 인터프리터로 선택하고 아래 화면의 코드를 실행하면 미리보기가 잘 출력된다.

      <img width="420" height="300" alt="image" src="https://github.com/user-attachments/assets/3328d5ba-ef49-41e2-81ad-33e531b7875f" />


    - 그러나, PyQt5가 설치된 (가상)환경이라도 VSCode에서 아래 화면에 보이는 코드를 동일하게 실행하면 미리보기 화면이 Display 장치에 출력되지 않는데, 이는 VS Code가 X11/Wayland GUI 환경을 제대로 물고 실행되지 않기 때문일 수 있다고 한다. 
      
  - VS Code에서 동일한 코드 실행 시에 미리보기 화면이 출력되게 하려면, 인터프리터를 Rpi 5 default python 환경으로 바꾸어서 실행해야 한다.
    
      <img width="353" height="150" alt="image" src="https://github.com/user-attachments/assets/62d58009-1603-41b0-a73b-0dcba403dd44" />

      <img width="660" height="400" alt="image" src="https://github.com/user-attachments/assets/51a6cb11-f552-42b3-b183-6541713d7094" />

      
  - 참고1: [Raspberry Pi Camera software](https://www.raspberrypi.com/documentation/computers/camera_software.html)
  - 참고2: [Picamera2 Library: QtGL preview](https://pip-assets.raspberrypi.com/categories/652-raspberry-pi-camera-module-2/documents/RP-008156-DS-2-picamera2-manual.pdf?disposition=inline)




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

<hr>

### 테스트 동영상

  - Rpi 5에서 파이썬 프로그램이 시작되면 카메라가 동작하여 촬영된 사진을 화면에 보여주고 지정된 디렉터리에 저장한다.
  - 그리고, Rpi 5에서 전진 신호와 정지 신호를 번갈아 보내면 Arduino에 연결된 모터 드라이버가 구동되며 LED가 켜지고 꺼진다.

  https://github.com/user-attachments/assets/adfd2326-0cde-4d17-9a73-549db6160625

<hr>

### 양방향 통신

  - Rpi 5는 Arduino에게 제어 신호를 보내고, Arduino는 Rpi 5에게 센서값을 보내는 양방향 통신 테스트 프로그램과 실험 동영상
    
    [Rpi 5 <==> Arduino Uno 양방향 Serial 통신 테스트](https://github.com/iispace/AI/blob/main/RL/RL%EA%B8%B0%EB%B0%98_%EC%9E%A5%EC%95%A0%EB%AC%BC%ED%9A%8C%ED%94%BC_%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/Phase_3_1_1.md)

<hr>

### 양방향 통신 및 Thread 간 데이터 접근

  - Rpi 5는 Arduino에게 랜덤으로 변경되는 제어 신호를 보내고, Arduino는 Rpi 5에 0~9 범위에 있는 임의의 숫자는 센서값으로 보내는 양방향 통신 테스트 프로그램과 실험 동영상.
  - Rpi 5의 main thread에서 생성한 제어 신호는 serial_thread에서 arudino에 전송하고, serial_thread에서 수신한 arduino의 센서값은 main_thread에서 출력함.

    [양방향 통신 및 Thread 간 데이터 접근](https://github.com/iispace/AI/blob/main/RL/RL%EA%B8%B0%EB%B0%98_%EC%9E%A5%EC%95%A0%EB%AC%BC%ED%9A%8C%ED%94%BC_%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/Phase_3_1_2.md)
