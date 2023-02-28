# UDP Made Easy

a simple udp wrapper.

## Quick Start

We can use the base class Server to inherit the basic common properties of a server. 
We need to overload the abstract method, handle_request
```python
import udpeasy

class Myserver(udpeasy.server.Server):

	def handle_request(self, data, address):
		packet = udpeasy.packet.Packet.deserialize(data)

		print(packet.packet_type)
		print(packet.payload)

server = Myserver("localhost", "1234")
server.run()
```

As for the client we can do something similar.

We need to overload the abstract method run_loop, and call the start method to start the thread.
```python
import udpeasy

class Myclient(udpeasy.server.Client):

	def run_loop(self):
		#make a packet instance and send it to the server
		packet = udpeasy.packet.Packet(1, self.sequence_number, b"hello, world")
		self.send(packet)

client = Myclient("localhost", "1234")
server.start()
server.stop()
```

## Good Practise

Make an enum with the packet types.
```python
class PacketType:
	MESSAGE = 1
	SCORE = 2
	POSITION = 3
	EVENT = 3
```

Would also advocate for making a enum for formating the payloads. This asbtraction will simplify packing, and unpacking on both ends.

```python
import struct

class PayloadFormat:
	MESSAGE = struct.Struct("32s")
	SCORE = struct.Struct("I")
	POSITION = struct.Struct("II")
	EVENT = struct.Struct("I")
```
(if the classes above are unfamiliar to you)
[read this](https://docs.python.org/3/library/struct.html#format-characters)
(alternatively [you can use JSON](#alternatives).)


Could even add more enums to abstract things like events:
```python
class EventTypes:
	CONNECTED = 1
	DISCONNECTED = 2
	WON = 3
	LOST = 4
```
We can now utilize the astractions we have made to simplify the first example.
```python
import udpeasy

class Myclient(udpeasy.server.Client):

	def run_loop(self):
		packet = udpeasy.packet.Packet(PacketType.MESSAGE, self.sequence_number, PayloadFormat.MESSAGE.pack(b"hello, world"))
		self.send(packet)

...
```
This will be helpful when I want to unpack the packet on the server as well.
```python
import udpeasy

class Myserver(udpeasy.server.Server):

	def handle_request(self, data, address):
		packet = udpeasy.packet.Packet.deserialize(data)

		print(packet.packet_type)
		print(packet.payload) # binary data

		if packet.packet_type == PacketType.MESSAGE:
			message = PayloadFormat.MESSAGE.unpack(packet.payload)
			#NOTE the unpack method always returns a touple, so in this case
			# message would be a one-dimensional tuple, we just index it by 0
			message = message[0]
			print(message)

		if packet.packet_type == PacketType.POSITION:
			x, y = PayloadFormat.POSITION.unpack(packet.payload)
			...

server = Myserver("localhost", "1234")
server.run()
```

## Alternatives
Okay that's all good an well for our basic types with specific lengths. How about arrays or objects with a dynamic length?

I would recommend just using json for this purpose.
```python
import json

...

	packet = udpeasy.packet.Packet(
		PacketType.ENEMIES,
		self.sequence_number,
		json.dumps([dict(enemy) for enemy in array of enemies]).encode()
		)
	self.send(packet)
```
