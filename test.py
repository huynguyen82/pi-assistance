# encoding: utf-8
import logging
import time
from threading import Thread, Event
from respeaker import Microphone
from pixels import Pixels, pixels
from google_home_led_pattern import GoogleHomeLedPattern
import requests
import json
import os
import random

##########
url = 'https://slp.bigdata.vin/client/dynamic/recognize'
headers = {'content-type': 'audio/x-raw-int; rate=16000'}

url2 = 'https://slp.bigdata.vin/tts/synthesize'
host='https://slp.bigdata.vin'
headers2 = {'content-type': 'application/json'}
msg='{"texts":"anh huy oi"}'

##
def playtts(msg):
    pixels.think()
    print('Sending to server ....')
    r = requests.post(url2, json=msg,  headers=headers2)
    pixels.off()
    links = json.loads(r.text)['message']
    if links:
        for link in links:
            if len(link)>0:
                link = host + link
                os.system('mplayer -volume 100 ' + link)
    
def send_raw(datain):
    r = requests.post(url,data=datain, headers=headers)
    return r.text

def task(quit_event):
    mic = Microphone(quit_event=quit_event)
    while not quit_event.is_set():
        pixels.off()
        print("Waiting for wakeup word!")
        if mic.wakeup(['sen ơi','senoi','maioi','mai ơi']):                        
            print('waked up')
            f_wav=random.randint(1,8)
            mic.stop()
            os.system('aplay /dev/shm/waves/' + str(f_wav)+'.wav')           
            print("Speaking something ...")
            data=mic.listen(duration=6, timeout=1.5)
            mic.stop()
            out=json.loads(send_raw(data))
            trans=out['hypotheses'][0]['utterance'].encode('utf-8')
            print('Recognized output: ' + trans)
            if len(trans)>0:
                try:
                    jmsg=json.loads(msg)
                    jmsg['texts']=trans
                    playtts(jmsg)
                except:
                    print("TTS has some problem")

def main():
    
    os.system('cp -rf waves /dev/shm/')    
    logging.basicConfig(level=logging.DEBUG)
    quit_event = Event()
    thread = Thread(target=task, args=(quit_event,))
    thread.daemon = True
    thread.start()
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print('Quit')
            quit_event.set()
            break
    time.sleep(1)

if __name__ == '__main__':
    main()
