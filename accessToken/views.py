
from datetime import date
from mimetypes import init
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .createUrl import *
import requests, base64
from .stored_token import *
import logging, json

logging.basicConfig(filename="file.log", format="%(asctime)s %(pathname)s: %(message)s", filemode="a")


log = logging.getLogger()
log.setLevel(logging.DEBUG)

# Create your views here.

auth = base64.b64encode("{}:{}".format(client_id, clinet_secret).encode())
header ={
            "Authorization" : "Basic {}".format(auth.decode()),
            "Content-Type": "application/x-www-form-urlencoded"
        } 

def token(code, stateReturn):
    if stateReturn == state:
      
        body = {
            "grant_type" : "authorization_code",
            "code" : code,
            "redirect_uri" : "http://localhost:8000/callback",
        }

        req = requests.post("https://accounts.spotify.com/api/token", headers=header, data=body)

        if req.ok:
            token_In_database(req.json())
        else:
            log.debug(" Status: {} \n Error:{} \n".format(req.status_code, req.json()))


    else:
        log.debug("{} \n".format("Sorry, The state do not match the provided one."))

def refreshToken(old_refreshtoken):
    body = {
        "grant_type" : "refresh_token",
        "refresh_token" : old_refreshtoken,
    }
    req = requests.post("https://accounts.spotify.com/api/token", headers=header, data=body)
    if req.ok:
        update_token(req.json())
        log.debug("Everything is working as expected")
    else:
        log.debug("Can not get the refresh token. {}".format(req.json()))
    

def getToken(request):
    try:
        token(request.GET['code'], request.GET['state'])
    except:
        log.debug("Not requesting the token")
    
    return render(request, "index.html", {'name': "Meacheal Miller"})

def requestToken(request):
    spotify_url = requests.request("GET", url=url, params=payload)
    return redirect(spotify_url.url)

##start making request to spotify API endPoint
def getRightToken(id:int)->tuple:
    data = fetch_token(id)
    instanceTime = int(time.time())
    if instanceTime > data[2]:
        refreshToken(data[3])
        data = fetch_token(id)
    return data

def getEmail(request):
    data = getRightToken(13)
    hds = {
        "Authorization": "Bearer {}".format(data[0]),
    }
    
    url = "https://api.spotify.com/v1/me/player"

    body = {
        
        "device_ids": [""],
        "play": True,
    }

    req = requests.put(url, headers=hds, data=json.dumps(body))
    

    if req.ok:
        return HttpResponse(req)
    else:
        return HttpResponse("<h3> Sorry something went wrong {}</h3>".format(req.json()))


def getAvailableDevices(request):
    data = getRightToken(13)

    hds = {
        "Authorization": "Bearer {}".format(data[0]), 
    }
    url = "https://api.spotify.com/v1/me/player/devices"
    req = requests.get(url, headers=hds)

    if req.ok:
        return HttpResponse(req)
    else:
        return HttpResponse("Sorry something went wrong {}".format(req.json()))

def transfersPlayToOtherDevices(id:str)->str:
    data = getRightToken(13)
    hds = {
        "Authorization": "Bearer {}".format(data[0]),
    }
    
    url = "https://api.spotify.com/v1/me/player"

    body = {
        
        "device_ids": ["".format(id)],
        "play": True,
    }

    req = requests.put(url, headers=hds, data=json.dumps(body))
    if req.ok:
        return True
    else:
        return False

