#!/usr/bin/env python3

from RosAPI3 import Core
from datetime import datetime, timedelta

### 
### Runs the script (commandos='') on the Mikrotik with delayed 2s to start by using scheduler
###

def run_script(ip, inUser='', inPass='', commandos=''):
  tik = Core(ip, DEBUG=False)
  tik.login(inUser, inPass)
  API_zapros = tik.response_handler(tik.talk(["/system/scheduler/print", "?name=ch_fr_script",]))
  for API_result in API_zapros:
      if API_result[".id"]:
          tik.response_handler(tik.talk(["/system/scheduler/remove", "=.id=" + API_result[".id"],]))            
  API_zapros = tik.response_handler(tik.talk(["/system/clock/print", ]))
  for API_result in API_zapros:
      my_on_time = datetime.strptime("{} {}".format(API_result["date"],API_result["time"]), "%b/%d/%Y %H:%M:%S") + timedelta(seconds=2)
  tik.response_handler(tik.talk(["/system/scheduler/add", "=interval=0s", 
          "=start-date=" + my_on_time.strftime("%b/%d/%Y"), "=start-time=" + my_on_time.strftime("%H:%M:%S"),
          "=name=ch_fr_script", "=on-event=" + " /system scheduler remove [ find name=ch_fr_script ];" + commandos]))
          
###
### Set new scan-list Frequensy on interface wlan1 by run_script()
###

def SetNewFreqByScript(ip, newFreq):
    wirInterface = 'wlan1'
    command = "/interface wireless set [find default-name={}] scan-list={}".format(wirInterface, newFreq)
    run_script(ip, 'login', 'password', command)     

###
### Set new scan-list Frequensy on interface wlan1
###

def SetNewFreqByScript(ip, newFreq):
    tik = Core(ip, DEBUG=False)
    tik.login('login', 'password')
    API_zapros = tik.response_handler(tik.talk(["/interface/wireless/print", "?default-name=wlan1", ]))
    for API_result in API_zapros:
        frequency_list = API_result["frequency"]
        tik.response_handler(tik.talk(["/interface/wireless/set", "=.id=" + API_result[".id"], "=frequency={}".format(newFreq),  ]))   
       
run_script('192.168.88.1', inUser='login', inPass='password', commandos='/ip address set [find name=earth1] address=192.168.88.2/24')
