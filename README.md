# Auto Updater for QBitTorrent listen port in Gluetun

This docker container will check every 5 minutes the Gluetun forwarded port in the control server, comparing it with the current port in QBitTorrent and changing it 

## Setup

The script can be set up as a cron task in a server, or by running the docker container.

```bash
docker build -t gluetun-torrent-autoport .
docker run --rm -e GLUETUN_ADDRESS='<URL of GLUETUN>' -e TORRENT_ADDRESS='<URL of Torrent>' -e TORRENT_USER='<torrent user>' -e TORRENT_PASSWORD='<Torrent password>' gluetun-torrent-autoport
```

