import logging
from logging.handlers import RotatingFileHandler
import datetime

import MovieDataProcessor
import MovieDataImporter

class MissionImpossible:
	def __init__(self):
		logger = logging.getLogger("MovieDataLog")
		logger.setLevel(logging.INFO)

		formatter = logging.Formatter("%(asctime)s -11s %(levelname)-10s %(message)s")
	
		# Log to file
		filehandler = RotatingFileHandler("./log/MovieDataImport.log", maxBytes=1000000, backupCount=5)
		filehandler.setLevel(logging.INFO)
		filehandler.setFormatter(formatter)
		logger.addHandler(filehandler)

		# Log to stdout too
		streamhandler = logging.StreamHandler()
		streamhandler.setLevel(logging.INFO)
		streamhandler.setFormatter(formatter)
		logger.addHandler(streamhandler)

	
	def Execute(self):
		logger = logging.getLogger("MovieDataLog")

		logger.info('Ehtan Hunt is stealing data from Facebook...[%s]', datetime.datetime.now().strftime("%d-%m-%Y_%H:%M:%S"))

		theEthanHunt = MovieDataImporter.EthanHunt()
		aStolenFBData = theEthanHunt.StealFBData()

		if aStolenFBData is not "":
			logger.info('Ethan Hunt successfully stolen the data => [%s]', aStolenFBData)
		else:
			logger.error("Ethan Hunt failed to steal the data")
			raise Exception("Ethan Hunt failed to steal the data")

		logger.info('Eugene Kittridge is processing the data...')

		theEugeneKittridge = MovieDataProcessor.EugeneKittridge(aStolenFBData)
		#theEugeneKittridge = MovieDataProcessor.EugeneKittridge("/home/unni/Desktop/MovieForum/data/moviedata_10012015_083814.txt")
		theEugeneKittridge.Consume()

		logger.info('Successfully processed the data')


theMI = MissionImpossible()

theMI.Execute()
