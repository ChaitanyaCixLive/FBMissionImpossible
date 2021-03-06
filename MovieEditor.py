import wx
import mysql.connector
import logging
from logging.handlers import RotatingFileHandler
from wx.lib.mixins.listctrl import TextEditMixin
import ConfigParser


class EditListCtrl(wx.ListCtrl, TextEditMixin):
	def __init__(self, parent, pos=wx.DefaultPosition,
		 size=wx.DefaultSize, style=0):
		wx.ListCtrl.__init__(self, parent, -1, pos, size, style)
		TextEditMixin.__init__(self) 


class MovieEditor(wx.Frame):
    
	def __init__(self, *args, **kwargs):
		super(MovieEditor, self).__init__(*args, **kwargs) 

		self.InitializeLogger()

		self.myConfig = ConfigParser.ConfigParser()
		self.myConfig.read("./LutherStickell.ini")
		self.myDB = mysql.connector.connect(user=self.myConfig.get("MovieConfig", "DBUser"), password=self.myConfig.get("MovieConfig", "DBPass"), host='127.0.0.1', database=self.myConfig.get("MovieConfig", "Database"),  use_unicode=True, charset='utf8')
	
		    
		self.InitUI()

	def __del__(self):
		self.myDB.close()

	def InitializeLogger(self):
		self.logger = logging.getLogger("MovieEditor")
		self.logger.setLevel(logging.INFO)

		formatter = logging.Formatter("%(asctime)s -11s %(levelname)-10s %(message)s")
		
		# Log to file
		filehandler = RotatingFileHandler("./log/MovieEditor.log", maxBytes=1000000, backupCount=5)
		filehandler.setLevel(logging.INFO)
		filehandler.setFormatter(formatter)
		self.logger.addHandler(filehandler)

	def RetrieveAllPostsForEditing(self):

		cursor = self.myDB.cursor()

		query = u"SELECT post.id, post.message, post.language, post_description.movie_id FROM post inner join post_description on post.id = post_description.post_id where post_description.movie_id is NULL and post.message  > '';"
		cursor.execute(query)

		return cursor.fetchall()

	def UpdatePost(self, aPostId_in, aLanguage_in, aMovieId_in):

		cursor = self.myDB.cursor()

		aCommit = False
		if aLanguage_in != "":
			self.logger.info("Updating language for post : %s",  aLanguage_in)
			cursor.execute(u"UPDATE post set language = %s where post.id = %s", (aLanguage_in, int(aPostId_in), ))
			aCommit = True

		if aMovieId_in != "":
			self.logger.info("Updating language for post : %s",  aMovieId_in)
			cursor.execute(u"UPDATE post_description set movie_id = %s where post_description.post_id = %s", (int(aMovieId_in),int(aPostId_in),))
			aCommit = True

		if aCommit:
			self.myDB.commit()
		

	def InitListCtrl(self):
		self.list = EditListCtrl(self.panel, size=(1100, 760), style=wx.LC_REPORT)
		
		self.list.InsertColumn(0, 'id', width=40)
		self.list.InsertColumn(1, 'message', width=900)
		self.list.InsertColumn(2, 'language', width=80)
		self.list.InsertColumn(3, 'movie_id', width=80)
		grid_2 = wx.GridSizer(1, 1, 0, 0)

		grid_2.Add(self.list)
		self.content_sizer.Add(grid_2, 4, wx.EXPAND | wx.ALL, 3)

   	def InitUI(self):    

		self.panel = wx.Panel(self)

		self.main_sizer = wx.BoxSizer(wx.VERTICAL)

		self.centred_text = wx.StaticText(self.panel, label="Edit Movies")
        	self.main_sizer.Add(self.centred_text, 0, wx.ALIGN_CENTRE | wx.ALL, 3)

		self.content_sizer = wx.BoxSizer(wx.HORIZONTAL)
		grid_1 = wx.GridSizer(2, 1, 0, 0)
		btn1 = wx.Button(self.panel, label='Get Empty Movie Posts')
		btn2 = wx.Button(self.panel, label='Save')
		grid_1.AddMany([btn1, btn2])
		self.content_sizer.Add(grid_1, 1, wx.EXPAND | wx.ALL, 3)

		self.main_sizer.Add(self.content_sizer, 1, wx.EXPAND)

		self.panel.SetSizer(self.main_sizer)

		btn1.Bind(wx.EVT_BUTTON, self.LoadPosts)
		btn2.Bind(wx.EVT_BUTTON, self.SavePosts)

		self.InitListCtrl()
		
		self.SetSize((1400, 800))
		self.SetTitle('Movie Editor')
		self.Centre()
		self.Show(True)

	def LoadPosts(self, event):
		
		anAllPosts = self.RetrieveAllPostsForEditing()
		
		self.list.DeleteAllItems()
		

		for aPost in anAllPosts:
			index = self.list.InsertStringItem(aPost[0], str(aPost[0]))
            		self.list.SetStringItem(index, 1, aPost[1].encode("utf-8"))
			self.list.SetStringItem(index, 2, str(aPost[2]))
			self.list.SetStringItem(index, 3, str(aPost[3]))
		
		self.main_sizer.Layout()

    	def SavePosts(self, event):
		count = self.list.GetItemCount()
		for row in range(count):
		    	aPostId = self.list.GetItem(itemId=row, col = 0)
			aLanguage = self.list.GetItem(itemId=row, col = 2)
			aMovieId = self.list.GetItem(itemId=row, col = 3)
			self.UpdatePost(aPostId.GetText(), aLanguage.GetText(), aMovieId.GetText())

    	
def main():
    
	ex = wx.App()
	MovieEditor(None)
	ex.MainLoop()    


if __name__ == '__main__':
    	main()
