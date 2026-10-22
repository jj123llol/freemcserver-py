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
		
		if req.find("currently expired") > -1 or req.find("website is using a security service") > -1:
			raise Exception("Server not renewed, or blocked by cloudflare.")
        	
		
		found_metrics = re.search('^window\.fmcs\.metrics = "([A-Za-z0-9]+)";$', req)
		if not found_metrics:
			raise Exception("Failed to find metrics. Try again?")

		found_metrics = found_metrics.group(1)

		found_auth = re.search('^window\.fmcs\.api_key="([. A-Za-z0-9]+)";$', req)
		if not found_auth:
			raise Exception("Failed to find auth. Try again?")

		found_auth = found_auth.group(1)
        
        # set up needed auth
		auth = {
        	"authorization": found_auth,
        	"x-fmcs-metrics-wfkpe9eata": found_metrics,
        }
        

	class server():

		def GetPlayers(self):
			req = requests.get(f"https://api.freemcserver.net/v4/server/{id}/ping", headers=auth).json()
			if not req.get("success"):
				print("Failed to get players", req.get("error"))
				return []

			users = []
			for user in req.get("players", []):
				users.append(freemcserver.user(user))

			return users

	class user():
		def __init__(self, user):
			self.user = user

		def kill(self):
			freemcserver.console().write(f"kill {self.user}")

	class console():

		def write(self, text):
			req = requests.post(f'https://api.freemcserver.net/v4/server/{id}/command', headers=auth, json={'command': text}).json()
			
			if not req.get("success"):
				print("Failed to write to console", req.get("error"))
				return

		def read(self, limit):
			limit = limit or 200
			req = requests.get(f"https://api.freemcserver.net/v4/server/{id}/logs?lines={limit}", headers=auth).json()
			if not req.get("success"):
				print("Failed to read console", req.get("error"))
				return

			return req.get("log")
