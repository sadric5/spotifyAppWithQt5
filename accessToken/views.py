from datetime import date
from turtle import ht
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .createUrl import *
import requests, base64
from .stored_token import *
# Create your views here.

auth = base64.b64encode("{}:{}".format(client_id, clinet_secret).encode())
header ={
            "Authorization" : "Basic {}".format(auth.decode()),
            "Content-Type": "application/x-www-form-urlencoded"
        } 

def token(code, stateReturn):
    if stateReturn == state:
        # print("Nice the state  match!")
        body = {
            "grant_type" : "authorization_code",
            "code" : code,
            "redirect_uri" : "http://localhost:8000/callback",
        }

        # print(auth.decode())
        req = requests.post("https://accounts.spotify.com/api/token", headers=header, data=body)

        if req.ok:
            token_In_database(req.json())
        else:
            with open("test.txt", 'w') as f:
                f.write("{} \n".format(req.status_code))
                f.write("{} \n".format(req.json()))


    else:
        with open("test.txt", 'w') as f:
                f.write("{} \n".format("Sorry, The state do not match the provided one."))

def refreshToken(old_refreshtoken):
    body = {
        "grant_type" : "refresh_token",
        "refresh_token" : old_refreshtoken,
    }
    req = requests.post("https://accounts.spotify.com/api/token", headers=header, data=body)
    if req.ok:
        update_token(req.json())
    else:
        print("Can not get the refresh token.")
    


def getToken(request):
    try:
        token(request.GET['code'], request.GET['state'])
    except:
        pass
    
    return render(request, "index.html", {'name': "Meacheal Miller"})

def requestToken(request):
    # url = 'https://accounts.spotify.com/authorize?'
    # url = "callback"
    spotify_url = requests.request("GET", url=url, params=payload)
    return redirect(spotify_url.url)

##start making request to spotify API endPoint

def getEmail(request):
    data = fetch_token(10)
    instanceTime = int(time.time())
    if instanceTime > data[2]:
        refreshToken(data[3])
        data = fetch_token(5)
    hds = {
        "Authorization": "Bearer {}".format(data[0]),
   
    }
    print(hds)

    url = "https://api.spotify.com/v1/me/playlists"
    req = requests.get(url, headers=hds)
    if req.ok:
        return HttpResponse((req))
    else:
        return HttpResponse("<h3> Sorry something went wrong {}</h3>".format(req.json()))