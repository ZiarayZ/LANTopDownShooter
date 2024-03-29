import pygame,socket,random,math,time,os
#create player object, movement and shooting defined inside
class Player(object):
    def __init__(self):
        self.rect=pygame.Rect(random.randint(0,1550),random.randint(0,850),50,50)
        self.health=9
        self.bullets=[]
        self.time=0
    def move(self,dx=0,dy=0):
        if dx!=0:
            self.rect.x+=dx
            if self.rect.x<0:
                self.rect.x=0
            if self.rect.x>1550:
                self.rect.x=1550
        if dy!=0:
            self.rect.y+=dy
            if self.rect.y<0:
                self.rect.y=0
            if self.rect.y>850:
                self.rect.y=850
    def fire(self,angle):
        x=2*math.cos(angle)
        y=2*math.sin(angle)
        vector=(x,y)
        if time.time()-self.time>1:
            self.bullets.append(Bullet((self.rect.x+25+(26*vector[0])/math.sqrt(2),self.rect.y+25+(26*vector[1])/math.sqrt(2)),vector))
            self.time=time.time()
#create bullet object, movement defined inside
class Bullet(object):
    def __init__(self,loc,obj):
        self.location=loc
        self.direction=obj
    def move(self):
        self.location=(self.location[0]+(5*math.sqrt(2)*self.direction[0]),self.location[1]+(5*math.sqrt(2)*self.direction[1]))
        if self.location[0]<0 or self.location[0]>1600:
            self.direction=(-self.direction[0],self.direction[1])
        if self.location[1]<0 or self.location[1]>900:
            self.direction=(self.direction[0],-self.direction[1])
#create socket and connect to server socket
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host=str(input("Server Host Name.\n>: "))
port=8184
s.connect((host,port))
#create game window
width=1600
height=900
r=True
bullets=[]
os.environ["SDL_VIDEO_WINDOW_POS"]="0,0"
pygame.init()
screen=pygame.display.set_mode((width,height),pygame.FULLSCREEN)
clock=pygame.time.Clock()
pygame.mouse.set_visible(False)
player=Player()
cursorimg=pygame.image.load("crosshair.png")
myfont=pygame.font.SysFont('Arial',50)
#game loop
while r:
    clock.tick(60)
    screen.fill((0,0,0))
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            r=False
    #shooting and calculating angles
    if pygame.mouse.get_pressed()[0] and player.health>=0:
        mouse_pos=pygame.mouse.get_pos()
        x=int(mouse_pos[0]-player.rect.x-25)
        y=int(mouse_pos[1]-player.rect.y-25)
        if x>0:
            if y>=0:
                theta=math.atan(y/x)
            if y<0:
                theta=math.atan(-x/y)+(3/2)*math.pi
        if x<0:
            if y>0:
                theta=math.atan(-x/y)+(1/2)*math.pi
            if y<=0:
                theta=math.atan(y/x)+math.pi
        if x==0:
            if y>0:
                theta=(1/2)*math.pi
            if y<0:
                theta=(3/2)*math.pi
            if y==0:
                theta="nothing"
        if theta!="nothing":
            player.fire(theta)
    #player movement
    user_input=pygame.key.get_pressed()
    if(user_input[pygame.K_w]or user_input[pygame.K_UP])and player.health>=0:
        player.move(dy=-10)
    if(user_input[pygame.K_s]or user_input[pygame.K_DOWN])and player.health>=0:
        player.move(dy=10)
    if(user_input[pygame.K_a]or user_input[pygame.K_LEFT])and player.health>=0:
        player.move(-10)
    if(user_input[pygame.K_d]or user_input[pygame.K_RIGHT])and player.health>=0:
        player.move(10)
    #player quits
    if user_input[pygame.K_ESCAPE]:
        r=False
    #attempt to send player location to server
    try:
        s.send((str(int(player.rect.x))+","+str(int(player.rect.y))+",").encode())
        somethings=s.recv(8192).decode()
    except:
        r=False
    #attempt to receive player locations from server
    coordinates=[[]]
    number1=0
    number2=0
    try:
        word=""
        for char in somethings:
            if char==",":
                if word!="empty":
                    coordinates[number1].append(int(word))
                    number2+=1
                    if number2==2:
                        coordinates.append([])
                        number1+=1
                        number2=0
                    word=""
                else:
                    word=""
                    number1+=1
                    number2=0
            else:
                word+=char
    except:
        pass
    #remove empty lists
    for coord in coordinates:
        if coord==[]:
            coordinates.remove(coord)
    #translate player bullet's locations into a long string
    word=""
    for bullet in player.bullets:
        bullet.move()
        word+=str(int(bullet.location[0]))+","+str(int(bullet.location[1]))+","
        for coord in coordinates:
            if pygame.Rect(coord[0],coord[1],50,50).collidepoint(bullet.location)and int(player.rect.x)!=coord[0]and int(player.rect.y)!=coord[1]:
                player.bullets.remove(bullet)
    #attempt to send player bullet's locations to server
    try:
        if word!="":
            s.send(word.encode())
        else:
            s.send("empty".encode())
        somethings=s.recv(8192).decode()
    except:
        r=False
    #attempt to reveive bullet locations from server
    try:
        bullets=[[]]
        word=""
        number1=0
        number2=0
        for char in somethings:
            if char==",":
                if word!="empty":
                    bullets[number1].append(int(word))
                    number2+=1
                    if number2==2:
                        bullets.append([])
                        number1+=1
                        number2=0
                    word=""
                else:
                    word=""
            else:
                word+=char
    except:
        pass
    #remove empty lists
    for bullet in bullets:
        if bullet==[]:
            bullets.remove(bullet)
    #calculate bullet collisions with player, ignore player bullets
    for bullet in bullets:
        pbull=False
        for pbullet in player.bullets:
            #badly implemented, player's own bullets are sent back and ignored through checking identical locations
            if int(pbullet.location[0])==bullet[0]and int(pbullet.location[1])==bullet[1]:
                pbull=True
    #draw objects onto game window
        if not pbull:
            if player.rect.collidepoint((bullet[0],bullet[1])):
                player.health-=1
            else:
                pygame.draw.rect(screen,(50,50,255),pygame.Rect(bullet[0]-5,bullet[1]-5,10,10))
        else:
            pygame.draw.rect(screen,(255,50,50),pygame.Rect(bullet[0]-5,bullet[1]-5,10,10))
    for coord in coordinates:
        pygame.draw.rect(screen,(50,50,255),pygame.Rect(coord[0],coord[1],50,50))
    #if player dies kick them out
    if player.health<0:
        r=False
    pygame.draw.rect(screen,(255,50,50),player.rect)
    textimg=myfont.render(str(player.health),False,(0,0,0))
    screen.blit(textimg,(player.rect.x+25-(textimg.get_width()/2),player.rect.y+25-(textimg.get_height()/2)))
    mouse_x,mouse_y=pygame.mouse.get_pos()
    screen.blit(cursorimg,(mouse_x-10,mouse_y-10))
    pygame.display.update()
    pygame.display.flip()
pygame.quit()
#send death message to server, may cause issues
s.send("True".encode())
#close connection to server
s.close()
