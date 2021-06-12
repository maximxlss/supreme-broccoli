from os import get_terminal_size
from time import sleep, time, ctime

text = ctime(time())
termsize = get_terminal_size().columns
buffer = " "*(termsize+len(text)*2)
timing = 10/(termsize+len(text))
offset = 0

while True:
	if offset >= termsize+len(text):
		offset = 0
	buffer = ((" "*offset)+text).ljust(len(buffer))
	print(buffer[len(text):-len(text)], end="\r")
	offset += 1
	text = ctime(time())
	sleep(timing)
