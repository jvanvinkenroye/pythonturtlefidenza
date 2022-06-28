"""
Python Turtle script for drawing Fidenza based generative art

Fidenza algorithm was created by Tyler Hobbs
https://tylerxhobbs.com/fidenza

Author: Tom Box, @mrtombox
"""
from noise import snoise2
import turtle
import random2
import math

WIDTH = 300
HEIGHT = 200
BLACK = 'red'
MARGIN = 50

def getFlowFieldValue(x,y,scale=0.0005,offset=200,octaves=1):
  # Returns a value from a Perlin noise field
  return snoise2((x+offset) * scale, (y+offset) * scale, octaves)

class Curve():
  # Object for storing, generating and plotting a single curve
  
  def __init__(self,colour = BLACK):
    self.colour = colour
    self.points = []

  def addPoint(self, x,y):
    # Add a new point onto the end of the curve
    self.points.append((x,y))

  def getNearest(self, x, y, list):
    # Find the distance to the nearest existing curve point
    max_dist = None
    for curve in list:
      for point in curve.points:
        dist = math.hypot(x-point[0], y-point[1])
        if max_dist == None or dist < max_dist:
          max_dist = dist
    return max_dist
          
  def create(self, x, y, steps, list):
    # Generate a new curve along the flowfield

    # Abort if first point is too close to another curve point
    dist = self.getNearest(x,y,list)
    if dist and dist < 10:
      return
      
    segment_length = 5
    
    for n in range(steps):
          angle = getFlowFieldValue(x,y) * 360
          x += math.cos(math.radians(angle))*segment_length
          y += math.sin(math.radians(angle))*segment_length  
      
          if x < -WIDTH+MARGIN or x > WIDTH-MARGIN:
            break
          if y < -HEIGHT+MARGIN or y > HEIGHT-MARGIN:
            break

          # Abort if too close to another curve point
          dist = self.getNearest(x,y,list)
          if dist and dist < 10:
            break

          self.addPoint(x,y)

  def plot(self, t):
    # Plot the curve on the page view

    # Move the plot head to the start without drawing
    t.color(self.colour)
    t.penup()
    first_point = self.points[0]
    t.setpos(first_point[0],first_point[1])
    t.pendown()

    # Plot along each point on curve
    for point in self.points:
      t.setpos(point[0],point[1])
        
def plotFlowField(t):
  # Draw the flowfield on the page in light grey
  
  t.pensize(5)
  t.color('#eeeeee')
  
  for y in range(-HEIGHT, HEIGHT, 25):
    for x in range(-WIDTH, WIDTH, 25):
      t.penup()
      t.setpos(x,y)
      flowfield_val = getFlowFieldValue(x,y) * 360
      t.setheading(flowfield_val)
      t.pendown()
      t.forward(10) 

def createCurves():
  # Create all the data for the curves
  curves = []
  total = 1000
  count = 1
  length = 50
  
  for n in range(total):
    print(f'Generating curve {count} of {total}')
    
    x = random2.randrange(-WIDTH,WIDTH)
    y = random2.randrange(-HEIGHT,HEIGHT) 
    curve = Curve()
    curve.create(x, y, length, curves)

    # Only add the curve if point list isn't empty
    if len(curve.points) > 0:
      curves.append(curve)
    
    count += 1
    
  total = len(curves)
  print(f'Saved {total} curves')
  return curves

def plotCurves(t, curves):
  # Draw every saved curve on the page
  
  for curve in curves:
    curve.plot(t)
  
def main():
  # Initialize all the Turtule stuff
  t = turtle.Turtle()
  t.speed(0)
  t.hideturtle()
  screen = turtle.Screen()
  screen.screensize(WIDTH, HEIGHT)

  # Turn off realtime view updates
  screen.tracer(0) 

  # Generate the page art
  plotFlowField(t)
  curves = createCurves()
  plotCurves(t, curves)

  # Refresh screen so pen marks appear
  screen.update() 

main()