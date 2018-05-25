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

# ------------------------------------------------------
# On Message
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    data = json.loads(msg.payload.decode("utf-8"))["data"]
    data = json.loads(data)

    action = data["action"]
    machine = data["machine"]

    if action == 'UP':
    	up(machine)
    elif action == 'DOWN':
    	down(machine)
    elif action == 'START':
    	start()
    elif action == 'STOP':
    	stop()

    print(data)
    print(action)
    print(MAGNUM_SPEED)
    print(SONIC_SPEED)

# ------------------------------------------------------
# Mabee Control
def up(target):
	global MAGNUM_SPEED
	global SONIC_SPEED

	if target == 'MAGNUM' :
		MAGNUM_SPEED = random.randint(30,70)
		# if MAGNUM_SPEED <= 100:
		# 	MAGNUM_SPEED+=20
		# if MAGNUM_SPEED > 100:
		# 	MAGNUM_SPEED = 100
	elif target == 'SONIC' :
		SONIC_SPEED = random.randint(30,70)
		# if SONIC_SPEED <= 100:
		# 	SONIC_SPEED+=20
		# if SONIC_SPEED > 100:
		# 	SONIC_SPEED = 100

def down(target):
	global MAGNUM_SPEED
	global SONIC_SPEED

	# if target == 'MAGNUM' :
		# if MAGNUM_SPEED >= 0:
		# 	MAGNUM_SPEED-=20
		# if MAGNUM_SPEED < 0:
		# 	MAGNUM_SPEED = 0
	# elif target == 'SONIC' :
		# if SONIC_SPEED >= 0:
		# 	SONIC_SPEED-=20
		# if SONIC_SPEED < 0:
		# 	SONIC_SPEED = 0

def start():
	global MAGNUM_SPEED
	global SONIC_SPEED

	magnuc_url = BASEURL + '/devices/1/set?pwm_duty=' + str(MAGNUM_SPEED)
	sonic_url = BASEURL + '/devices/2/set?pwm_duty=' + str(SONIC_SPEED)
	send_mabeee(magnuc_url)
	send_mabeee(sonic_url)

def stop():
	global MAGNUM_SPEED
	global SONIC_SPEED

	magnuc_url = BASEURL + '/devices/1/set?pwm_duty=0'
	sonic_url = BASEURL + '/devices/2/set?pwm_duty=0'
	send_mabeee(magnuc_url)
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
client.loop_forever()