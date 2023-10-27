import sys
import requests
import json
import os

gluetun_addr = os.environ.get('GLUETUN_ADDRESS', "http://localhost:8000")
torrent_addr = os.environ.get('TORRENT_ADDRESS', "http://localhost:8080")
torrent_user = os.environ.get('TORRENT_USER', "admin")
torrent_password = os.environ.get('TORRENT_PASSWORD', "adminadmin")

print(f"Expecting Gluetun at {gluetun_addr}")
print(f"Expecting Torrent at {torrent_addr}")

port_forwarded_path = "/v1/openvpn/portforwarded"

gluetun_req = requests.get(gluetun_addr + port_forwarded_path)

if gluetun_req.status_code != 200:
    print("Gluetun request failed, sleeping...")
    sys.exit(1)

forwarded_port = json.loads(gluetun_req.text)["port"]

print(f"Gluetun is forwarding port {forwarded_port}")




login_method = "/api/v2/auth/login"
pref_method = "/api/v2/app/preferences"
set_pref_path = "/api/v2/app/setPreferences"

torrent_session = requests.Session()
torrent_login = torrent_session.post(torrent_addr + login_method, data={"username": torrent_user,
                                                                        "password": torrent_password},
                                     headers={"Referer": torrent_addr})
if torrent_login.status_code != 200 and torrent_login.text != "Ok.":
    print("Torrent login failed, check the credentials")
    sys.exit(1)

print("Login successful")

preferences = torrent_session.get(torrent_addr + pref_method)

if preferences.status_code != 200:
    print("Preferences request failed")
    sys.exit(1)

print("Retrieved torrent preferences")

pref_dict = json.loads(preferences.text)
listen_port = pref_dict["listen_port"]
print(f"Torrent is listening in port {listen_port}")

if forwarded_port == listen_port:
    print("Port configuration OK, sleeping...")
    sys.exit(0)

else:
    print("Ports are different, changing config in torrent...")
    prefs_changed = {"listen_port": forwarded_port}
    req_body = json.dumps(prefs_changed)
    torrent_changing_prefs = torrent_session.post(torrent_addr + set_pref_path, data={"json": req_body})
    if torrent_changing_prefs.status_code != 200:
        print("Preferences changing failed")
        sys.exit(1)
    print(f"Ports changed to {forwarded_port}")
    sys.exit(0)
