from selenium import webdriver

import time
import logging
import os, errno
import datetime
import shutil

class ToolBox:

	@staticmethod
	def TeenageBoyWaitFor(isGirlComing, timeOut, peepInterval = 5):

		aTotalWaitTime = 0
		girlCame = True	# Start being opimist

		while not isGirlComing():	#	Is she around?

			if aTotalWaitTime > timeOut:
				girlCame = False	#	Optimism didn't work :(
				break	#	Go home

			time.sleep( peepInterval )	#	Sigh wait for some more time
			aTotalWaitTime = aTotalWaitTime + peepInterval
			

		return girlCame

	@staticmethod
	def SilentSniperKill(filename):
		try:
			os.remove(filename)
	    	except OSError as e: 
			if e.errno != errno.ENOENT: # Don't worrry if he is not there. Report kill.
		    		raise # 	Oh oh... something unexpected... raise alarm.


class Facebook:

	def __init__(self, theFaceBookKey):

		self.myDriver = theFaceBookKey

		self.logger = logging.getLogger("MissionImpossibleLog")

	def PickElement(self, elementId, aWaitTime = 20):

		aTotalWaitTime = 0
		anElement = None
		while anElement is None:
			anElement = self.myDriver.find_element_by_id(elementId)
			if anElement is None:
				time.sleep( 1 )
				aTotalWaitTime = aTotalWaitTime + 1
				if aTotalWaitTime > aWaitTime:
					break

		if anElement is None:
			raise "Unable to find element in web page : %s" % elementId

		return anElement

	def WaitForDataToForm(self):

		aDataStatusElement = self.PickElement("final_status")

		if ToolBox.TeenageBoyWaitFor(lambda : aDataStatusElement.text == "All the posts downloaded", 60) == True:
			self.logger.info( "Data collection finished")
		else:
			self.logger.error( "Failed to collect the data")
			raise Exception("Failed to collect the data") 
	    	

	
	def BringItToLocalSystem(self):

		aSrcFileName = "./data/moviedata.txt"
		ToolBox.SilentSniperKill(aSrcFileName)

		anImportLinkElement = self.PickElement("tfa_src_data")

		anImportLinkElement.click()

		if ToolBox.TeenageBoyWaitFor(lambda : os.path.exists(aSrcFileName), 60) == True:
			self.logger.info( "File download finished")
		else:
			self.logger.error( "Download wait timed out")
			raise Exception("Download wait timed out") 

		
		aDestFileName = "./data/moviedata_" + datetime.datetime.now().strftime("%d%m%Y_%H%M%S") + ".txt"
		self.logger.info( "The data file is stored at : " + aDestFileName)
		shutil.move(aSrcFileName, aDestFileName)
		
		return aDestFileName

	

	def PerformRetinaScanAndTriggerSteal(self, aUserName, aPassword):

		aGetDataElement = self.PickElement("login_button")

		aGetDataElement.click()

		time.sleep( 5 )

		self.myDriver.switch_to_window(self.myDriver.window_handles[-1])

		anEmailElement = self.PickElement("email")
		aPasswordElement = self.PickElement("pass")
		aLoginButtonElement = self.PickElement("u_0_1")

		anEmailElement.send_keys(aUserName)
		time.sleep( 2 )
		aPasswordElement.send_keys(aPassword)
		time.sleep( 2 )

		self.logger.info('Login data is entered')

		aLoginButtonElement.click()

		self.logger.info('Login data is submitted')

		time.sleep( 2 )

		self.myDriver.switch_to_window(self.myDriver.window_handles[-1])



