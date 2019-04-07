#!/usr/bin/env python

import RPi.GPIO as gpio
import time
import random
from demo_opts import device
from luma.core.interface.serial import spi, noop
from luma.core.legacy import text, show_message
from luma.led_matrix.device import max7219
from luma.core.render import canvas

gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
height = 7
width = 7

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, height=8, width=8)


def button_pressed(gpio):
  global direction
  if(gpio == 8):   #DOWN
   direction = [1,0]
  elif(gpio == 10): #UP
   direction = [0,-1]
  elif(gpio == 12: #LEFT
   direction = [0,1]
  elif(gpio == 16 #RIGHT
   direction = [-1,0]


gpio.setup(8,gpio.IN,pull_up_down=gpio.PUD_DOWN)
gpio.add_event_detect(10, gpio.RISING, callback=button_pressed)
gpio.setup(10,gpio.IN,pull_up_down=gpio.PUD_DOWN)
gpio.add_event_detect(10, gpio.RISING, callback=button_pressed)
gpio.setup(12,gpio.IN,pull_up_down=gpio.PUD_DOWN)
gpio.add_event_detect(10, gpio.RISING, callback=button_pressed)
gpio.setup(16, gpio.IN,pull_up_down=gpio.PUD_DOWN)
gpio.add_event_detect(10, gpio.RISING, callback=button_pressed)


def LED_PARTY():
    counter = 0
    while counter > 20:
        with canvas(device) as draw:
            for i in range(4):
                x = random.randint(0, device.width)
                y = random.randint(0, device.height)
                draw.point((x, y), fill="white")
                time.sleep(0.05)
       counter += 1


def gameStart():
  global snake, direction, food
  snake = [[4,4]]
  direction = [0,0]
  while direction == [0,0]:
    show_message(device, "START", fill="white", scroll_delay=0.1)
  newFood()


def newFood():
  global food, snake
  fedSnake = False
  while fedSnake == False:
    fedSnake = True
    x = random.randint(0,width)
    y = random.randint(0,height)
    food = [x,y]
    for index in snake:
      if(index == food):
        fedSnake = False
  print(food)


def gameOver():
  LED_PARTY()
  points = len(snake)-1
  show_message(device,"SCORE: "+ str(points), fill="white", scroll_delay=0.1)
  gameStart()


gameStart()

while True:
  pause = False
  newSnake = [snake[0][0]+direction[0],snake[0][1]+direction[1]]
  for index in snake:
    if(index == newSnake):
      gameOver()
      pass
  if(newSnake == food):
     newFood()
     pause = True
  else:
     snake.pop()
  snake.insert(0,newSnake)
  if(snake[0][0] > width or snake [0][1] > height
    or snake[0][0] < 0 or snake[0][1] < 0 ):
    gameOver()
    pass
  device.clear()


  with canvas(device) as draw:
     for i in snake:
       draw.point(food, fill ="white")
       draw.point(i, fill ="white")
  if(pause == False):
    newLength = (len(snake)-2)*0.05
    time.sleep(0.5-newLength)
  else:
    time.sleep(0.4)
