import pygame
import random
import math

pygame.init()
windowWidth = 1200
windowHeight = 800
win = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Dodger")
icon = pygame.image.load('resources/bitmap.png')
pygame.display.set_icon(icon)
hScoreFile = open('resources/hscore.txt', 'r')
score = 0
hScore = hScoreFile.read()
if not int(float((hScore))) > 1:
    hScore = 0
hScoreFile.close()


class Player(object):
    def __init__(self, xPos, yPos, width, height, vel):
        self.xPos = xPos
        self.yPos = yPos
        self.width = width
        self.height = height
        self.vel = vel
        self.color = (114, 119, 133)

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.xPos,
                                           self.yPos, self.width, self.height))


numberOfEnemies = 10
enemyXPos = []
enemyYPos = []
enemyHeight = []
enemyWidth = []
enemyVelY = []
enemyVelX = []
enemyDistance = []

enemyColor = (255, 0, 0)
for enemyx in range(numberOfEnemies):
    enemyXPos.append(1)
    enemyYPos.append(1)
    enemyHeight.append(1)
    enemyWidth.append(1)
    enemyVelY.append(1)
    enemyVelX.append(1)
    enemyDistance.append(1)


def addEnemies():
    global numberOfEnemies, enemyXPos, enemyYPos, enemyHeight, enemyWidth, enemyVelX, enemyVelX
    for i in range(numberOfEnemies):
        enemyXPos[i] = 1
        enemyYPos[i] = random.randint(50, windowHeight)
        enemyHeight[i] = 30
        enemyWidth[i] = 30
        enemyVelX[i] = random.randint(1, 5)
        enemyVelY[i] = random.randint(1, 5)


def enemyDraw():
    global enemyColor, numberOfEnemies, enemyXPos, enemyYPos, enemyHeight, enemyWidth, enemyVelX, enemyVelY
    for i in range(numberOfEnemies):
        pygame.draw.rect(
            win, enemyColor, (enemyXPos[i], enemyYPos[i], enemyWidth[i], enemyHeight[i]))


def enemyMove():
    global enemyVelY, enemyVelX, enemyXPos, enemyYPos, player1, enemyDistance, numberOfEnemies, targetYPos, score, gameOver
    for i in range(numberOfEnemies):
        enemyXPos[i] += enemyVelX[i]
        enemyYPos[i] += enemyVelY[i]
        if enemyXPos[i] <= 0 or enemyXPos[i] >= windowWidth - enemyWidth[i]:
            enemyVelX[i] *= -1
        if enemyYPos[i] <= 0 or enemyYPos[i] >= windowHeight - enemyHeight[i]:
            enemyVelY[i] *= -1

        enemyDistance[i] = math.sqrt(math.pow(
            enemyXPos[i] - player1.xPos, 2) + math.pow(enemyYPos[i] - player1.yPos, 2))

        if enemyDistance[i] <= 30:
            for j in range(numberOfEnemies):
                enemyXPos[j] = windowWidth + 1000
                enemyYPos[j] = windowHeight + 2000
                enemyVelX[j] = 0
                enemyVelY[j] = 0
                newHS(score)
                gameOver = 1

                targetYPos = windowHeight+5000
                pygame.display.set_caption("Dodger    Score: "+str(score))
                score = 0

            break


targetYPos = random.randint(0, windowHeight-50)
targetXPos = random.randint(0, windowWidth-50)


def targetRandom():
    global targetYPos, targetXPos
    targetYPos = random.randint(0, windowHeight-50)
    targetXPos = random.randint(0, windowWidth-50)


def addTarget(targetXPos, targetYPos):
    targetColor = (64, 235, 52)
    pygame.draw.rect(win, targetColor, (targetXPos, targetYPos, 30, 30))


def targetCollision():
    global targetXPos, targetYPos, player1, score
    targetDistance = math.sqrt(
        math.pow(targetXPos-player1.xPos, 2)+math.pow(targetYPos-player1.yPos, 2))
    if targetDistance <= player1.width or targetDistance <= player1.height:
        score += 1
        newHS(score)
        targetRandom()


def newHS(score):
    global hScore
    hScore = int(hScore)
    if score > hScore:
        hScoreFile = open('resources/hscore.txt', 'w')
        hScoreFile.write(str(score))
        hScoreFile.close()
        hScore = score


def gameOverFunction(gameOverCall):
    global win, fontGameOver
    if gameOverCall == 1:

        gameOverText = fontGameOver.render("GAME OVER", 1, (124, 129, 143))
        win.blit(gameOverText, (25, 200))


def drawing():
    global score, hScore, gameOver

    win.fill((255, 255, 255))
    scoreText = font.render('Score: '+str(score), 1, (124, 129, 143))
    hScoreText = fontHS.render('High Score: '+str(hScore), 1, (124, 129, 143))
    gameOverFunction(gameOver)
    player1.draw(win)
    win.blit(scoreText, (50, 50))
    win.blit(hScoreText, (50, 100))
    addTarget(targetXPos, targetYPos)
    enemyDraw()

    pygame.display.update()


fontGameOver = pygame.font.SysFont('arial', 180, True)
font = pygame.font.SysFont("arial", 30, True)
fontHS = pygame.font.SysFont("arial", 20, True)
player1 = Player(400, 400, 30, 30, 8)
music = pygame.mixer.music.load('resources/bgMusic.wav')
pygame.mixer.music.set_volume(0.09)
pygame.mixer.music.play(-1)
gameOver = 0


addEnemies()
# mainloop
run = True
while run:
    pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    # controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player1.yPos > 0:
        player1.yPos -= player1.vel
    if keys[pygame.K_DOWN] and player1.yPos < windowHeight - player1.height:
        player1.yPos += player1.vel
    if keys[pygame.K_LEFT] and player1.xPos > 0:
        player1.xPos -= player1.vel
    if keys[pygame.K_RIGHT] and player1.xPos < windowWidth - player1.width:
        player1.xPos += player1.vel
    if keys[pygame.K_r]:
        addEnemies()
        newHS(score)
        pygame.display.set_caption("Dodger")
        score = 0
        gameOver = 0
        targetRandom()
    targetCollision()
    enemyMove()
    drawing()
