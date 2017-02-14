import os

def shape_traffic(upload_bw, download_bw):
    # Make sure txqueuelen is nonzero for Wondershaper
    # TODO find better values than 1000 1000?
    os.system("sudo ifconfig docker0 1000 1000")

    os.system("sudo wondershaper docker0 " + str(download_bw) + " " + str(upload_bw))
