import logging
from logging.handlers import RotatingFileHandler
import datetime

import MovieDataProcessor
import MovieDataImporter


def InitializeLogger():
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

	
def Process():
	logger = logging.getLogger("MovieDataLog")

	logger.info('Importing data from Facebook...[%s]', datetime.datetime.now().strftime("%d-%m-%Y_%H:%M:%S"))

	aFileImporter = MovieDataImporter.MovieDataImporter()
	anImportedFile = aFileImporter.Import()

	if anImportedFile is not "":
		logger.info('Successfully imported the data => [%s]', anImportedFile)
	else:
		logger.error("Failed to import the data")
		raise Exception("Failed to import the data")

	logger.info('Importing data to database...')

	aFileProcessor = MovieDataProcessor.MovieDataProcessor(anImportedFile)
	#aFileProcessor = MovieDataProcessor.MovieDataProcessor("/home/unni/Desktop/MovieForum/data/moviedata_10012015_083814.txt")
	aFileProcessor.Process()

	logger.info('Successfully imported the data')


InitializeLogger()
Process()