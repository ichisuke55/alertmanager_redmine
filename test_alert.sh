#!/bin/bash

name=$RANDOM
url='http://localhost:9093/api/v1/alerts'

echo "firing up alert $name" 

# change url o
curl -XPOST $url -d "[{ 
	\"status\": \"firing\",
	\"labels\": {
		\"alertname\": \"ChangeBgpPeerState\",
		\"service\": \"my-service\",
		\"severity\":\"warning\",
		\"instance\": \"$name.example.net\"
	},
	\"annotations\": {
		\"summary\": \"Test alert!!!!\"
	},
	\"generatorURL\": \"http://prometheus.int.example.net/<generating_expression>\"
}]"

echo ""

echo "press enter to resolve alert"
read

echo "sending resolve"
curl -XPOST $url -d "[{ 
	\"status\": \"resolved\",
	\"labels\": {
		\"alertname\": \"ChangeBgpPeerState\",
		\"service\": \"my-service\",
		\"severity\":\"warning\",
		\"instance\": \"$name.example.net\"
	},
	\"annotations\": {
		\"summary\": \"Test alert!!!!\"
	},
	\"generatorURL\": \"http://prometheus.int.example.net/<generating_expression>\"
}]"

echo ""

