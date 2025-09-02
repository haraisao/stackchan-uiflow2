import os
import sys
import json

from machine import Pin,SDCard
from hardware import sdcard
import network

def reload(mod):
    mod_name = mod.__name__
    del sys.modules[mod_name]
    return __import__(mod_name)

def del_mod(mod):
    try:
        del sys.modules[mod.__name__]
    except:
        print("No such module". mod.__name__)
    return

def load_conf(fname):
    with open(fname, "r") as f:
        conts = f.read()
    keys=conts.split("\n")
    res={}
    for x in keys:
        k,v = x.split("=")
        res[k]=v
    return res

def get_file_contents(fname):
    with open(fname, "r") as f:
        conts = f.read()
    return conts

def mount_sd():
    if "sd" in os.listdir("/"):
        return
    sdcard.SDCard(slot=3, width=1, miso=35, mosi=37, sck=36, cs=4)
    return

def mount_sd_old():
    if "sd" in os.listdir("/"):
        return
    sd=SDCard(slot=2, width=1, miso=Pin(35), mosi=Pin(37), sck=Pin(36), cs=Pin(4))
    os.mount(sd, "/sd")
    return

def get_wlan_conf():
    mount_sd()
    try:
        return json.loads(get_file_contents("/sd/wlan.json"))
    except:
        return None

def setup_wlan(apoint="Home", passwd="", n=3):
    mount_sd()
    apoint_ = apoint
    passwd_ = passwd
    try:
        wlan_conf=json.loads(get_file_contents("/sd/wlan.json"))
        if apoint in wlan_conf:
            apoint_ = wlan_conf[apoint]["essid"]
            passwd_ = wlan_conf[apoint]["passwd"]
    except:
        pass
        
    wlan=network.WLAN(network.STA_IF)
    wlan.config(reconnects=n)
    print("Connect:", apoint_, passwd_)
    try:
        wlan.connect(apoint_, passwd_)
    except:
        pass
    return wlan

def connect_wlan(wlan=None,apoints=["Home", "Work", "Mobile"], retry=3):
    conf = get_wlan_conf()
    if wlan is None:
        wlan=network.WLAN(network.STA_IF)
    wlan.config(reconnects=retry)
    aps_ = scan_wlan(wlan)

    for name in apoints:
        if conf[name]['essid'] in aps_:
            try:
                wlan.connect(conf[name]['essid'], conf[name]['passwd'])
                if wlan.isconnected():
                    print(wlan.ifconfig())
                    return wlan
            except:
                pass
    print("Fail to connect wlan")
    return None

def scan_wlan(wlan=None):
    if wlan is None:
        wlan=network.WLAN(network.STA_IF)
        wlan.config(reconnects=3)
    aps_=wlan.scan()
    return [x[0].decode() for x in aps_]
