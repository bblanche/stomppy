from flask import Flask, url_for, request, flash, render_template, redirect
import time
import os
import stomp


user = os.getenv("ACTIVEMQ_USER") or "admin"
password = os.getenv("ACTIVEMQ_PASSWORD") or "admin"
host ="localhost"
port = os.getenv("ACTIVEMQ_PORT") or 61613
conn = stomp.Connection(host_and_ports = [(host, port)])
  
sms2 = ''
i = 0

app = Flask(__name__)

class MyListener(object):
        sms=''

        def __init__(self, conn):
            self.conn = conn
            self.count = 0
            self.start = time.time()
        

        def on_error(self, message):
            print('received an error %s' % message.body)

        def on_message(self, message):
            global sms2
            global i

            MyListener.sms=str(message.body)
            sms2 += str(message.body)+"\n"

            print (message.body)
            print("received")
       


@app.route('/', methods=['GET'])
def client():
    return render_template('client.html')

#@app.route('/deconnexion', methods=('GET', 'POST'))
#def deconnexion():
 #   conn.disconnect()
  #  global sms2
   # sms2=''
    #return render_template('deconnexion.html')

@app.route('/deconnexion', methods=('GET', 'POST'))
def deconnexion():
    conn.disconnect()
    global i
    i=0
    global sms2
    sms2=''
    return render_template('client.html', disconnect="succesfully disconnected")


@app.route('/discussion/sms2', methods = ['GET'])


def getMessage():
    global sms2

    return sms2

@app.route('/discussion',methods = ['POST'])
def discussion():
    result=request.form
    pseudo = result['pseudo']
    groupe = result['groupe']
    msg = result['monmessage']

    global i
    i=i+1
    if (i<=1):
        listener=MyListener(conn)

        conn.set_listener(pseudo, listener)
        conn.connect(login=user,passcode=password, headers = {'client-id': pseudo})

        conn.subscribe(destination=groupe, id=1, ack='auto')
    
    if msg!="":
        conn.send(body=msg, destination=groupe, wait='false')

   
    
    return render_template("discussion.html", pseudo=pseudo, groupe=groupe)


        


if __name__ == '__main__':
    app.run(debug=True)


#!/usr/bin/env python
# ------------------------------------------------------------------------
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------
 
