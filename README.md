# Speedtestcomplainer
A python app that will run a speedtest on your internet connection, store the results in a database or csv file and tweet a complaint to your ISP.  Designed and tested to run on a raspberry pi, but should run on any 'nix distro capable of supporting python3

Based on u/AlekseyP's original work in https://www.reddit.com/r/technology/comments/43fi39/i_set_up_my_raspberry_pi_to_automatically_tweet/

# Requirements

Needs the Python speedtest-cli found at https://pypi.python.org/pypi/speedtest-cli/

# Configuration

I've tried to make this script as flexible as possible sticking to give the user as much control as possible in how the script behaves. Configuration is handled in a basic config.py file.  Things that can be configured are:

##Script behavior settings:
- **speed_promised**: This is the speed _promised_ to you by your ISP.  If your package is 60mbit down simply enter `speed_promised = 60`.
- **warning_threshold**: Because we don't necessarily want to tweet if your speeds test slightly under what your were _promised_ we define a threshold percentage in decimal format.  To warn when your speeds are testing at or below 40% of what you expect define `warning_threshold = 0.4`.
- **logging**: There are three options for logging available _No Logging_, _Log to MYSQL Database_ and _Log to CSV_ . We use a numerical format to determine logging where `0` = No Logging, `1` = MySQL and `2` = CSV.
- **twitter_enabled**: This is a True/False Boolean to determine if we send tweets at all.  It defaults to True, however if you don't wish to send tweets and only want to capture data set `Twitter = False`.


##File location settings:
Define desired file locations for where your speedtest-cli is installed and where you wish your csv and error file logging to occur.  I.e. if your speedtest-cli is installed in /usr/local/bin set speedtest_location='/usr/local/bin/'

- **speedtest_location**: Set the absolute path to where speedtest-cli is installed on your system.  For example if it's in /usr/local/bin/speedtest-cli set `speedtest_location='/usr/local/bin'`
- **csv_file**: Determine where and what filename to log to csv file.  Typically in the homedir, but can be whereever you like.  Variable expects absolute path *and* filename _i.e._ `csv_file='/home/pi/speedtestcomplainer/speedtest_data.csv`.
- **error_file**: Determine where to log errors to.  Any errors will be output to the screen, but also to the `error_file` so automated run errors will be captured.   Variable expects absolute path *and* filename _i.e._ `error_file='/home/pi/speedtestcomplainer/error.log`.

##Credentials:
We store both MySQL connector settings and twitter oAuth2 credentials in a simple dictionary list.

```mysql = dict(
	host = '127.0.0.1',
	user = 'username',
	password = 'password',
	database = 'database',
)```	

```twitter = dict(
	token = '',
    consumer_key = '',
	token_secret = '',
	consumer_secret = ''
)```

### Tweet Details

On line 80 of the script edit the details in the `tweet` variable for your ISP and desired @mentions, hashtags and locations.  *Remember to keep the total length to no more than 140 char*.

### Cron Job
Currently the script must be called manually or via a cronjob.  On my pi I run it via cron every 15min

`*/15 * * * * /usr/bin/python3 /home/pi/speedtest_complainer/speedtestcomplainer.py > /dev/null 2>&1`