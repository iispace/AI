# Arduino Uno: 3축 가속도 센서 설치

### 3축 가속도 센서(MPU-6050 칩 기반 GY-521 모듈)

  <img width="162" height="200" alt="image" src="https://github.com/user-attachments/assets/25136f72-c91e-435f-9221-1fb939ad1148" />
  <img width="168" height="200" alt="image" src="https://github.com/user-attachments/assets/5273478e-4e2d-4256-80c2-485e567b03fd" />

<br>

### 결선도

  <img width="444" height="300" alt="image" src="https://github.com/user-attachments/assets/57eba9b3-f25a-4303-9c68-812cafab4d86" />

<br>

### Rpi 5에서 제어 신호 받아 모터 구동하며, 가속도 센서를 통해 아두이노에서 충돌 감지 시 Rpi 5로 "Y" 문자 전송하는 테스트 코드

  ```
  // 시리얼 통신으로 Rpi 5에서 제어 신호 받아 이동체를 제어하고 Rpi 5로 센서값 전달하는 프로그램 <2025-11-28>

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

// ISR (Interrupt Service Routine)
void collisionISR() {
  collisionDetected = true;
} 

// --------------------- Variables -------------------- //
char c = '\0';    // default control command to stop motor
int speed = 128;   // duty cycle: 25% i.e., 0.25
//int sensor_value = -2;  // This value will be 1 and sent to Rpi 5 when Collision is detected

void wakeUpMPU6050() ;
void enableCollisionDetection(uint8_t, uint8_t);

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

  // 아두이노가 준비 되었음을 알리기 위한 깜박임(Arduino Ready Indicator)
  for (int i=0;i<5;i++){
    digitalWrite(CtrlLED, HIGH);
    delay(100);
    digitalWrite(CtrlLED, LOW);
    delay(100);
  }

  // ----------------------- MPU-6050 Init ---------------------- //
  Wire.begin();
  wakeUpMPU6050();
  enableCollisionDetection(4, 20); // threshold = 4 LSB( ≈ 0.24 g), duration=20 samples(≈ 20 * 0.125 ms = 2.5 ms)

}


void loop() {
  // ---------------- 충돌 인터럽트 처리 ---------------- //
  if(collisionDetected){
    //sensor_value = 1; // 충돌 감지 시 센서 값 1로 설정
    for (int i=0; i<5; i++) { 
      rpiSerial.write('Y');   // 충돌 감지 신호를 Rpi 5로 5번 전송 (통신 실패할 경우를 대비하여...) 
      Serial.println("===== Collision detected! Sent to Rpi 5: Y ===== ");
      delay(100);
    }
    collisionDetected = false; // 플래그 리셋
    //sensor_value = -2; // 기본 센서 값으로 복귀
  } 

  // --------------- Rpi 5의 제어 신호 처리 ---------------- //
  if(rpiSerial.available() > 0){
    delay(10);
    c = rpiSerial.read();
    Serial.print("Received command from Rpi 5: ");
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
      digitalWrite(CtrlLED, HIGH);
      c = '\0';  // 명령어 처리 후 초기화
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
      digitalWrite(CtrlLED, HIGH);
      c = '\0';  // 명령어 처리 후 초기화
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
      digitalWrite(CtrlLED, HIGH);
      c = '\0';  // 명령어 처리 후 초기화
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
      digitalWrite(CtrlLED, HIGH);
      c = '\0';  // 명령어 처리 후 초기화
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
    analogWrite(Speed_R, 0);   // 6
    digitalWrite(CtrlLED, LOW);
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
  Wire.write(threshold);    // threshold 값 (필요시 조정, 단위: LSB)
  Wire.endTransmission(true);

  // Motion Detection Duration 설정 (Register 0x20)
  Wire.beginTransmission(MPU);
  Wire.write(0x20);  // MOT_DUR register
  Wire.write(duration);    // duration 값 (필요시 조정, 단위: 샘플)
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
<br>

### 테스트 결과 

  - 간혹 발생하는 통신 누락에 대비하기 위해 아두이노에서 충돌 감지 건별 마다 충돌 신호인 "Y"를 0.1초 간격으로 5번 전송한다.
  - 테스트에 사용된 충돌 감지 임계값:
    - 가속도: threshold = 4 LSB (=> 4 / 16384 ≈ 0.24 g)
    - 지속 시간: duration=20 samples(=> 20 * 0.125 ms = 2.5 ms)
      
  - 아래 그림과 같이, Rpi 5에서 모터 제어 신호를 받아 운행 중에 충돌 감지도 잘 일어나고, 충돌이 감지되었을 때 Rpi 5로 메시지 전송도 잘 된다.
         
  <img width="1196" height="502" alt="image" src="https://github.com/user-attachments/assets/10e140db-2cd7-4083-9e64-2cba28e97272" />

<br>

<hr>

# References

[1]<a id="ref_1"></a> [How to use the accelerometer-gyroscope GY-521](https://projecthub.arduino.cc/Nicholas_N/how-to-use-the-accelerometer-gyroscope-gy-521-647e65)

[2]<a id="ref_2"></a> [MPU-6000 and MPU-6050 Register Map and Description Revision 4.2](https://invensense.tdk.com/wp-content/uploads/2015/02/MPU-6000-Register-Map1.pdf)

[3]<a id="ref_3"></a> [MPU-6000 and MPU-6050 Product Specification Revision 3.4](https://invensense.tdk.com/wp-content/uploads/2015/02/MPU-6000-Datasheet1.pdf)

[4]<a id="ref_4"></a> [Arduino Tutorials: GY-521(MPU-6050)](https://github.com/iispace/Arduino_Learning_Tutorials/tree/main/GY_512_%EA%B0%80%EC%86%8D%EB%8F%84%EC%84%BC%EC%84%9C)
