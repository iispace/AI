# Arduino Uno: 3축 가속도 센서 설치

### 3축 가속도 센서(GY-521)

  <img width="162" height="200" alt="image" src="https://github.com/user-attachments/assets/25136f72-c91e-435f-9221-1fb939ad1148" />
  <img width="168" height="200" alt="image" src="https://github.com/user-attachments/assets/5273478e-4e2d-4256-80c2-485e567b03fd" />

<br>

### 결선도

  <img width="444" height="300" alt="image" src="https://github.com/user-attachments/assets/57eba9b3-f25a-4303-9c68-812cafab4d86" />

<br>

### 3축 가속도 센서(GY-521) 테스트 코드

  ```
#include <Wire.h>
#include <Arduino.h>

const int MPU = 0x68;   // I2C address of the MPU-6050
int16_t AcX, AcY, AcZ, Tmp, GyX, GyY, GyZ;

volatile bool collisionDetected = false; // 인터럽트 발생 플래그

// ISR (Interrupt Service Routine)
void collisionISR() {
  collisionDetected = true;
}

void readConfigValue();
void read_MOT_Detect_ConfigValue();

void setup() {
  Wire.begin();
  Serial.begin(9600);

  // MPU-6050 깨우기
  Wire.beginTransmission(MPU);
  Wire.write(0x6B);  // PWR_MGMT_1 register
  Wire.write(0);     // set to zero (wakes up the MPU-6050)
  Wire.endTransmission(true);

  // Motion Detection Threshold 설정 (Register 0x1F)
  Wire.beginTransmission(MPU);
  Wire.write(0x1F);  // MOT_THR register
  Wire.write(16);    // threshold 값 (필요시 조정, 단위: LSB)  => 16 LSB = (16 / 16384) * 1000 = 0.976 g (약 1 g. 즉 지구 중력 가속도와 유사한 크기의 가속도)
  Wire.endTransmission(true);

  // Motion Detection Duration 설정 (Register 0x20)
  Wire.beginTransmission(MPU);
  Wire.write(0x20);  // MOT_DUR register
  Wire.write(40);    // duration 값 (필요시 조정, 단위: 샘플) => 40 샘플 = 40 * 0.125 ms = 5ms (샘플링 레이트가 8kHz일 때, 샘플 주기는 1000 ms / 8000 Hz = 0.125 ms) 
  Wire.endTransmission(true);

  // Interrupt Enable 설정 (Register 0x38)
  Wire.beginTransmission(MPU);
  Wire.write(0x38);  // INT_ENABLE register
  Wire.write(0x40);  // MOT_EN 비트 활성화
  Wire.endTransmission(true);

  // Arduino 외부 인터럽트 핀 연결 (GY-521 INT → D2)
  pinMode(2, INPUT);
  attachInterrupt(digitalPinToInterrupt(2), collisionISR, RISING);

  readConfigValue();
  read_MOT_Detect_ConfigValue();

  Serial.println("\nMPU6050 Initialized, Collision Detection is waiting...");
}

void loop() {
  if (collisionDetected) {
    Serial.println("COLLISION");
    collisionDetected = false; // 플래그 초기화
  }

  // 기존 센서 데이터 읽기
  Wire.beginTransmission(MPU);
  Wire.write(0x3B);  // starting with register 0x3B (ACCEL_XOUT_H)
  Wire.endTransmission(false);
  Wire.requestFrom(MPU, 14, true);  // request a total of 12 registers

  AcX=Wire.read()<<8|Wire.read();  // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)
  AcY=Wire.read()<<8|Wire.read();  // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
  AcZ=Wire.read()<<8|Wire.read();  // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L) 
  Tmp=Wire.read()<<8|Wire.read();  // 0x41 (TEMP_OUT_H) & 0x42 (TEMP_OUT_L)       
  GyX=Wire.read()<<8|Wire.read();  // 0x43 (GYRO_XOUT_H) & 0x44 (GYRO_XOUT_L)
  GyY=Wire.read()<<8|Wire.read();  // 0x45 (GYRO_YOUT_H) & 0x46 (GYRO_YOUT_L)          
  GyZ=Wire.read()<<8|Wire.read();  // 0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)

  Serial.print("Accelerometer (in LSB unit): ");
  Serial.print("X = "); Serial.print(AcX); 
  Serial.print(" | Y = "); Serial.print(AcY); 
  Serial.print(" | Z = "); Serial.print(AcZ); 
  Serial.print(" Temperature: ");
  Serial.print(Tmp / 340.00 + 36.53);
  Serial.print(" Gyroscope  (in LSB unit): ");
  Serial.print("X = "); Serial.print(GyX);  
  Serial.print(" | Y = "); Serial.print(GyY); 
  Serial.print(" | Z = "); Serial.println(GyZ); 
  Serial.println();

  delay(1000);
}

// 측정값의 정확한 이해를 돕기 위한 설정 레지스터 값 읽기
void readConfigValue() {
  uint16_t fs_sel, afs_sel;
  Wire.beginTransmission(MPU);
  Wire.write(0x1B);  // GYRO_CONFIG register
  Wire.endTransmission(false);
  Wire.requestFrom(MPU, 2, true);  // request a total of 2 registers

  if (Wire.available()) {
    fs_sel = Wire.read();
    afs_sel = Wire.read();
    Serial.print("\nGyro FS_SEL: ");  Serial.print(fs_sel);
    Serial.print(" | Accel AFS_SEL: ");  Serial.println(afs_sel);
  }
}

// MOT_THR, MOT_DUR 값을 의도한 대로 설정하기 위해 센서에 설정된 레지스터 값 읽어 확인하기
void read_MOT_Detect_ConfigValue() {
// Register 25 (SMPLRT_DIV) 읽기
  Wire.beginTransmission(MPU);
  Wire.write(0x19);  // 25 decimal
  Wire.endTransmission(false);
  Wire.requestFrom(MPU, 1, true);
  uint8_t smplrt_div = Wire.read();

  // Register 26 (CONFIG) 읽기
  Wire.beginTransmission(MPU);
  Wire.write(0x1A);  // 26 decimal
  Wire.endTransmission(false);
  Wire.requestFrom(MPU, 1, true);
  uint8_t config = Wire.read();

  Serial.print("SMPLRT_DIV (Reg 25): ");
  Serial.println(smplrt_div);
  Serial.print("CONFIG (Reg 26)    : ");
  Serial.println(config);

  // DLPF_CFG 추출 (하위 3비트)
  uint8_t dlpf_cfg = config & 0x07; // 0x07 = 0000 0111 이므로, config와 0x07의 AND 연산을 통해 하위 3비트만 추출
  Serial.print("DLPF_CFG bits: ");
  Serial.println(dlpf_cfg);

  // 기본 클럭은 8kHz, DLPF 활성화 시 1kHz
  int base_rate = (dlpf_cfg == 0 || dlpf_cfg == 7) ? 8000 : 1000;
  float sample_rate = base_rate / (1.0 + smplrt_div);

  Serial.print("Calculated Sample Rate: ");
  Serial.print(sample_rate);
  Serial.println(" Hz");
}
  ```
<br>

### 테스트 결과

<img width="1082" height="275" alt="image" src="https://github.com/user-attachments/assets/b410634f-772b-4d30-95e8-0e4189ac6c81" />

<br>

<hr>

# References

[1]<a id="ref_1"></a> [How to use the accelerometer-gyroscope GY-521](https://projecthub.arduino.cc/Nicholas_N/how-to-use-the-accelerometer-gyroscope-gy-521-647e65)

[2]<a id="ref_2"></a> [MPU-6000 and MPU-6050 Register Map and Description Revision 4.2](https://invensense.tdk.com/wp-content/uploads/2015/02/MPU-6000-Register-Map1.pdf)

[3]<a id="ref_3"></a> [MPU-6000 and MPU-6050 Product Specification Revision 3.4](https://invensense.tdk.com/wp-content/uploads/2015/02/MPU-6000-Datasheet1.pdf)
