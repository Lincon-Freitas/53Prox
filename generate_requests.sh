#!/bin/bash

# Description: This script performs multiple DNS queries against the 53Prox application.
# Author: Lincon Freitas

DNS_SERVER=`docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' 53prox`
DNS_PORT="53"

# Domain to query
DOMAIN="google.com"

# Loop to execute dig commands concurrently over TCP and UDP
for i in seq{1..3}; do
  dig @$DNS_SERVER -p $DNS_PORT $DOMAIN +time=1 +tcp &
  dig @$DNS_SERVER -p $DNS_PORT $DOMAIN +time=1 &
done

# Wait for all background jobs to finish
wait
echo "All DNS queries completed."
