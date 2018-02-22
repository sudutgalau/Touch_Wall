"""Small example OSC server
This program listens to several addresses, and prints some information about
received packets.
"""
import argparse
import math

from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client
client = udp_client.SimpleUDPClient("127.0.0.1", 7000) #Puerto por el que escucha el Resolume


def playTrack(track):
    client.send_message("/track"+str(track)+"/connect/", 1) #Darle play a una columna

def videoSolo(unused_addr, args, p):
    if p == 1:
        print("Iniciado")
        client.send_message("/layer4/select", 1)
        client.send_message("/activelayer/solo", 1)  #HACE QUE LA CAPA ACTIVA SE VEA SOLA
    else:
        client.send_message("/layer4/select", 1)
        client.send_message("/activelayer/solo", 0)  # HACE QUE LA CAPA ACTIVA SE VEA SOLA
        client.send_message("/layer4/select", 0)
        # client.send_message("/composition/select", 0)
        playTrack(1)

# def OpacityTrack(unused_addr, args, p):
#     if p == 1:
#         print("ReduceOp")
#         for i in range(1, 4):
#             "/layer"+str(i)+"/clip1/connect"
#             client.send_message("/activeclip/video/opacity/values", 0.5) #Lleva la opacidad a 0.2
#     else:
#         for i in range(3):
#             print("IncrementOp")
#             "/layer"+str(i)+"/clip1/connect"
#             client.send_message("/activeclip/video/opacity/values", 1) #Lleva la opacidad a 0.2


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip",
      default="127.0.0.1", help="The ip to listen on")
  parser.add_argument("--port",
      type=int, default=7001, help="The port to listen on")
  args = parser.parse_args()

  dispatcher = dispatcher.Dispatcher()
  dispatcher.map("/layer4/clip3/connect", videoSolo, print)  #Este es el video que cuando termina debe iniciar el track1

  # dispatcher.map("/activeclip/video/position/values", getPosition, "Position")
  # dispatcher.map("/layer1/clip2/connect", OpacityTrack, print)  #Si este video se reproduce debe oscurecer a los del track1
  # dispatcher.map("/layer2/clip2/connect", OpacityTrack, print)  #Si este video se reproduce debe oscurecer a los del track1
  # dispatcher.map("/layer3/clip2/connect", OpacityTrack, print)  #Si este video se reproduce debe oscurecer a los del track1

  server = osc_server.ThreadingOSCUDPServer(
      (args.ip, args.port), dispatcher)
  print("Serving on {}".format(server.server_address))
  server.serve_forever()


