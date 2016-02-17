# Configuration Variables

speed_promised = 25 # Speed paid for
warning_threshold = 0.4 # Percentage of speed_promised that you wish to alert on when results equal or are below.  
logging = 1  # 0 for no logging.  1 for MySQL.  2 for CSV
twitter_enabled = False # Determine via True/False Boolean if we're going to send tweets or just capture data
speedtest_location = '/home/python_projects/speed'
csv_file = '/home/pi/speedtest_complainer/data.csv'
error_file = '/home/pi/speedtest_complainer/error.log'

mysql = dict(
	host = '127.0.0.1',
	user = 'username',
	password = 'password',
	database = 'database',
)	

twitter = dict(
	token = '',
    consumer_key = '',
	token_secret = '',
	consumer_secret = ''
)
