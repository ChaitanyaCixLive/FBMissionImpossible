import json
import mysql.connector
import time
import logging
import ConfigParser

class MovieDataProcessor:

	def __init__(self, aDataFileName_in):
		self.logger = logging.getLogger("MovieDataLog")
		self.myConfig = ConfigParser.ConfigParser()
		self.myConfig.read("./MovieConfig.ini")

		self.myDB = mysql.connector.connect(user=self.myConfig.get("MovieConfig", "DBUser"), password=self.myConfig.get("MovieConfig", "DBPass"), host='127.0.0.1', database=self.myConfig.get("MovieConfig", "Database"),  use_unicode=True, charset='utf8')
		self.myDataFileName = aDataFileName_in
		

	def __del__(self):
		self.myDB.close()

	def RetrieveId(self, aTableName_in, anObj_in):

		cursor = self.myDB.cursor()

		query = u"SELECT id FROM " + aTableName_in + " where fb_id = %s"
		cursor.execute(query, (anObj_in["id"],))

		anId = -1
		aResultRecords = cursor.fetchone()
		if aResultRecords is not None:
			anId = aResultRecords[0]

		return anId

	def RetrieveAllPostIds(self):

		cursor = self.myDB.cursor()

		query = u"SELECT fb_id FROM post"
		cursor.execute(query)

		return map(lambda x: x[0], cursor.fetchall())


	def InsertPerson(self, aPerson_in):

		anId = self.RetrieveId('person', aPerson_in)

	
		if anId == -1:
			self.logger.info("Inserting person")
			cursor = self.myDB.cursor()
			cursor.execute(u"INSERT INTO person(name, fb_id) VALUES(%s, %s)", (aPerson_in["name"], aPerson_in["id"],))
			self.myDB.commit()
			anId = cursor.lastrowid

		self.logger.info(("anId = %d") % anId)
		return anId

	def GetSQLDateTime(self, anObj_in):

		aPostTime = time.strptime(anObj_in["created_time"][:18], "%Y-%m-%dT%H:%M:%S")	#2015-01-06T17:07:27+0000
		anSQLDateTime = time.strftime('%Y-%m-%d %H:%M:%S', aPostTime)
		return anSQLDateTime

	def InsertPost(self, aPost_in, anAuthorId_in):

		anId = self.RetrieveId('post', aPost_in)
	
		if anId == -1:
			self.logger.info("Inserting post")
			cursor = self.myDB.cursor()
		
			cursor.execute(u"INSERT INTO post(fb_id, author_id, message, date_time, type) VALUES(%s, %s, %s, %s, %s)", (aPost_in["id"], anAuthorId_in, aPost_in.get("message", ""), self.GetSQLDateTime(aPost_in), aPost_in["type"],))

			anId = cursor.lastrowid

			cursor.execute(u"INSERT INTO post_description(post_id) VALUES(%s)", (anId,))

			self.myDB.commit()
			
		self.logger.info(("anId = %d") % anId)
		return anId


	def RetrieveLikeId(self, aPostId_in, aPersonId_in):

		cursor = self.myDB.cursor()

		query = u"SELECT id FROM fb_like where post_id = %s and person_id = %s"
		cursor.execute(query, (aPostId_in, aPersonId_in,))

		anId = -1
		aResultRecords = cursor.fetchone()
		if aResultRecords is not None:
			anId = aResultRecords[0]

		return anId

	def InsertLikes(self, aPost_in, aPostId_in):

		if "likes" in aPost_in:
			for aLikePerson in aPost_in["likes"]["data"]:
				aPersonId = self.InsertPerson(aLikePerson)
				aLikeId = self.RetrieveLikeId(aPostId_in, aPersonId)
				if aLikeId == -1:

					self.logger.info("Inserting like")
					cursor = self.myDB.cursor()
		
					cursor.execute(u"INSERT INTO fb_like(post_id, person_id) VALUES(%s, %s)", (aPostId_in, aPersonId,))
					self.myDB.commit()
					anId = cursor.lastrowid

	def InsertComments(self, aPost_in, aPostId_in):

		if "comments" in aPost_in:
			for aComment in aPost_in["comments"]["data"]:
				aPersonId = self.InsertPerson(aComment["from"])
				aCommentId = self.RetrieveId('comment', aComment)
				if aCommentId == -1:

					self.logger.info("Inserting comment")
					cursor = self.myDB.cursor()
		
					cursor.execute(u"INSERT INTO comment(fb_id, post_id, person_id, date_time, message, like_count) VALUES(%s, %s, %s, %s, %s, %s)", (aComment["id"], aPostId_in, aPersonId, self.GetSQLDateTime(aComment), aComment["message"], aComment.get("like_count", 0)))
					self.myDB.commit()
					anId = cursor.lastrowid
	
	def HandlePost(self, aPost_in):

		self.logger.info("Post data : [%s, %s, %s]" , aPost_in["id"], aPost_in["from"], aPost_in["created_time"])
		
		aPersonId = self.InsertPerson(aPost_in["from"])
		aPostId = self.InsertPost(aPost_in, aPersonId)
		self.InsertLikes(aPost_in, aPostId)
		self.InsertComments(aPost_in, aPostId)
	
		
	
	
	def Process(self):

		with open(self.myDataFileName) as data_file:    
	    		aMovieJson = json.load(data_file)

		self.logger.info("There are %s posts, inserting them to database...", len(aMovieJson))

		self.logger.info("The set of facebook posts that are not in the facebook downloaded list is : %s", list(set(self.RetrieveAllPostIds()) - set(map(lambda x: x["id"], aMovieJson))))

		for aPost in aMovieJson:
			self.HandlePost(aPost)

	
