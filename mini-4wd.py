#!/usr/bin/python3

import sys
import requests
import json
import paho.mqtt.client as mqtt
import json
import time

TOKEN = "token_YrIVwpnLhgF1aVDN"
TOPIC = "mabeee/hoge"
BASEURL = 'http://localhost:11111'
MAGNUM_SPEED = 0

# ------------------------------------------------------
# On Connect
def on_connect(client, userdata, flags, respons_code):
    print('status {0}'.format(respons_code))
    client.subscribe(TOPIC)

# ------------------------------------------------------
# On Message
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    forward()
    # data = json.loads(msg.payload.decode("utf-8"))["data"]
    # data = {key:value.strip() for key, value in data.items()}
    # if "room" in data.keys():
    #     print(data)

# ------------------------------------------------------
# Mabee Control
def forward():
	global MAGNUM_SPEED
	if MAGNUM_SPEED <= 100:
		MAGNUM_SPEED+=10
		if MAGNUM_SPEED > 100:
			MAGNUM_SPEED = 100
		url = BASEURL + '/devices/1/set?pwm_duty=' + str(MAGNUM_SPEED)
		send_mabeee(url)

def down():
	global MAGNUM_SPEED
	if MAGNUM_SPEED != 0:
		MAGNUM_SPEED-=1
		url = BASEURL + '/devices/1/set?pwm_duty=' + str(MAGNUM_SPEED)
		send_mabeee(url)

def send_mabeee(url):
    print(url)
    response = requests.get(url)
    print(response.status_code)

# ------------------------------------------------------
# Setting MQTT Clinet
client = mqtt.Client()
client.username_pw_set("token:%s"%TOKEN)
client.on_connect = on_connect
client.on_message = on_message
client.tls_set("mqtt.beebotte.com.pem")
client.connect("mqtt.beebotte.com", port=8883, keepalive=60)

# ------------------------------------------------------
# Loop
client.loop_start()

while True:
	down()
	time.sleep(.1)

client.disconnect()
client.loop_stop()