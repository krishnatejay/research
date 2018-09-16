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
"priority": 1234,
"match":{
   "nw_src" : "10.0.1.0/24",
      "nw_dst" : "1.1.1.1"
       },
       "actions":[{"type": "SET_NW_DST", "nw_dst": "10.0.3.101"}]
   }'


curl -X POST -i http://localhost:8080/stats/flowentry/add --data '{
"dpid": 64,
"idle_timeout" : 1030,
"hard_timeout" : 1030,
"priority": 1111,
"match":{
   "ipv4_src" : "10.0.1.0/24",
   "tcp_dst" : 80,
   "nw_dst" : "1.1.1.1"
 },
"actions":[    {
        "type": "SET_FIELD",
        "field": "ipv4_dst",   
        "value": "10.0.3.101"         
    }]
}'

curl -X POST -i http://localhost:8080/stats/flowentry/add --data '{
"dpid": 64,
"idle_timeout" : 1030,
"hard_timeout" : 1030,
"priority": 1111,
"match":{
   "ipv4_src" : "10.0.3.101",
   "tcp_src" : 80,
   "nw_dst" : "10.0.1.0/24"
 },
"actions":[    {
        "type": "SET_FIELD",
        "field": "ipv4_src",   
        "value": "1.1.1.1"         
    }]
}'


