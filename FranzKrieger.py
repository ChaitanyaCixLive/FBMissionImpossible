from selenium import webdriver




class FranzKrieger:

	def DriveToFacebook(self, aDirections):

		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_argument('--disable-application-cache')
		prefs = {"download.default_directory" : "./data"}
		chrome_options.add_experimental_option("prefs",prefs)
		self.myDriver = webdriver.Chrome('/usr/bin/chromedriver', service_args=['--verbose'], chrome_options=chrome_options, service_log_path="./log/chromedriver.log")
		self.myDriver.get(aDirections)

	def DriveAwayFromFacebook(self):
		self.myDriver.quit()

	def GetFacebookKey(self):
		return self.myDriver




