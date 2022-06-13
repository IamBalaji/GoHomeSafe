from scipy.spatial import distance
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np 
import argparse
import imutils
import time
import dlib
import cv2
import json
from PIL import Image
import io
import time
import os
x = time.time()


class FatigueDetection:
	def __init__(self):
		self.EYE_AR_THRESH = 0.3
		self.EYE_AR_CONSEC_FRAMES = 3
		self.MOUTH_AR_THRESH = 0.5
		self.MOUTH_AR_CONSEC_FRAMES = 3
		self.HEAD_DROP_CONSEC_FRAMES = 3
		self.COUNTER_HEAD_DROP = 0
		self.TOTAL_head_drops = 0
		self.COUNTER_eye = 0
		self.TOTAL_eye = 0
		self.TOTAL_blinks = 0
		self.COUNTER_mouth = 0
		self.TOTAL_yawns = 0
		self.path2shape_predictor = "shape_predictor_68_face_landmarks.dat"
		self.detector = dlib.get_frontal_face_detector()
		self.predictor = dlib.shape_predictor(self.path2shape_predictor)
		self.output_video = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc(*'DIVX'),6,(900,900))
		self.BlinkEARs = []
		self.YawnEARs = []
	def getEarBlink(self,Eye):
		dist15 = distance.euclidean(Eye[1], Eye[5])
		dist24 = distance.euclidean(Eye[2],Eye[4])
		dist03 = distance.euclidean(Eye[0], Eye[3])
		EAR = (dist15 + dist24)/float(2.0*dist03)
		return EAR

	def getEarYawn(self,Mouth):
		dist_horizontal = distance.euclidean(Mouth[0], Mouth[4])
		dist_vertical1 = distance.euclidean(Mouth[1], Mouth[7])
		dist_vertical2 = distance.euclidean(Mouth[2], Mouth[6])
		dist_vertical3 = distance.euclidean(Mouth[3], Mouth[5])
		yawn_ar = (dist_vertical1 + dist_vertical2 + dist_vertical3)/(3.0*dist_horizontal)
		return yawn_ar

	def displayFrame(frame):
		cv2.imshow("current frame", frame)
		cv2,waitKey()

	def detectBlink(self,frame):
		(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
		(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
		frame = cv2.resize(frame, (900,900))
		gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
		rects = self.detector(gray,0)
		for rect in rects:
			shape = self.predictor(gray, rect)
			shape = face_utils.shape_to_np(shape)

			leftEye = shape[lStart:lEnd]
			rightEye = shape[rStart:rEnd]
			leftEAR = self.getEarBlink(leftEye)
			rightEAR = self.getEarBlink(rightEye)

			ear = (leftEAR + rightEAR) / 2.0

			leftEyeHull = cv2.convexHull(leftEye)
			rightEyeHull = cv2.convexHull(rightEye)
			cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
			cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

			if ear < self.EYE_AR_THRESH:
				self.COUNTER_eye += 1
				if self.COUNTER_eye >= self.EYE_AR_CONSEC_FRAMES:
					self.TOTAL_blinks += 1
					cv2.putText(frame, "Driver Drowsiness Alert",(10,100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
			else:
				self.COUNTER_eye = 0

		if(len(rects)==0):
			self.COUNTER_HEAD_DROP += 1
			if self.COUNTER_HEAD_DROP >= self.HEAD_DROP_CONSEC_FRAMES:
				self.TOTAL_head_drops += 1
				cv2.putText(frame, "Driver Distraction Alert", (10,100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255),2)
		return frame
	def detectYawn(self,frame):
		(mouthStart, mouthEnd) = face_utils.FACIAL_LANDMARKS_IDXS['mouth']
		frame = cv2.resize(frame,(900,900))
		gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
		rects = self.detector(gray,0)

		for rect in rects:
			shape = self.predictor(gray,rect)
			shape = face_utils.shape_to_np(shape)

			mouth = np.asarray([shape[48],shape[50],shape[51],shape[52],shape[54],shape[56],shape[57],shape[58]])
			mouthEAR = self.getEarYawn(mouth)

			mouthHull = cv2.convexHull(mouth)
			cv2.drawContours(frame,[mouthHull],-1,(0,255,0),1)

			if mouthEAR < self.MOUTH_AR_THRESH:
				self.COUNTER_mouth += 1
			else:
				if self.COUNTER_mouth >= self.MOUTH_AR_CONSEC_FRAMES:
					self.TOTAL_yawns += 1
				self.COUNTER_mouth = 0

			cv2.putText(frame,"Yawns: {}".format(self.TOTAL_yawns),(10,300),cv2.FONT_HERSHEY_SIMPLEX, 0.7,(100,100,0),2)
		return frame

	def paramCalibration(self):
		# print("Please blink or yawn or blink and yawn as fast as possible and as slow as possible......")
		# print("Calibration will be done for 300 frames as of now.....")

		# BlinkEARs = []
		# YawnEARs = []
		# counter = 300
		# while counter >= 0:
		# 	# if not vs.more():
		# 	# 	break
		# 	# ret, frame = vs.read()

		# 	(lStart,lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
		# 	(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']

		# 	frame = cv2.resize(frame,(900,900))

		# 	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
		# 	rects = self.detector(gray,0)

		# 	for rect in rects:
		# 		shape = self.predictor(gray,rect)
		# 		shape = face_utils.shape_to_np(shape)

		# 		leftEye = shape[lStart:lEnd]
		# 		rightEye = shape[rStart:rEnd]
		# 		leftEAR = self.getEarBlink(leftEye)
		# 		rightEAR = self.getEarBlink(rightEye)

		# 		ear = (leftEAR + rightEAR) / 2.0
		# 		mouth = np.asarray([shape[48],shape[50],shape[51],shape[52],shape[54],shape[56],shape[57],shape[58]])
		# 		mouthEAR = self.getEarYawn(mouth)

		# 		BlinkEARs.append(ear)
		# 		YawnEARs.append(mouthEAR)
		# 	counter -= 1
		# 	cv2.putText(frame, "Calibration is being done.",(10,50),cv2.FONT_HERSHEY_SIMPLEX,0.7,(100,100,0),2)
		# 	cv2.putText(frame,"Please look at the camera and try to blink, yawn and blink-yawn together.",(10,70),cv2.FONT_HERSHEY_SIMPLEX,0.7,(100,100,0),2)
		# 	cv2.imshow("Frame",frame)
		# 	self.output_video.write(frame)
		# 	cv2.waitKey(1)

		BlinkEARs = np.asarray(self.BlinkEARs)
		min_blinkEAR = min(BlinkEARs)
		max_blinkEAR = max(BlinkEARs)

		median_blinkEAR = (min_blinkEAR + max_blinkEAR)/2.0

		temp_min = 0
		temp_max = 0
		count = 0
		for ear in range(BlinkEARs.size):
			if BlinkEARs[ear] <= median_blinkEAR:
				temp_min = temp_min + BlinkEARs[ear]
				count += 1
			else:
				temp_max = temp_max + BlinkEARs[ear]
		temp_min = temp_min / float(count)
		temp_max = temp_max / float(BlinkEARs.size - count)

		self.EYE_AR_THRESH = (temp_min + temp_max)/2.0

		YawnEARs = np.asarray(self.YawnEARs)
		min_yawnEAR = min(YawnEARs)
		max_yawnEAR = max(YawnEARs)

		median_yawnEAR = (min_yawnEAR+max_yawnEAR) / 2.0

		temp_min = 0
		temp_max = 0
		count  = 0
		for ear in range(YawnEARs.size):
			if YawnEARs[ear] <= median_yawnEAR:
				temp_min = temp_min + YawnEARs[ear]
				count += 1
			else:
				temp_max = temp_max + YawnEARs[ear]

		temp_min = temp_min / float(count)
		temp_max = temp_max / float(YawnEARs.size - count)

		self.MOUTH_AR_THRESH = (temp_min+temp_max)/2.0
	def execute(self,frame,count):
		if count == 1:
			print("Starting Calibration......Stay tuned....")
			# ret, frame = vs.read()
			# frame = cv2.UMat(frame)
			# frame = cv2.resize(frame,(900,900))
			# cv2.putText(frame,"Starting Calibration......Stay tuned....",(100,50),cv2.FONT_HERSHEY_SIMPLEX,0.7,(100,100,0),2)
			# cv2.imshow("Frame",frame)
			# cv2.waitKey(1)
			print("Please blink or yawn or blink and yawn as fast as possible and as slow as possible......")
			print("Calibration will be done for 300 frames as of now.....")

		if count <= 300:
			(lStart,lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
			(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']

			frame = cv2.resize(frame,(900,900))

			gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
			rects = self.detector(gray,0)

			for rect in rects:
				shape = self.predictor(gray,rect)
				shape = face_utils.shape_to_np(shape)

				leftEye = shape[lStart:lEnd]
				rightEye = shape[rStart:rEnd]
				leftEAR = self.getEarBlink(leftEye)
				rightEAR = self.getEarBlink(rightEye)

				ear = (leftEAR + rightEAR) / 2.0
				mouth = np.asarray([shape[48],shape[50],shape[51],shape[52],shape[54],shape[56],shape[57],shape[58]])
				mouthEAR = self.getEarYawn(mouth)

				self.BlinkEARs.append(ear)
				self.YawnEARs.append(mouthEAR)
				cv2.putText(frame, "Calibration is being done.",(10,50),cv2.FONT_HERSHEY_SIMPLEX,0.7,(100,100,0),2)
				cv2.putText(frame,"Please look at the camera and try to blink, yawn and blink-yawn together.",(10,70),cv2.FONT_HERSHEY_SIMPLEX,0.7,(100,100,0),2)
				# cv2.imshow("Frame",frame)
				self.output_video.write(frame)
				# cv2.waitKey(1)

		
		if count == 300:
			self.paramCalibration()
			print("EYE THRESHOLD: "+str(self.EYE_AR_THRESH)+"\n")
			print("MOUTH THRESHOLD: "+str(self.MOUTH_AR_THRESH)+"\n")
		if count>300:
			frame = self.detectBlink(frame)
			frame = self.detectYawn(frame)

			self.output_video.write(frame)
			cv2.imshow("Frame", frame)
			cv2.waitKey(1)
			# key = cv2.waitKey(1) & 0xFF

			# if key == ord("q"):
			# 	break
		return frame


def send_frame():
	print("[INFO] starting video stream thread...")
	vs = cv2.VideoCapture(0)
	fd = FatigueDetection()
	count = 1
	while True:
		ret,frame = vs.read()
		# cv2.imshow('f',frame)
		# cv2.waitKey(1)
		fd.execute(frame,count)
		count += 1
		key = cv2.waitKey(1) & 0xFF
		if key == ord("q"):
			break

	self.output_video.release()
	vs.release()
	print('done')
	cv2.destroyAllWindows()

# send_frame()