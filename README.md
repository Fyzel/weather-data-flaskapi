# weather-data-flaskapi
A small Flask based RESTful API for collecting and reporting on humidity, pressure, and temperature for locations.

This API is intended to receive humidity, pressure, and temperature from weather Raspberry Pi based weather stations. The weather station setup will be documented along with the Python code to read data from the sensor and submit the data to either [MQTT](http://mqtt.org/), an Internet of Things ([IoT](https://en.wikipedia.org/wiki/Internet_of_things)) or Machine-2-Machine ([M2M](https://en.wikipedia.org/wiki/Machine_to_machine)) lightweight connectivity protocol. Alternatively, the weather station can submit data directly to the *weather-data-flaskapi* service.

There will be a user interface for dsplaying current and historic humidity, pressure, and temperature data.

![Architecture Diagram][architecture]

[architecture]: https://github.com/Fyzel/weather-data-flaskapi/blob/master/static/images/architecture.png?raw=true
