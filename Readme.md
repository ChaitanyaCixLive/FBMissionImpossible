Welcome to Mission Impossible.
-----------------------------

This project aims to mine the sacred data hidden inside the secret walls of Facebook under the group named "മികച്ച അന്താരാഷ്‌ട്ര സിനിമകൾ" which is based on an exotic language named Malayalam spoken in the backwaters of a tiny warm tropical region called Kerala. Ethan set up a team with his old pals Franz and Luther to steal the data. He could login with the secret data supplied by Luther which is stored in an ultra secure ini file. Franz supplies the necessary tools and transportation which is based on Selenium automation driver for python. Ethan navigates the Facebook facility with a html/javascript component which works with the Facebook graph API.

The stolen data will then be passed over to Eugene and he will tear open the json file, will pick up the posts, comments and likes and will insert them to his secrete mysql server based movie database. Unfortunately the posts themselves don't contain any information which indicates which movie they are describing. This is a job later should be done by those who sets up the Mission manually.



To Set up the Mission yourself
------------------------------

=> Preconditions:

- Ubuntu or compatible linux is set up
- Mysql server is installed
- Preferrably mysql workbench installed. It might be handy
- The necessary python packages are installed. Some packages will need additional ubuntu packages, such as gcc to be present. So install them also.

=> Steps to install:

- Download the files to a local folder. 
- Create a two more sub-folders in this folder named 'data' and 'log'. 
- Import the MovieImport.sql to mysql server using your database login. 
- Update the LutherStickell.ini with the database connection details.

- Host the folder MovieForumFBAPI in some webserver (e.g google drive) and make sure that this can be publicly accessible. 
- Test with your chrome browser that you can manually open this URL and download the facebook data.
- Facebook API will need your permission to read the data. So, provide that when asked.

- Configure LutherStickell.ini with facebook access details.
- The password is bit tricky. Generate the encrypted password with the tool GenerateEncryptedPassword.py and keep this in the ini file. 
	However, remember that this is a very weak security mechanism and this should be used only to prevent any over the shoulder attacks.

=> Working with the set-up:

Now you should be able to run the MissionImpossible.sh successfully. If everything is OK, it will download the datafile after connecting to facebook and import the data to the database.
Check the movie database in mysql workbench for the data.
It doesn't fill in the movie names automatically. You need to read the post and enter the movie details in the movie table using mysql workbench. 
Then use the MovieEditTask.sh to link the newly inserted movie id to each post.

A backup utility is provided as BackupDB.sh. Ensure that the database connection details are correct here. Schedule this script with a cron job to run this automatically every day.
