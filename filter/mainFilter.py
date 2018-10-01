import sys
import os
import numpy as np
from filters import  LDRFilter
from filters import  LDRFilterRange
#import utils as U
import csv


def main():
	try:
		LDRFilterObj = LDRFilter() #Media Filter object
		LDRFilterRangeObj = LDRFilterRange() #Media Filter object
		mylistX = [] # Sotres only one canned data array. Argument to filter functions
		
		#Check source of data for the input to the function
		print('\n**************************************************************************************************')
		print('\nDo you want to read data from CSV file or from User. Make a selection')
		print('\n**************************************************************************************************')
		flagCSV = input('\nEneter your choice (1=read from CSV, 0=read from user): ') #1=read from CSV, 0=read from user

		if flagCSV == 1:
			#Read from the csv file
			print('\n******************** Reading from CSV file *******************************\n\n')
			
			#Get abs path of the data file	
			dataFile = os.path.abspath('data.csv') 
			print('\nReading data from CSV file ' + dataFile)

			#Read csv file
			with open(dataFile, 'rb') as csv_file:
				csv_reader = csv.reader(csv_file, delimiter = ',')
				
				#Read metadata, N, D, min range and max range
				csv_Header = csv_reader.next() 
				
				#Set attributes
				LDRFilterObj.setNandD(csv_Header[0], csv_Header[1]) 
				LDRFilterRangeObj.setMinRange(csv_Header[2])
				LDRFilterRangeObj.setMaxRange(csv_Header[3])
				
				#Read attributes	
				print ('\nLength of the array (N) is: ', LDRFilterObj.getN())
				print ('\nDepth of the scan (D) is: ',  LDRFilterObj.getD())
				print ('\nminRange is: ', LDRFilterRangeObj.getMinRange())
				print ('\nmaxRange is: ', LDRFilterRangeObj.getMaxRange())

				#Read each scanned data from the csv file i.e. read each data row from the file.
				for each_row in csv_reader:
					validRow = True #Flag set to false in any of the row data item is non-numeric/empty
					tmpListX = [] #Temp input array
					#print('\neach_row ', each_row)
					
					
					#Parse and convert string data read from each line of the csv file to float	
					for i in range(LDRFilterObj.getN()):
						
						
						if each_row[i].isdigit():
							tmpListX.append(float(each_row[i]))
						else:
							#If row from csv file has non-numeric/empty value, skip the row
							print('\nRow has non numeric data. Skip row.')
							validRow = False
							break

					#Skip non-numeric/empty rows from the CSV file		
					if validRow:
						#Crop input data and store it in input array.				
						mylistX = LDRFilterRangeObj.filterRange(tmpListX)	

						#Find median for last 'D' scans, plus current scan
						mylistY = LDRFilterObj.medianFilter(mylistX) 

						#Print Array of medians
						print('\nMedian list Y is :   ', mylistY)
		elif flagCSV == 0:
			#Reading from user
			print('\n******************** Reading from User *******************************\n\n')

			#Read Metadata, N, D, minRange, maxRange	
			myN = int(input('\n\nEnter Length (N) of Array: '))
			if	myN < 1:
				raise  ValueError

			myD = int(input('\n\nEnter Depth (D) 0f scan: '))
			LDRFilterObj.setNandD(myN, myD)
			LDRFilterRangeObj.setMinRange(float(input('\n\nEnter minRange:  ')))
			LDRFilterRangeObj.setMaxRange(float(input('\n\nEnter maxRange:  ')))
			#Read attributes	
			print ('\nLength of the array (N) is: ', LDRFilterObj.getN())
			print ('\nDepth of the scan (D) is: ',  LDRFilterObj.getD())
			print ('\nminRange is: ', LDRFilterRangeObj.getMinRange())
			print ('\nmaxRange is: ', LDRFilterRangeObj.getMaxRange())			
			#Flag to check if continue with read next scanned data from user	
			flagContinue = 1 
			while flagContinue:
				try:
					mylistX = []
					tmpListX =[]
					#Not Validating the input here. Assuming it is correct
					myInput = raw_input('\nPress "q" to Exit. Enter comma separated input array, where "N" is array length : ')
					
					#Quit the program
					if myInput == 'q':
						raise Exception
						print("\nquite")
					#print myInput		
					myInput = myInput.lstrip('[').rstrip(']') 
					#print myInput
					#Generate list from comma or space separated string
					if "," in myInput:
						#print("CSV")
						myInput.strip(' ')
						tmpListX = myInput.split(',')	
					elif " " in myInput:
						tmpListX = myInput.split(' ')

						
					
					#Read data again if entered array length is same as expected(N)
					if len(tmpListX) != LDRFilterObj.getN():
						print('\nArray length mismatch. Enter again!!!')
						continue

					#Generate array of floats		
					for i in range(len(tmpListX)):
						if tmpListX[i].isdigit():
							mylistX.append(float(tmpListX[i]))
						else:
							raise TypeError

					#Crop input data				
					mylistX = LDRFilterRangeObj.filterRange(mylistX)

					#Find median for last 'D', plus current scan
					mylistY = LDRFilterObj.medianFilter(mylistX)
					#Print Array of medians_
					print('\nMedian list Y is : ', mylistY)
				except NameError as e:
					print('Not a valid data. Enter again')
				except (TypeError):
					print '\nScanned element type mismatch!!'

			#return
		
	
	except (TypeError):
					print '\nScanned element type mismatch!!'
	except (ValueError):
		print '\nLength cannot be 0'

	except Exception as e:
		print('\nYou QUIT!. STOP execution!!')
	


if __name__ == "__main__":
	main()
