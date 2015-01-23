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

import urllib2
import json
from exceptions import PushettaException, TokenValidationError, ChannelNotFoundError


class Pushetta(object):
	
	def __init__(self, apiKey):
		self._apiKey = apiKey
		
	def pushMessage(self, channel, body, expire=None):
		try:
			req = urllib2.Request('http://api.pushetta.com/api/pushes/{0}/'.format(channel))
			req.add_header('Content-Type', 'application/json')
			req.add_header('Authorization', 'Token {0}'.format(self._apiKey))
		
			payload = dict()
			payload["body"] = body
			payload["message_type"] = "text/plain"
			if expire is not None:
				payload["expire"] = expire

			response = urllib2.urlopen(req, json.dumps(payload))
		except urllib2.HTTPError, e:
			if e.code == 401:
				raise TokenValidationError("Invalid token")
			elif e.code == 404:
				raise ChannelNotFoundError("Channel name not found")
			else:
				raise PushettaException(e.reason)
		except urllib2.URLError, e:
			raise PushettaException(e.reason)
		except Exception:
			import traceback
			raise PushettaException(traceback.format_exc())
