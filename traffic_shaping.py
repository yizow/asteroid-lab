import os

def shape_traffic(upload_bw, download_bw):
    # Make sure txqueuelen is nonzero for Wondershaper
    # TODO find better values than 1000?
    os.system("sudo ifconfig docker0 txqueuelen 1000")

    os.system("sudo wondershaper docker0 " + str(download_bw) + " " + str(upload_bw))

def reset():
    os.system("sudo wondershaper clear docker0")