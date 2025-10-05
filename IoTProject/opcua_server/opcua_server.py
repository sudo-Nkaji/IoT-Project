#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import datetime
from opcua import Server

# ==== 設備名 ====
MACHINE_NAME = "pa-1"

# ==== GPIO設定 ====
GPIO.setmode(GPIO.BOARD)
PIN_RUN     = 7
PIN_STOP    = 11
PIN_ERROR   = 13
PIN_COUNTER = 15

GPIO.setup([PIN_RUN, PIN_STOP, PIN_ERROR, PIN_COUNTER], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# ==== OPC UAサーバー設定 ====
server = Server()
server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")
server.set_server_name("RaspberryPi_OPCUA_Server")

uri = f"http://example.org/opcua/rpi/{MACHINE_NAME}"
idx = server.register_namespace(uri)

machine = server.nodes.objects.add_object(idx, "Machine")

status_node  = machine.add_variable(f"ns={idx};s=Machine.Status",  "Status",  "STOP")
counter_node = machine.add_variable(f"ns={idx};s=Machine.Counter", "Counter", 0)

status_node.set_writable()
counter_node.set_writable()

server.start()
print("✅ OPC UA Server started at opc.tcp://<172.16.126.52>:4840/freeopcua/server/")
print("Monitoring GPIO pins...")

# ==== 状態監視ループ ====
last_status = None
last_counter = 0

try:
    while True:
        # GPIO状態を読む
        run = GPIO.input(PIN_RUN)
        stop = GPIO.input(PIN_STOP)
        error = GPIO.input(PIN_ERROR)
        count = GPIO.input(PIN_COUNTER)

        # 状態決定
        if error:
            status = "ERROR"
        elif run:
            status = "RUN"
        elif stop:
            status = "STOP"
        else:
            status = "IDLE"

        # 状態変化時のみ更新
        if status != last_status:
            status_node.set_value(status)
            print(f"[{datetime.datetime.now()}] Status changed → {status}")
            last_status = status

        # 生産カウント（立ち上がり検出でカウントアップ）
        if count == 1 and last_counter == 0:
            current_val = counter_node.get_value() + 1
            counter_node.set_value(current_val)
            print(f"[{datetime.datetime.now()}] Counter increment → {current_val}")

        last_counter = count
        time.sleep(0.1)

finally:
    server.stop()
    GPIO.cleanup()
    print("Server stopped and GPIO cleaned up.")