#!/usr/bin/env python3

# simpleircbot.py - A simple IRC-bot written in python
#
# Copyright (C) 2015 : Niklas Hempel - http://liq-urt.de
# Modified by mcen1 on github 2019
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import re
import socket
import cgi
from playsound import playsound
with open('config.txt','r') as inf:
    mydict = eval(inf.read())

HOST = str(mydict["host"])
PORT = int(mydict["port"])
CHAN = str(mydict["channel"])
NICK = str(mydict["username"])
PASS = str(mydict["oauth"])

def send_pong(msg):
    con.send(bytes('PONG %s\r\n' % msg, 'UTF-8'))


def send_message(chan, msg):
    con.send(bytes('PRIVMSG %s :%s\r\n' % (chan, msg), 'UTF-8'))


def send_nick(nick):
    con.send(bytes('NICK %s\r\n' % nick, 'UTF-8'))


def send_pass(password):
    con.send(bytes('PASS %s\r\n' % password, 'UTF-8'))


def join_channel(chan):
    con.send(bytes('JOIN %s\r\n' % chan, 'UTF-8'))


def part_channel(chan):
    con.send(bytes('PART %s\r\n' % chan, 'UTF-8'))
# --------------------------------------------- End Functions ------------------------------------------------------


# --------------------------------------------- Start Helper Functions ---------------------------------------------
def get_sender(msg):
    result = ""
    for char in msg:
        if char == "!":
            break
        if char != ":":
            result += char
    return result


def get_message(msg):
    result = ""
    i = 3
    length = len(msg)
    while i < length:
        result += msg[i] + " "
        i += 1
    result = result.lstrip(':')
    return result


def parse_message(msg):
    if len(msg) >= 1:
        msg = msg.split(' ')
        options = {'!test': command_test,
                   '!asdf': command_asdf}
        if msg[0] in options:
            options[msg[0]]()
# --------------------------------------------- End Helper Functions -----------------------------------------------


# --------------------------------------------- Start Command Functions --------------------------------------------
def command_test():
    send_message(CHAN, 'testing some stuff')


def command_asdf():
    send_message(CHAN, 'asdfster')
# --------------------------------------------- End Command Functions ----------------------------------------------
print("Starting up...")
con = socket.socket()
print("Connecting to "+HOST+" on port "+str(PORT))
con.connect((HOST, PORT))
print("Sending password")
send_pass(PASS)
print("Sending username")
send_nick(NICK)
print("Joining channel...")
join_channel(CHAN)
print("Maybe joined?")
data = ""

while True:
  try:
    data = data+con.recv(1024).decode('UTF-8')
    data_split = re.split(r"[~\r\n]+", data)
    data = data_split.pop()

    for line in data_split:
      line = str.rstrip(line)
      line = str.split(line)

      if len(line) >= 1:
        if line[1] == 'PRIVMSG':
          sender = get_sender(line[0])
          message = get_message(line)
          parse_message(message)
          
          print(sender + ": " + message)
          if str(message).startswith("!sound"):
            mysong=message.split(" ")[1]
            try:
              playsound('./'+cgi.escape(str(mysong).replace('.','').replace('/','').replace("\\",'').replace('"','').replace("'","").replace('?','').replace('!','').replace('*','').replace('$',''))+'.mp3')
            except:
              pass
        if line[0] == 'PING':
          send_pong(line[1])

  except socket.error:
        print("Socket died")

  except socket.timeout:
        print("Socket timeout")
  except:
    pass