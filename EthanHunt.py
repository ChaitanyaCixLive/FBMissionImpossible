import logging

import LutherStickell
import FranzKrieger
import Facebook

class EthanHunt:

	def __init__(self):

		self.logger = logging.getLogger("MissionImpossibleLog")
		

	def StealFBData(self):

		aPostsFile = ""
		try:
			#	Set up the team
			theLutherStickell = LutherStickell.LutherStickell()
			theFranzKrieger = FranzKrieger.FranzKrieger()
		

			#	Go......

			theFranzKrieger.DriveToFacebook(theLutherStickell.GetMeFacebookAppURL())

			theFacebook = Facebook.Facebook(theFranzKrieger.GetFacebookKey())

			self.logger.info('Reached Facebook. Going to sneak in...')

			theFacebook.PerformRetinaScanAndTriggerSteal(theLutherStickell.GetMeFacebookUserId(), theLutherStickell.SsssssshGetFacebookPassword())

			self.logger.info('Logged in. Waiting for the data to be stolen...')

			theFacebook.WaitForDataToForm()

			self.logger.info('Page has stolen the data. Importing it now...')
			
			aPostsFile = theFacebook.BringItToLocalSystem()

			self.logger.info('Data is now in local disk')

			theFranzKrieger.DriveAwayFromFacebook()

			self.logger.info('Everything is OK. Mission success')
		
		except:
			self.logger.error('Grrrr.. Ethan Got shot...escape.......')
		finally:
			return aPostsFile


