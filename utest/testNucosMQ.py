from __future__ import print_function

import unittest, time
import sys
sys.path.append('../../')
client = None
server = None

socketIP = "127.0.0.1"
socketPort = 4000

from nucosMQ import NucosClient
from nucosMQ import NucosServer

def auth(uid, signature):
    print("TEST signature",uid, signature)
    allowed = signature == "1234"
    if not allowed:
        #logger.log("auth failed, disconnect")
        return False
    else:
        #logger.log("auth success, connect")
        return True

def on_challenge(x):
    return "1234"

class UTestClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global client, server
        client = NucosClient(socketIP, socketPort)
        server = NucosServer(socketIP, socketPort, do_auth=auth)
        server.start()
        
    def setUp(self):
        global client, server
        client.prepare_auth( "testuser", on_challenge)
        client.start()
        
    def tearDown(self):
        global client, server
        #wait at least 1 second before closing the client
        time.sleep(1.0)
        server.force_close()
        #time.sleep(4.0)
        #client.close()
        
    def test_connect(self):
        print("hallo")
        time.sleep(1.0)
        
    
if __name__ == '__main__':
    unittest.main()