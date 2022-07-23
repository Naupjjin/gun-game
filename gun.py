import pygame
from pygame.locals import QUIT
import random
import os
import time
WIDTH=1400
HEIGHT=700
BLACK=(0,0,0)
player_img_size=(79,93)
enemy_img_size=(113,174.5)
bullet_img_size=(20,10)
light_img_size=(1400,5)
plushp_img_size=(50,30)
score=0
WINDOW=pygame.display.set_mode((WIDTH,HEIGHT))

clock=pygame.time.Clock()
WINDOW.fill((0,0,0))
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("GUN")
player_img=pygame.image.load(os.path.join("img","player.png"))
enemy_img=pygame.image.load(os.path.join("img","enemy.png"))
bullet_img=pygame.image.load(os.path.join("img","bullet.png"))
light_img=pygame.image.load(os.path.join("img","light.png"))
plushp_img=pygame.image.load(os.path.join("img","plushp.png"))

gun_mp3=pygame.mixer.Sound(os.path.join("sound","gun.mp3"))
A_mp3=pygame.mixer.Sound(os.path.join("sound","A.mp3"))
lose_mp3=pygame.mixer.Sound(os.path.join("sound","lose.mp3"))
enemyhit_mp3=pygame.mixer.Sound(os.path.join("sound","enemyhit.mp3"))
hp_mp3=pygame.mixer.Sound(os.path.join("sound","hp.mp3"))

player_img=pygame.transform.scale(player_img,player_img_size)
enemy_img=pygame.transform.scale(enemy_img,enemy_img_size)
bullet_img=pygame.transform.scale(bullet_img,bullet_img_size)
light_img=pygame.transform.scale(light_img,light_img_size)
plushp_img=pygame.transform.scale(plushp_img,plushp_img_size)

font_name=pygame.font.match_font("arial")

pygame.display.set_icon(player_img)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=player_img
        self.rect=self.image.get_rect()
        self.rect.x=WIDTH-100
        self.rect.y=20
        self.speed=10
        self.health=100
        
    def update(self):
        key_pressed=pygame.key.get_pressed()
        if key_pressed[pygame.K_w]:
            self.rect.y-=self.speed
        if key_pressed[pygame.K_s]:    
            self.rect.y+=self.speed
        if key_pressed[pygame.K_a]:    
            self.rect.x-=self.speed
        if key_pressed[pygame.K_d]:    
            self.rect.x+=self.speed

        if self.rect.x<0:
            self.rect.x=0
        if self.rect.right>WIDTH:
            self.rect.right=WIDTH
        if self.rect.y<0:
            self.rect.y=0
        if self.rect.bottom>HEIGHT:
            self.rect.bottom=HEIGHT
    def shoot(self):
        bullet=Bullet(self.rect.x,self.rect.centery)
        
        bullets_sprites.add(bullet)
        gun_mp3.play()

            
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=enemy_img
        self.rect=self.image.get_rect()
        self.radius=60
        self.rect.x=0
        self.rect.y=random.randrange(0,HEIGHT-175)
        self.speedx=random.randrange(10,20)
        self.speedy=random.randrange(-3,3) 

    def update(self):
        self.rect.x+=self.speedx
        self.rect.y+=self.speedy
        if self.rect.x>WIDTH:
            self.rect.x=0
            self.rect.y=random.randrange(0,HEIGHT-175)
            self.speedx=random.randrange(1,10)
            self.speedy=random.randrange(-10,10)
        if self.rect.top<0:
            self.y=0
            self.speedy=3
        if self.rect.bottom>HEIGHT:
            self.rect.bottom=HEIGHT
            self.speedy=-3
        

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        
        self.image=bullet_img  
        self.image.set_colorkey((255,255,255))
        self.rect=self.image.get_rect()
        self.radius=15
        self.rect.x=x
        self.rect.y=y
        self.speedx=-15
    
    def update(self):
        self.rect.x+=self.speedx
        if self.rect.x<0 or self.rect.y<0 or self.rect.bottom>700:
            self.kill()

class Light(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=light_img
        self.rect=self.image.get_rect()
        self.rect.top=0  
        self.rect.x=0
        self.speedy=10
    def update(self):
        self.rect.y+=self.speedy 
        if self.rect.bottom>350 :
          self.kill()  

class Light2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=light_img
        self.rect=self.image.get_rect()
        self.rect.bottom=700
        self.rect.x=0
        self.speedy=-10
    def update(self):
        self.rect.y+=self.speedy 
        if self.rect.bottom<350 :
          self.kill()  

class Hp_box(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=plushp_img
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.speedx=20
    def update(self):
        self.rect.x+=self.speedx
        if self.rect.right>1400:
            self.kill()
        
def Overload_the_enemy():
    
    enemy=Enemy()

    enemy_sprites.add(enemy)

def draw_health(surf,hp,x,y):
    WIDTH_D=100
    HEIGHT_D=10
    fill=(hp/1400)*WIDTH
    box_rect=pygame.Rect(x,y,WIDTH_D,HEIGHT_D)
    fill_rect=pygame.Rect(x,y,fill,HEIGHT_D)
    pygame.draw.rect(surf,(0,255,0),fill_rect)
    pygame.draw.rect(surf,(255,255,255),box_rect,2)

def draw_text(surf,text,size,x,y):
    score_font=pygame.font.Font(font_name,size)
    text_surface=score_font.render(text,True,(255,255,255))
    text_rect=text_surface.get_rect()
    text_rect.centerx=x
    text_rect.top=y
    surf.blit(text_surface,text_rect)

def draw_init():
    
    draw_text(WINDOW,"GUN",200,700,100)
    draw_text(WINDOW,"Press WASD to move.",30,700,350)
    draw_text(WINDOW,"Left mouse button launch.",30,700,400)
    draw_text(WINDOW,"Press any key to start.",30,700,450)
    draw_text(WINDOW,"Medical kits can restore blood.",30,700,500)

    pygame.display.update()
    wait=True
    while wait:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                
            elif event.type==pygame.KEYUP:
               wait=False 
               time.sleep(0.5)
               

player_sprites=pygame.sprite.Group()
bullets_sprites=pygame.sprite.Group()
enemy_sprites=pygame.sprite.Group()
light_sprites=pygame.sprite.Group()
hp_box_sprites=pygame.sprite.Group()

player=Player()
player_sprites.add(player)
running=True
n=0

for i in range(5):
    Overload_the_enemy()

show_init=True

while running:

    if show_init:
        draw_init()        
        show_init=False


    #FPS
    clock.tick(100)
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        elif event.type==pygame.MOUSEBUTTONDOWN	:
            
            pygame.mixer.music.set_volume(0.3)
            player.shoot()

    #繪製和運行
    #WINDOW.blit(player_img,(1000,0))
    #WINDOW.blit(enemy_img,(0,0))

    WINDOW.fill(BLACK)
    
    player_sprites.draw(WINDOW)
    player_sprites.update()
    bullets_sprites.draw(WINDOW)
    bullets_sprites.update()
    enemy_sprites.draw(WINDOW)
    enemy_sprites.update()
    light_sprites.draw(WINDOW)
    light_sprites.update()

    hp_box_sprites.draw(WINDOW)
    hp_box_sprites.update()
    #碰撞
    hits1=pygame.sprite.groupcollide(bullets_sprites,enemy_sprites,True,True,pygame.sprite.collide_circle)
    hits2=pygame.sprite.groupcollide(player_sprites,enemy_sprites,False,True)
    hits3=pygame.sprite.groupcollide(player_sprites,light_sprites,False,False)
    hits4=pygame.sprite.groupcollide(player_sprites,hp_box_sprites,False,True)
    
    for i in hits1:
        Overload_the_enemy()
        score+=1
        #0.5
        pygame.mixer.music.set_volume(0.5)
        enemyhit_mp3.play()
        
        if 1==random.randint(1,10):
            hp_box=Hp_box(0,random.randint(0,HEIGHT-30)) 
            hp_box_sprites.add(hp_box)

    for i in hits4:
        player.health+=10 
        pygame.mixer.music.set_volume(1)
        hp_mp3.play()

    if hits1 :
        n+=1
        

    if n>4:
        b=random.randint(1,2)
        if b==1:
            light=Light()
            light_sprites.add(light)
            n=0
        elif b==2:
            light=Light2()
            light_sprites.add(light)
            n=0


    for hit in hits2:

        player.health-=10

        Overload_the_enemy()
         
        if player.health<=0:
            
            running=False 

    if hits3:
        player.health-=1  
        A_mp3.play()

        
        if player.health<=0:    
            running=False 

    if player.health>100:
        player.health=100
    draw_health(WINDOW,player.health,player.rect.x-10,player.rect.y-10)   
    draw_text(WINDOW,str(score),18,WIDTH/2,10) 
    pygame.display.flip()
    pygame.display.update()

time.sleep(1)
if player.health<=0:
    lose_mp3.play()
    time.sleep(3.3)
pygame.quit()
