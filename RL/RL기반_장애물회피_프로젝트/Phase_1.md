# 1 단계: RC Car 제작 


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
