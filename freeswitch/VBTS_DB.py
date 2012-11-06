#Copyright 2011 Kurtis Heimerl <kheimerl@cs.berkeley.edu>. All rights reserved.
#
#Redistribution and use in source and binary forms, with or without modification, are
#permitted provided that the following conditions are met:
#
#   1. Redistributions of source code must retain the above copyright notice, this list of
#      conditions and the following disclaimer.
#
#   2. Redistributions in binary form must reproduce the above copyright notice, this list
#      of conditions and the following disclaimer in the documentation and/or other materials
#      provided with the distribution.
#
#THIS SOFTWARE IS PROVIDED BY Kurtis Heimerl ''AS IS'' AND ANY EXPRESS OR IMPLIED
#WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
#FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL Kurtis Heimerl OR
#CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
#ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
#ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#The views and conclusions contained in the software and documentation are those of the
#authors and should not be interpreted as representing official policies, either expressed
#or implied, of Kurtis Heimerl.

from freeswitch import *
from libvbts import FreeSwitchMessenger

def usage():
    return "VBTS_DB item|field|qualifier[|table]\nVBTS_DB name|callerid|12345|sip_buddies"

def parse(args):
    res = args.split("|")
    if (len(res) < 3):
        return (None, None, None)
    table = "sip_buddies"
    if (len(res) > 3):
        table = res[3]
    return (res[0], (res[1], res[2]), res[3])

def get(args):
    (item, qualifier, table) = parse(args)
    if not (item and qualifier and db):
        consoleLog('info', usage())
        exit(1)
    fs = FreeSwitchMessenger.FreeSwitchMessenger()
    if (table == "sip_buddies"):
        res = fs.SR_get(item, qualifier)
    elif (table == "dialdata_table"):
        res = fs.SR_ge_dialdata(item, qualifier)
    else:
        consoleLog('info', "Bad Table %s" % table)
    return res

def chat(message, args):
    res = get(args)
    consoleLog('info', "Returned: " + res + "\n")
    message.chat_execute('set', '_openbts_ret=%s' % res)

def fsapi(session, stream, env, args):
    res = get(args)
    consoleLog('info', "Returned: " + res)
    if (res):
        stream.write(res)

