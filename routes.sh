curl -X POST -d '{"address": "10.0.1.1/24"}' http://localhost:8080/router/0000000000000040
curl -X POST -d '{"address": "10.0.2.1/24"}' http://localhost:8080/router/0000000000000040
curl -X POST -d '{"address": "10.0.2.2/24"}' http://localhost:8080/router/0000000000000050
curl -X POST -d '{"address": "10.0.3.1/24"}' http://localhost:8080/router/0000000000000050
curl -X POST -d '{"address": "10.0.4.1/24"}' http://localhost:8080/router/0000000000000050
curl -X POST -d '{"gateway": "10.0.2.2"}' http://localhost:8080/router/0000000000000040
curl -X POST -d '{"gateway": "10.0.2.1"}' http://localhost:8080/router/0000000000000050

curl -X POST -i http://localhost:8080/stats/flowentry/add --data '{
"dpid": 64,
"idle_timeout" : 10030,
"hard_timeout" : 10030,
"priority": 1113,
"match":{
   "ipv4_src" : "10.0.3.102/0.0.0.127",
   "ipv4_dst" : "10.0.1.101/0.0.0.127",
   "eth_type": 2048
 },
"actions":[    {
        "type": "SET_FIELD",
        "field": "ipv4_src",   
        "value": "1.1.1.1"         
    },
    {
        "type": "SET_FIELD",
        "field": "eth_dst",   
        "value": "00:00:00:00:00:c1"         
    },
    {
            "type":"OUTPUT",
            "port": 1
    }
]
}'

curl -X POST -i http://localhost:8080/stats/flowentry/add --data '{
"dpid": 64,
"idle_timeout" : 10030,
"hard_timeout" : 10030,
"priority": 1113,
"match":{
   "ipv4_dst" : "1.1.1.1",
   "ipv4_src" : "10.0.1.101/0.0.0.127",
   "eth_type": 2048
 },
"actions":[   
    {
        "type": "SET_FIELD",
        "field": "ipv4_dst",   
        "value": "10.0.3.102"         
    },
    {
        "type": "SET_FIELD",
        "field": "eth_dst",   
        "value": "00:00:00:00:00:b2"         
    },
    {
            "type":"OUTPUT",
            "port": 2
    }
]
}'

c1 iptables -A OUTPUT -p tcp --tcp-flags RST RST -d 1.1.1.1 -j DROP
//This should be ran on both c1 and c2 for httpRequests from scappy to
//work
