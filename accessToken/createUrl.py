from django.shortcuts import redirect
from .credentials import *
import hashlib

response_type = "code"
redirect_url = "http://localhost:8000/callback"
state = ''
scope = "user-read-email user-read-playback-state user-modify-playback-state"
url = "https://accounts.spotify.com/authorize?"
state = hashlib.sha256("spotify King".encode()).hexdigest()
# print(state)
payload = {
    "client_id" : client_id,
    "response_type": response_type,
    "redirect_uri": redirect_url,
    "scope": scope,
    "state" : state,
    
}





