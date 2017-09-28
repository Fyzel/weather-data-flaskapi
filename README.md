# weather-data-flaskapi
A small Flask based RESTful API for collecting and reporting on humidity, pressure, and temperature for locations.

This API is intended to receive humidity, pressure, and temperature from weather Raspberry Pi based weather stations. The weather station setup will be documented along with the Python code to read data from the sensor and submit the data to either [MQTT](http://mqtt.org/), an Internet of Things (IOT) or Machine-2-Machine lightweight connectivity protocol. Alternatively, the weather station can submit data directly to the *weather-data-flaskapi* service.

There will be a user interface for dsplaying current and historic humidity, pressure, and temperature data.
