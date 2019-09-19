import time
from datetime import datetime

from pythonosc import osc_message_builder
from pythonosc import udp_client
osc_client = udp_client.UDPClient('localhost', 5005)

for _ in range(10):
    msg = osc_message_builder.OscMessageBuilder(address="/debug")
    msg = msg.build()
    print(msg.dgram)
    now = datetime.now()
    print('Sending at {}:{}.{}'.format(now.minute, now.second, now.microsecond))
    osc_client.send(msg)
    time.sleep(1)
