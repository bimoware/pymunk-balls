from pygame import draw, Surface
from pymunk import Body

class Sprite:
    def __init__(self, x: int, y: int, type: str):
        self.color = "red"
        self.width = 10
        self.pos = [x, y]  # Coordonates
        self.speed = [0, 0]  # x & y speed
        self.type = Body.STATIC if type == "STATIC" else Body.DYNAMIC if type == "DYNAMIC" else Body.KINEMATIC
        self.body = Body(body_type=self.type) 
        self.body.position = tuple(self.pos)
        
    def go_to(self, x=0, y=0):  # Go to (x,y) coordinates
        self.go_toX(x)
        self.go_toY(y)

    def go_toX(self, x):
        self.pos[0] = x

    def go_toY(self, y):
        self.pos[1] = y

    def moveX(self, x=0):  # Move by x pixels on the X axis
        self.go_toX(self.pos[0]+x)

    def moveY(self, y=0):  # Move by y pixels on the Y axis
        self.go_toY(self.pos[1]+y)

    def move(self, x=0, y=0):  # Move by (x,y) pixels
        self.moveX(x)
        self.moveY(y)

    def draw(self, screen: Surface):
        draw.circle(
            screen,
            self.color,
            tuple(self.pos),
            self.width,
            10
        )



# --
for line in lines:
    if len(balls[0][0].shapes_collide(line).points):
        COLLISIONS += 1
        mp3.play()
        break
# --