# Introdution

Interface to use Pushetta API with Python.
Pushetta is a service made to make it simple send push notifications from/to (almost) any device.
It can be used to send a notifications from Arduino to iPhone, from Raspberry Pi to Android, from web page to Beaglebone and many others.


# Getting started

```python
from pushetta import Pushetta

# API Key You get after signup on www.pushetta.com
API_KEY="00112233445566778899aabbccddeeff00112233"
p=Pushetta(API_KEY)
p.pushMessage("raspi", "Hello World")
```

### 
Release 1.0.14

Introduced subscription capability to receive notifications.

### 
Release 1.0.15

Subscribe callback  now brings informations on channel and timestamp in payload.


Sample use:

```python
import time
from pushetta import Pushetta

# Callback called when a message is received
def my_callback(payload):
	# payload contains body, channel and time of notification
	print "I received \"" + payload['message'] + '\" from ' + payload['channel'] + ' at ' \
	+ str(datetime.datetime.fromtimestamp(int(payload['timestamp'])))

# API Key You get after signup on www.pushetta.com
API_KEY="00112233445566778899aabbccddeeff00112233"
p=Pushetta("API_KEY")
# Subscribe a channel ("WebPush")
p.subscribe("WebPush", my_callback)

while True:
    time.sleep(1)
```