#!/usr/bin/python

# Read and print data from DHT11 sensors.
# Author: Jani Jansson
# Version: 0.1
# Date: Dec 16, 2017

# Example used as a basis of the code by:
# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola

import sys
import Adafruit_DHT
import sqlite3


# Using a Raspberry Pi with DHT11 sensors
# connected to GPIO2, GPIO3 and GPIO4.

# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
sensor1 = Adafruit_DHT.DHT11
sensor2 = Adafruit_DHT.DHT11
sensor3 = Adafruit_DHT.DHT11
sensor1_pin = 2
sensor2_pin = 3
sensor3_pin = 4
sensor1_temperature, sensor2_temperature, sensor3_temperature = None, None, None
sensor1_humidity, sensor2_humidity, sensor3_humidity = None, None, None

# Specify the database for the logging of data:
# Using 'temperaturelog.db' SQLite3 database with table 'temperatures' for storing the data
conn = sqlite3.connect('temperaturelog.db')
curs = conn.cursor()


def measure():
	global sensor1_humidity
	global sensor2_humidity
	global sensor3_humidity
	global sensor1_temperature
	global sensor2_temperature
	global sensor3_temperature

	# Try to grab a sensor reading.  Use the read_retry method which will retry up
	# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
	sensor1_humidity, sensor1_temperature = Adafruit_DHT.read_retry(sensor1, sensor1_pin)
	sensor2_humidity, sensor2_temperature = Adafruit_DHT.read_retry(sensor2, sensor2_pin)
	sensor3_humidity, sensor3_temperature = Adafruit_DHT.read_retry(sensor3, sensor3_pin)


def write_to_prompt():
	# Note that sometimes you won't get a reading and
	# the results will be null (because Linux can't
	# guarantee the timing of calls to read the sensor).
	# If this happens try again!
	if sensor1_humidity is not None and sensor1_temperature is not None:
	    print('Sensor 1: Temp={0:0.2f}*C  Humidity={1:0.2f}%'.format(sensor1_temperature, sensor1_humidity))
	else:
	    print('Sensor 1: Failed to get reading from sensor 1. Try again!')

	if sensor2_humidity is not None and sensor2_temperature is not None:
	    print('Sensor 2: Temp={0:0.2f}*C  Humidity={1:0.2f}%'.format(sensor2_temperature, sensor2_humidity))
	else:
	    print('Sensor 2: Failed to get reading from sensor 2. Try again!')

	if sensor3_humidity is not None and sensor3_temperature is not None:
	    print('Sensor 3: Temp={0:0.2f}*C  Humidity={1:0.2f}%'.format(sensor3_temperature, sensor3_humidity))
	else:
	    print('Sensor 3: Failed to get reading from sensor 3. Try again!')

def write_to_sql():
	global conn
	global curs

	# Write data to SQL:
	# temperatures (id INTEGER PRIMARY KEY AUTOINCREMENT, sensor_id INTEGER, temperature NUMERIC, humidity NUMERIC, currentdate DATE, currenttime TIME, misc TEXT)
	curs.execute("INSERT INTO temperatures values(NULL, 1, (?), (?), date('now'), time('now'), NULL)", (sensor1_temperature, sensor1_humidity))
	curs.execute("INSERT INTO temperatures values(NULL, 2, (?), (?), date('now'), time('now'), NULL)", (sensor2_temperature, sensor2_humidity))
	curs.execute("INSERT INTO temperatures values(NULL, 3, (?), (?), date('now'), time('now'), NULL)", (sensor3_temperature, sensor3_humidity))
	
	# Commit the changes to SQL:
	conn.commit()

# Run the functions:

measure()
write_to_prompt()
write_to_sql()
