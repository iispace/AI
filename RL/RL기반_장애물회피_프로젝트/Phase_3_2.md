# 3단계: 2. Raspberry Pi Power Supply & Display


### 1. Power Supply  

  - **보호 회로가 장착된 18650 Battery의 크기가 구입한 UPS(X1200)의 배터리 홀더 크기보다 커서 장착할 수 없었으므로, UPS 대신 5V 2A 출력의 보조배터리를 USB-C로 연결함**
  - 5V 5A를 공급할 수 있는 UPS 대신에 5V 2A 출력의 보조배터리를 사용하므로, 필요한 전력을 최소화할 수 있도록 Display 장치는 부착하지 않도록 하였음.

  - 나중에 보호 회로가 없는 18650 배터리가 준비되었을 때 사용할 수 있도록 UPS 관련 내용을 아래에 기록해 둠.

    ##### X1200 UPS
    
    - 포고 핀(Pogo pin) 연결 방식의 UPS 모듈이므로 Raspberry Pi 5 하단에 직접 적층하여 연결
    
      <img width="182" height="144" alt="image" src="https://github.com/user-attachments/assets/0a8a995c-08ce-43a9-9471-5c2f1ad4bda3" />
      <img width="223" height="144" alt="image" src="https://github.com/user-attachments/assets/86fd045e-0bd7-4202-840f-768e4a8de1c5" />

      <img width="599" height="139" alt="image" src="https://github.com/user-attachments/assets/ca89f1b5-2649-49da-9060-05761484f717" />

      [Raspberry Pi 5 power mgmt UPS shield X1200 설명](https://suptronics.com/Raspberrypi/Power_mgmt/x1200-v1.2.html)

      [Rpi 5에 X1200 설정 방법](https://suptronics.com/Raspberrypi/Power_mgmt/x120x-v1.0_software.html) 

<br>

     
<hr>    

### 2. Raspberry Pi 5 Display 

  #### 2.1. PiTFT Display     

  - [Adafruit 2.2" PiTFT HAT - 320x240 Display](https://learn.adafruit.com/adafruit-2-2-pitft-hat-320-240-primary-display-for-raspberry-pi)

    <img width="240" height="180" alt="image" src="https://github.com/user-attachments/assets/c1a7c082-d7f8-4693-9a36-8da8b55c2ef5" />

<br>

  #### 2.2. Rpi 5 pin map

  <img width="632" height="400" alt="image" src="https://github.com/user-attachments/assets/4f362feb-b717-4978-8a53-f26366a93247" />
