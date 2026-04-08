import pygame
import random

class Text:
    def __init__(self, surface, text, size, color, x, y):
        self.surface = surface
        self.text = text
        self.size = size
        self.color = color
        self.x = x
        self.y = y
        font_name = pygame.font. match_font("twcencondensedextra")
        self.font = pygame.font.Font(font_name, self.size)
    def draw(self):
        text_surface = self.font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (self.x, self.y)
        self.surface.blit(text_surface, text_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y,image,scale):
        pygame.sprite.Sprite.__init__(self)
        self.width = image.get_width()
        self.height = image.get_height()
        self.image = pygame.transform.scale(image,(int(self.width*scale),int(self.height*scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.speed = 3
        self.scale = scale
        self.picture = image
    
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] == 1:
            self.rect.y -= self.speed
        if keys[pygame.K_a] == 1:
            self.rect.x -= self.speed
        if keys[pygame.K_s] == 1:
            self.rect.y += self.speed
        if keys[pygame.K_d] == 1:
            self.rect.x += self.speed

    def bigger(self,size):
        self.scale += size
        x,y = self.rect.center
        self.image = pygame.transform.scale(self.picture,(int(self.width*self.scale),int(self.height*self.scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

myface = pygame.image.load("sprites/me.png")
myface2 = pygame.image.load("sprites/me2.png")
guy = Player(640, 360, myface, 0.5)
time = 0
interval = 60

playergroup = pygame.sprite.Group()
playergroup.add(guy)
enemygroup = pygame.sprite.Group()
for i in range(0,8):
    guy2 = Player(random.randint(0,1280), random.randint(0,720), myface2, .2)
    enemygroup.add(guy2)
score = 0

loop = True


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("blue")

    if loop == True:
        scoretext = Text(screen,"Score: "+str(score),50,(0,0,0),80,15)
        scoretext.draw()

        if time >= interval:
            guy2 = Player(random.randint(0,1280), random.randint(0,720), myface2, .2)
            enemygroup.add(guy2)
            time = 0
            interval -= .5
        else:
            time += 1

        playergroup.draw(screen)
        playergroup.update()
        enemygroup.draw(screen)
        playercollisions = pygame.sprite.spritecollide(guy,enemygroup,True)
        for enemy in playercollisions:
            score += 1
            guy.speed += .1
            guy.bigger(.01)
        
        if score >= 100:
            loop = False

    if loop == False:
        screen.fill("black")
        scoretext = Text(screen,"YOU WIN!11!",200,(255,255,255),640,300)
        scoretext.draw()

    pygame.display.flip()

    clock.tick(60)
