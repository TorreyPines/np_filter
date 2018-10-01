import sys
import os
import numpy as np

class LDRFilter:
	def __init__(self, myN=5, myD=3):
		self.myD = myD
		self.myN = myN
		self.tmpD = 0
		
		self.npArrayHistory = np.array([], float)
		
	#Getters
	def getN(self):
		return self.myN

	def getD(self):
		return self.myD

	#Setters		
	def setNandD(self, n=5, d=3):
		self.myN = int(n)
		self.myD = int(d)


	#Function to  return the median for a sorted array.
	def findMedian(self, mytmpList):
		
		if len(mytmpList) % 2 == 0:
			return (mytmpList[len(mytmpList) / 2] + mytmpList[len(mytmpList) / 2 - 1]) / 2
		else:
			return mytmpList[len(mytmpList) / 2]
		return myMid
	#End def findMedian(self, mytmpList)


	#Filter function to find median
	def medianFilter(self, listX):
		myMedianList = [] #List of medians return
		
		#Temp array for input before adding to input history
		tmpArray = np.array(listX, float).reshape(1, self.myN) 
		
		#Check if first item of the history input and/od add iems to input history                                         		
		if len(self.npArrayHistory) == 0:
			#Return the list as median. It is the first scan. Add it to input History
			myMedianList = np.array(listX, float)
			self.npArrayHistory =  tmpArray
		else:
			#Add all scans starting from 2nd scan to the input history
			self.npArrayHistory = np.concatenate((self.npArrayHistory, tmpArray))

			#Find median for current input history
			myMedianList = np.median(self.npArrayHistory, axis = 0)
		
		#Maintain Input History for only D number of scan	
		if len(self.npArrayHistory) > self.myD:
			#Eleminate most first scan
			self.npArrayHistory = self.npArrayHistory[1:, :]
		#print('\nInput History Array is: ', self.npArrayHistory)


		return myMedianList
	#End def medianFilter(self, listX)		
#End class LDRFilter


class LDRFilterRange:

	def __init__(self, minRange=0.03, maxRange=50):
		self.minRange = minRange
		self.maxRange = maxRange
		
	# Getters		
	def getMinRange(self):
		return self.minRange

	def getMaxRange(self):
		return self.maxRange


	#Setters		
	def setMinRange(self, minRange=0.03):
		self.minRange = float(minRange)

	def setMaxRange(self, maxRange=50.):
		self.maxRange = float(maxRange)
	

	#Function to crop values beyond allowed range 0.03 ~ 50
	def filterRange(self, listX):
		#print("\nin filterRange")
		for i in range(len(listX)):
			if listX[i] < self.minRange:
				listX[i] = self.minRange
			elif listX[i] > self.maxRange:
				listX[i] = self.maxRange
		#print(listX)		
		return listX
	#End filterRange(self, listX)	
#End class LDRFilterRange
	

