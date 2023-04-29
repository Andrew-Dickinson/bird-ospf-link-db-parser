#!/bin/bash

export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin"
export TIMESTAMP=$(date +%s)
birdc show ospf state | parse-bird-link-db - | tail -1 | sed "s/$/ {\"updated\": $TIMESTAMP}/" | jq -s add -c > /var/www/html/api/v1/mesh_ospf_data.json


