import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .run import FatigueDetection
import cv2
import numpy as np
import base64
class detectConsumer(AsyncWebsocketConsumer):
	# def __init__(self):
	# 	self.count = 1
	# 	self.fd = FatigueDetection()
	async def connect(self):
		await self.accept()
		self.count = 1
		self.fd = FatigueDetection()
		# await self.send(json.dumps({
		# 	'type':"connection_established",
		# 	'message':"Welcome, You are now connected!"
		# 	}))
	async def receive(self,text_data):
		print("Frames: {}".format(self.count))
		img_str = base64.b64decode(text_data[22:])
		head = text_data[:22]
		img_arr = np.fromstring(img_str,np.uint8)
		img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
		# print(img.shape)
		# cv2.imshow('f',img)
		# cv2.waitKey(10000)
		# print(type(text_data))
		# print(text_data[:100])
		# image = np.fromstring(text_data, np.uint8)

		f = self.fd.execute(img,self.count)
		self.count += 1
		resp  = cv2.imencode('.png', f)[1]
		resp = resp.tobytes()
		# print(type(resp))
		s = base64.b64encode(resp)
		# print(s[:100])
		# cv2.imshow('f',f)
		# cv2.waitKey(10000)
		s = str(s,'UTF-8')
		s = head + s
		await self.send(s)
	# async def handle(self, body):
	# 	await asyncio.sleep(10)
	# 	await self.send_response(200, b"YOu are now connected", headers=[
	# 		(b"Content-Type", b"text/plain"),
	# 	])