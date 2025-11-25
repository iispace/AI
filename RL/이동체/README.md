# 강화학습 기반 장애물 회피 자율 주행 시스템 탑재를 위한 이동체 제작


## 재료
|항목|기능|비고|
|:-|:-|:-|
|RC카 기본 키트<br><img width="177" height="158" alt="image" src="https://github.com/user-attachments/assets/536127da-77e4-485f-9589-66861c2351dc" />|모터 구동 이동체|프레임 x  1<br>기어 모터 x 4<br>바퀴 x 4|
|Arduino Uno<br><img width="118" height="109" alt="image" src="https://github.com/user-attachments/assets/f5e01340-dfe8-4e77-b464-867a8409d225" />|1.Raspberry Pi와의 통신을 통한 모터 제어용 보드<br>2.조이스틱용 보드|마이크로 컨트롤러 x 2|
|L298N<br><img width="107" height="116" alt="image" src="https://github.com/user-attachments/assets/51432e49-b19d-468b-af04-f6f1b9707211" />|모터 드라이버|휠 동력 전달|
|18650 배터리 홀더<br><img width="138" height="146" alt="image" src="https://github.com/user-attachments/assets/224e7e3e-0272-4b3d-b46e-dafc16de391c" />|아두이노용 베터리 홀더|3.7V 18650 배터리 2구용|
|18650 배터리(3.7V)<br><img width="168" height="51" alt="image" src="https://github.com/user-attachments/assets/f58726c5-6bc2-4113-bfc5-ce7969be89ca" />|아두이노, Rpi 5 파워 소스|18650 x 4|
|볼트미터<br><img width="118" height="98" alt="image" src="https://github.com/user-attachments/assets/f5cffe3f-598a-4cc1-a949-154e58461df1" />|배터리 전압 표시|4.5V ~ 30V|
|On/Off 스위치<br><img width="75" height="88" alt="image" src="https://github.com/user-attachments/assets/56ea6b40-88fa-4f26-b64b-448ab49aba9f" />|Main power On/Off 스위치||
|DC Barrel Jack Adapter(male)<br><img width="123" height="149" alt="image" src="https://github.com/user-attachments/assets/5631ed4f-abf4-478a-a51f-d50a23cbb3de" />|Arduino 전원 연결부|Positive Polarity(center-positive)|
|JST XH2.54 케이블 커넥터(M & F)<br><img width="156" height="116" alt="image" src="https://github.com/user-attachments/assets/509fa21d-83b6-44d5-8a92-ef5f6bbc4697" />|배터리<-> 스위치, 배터리 <-> 볼트미터 연결|약 7cm 길이 x 2|
|HC-05<br><img width="163" height="67" alt="image" src="https://github.com/user-attachments/assets/aa0a5d71-34c2-4cba-a81d-5bcd2fedcb31" />|블루투스 통신|블루투스 모듈 x 2|
|9V 배터리 홀더(배터리 포함)<br><img width="147" height="171" alt="image" src="https://github.com/user-attachments/assets/590e9d58-7672-45ec-b1bf-a82b4b8cbe40" />|조이스틱 power source||
|Joystick Shield<br><img width="163" height="104" alt="image" src="https://github.com/user-attachments/assets/fe78cfb3-96a5-48bd-9df9-72f9d4bd3657" />|무선 조정기|무선 조정기 쉴드|
|Raspberry Pi 5<br><img width="166" height="107" alt="image" src="https://github.com/user-attachments/assets/ee9c82a5-d972-41a3-ae7a-75169bf61d5e" />|강화학습 모델 구동|마이크로 컴퓨터|
|OV5647 5M camera<br><img width="101" height="112" alt="image" src="https://github.com/user-attachments/assets/a7979b21-526f-4eef-8e29-7dbd3edac1a9" />|라즈베리파이 호환 카메라|Raspberry Pi 5용 연결 케이블 포함|
|Rpi TFT LCD(2.2")<br><img width="128" height="99" alt="image" src="https://github.com/user-attachments/assets/df85263e-b199-404b-a6e1-91814022dfdc" />|Raspberry Pi 5 Display|Adafruit 2.2" PiTFT HAT - 320x240 Display|
|18650 UPS for Rpi 5<br><img width="188" height="144" alt="image" src="https://github.com/user-attachments/assets/f2495056-ceca-4be2-85be-06a020088949" />|Raspberry Pi 5 파워 보드|5V 5A 충전 모듈(X1200 v1.2)|
|ADXL345 3출 가속도 센서 모듈<br><img width="129" height="84" alt="image" src="https://github.com/user-attachments/assets/c679cd16-51cf-4549-84e1-71a5f6efe982" />|장애물 충돌 감지|IIC / SPI 통신 지원|
|추가 프레임<br><img width="287" height="146" alt="image" src="https://github.com/user-attachments/assets/cc902b85-3ef2-4eeb-ad4e-eedf7414d8ab" />|부품 실장|3D 프린팅|

## 1 단계: RC Car 제작 


### 이동체 부분

  - 핀연결
    |HC-05|L298N|Arduino Uno|
    |:-|:-|:-|
    ||ENA|11(PWM pin)|
    ||IN1|10|
    ||IN2|9|
    ||IN3|8|
    ||IN4|7|
    ||ENB|6(PWM pin)|
    |VCC|5V+||
    |GND||GND|
    |TX||D2|
    |RX||D3|

    <img width="426" height="300" alt="image" src="https://github.com/user-attachments/assets/04178c57-8c2e-4a54-bf90-431877aa394a" />

    <img width="520" height="400" alt="image" src="https://github.com/user-attachments/assets/b246876a-7c48-4c88-a510-bb53d7e84ca1" />


  - 아두이노 코드 업로드
    ```
    #include <Arduino.h>
    #include <SoftwareSerial.h>
    
    SoftwareSerial btSerial(2,3);
    
    #define Speed_L 11
    #define LEFT_1 10    // left motor forward
    #define LEFT_2 9     // left motor reverse
    #define RIGHT_1 8    // right motor forward
    #define RIGHT_2 7    // right motor reverse
    #define Speed_R 6
    
    char c;
    int speed = 128;  // duty cycle: 50% i.e., 0.5
    
    
    void setup() {
      btSerial.begin(9600);
      //Serial.begin(9600);
    
      pinMode(Speed_L, OUTPUT);  // 11
      pinMode(LEFT_1, OUTPUT);   // 10
      pinMode(LEFT_2, OUTPUT);   // 9
      pinMode(RIGHT_1, OUTPUT);  // 8
      pinMode(RIGHT_2, OUTPUT);  // 7
      pinMode(Speed_R, OUTPUT);  // 6
    
      //Serial.println("....bluetooth test....");
    
    }
    
    void loop() {
      if(btSerial.available()){
        c = btSerial.read();
        //Serial.println(c);
    
        // 전진,후진,좌회전,우회전 제어는 각 모터와 모터 드라이버 사이의 선 연결을 어떻게 했는지에 따라 달라질 수 있음.
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
          //LEFT_1=LOW,  LEFT_2=HIGHT이면 두 핀 사이의 전압 차이가 발생하므로 전류가 흐름. 즉, 왼쪽 모터가 정방향으로 회전  
          digitalWrite(LEFT_1, LOW);    // 10 
          digitalWrite(LEFT_2, HIGH);    // 9
          //RIGHT_1=LOW, RIGHT_2=HIGH 이면 두 핀 사이의 전압 차이가 발생하므로 전류가 흐름. 즉, 오른쪽 모터가 정방향으로 회전
          digitalWrite(RIGHT_1, LOW);   // 8
          digitalWrite(RIGHT_2, HIGH);   // 7
          analogWrite(Speed_R, speed);   // 6
        }
        else if (c == 'L'){  // (좌회전) 
          analogWrite(Speed_L, speed);   // 11
          //LEFT_1=LOW,  LEFT_2=HIGHT이면 두 핀 사이의 전압 차이가 발생하므로 전류가 흐르지만 방향은 거꾸로. 즉, 왼쪽 모터가 정방향으로 회전  
          digitalWrite(LEFT_1, LOW);    // 10 
          digitalWrite(LEFT_2, HIGH);    // 9
          //RIGHT_1 = HIGH 이고 RIGHT_2 = LOW이면 두 핀 사이의 전압이 다르므로 전류가 흐름. 즉, 오른쪽 모터가 역방향으로 회전함 
          digitalWrite(RIGHT_1, HIGH);   // 8
          digitalWrite(RIGHT_2, LOW);   // 7
          analogWrite(Speed_R, speed);   // 6
        }
        else if (c == 'R'){ // (우회전) 
          analogWrite(Speed_L, speed);   // 11
          //LEFT_1 = HIGH 이고 LEFT_2 = LOW이면 두 핀 사이의 전압 차이가 생기므로 전류가 흐르지만 방향은 역방향. 즉, 왼쪽 모터가 역방향으로 회전함 
          digitalWrite(LEFT_1, HIGH);    // 10 
          digitalWrite(LEFT_2, LOW);    // 9
          //RIGHT_1=LOW, RIGHT_2=HIGH 이면 두 핀 사이의 전압 차이가 발생하므로 전류가 흐름. 즉, 오른쪽 모터가 정방향으로 회전
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
        }
      }
    }

    ```

### 조이스틱 부분

- Pin 연결
  |Joystick Shield|HC-05|
  |:-|:-|
  |5V+|VCC|
  |GND|GND|
  |D2|TX|
  |D3|RX|

  <img width="207" height="150" alt="image" src="https://github.com/user-attachments/assets/b644778c-45e4-4638-9e4b-bceccbc00191" />

- 아두이노 코드 업로드 
  ```
  #include <Arduino.h>
  #include <NeoSWSerial.h>
  
  #define BT_RX 7  // 아두이노 7번 핀 <-> HC-05 TX 연결 
  #define BT_TX 6  // 아두이노 6번 핀 <-> HC-05 RX 연결 
  
  NeoSWSerial HC05(BT_RX, BT_TX); // RX, TX
  
  int up_button = 2;      // 'G' : Go Straight
  int down_button = 4;    // 'B' : Go Back
  int buzzer_button = 5;  // '1' : Buzzer
  int stop_button = 3;   //  '0' : Stop
  
  //int select_button = 7;    // F  keyboard interrupt용
  int joystick_button = 8;  // for Funduino Joystick Module 정지 버튼으로 사용 예정 ('0' 명령어용)
  
  int axis_x = A0;  // for Funduino Joystick Module
  int axis_y = A1;  // for Funduino Joystick Module
  
  int axis_pins[2] = {axis_x, axis_y};
  int axis_values[2] = {0, 0};
  
  char data='0';
  
  String carState = "";
  
  void setup() {
    Serial.begin(9600);
    //HC05.begin(38400);  // HC-05 AT mode 기본 통신 속도
    HC05.begin(9600);  // HC-05 기본 Data 통신 속도
    pinMode(up_button, INPUT_PULLUP);
    pinMode(down_button, INPUT_PULLUP);
    pinMode(buzzer_button, INPUT_PULLUP);
    pinMode(stop_button, INPUT_PULLUP);
    
    //pinMode(select_button, INPUT_PULLUP);
    pinMode(buzzer_button, INPUT_PULLUP);
    
    pinMode(joystick_button, INPUT_PULLUP);
  
    delay(1000);
    Serial.println("Test Master started...");
    
  }
  
  void loop() {
    if(digitalRead(up_button) == 0){   // button pressed
      data = 'G';      
      carState = "Go straight";
    }
    else if(digitalRead(down_button) == 0){
      data = 'B';       
      carState = "Go Back";
    }
    else if(digitalRead(buzzer_button) == 0){
      data = '1';       
      carState = "Buzzer on";
    }
    else if(digitalRead(stop_button) == 0){
      data = '0';      
      carState = "Stop";
    }
    else if(digitalRead(joystick_button) == 0){
      data = '0';      // Stop
      carState = "Stop";
    }
    //else if(digitalRead(select_button) == 0){
    //  data = 'C';      // keyboard interrupt
    //  carState = "keyboard interrupt";
    //} 
     
    else{
      //data = '.';      // No command
      for (int i = 0; i < 2; i++) {
        axis_values[i] = analogRead(axis_pins[i]);
        axis_values[i] = map(axis_values[i], 0, 1023, -10, 10);
      }
  
      if ((axis_values[0] == -10) && (axis_values[1] == -4)) {
      data = 'L';      // Turn Left
      carState = "Turn Left (Joystick)";
      }
      else if ((axis_values[0] == 3) && (axis_values[1] == -4)) {
        data = 'R';      // Turn Right
        carState = "Turn Right (Joystick)";
      }
      else if ((axis_values[0] == -4) && (axis_values[1] == 3)) {
        data = 'G';      // Go straight
        carState = "Go straight (Joystick)";
      }
      else if ((axis_values[0] == -4) && (axis_values[1] == -10)) {
        data = 'B';      // Go Back
        carState = "Go Back (Joystick)";
      }
      else if ((axis_values[0]== -4) && (axis_values[1] == -4) ) {
        data = '.';      // No command
        carState = "No command";
      }
    }
    
  
    if (data != '.') {
      HC05.write(data);       // 읽은 데이터를 시리얼 모니터에 출력
      // Serial.print(data);
      // Serial.print(" axis x: ");
      // Serial.print(axis_values[0]);
      // Serial.print(" y: ");
      // Serial.println(axis_values[1]);
      delay(1);
    }
  }
  
  ```
