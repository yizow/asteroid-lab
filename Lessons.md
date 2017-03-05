# Lessons learned

## Traffic shaping

**Lessons learned:** Knowledge of Linux networking and terminology is helpful if you want to really understand the quirks of Docker networking. The solution to your problem may be simpler than you expect. 

**Problem:** We tried to use Wondershaper to throtle the bandwidth of our Docker containers, but if we used this tool to set *any* limit on the bandwidth, no matter how high, the traffic going in/out of the containers would eventually fall to 0.

**Attempted solutions:** Using a different OS, using other traffic-shaping tools (not helpful as most of them are based on the same `tc` and `qdisc` technology)

**Solution:** Was staring us in the face whenever we ran `ifconfig`. Wondershaper relied on the `txqueuelen` value of the `docker0` bridge, as suggested by [this GitHub issue](https://github.com/kubernetes/kubernetes/issues/25092) for Kubernetes:

> It seems the *fifo qdiscs default their packet limit to the txquelen of the interface (man tc-pfifo). It also seems most virtual interface types (bridge, etc) set a dev->tx_queue_len of 0. It further seems that pkg/util/bandwidth/linux.go relies on the default packet limit...

The value was `0` by default, so Wondershaper would end up dropping all packets. Easily fixed by running `sudo ifconfig docker0 txqueuelen <nonzero queue length>`

## Snort

**Lessons learned:** Adding `config daq-mode: inline` to a Snort rule file, or even specifying `--daq-mode inline` on the command line, is *not* equivalent to specifying `-Q`.

**Problem:** Snort wasn't reading any of the `drop` or `reject` rules we'd written in our rules file when we used the nfq daq, although we didn't realize this at first.

**Attempted solutions:** Proofreading the Snort file, adding `--daq-mode inline` on the command line

**Solutions:** Adding `-Q` to the call to Snort, via lucky guess.







