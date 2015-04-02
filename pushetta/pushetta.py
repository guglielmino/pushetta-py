from __future__ import absolute_import

# The MIT License (MIT)
#
# Copyright (c) 2015 Fabrizio Guglielmino <guglielmino@gumino.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import future 
import paho.mqtt.client as mqtt
import re
import json
import uuid

from .exceptions import PushettaException, TokenValidationError, ChannelNotFoundError

try:
	from urllib2 import urlopen as urlopen
	import urllib2 as urllib
	from urllib2 import Request
	from urllib2 import HTTPError
	from urllib2 import URLError
except:
	import urllib
	from urllib.request import Request
	from urllib.error import HTTPError
	from urllib.error import URLError
	from urllib.request import urlopen as urlopen



class Pushetta(object):
	iot_url = "iot.pushetta.com"
	sub_pattern = "/pushetta.com/channels/{0}"

	message_callback = None

	def __init__(self, apiKey):
		self._apiKey = apiKey
		self.mqtt_client = None
		
	def pushMessage(self, channel, body, expire=None):
		try:
			req = Request('http://api.pushetta.com/api/pushes/{0}/'.format(channel))
			req.add_header('Content-Type', 'application/json')
			req.add_header('Authorization', 'Token {0}'.format(self._apiKey))
		
			payload = dict()
			payload["body"] = body
			payload["message_type"] = "text/plain"
			if expire is not None:
				payload["expire"] = expire

			response = urlopen(req, json.dumps(payload).encode('utf8'))
		except HTTPError as e:
			if e.code == 401:
				raise TokenValidationError("Invalid token")
			elif e.code == 404:
				raise ChannelNotFoundError("Channel name not found")
			else:
				raise PushettaException(e.reason)
		except URLError as e:
			raise PushettaException(e.reason)
		except Exception:
			import traceback
			raise PushettaException(traceback.format_exc())

	def subscribe(self, channel, callback):
		topic = Pushetta.sub_pattern.format(channel)

		self.message_callback = callback
		
		if self.mqtt_client is None:
			self.mqtt_client = mqtt.Client(client_id="pushetta-" + str(uuid.uuid4()))
			self.mqtt_client.on_message = self.__message_callback
			self.mqtt_client.on_connect = self.__connect_callback
			
			self.mqtt_client.username_pw_set(self._apiKey, password="pushetta")
		
			self.mqtt_client.connect(Pushetta.iot_url, 1883, 60)

			self.mqtt_client.user_data_set(topic)
			self.mqtt_client.loop_start()
		else:
			self.mqtt_client.subscribe(topic)

	def unsubscribe(self, channel):
		topic = Pushetta.sub_pattern.format(channel)

		self.mqtt_client.unsubscribe(topic)

	def __connect_callback(self, client, userdata, flags, rc):
		client.subscribe(userdata)

	def __message_callback(self, client, userdata, message):
		if self.message_callback is not None:
			notification = {'channel' : message.topic.split('/')[-1], 'message' : message.payload, 'timestamp' : message.timestamp}
			self.message_callback(notification)

