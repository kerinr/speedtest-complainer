#!/usr/bin/python3
import os
import sys
import csv
import datetime
import time
import mysql.connector
import twitter
import config
 
def test():
 
        #run speedtest-cli
        print('running test')
        a = os.popen("python {speedtest}/speedtest-cli --simple".format(speedtest=config.speedtest_location)).read()
        print('ran')
        #split the 3 line result (ping,down,up)
        lines = a.split('\n')
        print(a)
        ts = int(time.time())
        date =datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        #if speedtest could not connect set the speeds to 0
        if "Cannot" in a:
                p = 100
                d = 0
                u = 0
        #extract the values for ping down and up values
        else:
                p = lines[0][6:11]
                d = lines[1][10:14]
                u = lines[2][8:12]
        print(date,p, d, u)
        
        if config.logging == 2:
        	#save the data to file for local network plotting
        	out_file = open('{}' .format(config.csv_file), 'a')
        	writer = csv.writer(out_file)
        	writer.writerow((ts,p,d,u))
        	out_file.close()
        elif config.logging == 1:
        	#save the data to a mysql database
        	try:
        		db = mysql.connector.connect(**config.mysql)
        		curs = db.cursor()
        	except mysql.connector.Error as err:
        			with open('{}' .format(config.error_file), 'a') as error_file:
        				error_file.write("{date}: Error Occured during MySQL connection: {error}\n" .format(date=date, error=err))
        				error_file.close()
        			print("Something went wrong: {}".format(err))
        	try:
        		curs.execute("INSERT INTO speedtest (date, ping, download, upload) VALUES ('{}', '{}', '{}', '{}')" .format(date, p, d, u))
        		db.commit()
        		print("Data committed")
        		curs.close()
        		db.close()
        	except Exception as commit_err:
        		with open('{}' .format(config.error_file), 'a') as error_file:
        			error_file.write("{date}: Error Occured during database insert: {error}. The database is being rolled back\n" .format(date=date, error=commit_err))
        			error_file.close()
        		print("Error: the database is being rolled back")
        		db.rollback()
        
        def determine_alert(download, sold, threshold):
        	""" We use this to check download speeds against the sold:threshold value to determine if we send a tweet"""
        	if download <= (sold * threshold):
        		return True
        	else:
        		return False  
        alert = determine_alert(float(d), config.speed_promised, config.warning_threshold)    	
        			
        if config.twitter_enabled:
		#connect to twitter
        	my_auth = twitter.OAuth(**config.twitter)
        	twit = twitter.Twitter(auth=my_auth)
 
        # tweet if down speed is less than whatever I set
        if alert:
        		print("trying to tweet")
        		try:
        			tweet="Hey @Comcast why is my internet speed {:.0f} down\\{:.0f} up when I pay for 80 down\\10 up in Santa Rosa CA? @ComcastCares @xfinity #comcast #speedtest" .format(float(d), float(u))
        			twit.statuses.update(status=tweet)
        		except Exception as e:
        			with open('{}' .format(config.error_file), 'a') as error_file:
        				error_file.write("{date}: Error Occured when trying to tweet: {error}\n" .format(date=date, error=e))
        				error_file.close()
        			print ("Error Occured:  ", e)
        			pass
        return
       
if __name__ == '__main__':
        test()
        print('completed')