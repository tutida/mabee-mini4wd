#!/usr/bin/python3

import sys
import requests
import json
import paho.mqtt.client as mqtt
import json
import time
import random

TOKEN = "token_oGASkTyGpKhRtDhN"
TOPIC = "mini4ku/action"
BASEURL = 'http://localhost:11111'
MAGNUM_SPEED = 0
SONIC_SPEED = 0


# ------------------------------------------------------
# On Connect
def on_connect(client, userdata, flags, respons_code):
    print('status {0}'.format(respons_code))
    client.subscribe(TOPIC)
    up()

# ------------------------------------------------------
# On Message
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    data = json.loads(msg.payload.decode("utf-8"))["data"]
    data = json.loads(data)

    machine = data["machine"]

    if machine == 'MAGNUM':
    	boost(machine)
    elif machine == 'SONIC':
    	boost(machine)

    print(data)
    print(MAGNUM_SPEED)
    print(SONIC_SPEED)

# ------------------------------------------------------
# Mabee Control

def up():
	global MAGNUM_SPEED
	global SONIC_SPEED

	MAGNUM_SPEED=20
	SONIC_SPEED=20
	magnuc_url = BASEURL + '/devices/1/set?pwm_duty=' + str(MAGNUM_SPEED)
	sonic_url = BASEURL + '/devices/2/set?pwm_duty=' + str(SONIC_SPEED)
	send_mabeee(magnuc_url)
	send_mabeee(sonic_url)

def boost(machine):
	global MAGNUM_SPEED
	global SONIC_SPEED

	if machine == 'MAGNUM':
		magnuc_url = BASEURL + '/devices/1/set?pwm_duty=100'
		send_mabeee(magnuc_url)
	elif machine == 'SONIC':
		sonic_url = BASEURL + '/devices/2/set?pwm_duty=100' 
		send_mabeee(sonic_url)
 

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
	time.sleep(.05)

client.disconnect()
client.loop_stop()