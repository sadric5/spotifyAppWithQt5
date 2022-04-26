
from .credentials import *
from mysql import connector
import time

## Set up my own database system
## Will be remore

my_db = connector.connect (
	user = USERNAME,
	password = PASSWORD,
	host = HOST,
	database = DATABASE
)

mycursor = my_db.cursor()
def token_In_database(data):	
	sql = """ 
                INSERT INTO token (access_token, scope, expires_in, refresh_token) values ("{}", "{}", {}, "{}")
        """.format(data["access_token"], data["scope"], int(time.time())+data["expires_in"], data["refresh_token"])
	
	mycursor.execute(sql)
	my_db.commit()

def update_token(data):
	sql = """ 
                UPDATE token 
				SET access_token="{}", expires_in={}
				where scope="{}"
        """.format(data["access_token"], int(time.time())+data["expires_in"], data["scope"])
	mycursor.execute(sql)
	my_db.commit()

def fetch_token(id):
	sql = """
			SELECT access_token, scope, expires_in, refresh_token FROM token WHERE id={}
			""".format(id)
	mycursor.execute(sql)
	return mycursor.fetchone()