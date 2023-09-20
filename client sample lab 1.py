import socket
import keyboard
from time import *

# CONFIGURATION PARAMETERS
IP_ADDRESS = "192.168.1.106"  # SET THIS TO THE RASPBERRY PI's IP ADDRESS
CONTROLLER_PORT = 5001
TIMEOUT = 5  # If its unable to connect after 5 seconds, give up.


# Want this to be a while so robot can initialize.
def square():
    for i in range(4):
        sock.sendall("a drive_straight(100)".encode())
        sleep(2)
        sock.sendall("a spin_left(100)".encode())
        sleep(1.6)
    # checkpoint one


# Bonus Polygon
def polygon(num_sides):
    if num_sides < 3:
        print("A polygon must have at least 3 sides.")
        return
    for i in range(num_sides):
        # Move forward
        sock.sendall("a drive_straight(200)".encode())
        sleep(2)

        # Turn the calculated angle to form the next side
        # angle = 360 / N
        sock.sendall("a spin_left(100)".encode())
        sleep(1.6 * 4.5 / num_sides)

#     # Change LED colors while the song is playing
#     for i in range(10):
#         # Set LED color to green
#         sock.sendall("a set_led(0, 0, 255, 0)".encode())  # Green color (red=0, green=255, blue=0)
#         sleep(1)

#         # Set LED color to red
#         sock.sendall("a set_led(0, 255, 0, 0)".encode())  # Red color (red=255, green=0, blue=0)
#         sleep(1)

def song():
    sock.sendall("a set_song(0, [(64,32),(62,32),(60,32),(62,32),(64,32),(64,32),(64,64),(62,32),(62,32),(62,64)])".encode())
    sleep(2)
    sock.sendall("a play_song(0)".encode())
    sleep(10)
    # checkpoint two


# Bonus Dance while robot sings
def song2():
    sock.sendall(
        "a set_song(0, [(64,32),(62,32),(60,32),(62,32),(64,32),(64,32),(64,64),(62,32),(62,32),(62,64)])".encode())
    sleep(.1)
    sock.recv(128).decode()
    sock.sendall("a play_song(0)".encode())
    sock.recv(128).decode()
    for i in range(4):
        sock.sendall("a spin_left(100)".encode())
        sock.recv(128).decode()
        sleep(1)
        sock.sendall("a spin_right(100)".encode())
        sock.recv(128).decode()
        sleep(1)

#Last checkpoint 
def remote():
    # #checkpoint three
    # while True:
    #         event = keyboard.read_event()

    #         if event.event_type == keyboard.KEY_DOWN:
    #             if event.name == "w":
    #                 sock.sendall("a drive_direct(100, 100)".encode())
    #             elif event.name == "a":
    #                 sock.sendall("a drive_direct(0, 100)".encode())
    #             elif event.name == "d":
    #                 sock.sendall("a drive_direct(100, 0)".encode())
    #             elif event.name == "s":
    #                 sock.sendall("a drive_straight(-100, -100)".encode())
    #             elif event.name == "q":
    #                 break
    #         elif event.event_type == keyboard.KEY_UP:
    #             # Stop the robot when the key is released
    #             sock.sendall("a drive_direct(0, 0)".encode())

    while(1):
        direction = keyboard.read_key()
        print(direction)
        match direction:
            case "w":
                sock.sendall("a drive_direct(100,100)".encode())
                print(sock.recv(128).decode())
                sleep(0.1)
            case "a":
                #the turns currently don't work probably better to use spin_left and spin_right
                sock.sendall("a spin_left(100)".encode())
                print(sock.recv(128).decode())
                sleep(0.1)
            case "d":
                sock.sendall("a spin_right(100)".encode())
                print(sock.recv(128).decode())
                sleep(0.1)
            case "s":
                #the backward also doesn't work
                sock.sendall("a drive_direct(-100,-100)".encode())
                print(sock.recv(128).decode())
                sleep(0.1)
            case "c":
                #exit the code by pressing q
                break
            case "q":
                sock.sendall("a drive_direct(100,50)".encode())
                sleep(0.1)
            case "e":
                sock.sendall("a drive_direct(50,100)".encode())
                sleep(0.1)
            case _:
                sleep(2)

sock = socket.create_connection((IP_ADDRESS, CONTROLLER_PORT), TIMEOUT)

""" The t command tests the robot.  It should beep after connecting, move forward 
slightly, then beep on a sucessful disconnect."""
# sock.sendall("t /dev/tty.usbserial-DA01NYDH")			# send a command
# print(sock.recv(128))        # always recieve to confirm that your command was processed

""" The i command will initialize the robot.  It enters the create into FULL mode which
 means it can drive off tables and over steps: be careful!"""
sock.sendall("i /dev/ttyUSB0".encode())
print(sock.recv(128).decode())

"""
    Arbitrary commands look like this 
        a *
    Whatever text is given where the * is, is given to the Create API in the form
        result = robot.*
    then any result will be send back.  If there is no result the command will be echoed.
    
    You can see the possible commands here:
    https://github.com/tribelhb/irobot
    
    You may wish to extend the control_server.py on the raspberry pi.
"""

# sock.sendall("a drive_straight(100)".encode())
# print(sock.recv(128).decode())

# sleep(2)
# square()
# song()
# remote()
# polygon(3)
# sleep(2)
# polygon(5)
# sleep(.1)
song2()
# sleep(.1)

sock.sendall("a battery_charge".encode())
print("Battery charge is: ", sock.recv(128).decode())
sock.sendall("a battery_capacity".encode())
print("Battery capacity is: ", sock.recv(128).decode())


""" The c command stops the robot and disconnects.  The stop command will also reset 
the Create's mode to a battery safe PASSIVE.  It is very important to use this command!"""
sock.sendall("c".encode())
print(sock.recv(128).decode())

sock.close()
