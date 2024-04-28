#!/bin/bash
# Description: This script performs multiple.
# Author: Lincon Freitas


# Define the DNS server address
DNS_SERVER="192.168.178.22"
DNS_PORT="53"

# Domain to query
DOMAIN="amazon.com"

# Loop to execute dig commands concurrently
for i in seq{1..3}; do
  dig @$DNS_SERVER -p $DNS_PORT $DOMAIN +time=1 +tcp &
  dig @$DNS_SERVER -p $DNS_PORT $DOMAIN +time=1 &
done

# Wait for all background jobs to finish
wait
echo "All DNS queries completed."
