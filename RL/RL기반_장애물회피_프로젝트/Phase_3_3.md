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
int16_t AC_scale = 16384; // 가속도계 스케일 (±2g 설정 시 16384 LSB/g)
uint8_t GY_scale = 131;  // 자이로스코프 스케일 (±250°/s 설정 시 131 LSB/°/s)
int8_t interruptPin = 2; // Arduino 외부 인터럽트 핀 번호

volatile bool collisionDetected = false; // 인터럽트 발생 플래그

// ISR (Interrupt Service Routine)
void collisionISR() {
  collisionDetected = true;
}

/* 설정 레지스터 값 읽기용 마스크 및 제목 배열 
  - SEL_masks, SEL_titles: 기본 스케일 범위(Full scale range) 확인 (측정값을 사람이 이해할 수 있는 물리량으로 변환하기 위해 필요)
  - MOT_masks, MOT_titles: 충격 감지 시 인터럽트 발생을 위한 모션 디텍션 설정값 확인
*/
const uint8_t SEL_masks[] = {0x18, 0x18}; // GYRO_CONFIG 레지스터의 FS_SEL 비트와 ACCEL_CONFIG 레지스터의 AFS_SEL 비트 추출용 마스크
const char* SEL_titles[] = {"GYRO_FS_SEL", "ACCEL_AFS_SEL"};

const uint8_t MOT_masks[] = {0xFF, 0x07}; // SMPLRT_DIV 레지스터의 모든 비트와 CONFIG 레지스터의 DLPF_CFG 비트 추출용 마스크
const char* MOT_titles[] = {"SMPLRT_DIV(Reg 25)", "DLPG_CFG(Reg 26)"};

void readRegistryValue(uint8_t, int8_t, const uint8_t*, const char*[]); 


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
  Wire.write(8);    // threshold 값 (필요시 조정, 단위: LSB)  => 16 LSB = (16 / 16384) * 1000 = 0.976 g (약 1 g. 즉 지구 중력 가속도와 유사한 크기의 가속도)
  Wire.endTransmission(true);

  // Motion Detection Duration 설정 (Register 0x20)
  Wire.beginTransmission(MPU);
  Wire.write(0x20);  // MOT_DUR register
  Wire.write(20);    // duration 값 (필요시 조정, 단위: 샘플) => if 40 샘플: 40 * 0.125 ms = 5ms (샘플링 레이트가 8kHz일 때, 샘플 주기는 1000 ms / 8000 Hz = 0.125 ms) 
  Wire.endTransmission(true);

  // Interrupt Enable 설정 (Register 0x38)
  Wire.beginTransmission(MPU);
  Wire.write(0x38);  // INT_ENABLE register
  Wire.write(0x40);  // MOT_EN 비트 활성화
  Wire.endTransmission(true);

  // Arduino 외부 인터럽트 핀 연결 (GY-521 INT → D2)
  pinMode(interruptPin, INPUT);
  attachInterrupt(digitalPinToInterrupt(2), collisionISR, RISING);


  // 설정 레지스터 값 읽기 및 출력
  readRegistryValue(0x1B, 2, SEL_masks, SEL_titles);
  readRegistryValue(0x19, 2, MOT_masks, MOT_titles);

  Serial.println("\nACCELEROMETER(LSB)\tTEMP\tGYROSCOPE(LSB)");
  Serial.println("ax\tay\taz\tT\tgx\tgy\tgz");
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

  // 변환 및 출력 (소수점 3자리)
  Serial.print((float)AcX / AC_scale, 3); Serial.print("\t");
  Serial.print((float)AcY / AC_scale, 3); Serial.print("\t");
  Serial.print((float)AcZ / AC_scale, 3); Serial.print("\t");
  Serial.print(Tmp / 340.00 + 36.53, 2); Serial.print("\t"); // 온도는 소수점 2자리만
  Serial.print((float)GyX / GY_scale, 3); Serial.print("\t");
  Serial.print((float)GyY / GY_scale, 3); Serial.print("\t");
  Serial.println((float)GyZ / GY_scale, 3);

  delay(333);
}

// 측정값의 정확한 이해를 돕기 위한 설정 레지스터 값 읽기
void readRegistryValue(uint8_t Reg_Addr, int8_t num_regs, const uint8_t* bit_masks, const char* titles[]) {
  /*
    - Reg_Addr: 읽고자 하는 시작 레지스터 주소
    - num_regs: 읽고자 하는 연속 레지스터의 개수
    - bit_mask: 관심 있는 비트만 추출하기 위한 마스크 (예: 0x07은 하위 3비트 추출용)
  */
  uint16_t configs[2];  // 가변 길이 배열을 지원하지 않으므로, 최대 2개 레지스터까지만 처리할 수 있게 제한
  Wire.beginTransmission(MPU);
  Wire.write(Reg_Addr);  // start register address to read
  Wire.endTransmission(false);
  Wire.requestFrom(MPU, num_regs, true);  // request a total num_regs number of registers

  if (Wire.available() >= num_regs) {
    for (int i = 0; i < num_regs; i++) {
      configs[i] = Wire.read() & bit_masks[i]; // 비트 마스크 적용하여 관심 비트만 추출
    }

  for (int i = 0; i < num_regs; i++) {
      Serial.print(titles[i]);
      Serial.print(": ");
      Serial.print(configs[i]);
      Serial.print(" | ");
    }
    Serial.println();
  }

  // 샘플링 레이트 계산 및 출력 (Reg_Addr가 0x19인 경우에만)
  if (Reg_Addr == 0x19) {
    // 기본 클럭은 8kHz, DLPF 활성화 시 1kHz
    int base_rate = (configs[1] == 0 || configs[1] == 7) ? 8000 : 1000;
    float sample_rate = base_rate / (1.0 + configs[0]);

    Serial.print("Calculated Sample Rate: ");
    Serial.print(sample_rate);
    Serial.println(" Hz");
  }
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
