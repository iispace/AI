# Arduino Uno: 3축 가속도 센서 설치

### 3축 가속도 센서(GY-521)

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

### 테스트 결과 (가독성을 위해 센서 측정값에 scale을 적용하여 변환한 값 출력)

<img width="720" height="500" alt="image" src="https://github.com/user-attachments/assets/12885eb1-9e8b-4655-aa14-21b0db8c819d" />

<br>

<hr>

### ※ 센서 측정값(raw data)을 그대로 출력할 경우의 값 해석 방법 

<img width="1082" height="275" alt="image" src="https://github.com/user-attachments/assets/b410634f-772b-4d30-95e8-0e4189ac6c81" />

- **Accelerometer(가속도) 해석**
  - MPU-6050의 Full Scale Range: +/-2g, 1g ≈ 16384 LSB(raw값) <== 28번 레지스터(ACCEL_CONFIG)에 설정된 값

    <img width="1347" height="252" alt="image" src="https://github.com/user-attachments/assets/31a719b8-b79c-44fb-ad16-46a7a52b9ff2" />

    <img width="855" height="209" alt="image" src="https://github.com/user-attachments/assets/a948b630-47f0-4ac8-a3e4-4e6d06ea9f17" />

    - Accelerometer(가속도)의 측정값이 X=780, Y=732, Z=17640일 때,
      - X축: 780 / 16384 ≈ 0.048 g = 48mg
      - Y축: 732 / 16384 ≈ 0.045 g = 45mg
      - Z축: 17640 / 16384 ≈ 1.08 g = 1080mg
        
    - **의미:**
      - 센서가 평평한 바닥에 놓여 있을 때, 중력은 Z축 방향으로 작용하므로, 약 1g 근처 값이 나오면 정상
      - 위의 예에서 보면, Z축에서 1.08g가 측정되었으므로 중력 방향이 Z축임을 확인할 수 있음
      - X,Y축의 값은 거의 0g에 가까우므로, 센서가 바닥에 거의 수평으로 놓여 있다는 것을 확인할 수 있음(약간의 기울기만 존재)

  <br>
  
- **Gyroscope(각속도) 해석**
  - MPU-6050의 Full Scale Range: +/-250°/s , 1 LSB ≈ 131°/s  <== 27번 레지스터(GYRO_CONFIG)에 설정된 값

    <img width="911" height="178" alt="image" src="https://github.com/user-attachments/assets/a4223f92-5e1a-46ec-ae39-5d8997106b45" />

    - Gyroscope(각속도)의 측정값이 X=-423, Y=589, Z=143일 때,
      - X축: -423 / 131 ≈ -3.2°/s  (=> 1초에 시계 방향으로 3.2도 회전. 이는 아주 작은 값으로 거의 정지 상태를 의미)
      - Y축: 589 / 131 ≈ 4.5°/s    (=> 1초에 반시계 방향으로 4.5도 회전. 이는 아주 작은 값으로 거의 정지 상태를 의미)
      - Z축: 143 / 131 ≈ 1.1°/s    (=> 1초에 반시계 방향으로 1.1도 회전. 이는 아주 작은 값으로 거의 정지 상태를 의미)

    - **의미:**
      - 센서가 가만히 놓여 있는 것 같지만, 노이즈 또는 미세한 흔들림으로 인해 아주 작은 회전 값이 측정됨.
      - 실제로는 거의 회전하지 않고 있는 상태를 보여줌.

<br>

<hr>

# References

[1]<a id="ref_1"></a> [How to use the accelerometer-gyroscope GY-521](https://projecthub.arduino.cc/Nicholas_N/how-to-use-the-accelerometer-gyroscope-gy-521-647e65)

[2]<a id="ref_2"></a> [MPU-6000 and MPU-6050 Register Map and Description Revision 4.2](https://invensense.tdk.com/wp-content/uploads/2015/02/MPU-6000-Register-Map1.pdf)

[3]<a id="ref_3"></a> [MPU-6000 and MPU-6050 Product Specification Revision 3.4](https://invensense.tdk.com/wp-content/uploads/2015/02/MPU-6000-Datasheet1.pdf)

[4]<a id="ref_4"></a> [Arduino Tutorials: GY-521](https://github.com/iispace/Arduino_Learning_Tutorials/tree/main/GY_512_%EA%B0%80%EC%86%8D%EB%8F%84%EC%84%BC%EC%84%9C)
