# !/usr/bin/python3

import serial
import time
import argparse
# from pythonosc import osc_message_builder
from pythonosc import udp_client

parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="127.0.0.1",
    help="The ip of the OSC server")
parser.add_argument("--port", type=int, default=7000,
    help="The port the OSC server is listening on")
args = parser.parse_args()

client = udp_client.SimpleUDPClient(args.ip, args.port)

ser = serial.Serial('COM3', 9600, timeout=0) # Comment if S.O is Windows
#ser = serial.Serial('/dev/ttyACM0', 9600, timeout=0.1) # Uncomment if S.O. is RASPBERRY PI


def play(layer,clip):
    layer = str(layer)
    clip = str(clip)
    client.send_message("/layer"+layer+"/clip"+clip+"/connect", 1) #CONECTO CON LA CAPA
    time.sleep(0.1)
    client.send_message("/activeclip/audio/position/playmode", 2) #Reproducir hasta el final
    time.sleep(0.1)
    client.send_message("/activeclip/audio/position/direction", 1) #PLAY para adelante
    client.send_message("/activeclip/video/position/playmodeaway", 1) #Reproduce desde el ultimo cuadro(ignora multiples touchs)


def playTrack(track):
    client.send_message("/track"+str(track)+"/connect/", 1) #Le da play a la columna 1
    client.send_message("/activeclip/video/position/playmodeaway", 1) #Reproduce desde el ultimo cuadro(ignora multiples touchs)

if __name__ == "__main__":
    while True:
        pin = 99
        status = 99
        amessage = ser.readline()
        amessage = amessage.decode()
        now = time.time()

        # if amessage != '':
        #     print("Mensaje: " +amessage);
        if amessage == '0' or amessage == '9':
            print("Rueda Delantera")
            play(1, 2)
        elif amessage == '2' or amessage == '7':
            print("Rueda Trasera")
            play(2, 2)
        elif amessage == '11':
            print("Trompa")
            play(3, 2)
        elif amessage == '4':
            print('Cabina')
            playTrack(3)
        time.sleep(0.01)
