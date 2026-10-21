# Developed as a way to improve my skills
# - ant<3
import requests, re, os

class freemcserver():
	global auth, id, header
	
	def __init__(self, serverid):
		global auth, id, header
		
		# get needed info for the request
		id = serverid
		
		if not os.path.exists("cookie.txt"):
			cookie = input("cookie: ").replace("\n", "")
			with open("cookie.txt", "w") as file:
				file.write(cookie)
				
		with open("cookie.txt", "r") as file:
			cookie = file.read()
		
		header = {"user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Mobile Safari/537.36 Edg/140.0.0.0",
            "cookie": cookie
        }
        
        # request panel to get auth and metrics
        req = requests.get(f"https://panel.freemcserver.net/server/{id}/console", headers=header).text
        
        if req.find("currently expired") > -1:
        	raise Exception("Renew your server first!")
        	
        print(req)
        
        # set up needed auth
        auth = {
        	"authorization": found_auth,
        	"x-fmcs-metrics-wfkpe9eata": found_metrics,
        }
        
        
	class user():
		global name
		
		def __init__(self, user):
			name = user