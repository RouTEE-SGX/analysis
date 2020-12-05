## Check IP address

```ifconfig``` or ``ip addr```

## Set nerwork delay

### New
```
$ sudo tc qdisc add dev eno1 root netem delay 90ms 10ms distribution normal
```

### Change
```
$ sudo tc qdisc change dev eno1 root netem delay 90ms 10ms distribution normal
```

### Delete
```
$ sudo tc qdisc del dev eno1 root
```

## Check RTT
```
$ ping <server_ip> -c 20
```

## Check B/W
```
$ iperf3 -c <server_ip> -f m -p 8327
```

Require running ```iperf3 -s -f m -p 8327``` at server side first.
