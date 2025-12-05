# Raspberry Pi 5의 파이썬 프로그램 동작 On/Off 버튼 추가

## 결선도


<img width="516" height="300" alt="image" src="https://github.com/user-attachments/assets/37103bbc-f64d-41c0-8256-a68dcef9d651" />

<img width="471" height="300" alt="image" src="https://github.com/user-attachments/assets/c1729632-c819-4d10-8fed-1ab479787d63" />


## Rpi 5 Code

```
from typing import List
from gpiozero import Button, DigitalOutputDevice, PWMOutputDevice, TonalBuzzer, LED 

import carserve_camera
import cv2
import threading
import serial 
import time, sys, os

import random 

# 실행 상태 플래그
thread_running = True
stop_event = threading.Event() # 종료 이벤트

LED_Green = LED(17)  # Rpi 5 Ready Indicator
SW_Btn = Button(23, pull_up=True)  # 라즈베리파이 5에 내장된 풀업 저항 사용

def uart_task():
    global thread_running
    global gSensorValue
    global gCtrlData
    
    try:
        ser = serial.Serial('/dev/ttyAMA2', 9600, timeout=0.1)  # UART2 (GPIO4-TX, GPIO5-RX)

        # 버퍼 초기화
        ser.reset_input_buffer()
        time.sleep(0.2)

        while not stop_event.is_set():
            if thread_running:
                if gCtrlData != '-1':
                    ser.write(gCtrlData.encode())
                    time.sleep(0.5)
                    print(f"data sent to uno: {gCtrlData}")
                    gCtrlData = '-1'
                while ser.in_waiting > 0:
                    gSensorValue = ser.read(1).strip().decode('utf-8', errors='ignore') # 1byte 읽어서 문자로 변환

                time.sleep(0.2)
            else:
                time.sleep(0.1)
    except Exception as e:
        print(f"Exception arose in uart_task: {e}")
    finally:
        ser.close()

def toggle_running():
    global thread_running
    thread_running = not thread_running
    if thread_running:
        print("... Program resummed ...")
        led_blicking(0.1, 2)
    else:
        print("--- Program standby ...")
        led_blicking(0.1, 2)

def led_blicking(ts:float, cnt=10):
    for i in range(cnt):
        LED_Green.on()
        time.sleep(ts)
        LED_Green.off()
        time.sleep(ts)


def main():

    global thread_running        
    global gCtrlData 
    global gSensorValue

    gCtrlData = '-1'   
    #gSensorValue = '-1'.encode()
    gSensorValue = None
    chars = ['G', 'B', 'L', 'R', '0']

    SW_Btn.when_pressed = toggle_running 

    # Rpi 5 ready indication
    led_blicking(0.1)

    task1  = threading.Thread(target=uart_task, daemon=True)
    task1.start()

    W, H = 640, 480
    # 카메라 객체 생성
    camera = carserve_camera.Carserve_PiCamera(W, H)
    filepath = "/home/pi/{프로젝트_폴더}/video/train"
    i = 0

    try:
        while not stop_event.is_set():
            while (camera.isOpened()) and thread_running:
                # 제어 데이터 값 갱신
                gCtrlData = random.choice(chars) 
                # 아두이노에서 수신한 센서 값 출력
                #print("sensor data from Uno: ", int.from_bytes(gSensorValue, 'big', signed=True)) 
                if gSensorValue is not None:
                    print("sensor data from Uno: ",gSensorValue) 
                    # 충돌 발생 시그널 받았을 때 처리해야 할 일 여기에 구현
                    led_blicking(0.05)   # 50ms 간격으로 10번 깜박임
                    time.sleep(3)  # 충돌 감지 신호 수신 후 3초 동안 대기 (아두이노 쪽에서도 같은 시간 동안 대기함)
                    time.sleep(0.1)
                    gSensorValue = None
                

                _, image = camera.read()
                image = cv2.flip(image, -1)
                cv2.imshow('Original image', image)

                height, _, _ = image.shape  # (480, 640, 3) => height: 480
                save_image = image[int(height/2):, :, :]
                cv2.imshow('Save image', save_image)

                # 이미지 파일로 저장
                cv2.imwrite("%s_%05d.png" % (filepath, i), save_image)
                i += 1
                time.sleep(1)  # 1초마다 반복

            cv2.destroyAllWindows()

    except KeyboardInterrupt:
        print("Keyboard Interrupt arose")
        cv2.destroyAllWindows()
        stop_event.set()
        task1.join()      # 서브 스레드가 종료될 때까지 기다림
        print("All threads stopped.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Program ended")
    

```

## 테스트 결과

  <img width="800" height="400" alt="image" src="https://github.com/user-attachments/assets/80cb2f1c-fa63-4862-ba4c-a5fd807dbdd4" />

