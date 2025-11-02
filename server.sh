#!/bin/sh
microsocks -p 1080 1>/dev/null 2>/dev/null &

while true; do
  ip=$(ip -4 addr show wlan0 | awk '/inet /{print $2}' | cut -d/ -f1)
  echo -n "$ip" | nc -b -u -w 1 255.255.255.255 45454
  sleep 1
done
