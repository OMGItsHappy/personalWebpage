import requests as r
import constantsAndKeys as ck
import base64
import spotipy
"""

auth_response = r.post(ck.AUTH_URL + "/api/token", {
    'grant_type': 'client_credentials',
    'client_id': ck.spotifyClientId,
    'client_secret': ck.spotifyClientSecret,
})

auth_response = r.get(ck.AUTH_URL + "/authorize", 
{"client_id" : ck.spotifyClientId, 
"response_type" : "code", 
"redirect_uri" : ck.callBackURI, 
"scope" : "app-remote-control streaming"} )

stuff = ck.spotifyClientId + ":" + ck.spotifyClientSecret

stuff = base64.b64encode(stuff.encode("ascii")).decode("ascii")

print(stuff)

headers = {'Authorization': f'Basic {stuff}'}

auth_response = r.post(ck.AUTH_URL + "/api/token", {"grant_type" : "client_credentials"}, headers=headers)

a= auth_response.json()['access_token']

#print(auth_response.content)

authToken = auth_response.json()["access_token"]

header = {'Authorization': 'Bearer {token}'.format(token=)}

a = r.post(ck.spotifyBaseUrl + "/v1/me/player/queue", {"uri" : "spotify:track:4iV5W9uYEdYUVa79Axb7Rh"}, headers=header)

print(a.json())
"""