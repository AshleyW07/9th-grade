#pingpong V1.2
#V1.2 摩擦力
#V1.21 多个小球
#V2.01 两个拍子
import pygame, sys, random
SCREEN_W, SCREEN_H = 1024, 600
BORDER_W = 10
ACCURACY = 2
G = 0.01  #重力
SPEEDY_MAX = 3
def RT_show_txt( scr, txt, font, x, y, c):
    img = font.render( txt, True, c )
    scr.blit( img, (x, y) )
def set_new_ball(ball):
    ball.x, ball.y = SCREEN_W // 2, 10
    ball.spdX = (random.random()*2 + 2) * (random.randint(0,1) * 2 - 1)
    ball.spdY = random.random()*2 + 1
def RT_draw(screen, pixel, x0, y0, scale):
    color = ( pygame.color.THECOLORS['black'],
              pygame.color.THECOLORS['gray32'],
              pygame.color.THECOLORS['gray64'],
              pygame.color.THECOLORS['white'],
              pygame.color.THECOLORS['red'],
              pygame.color.THECOLORS['green'],
              pygame.color.THECOLORS['blue'],
              pygame.color.THECOLORS['orange'],
              pygame.color.THECOLORS['brown'],
              pygame.color.THECOLORS['purple'],
              pygame.color.THECOLORS['yellow'],
              pygame.color.THECOLORS['cyan'],
              pygame.color.THECOLORS['sienna'],
              pygame.color.THECOLORS['chocolate'],
              pygame.color.THECOLORS['coral'],
              pygame.color.THECOLORS['darkgreen'])
    for y in range(len(pixel)):   #在高度方向循环
        line = pixel[y] #第y行像素字符串
        for x in range(len(line)):  #在宽度方向循环
            if 'A' <= line[x] <= 'F':   #A-F的ASCII码产生10-15
                c = color[ord(line[x]) - 55]
            elif '0' <= line[x] <= '9':  
                c = color[eval(line[x])]  #0-9对应颜色编号0-9
            else:
                continue
            pygame.draw.rect(screen, c,\
                    (int(x*scale + x0), int(y*scale + y0), scale, scale), 0)

class CLS_ball( object ):   
    def __init__( self, x, y, spdX, spdY, scale ):
        self.x, self.y = x, y
        self.spdX, self.spdY = spdX, spdY
        self.scale = scale
        self.w, self.h = 0, 0
        self.interval = 8 #动画时间间隔
        self.counter = 0  #动画计时器
        self.picList = [] #动画list
    def add_pic( self, pixel ):
        self.picList.append( pixel )
        self.w = len(pixel[0]) * self.scale
        self.h = len(pixel) * self.scale
    def move( self ):  #小球坐标计算
        self.x += self.spdX
        self.spdY += G
        if self.spdY > SPEEDY_MAX:
            self.spdY = SPEEDY_MAX
        self.y += self.spdY
        '''
        if self.x < BORDER_W:  # x方向出界
            self.spdX *= -1
            soundPong2.play()
        '''
        if self.y < BORDER_W or \
           self.y > SCREEN_H - self.h - BORDER_W:   # y方向出界
            self.spdY *= -1
            soundPong2.play()
        self.collide( paddleL )  #调用collide
        self.collide( paddleR )
        self.collide( net )
    def draw( self, scr ):
        RT_draw( scr, \
                 self.picList[int(self.counter) // self.interval % len(self.picList)], \
                 self.x, self.y, self.scale)
        self.counter += self.spdX * 0.5
    def collide ( self, pad ): #处理碰撞
        global gameStatus
        if gameStatus == 1:
            return
        if self.spdX < 0:
            distance = abs(pad.x + pad.w - self.x)
        else:
            distance = abs(self.x + self.w - pad.x)
        if distance <= ACCURACY:
            if pad.y <= self.y + self.h//2 <= pad.y + pad.h:
                self.spdX *= -1
                self.spdY += pad.spdY * pad.friction #friction
                soundPong4.play()
                if pad.type == 1:
                    gameStatus = 1
                    if self.spdX < 0:
                        paddleR.score += 1
                    else:
                        paddleL.score += 1
            elif pad.type == 0: #没接到 对方赢
                gameStatus = 1
                if self.spdX > 0:
                    paddleL.score += 1
                else:
                    paddleR.score += 1


class CLS_paddle( object ):   #球拍类定义
    def __init__( self, x, y, w, h, c = (200, 200, 0) ):
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.spdY = 0   #球拍上下移动，只有y
        self.c = c
        self.accY = 0
        self.friction = 0.5
        self.score = 0   #score
        self.type = 0  #0:paddle, 1:net
    def move( self ):
        self.spdY += self.accY
        self.y += self.spdY
        if self.y < BORDER_W:
            self.y = BORDER_W
            self.spdY = 0
        if self.y > SCREEN_H - self.h - BORDER_W:
            self.y = SCREEN_H - self.h - BORDER_W
            self.spdY = 0
    def draw( self, scr ):
        pygame.draw.rect(scr, self.c, (self.x, self.y, self.w, self.h), 0)
def draw_field( scr ):   #绘制场地
    c = pygame.color.THECOLORS['brown']
    pygame.draw.rect(scr, c, (0, 0, SCREEN_W, BORDER_W), 0)
    pygame.draw.rect(scr, c, (0, SCREEN_H - BORDER_W, SCREEN_W, BORDER_W), 0)
    #pygame.draw.rect(scr, c, (0, 0, BORDER_W, SCREEN_W), 0)   #deleted
    #score display
    RT_show_txt(scr, 'RT PINGPONG', font64, 300, 200, (255,255,0) )
    RT_show_txt(scr, 'SCORE:'+str(paddleL.score), font64, 20, 20, paddleL.c)
    RT_show_txt(scr, 'SCORE:'+str(paddleR.score), font64, 750, 20, paddleR.c)
        
#----pygame init-----pygame初始化
pygame.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption('RT - PingPong Ball')  #窗口命名
clock = pygame.time.Clock() #帧率定时器初始化
font64 = pygame.font.Font('simkai.ttf', 64)

#----data init------
ball = CLS_ball(10, 10, 2, 2, 3)  #生成小球对象
ball2 = CLS_ball(100, 10, 2.5, 1.5, 4)  #小球2
paddleL = CLS_paddle(0, 200, 10, 150, c = (0,0,255) )  #球拍对象初始化
paddleR = CLS_paddle( SCREEN_W - BORDER_W, 200, 10, 150, c = (0,0,255) )
net = CLS_paddle( SCREEN_W // 2, SCREEN_H - 150, 10, 150, c = (128,128,128) )
net.type = 1

pixel = []
pixel.append('....DD....')
pixel.append('..DDAADD..')
pixel.append('.DDDAADDD.')
pixel.append('.DDDAADDD.')
pixel.append('DDDDAADDDD')
pixel.append('DDDDAADDDD')
pixel.append('.DDDAADDD.')
pixel.append('.DDDAADDD.')
pixel.append('..DDAADD..')
pixel.append('....DD....')
ball.add_pic( pixel )
ball2.add_pic( pixel )

pixel = []
pixel.append('....DD....')
pixel.append('..DDDDDD..')
pixel.append('.DDDDDDAD.')
pixel.append('.DDDDDAAD.')
pixel.append('DDDDDAADDD')
pixel.append('DDDDAADDDD')
pixel.append('.DDAADDDD.')
pixel.append('.DAADDDDD.')
pixel.append('..DDDDDD..')
pixel.append('....DD....')
ball.add_pic( pixel )
ball2.add_pic( pixel )

pixel = []
pixel.append('....DD....')
pixel.append('..DDDDDD..')
pixel.append('.DDDDDDDD.')
pixel.append('.DDDDDDDD.')
pixel.append('DAAAAAAAAD')
pixel.append('DAAAAAAAAD')
pixel.append('.DDDDDDDD.')
pixel.append('.DDDDDDDD.')
pixel.append('..DDDDDD..')
pixel.append('....DD....')
ball.add_pic( pixel )
ball2.add_pic( pixel )


pixel = []
pixel.append('....DD....')
pixel.append('..DDDDDD..')
pixel.append('.DADDDDDD.')
pixel.append('.DAADDDDD.')
pixel.append('DDDAADDDDD')
pixel.append('DDDDAADDDD')
pixel.append('.DDDDAADD.')
pixel.append('.DDDDDAAD.')
pixel.append('..DDDDDD..')
pixel.append('....DD....')
ball.add_pic( pixel )
ball2.add_pic( pixel )

soundPong2 = pygame.mixer.Sound('pong2.wav')
soundPong4 = pygame.mixer.Sound('pong4.wav')
soundGo = pygame.mixer.Sound('readygo.wav')
pygame.mixer.music.load('plantzombie.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
soundGo.play()

set_new_ball(ball)
gameStatus = 0   #0:正常  1:四球
key = '' #2.2a 怎加作弊
#------- main loop --------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            #add in V2.2a
            if 0 <= event.key <= 128:
                key += chr(event.key)
            if key[-3:] == 'iop': #如果最后三个是iop 球自动向相反方向
                ball.spdX *= -1
            if key[-3:] =='jkl':  #如果最后三个是jkl 球网增高
                net.y -= 50
                net.h += 50
            if key[-3:] == 'bnm':
                net.y += 50
                net.h -= 50
            #以上是作弊代码
            if event.key == ord('w'):
                paddleL.accY = -0.2
            elif event.key == ord('s'):
                paddleL.accY = 0.2
            elif event.key == pygame.K_UP:
                paddleR.accY = -0.2
            elif event.key == pygame.K_DOWN:
                paddleR.accY = 0.2
            elif event.key == pygame.K_SPACE and gameStatus == 1:
                set_new_ball(ball)
                gameStatus = 0
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                paddleR.spdY = 0
                paddleR.accY = 0
            if event.key in (ord('w'), ord('s')):
                paddleL.spdY = 0
                paddleL.accY = 0
        

    screen.fill((0,64,0))
    draw_field( screen )
    ball.move( )
    ball.draw( screen )
    ball2.move( )
    ball2.draw( screen )
    paddleL.move( )
    paddleL.draw( screen )
    paddleR.move( )
    paddleR.draw( screen )
    net.move( )
    net.draw( screen )
    pygame.display.update()
    clock.tick(200)  #FPS Frame Per Second



