#! /bin/bash

for tweetsFile in /data/Twitter\ dataset/geoTwitter20-*; do
    echo "Running map.py on $tweetsFile"

    nohup ./src/map.py --input_path="$tweetsFile" &
done
