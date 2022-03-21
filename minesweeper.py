import pygame, settings, math, random

class Cell:
    def __init__(self, _screen, _font) -> None:
        self.shown = False

        self.render = None
        self.textPos = None

        self.value = 0

        self.screen = _screen
        self.font = _font

    def renderText(self):
        self.render = self.font.render(str(self.value), 1, settings.WHITE)
        self.textPos = self.render.get_rect()

    def drawBomb(self, pos):
        pygame.draw.circle(self.screen, settings.WHITE, pos, settings.CUBESIZE / 2 * 0.8, 3)

    def show(self, pos):
        if self.shown:
            pygame.draw.rect(self.screen, settings.GREY, (pos[0]+1, pos[1]+1, settings.CUBESIZE-2, settings.CUBESIZE-2))

            pos[0] += settings.CUBESIZE / 2
            pos[1] += settings.CUBESIZE / 2

            if self.value == -1:
                self.drawBomb(pos)
            elif self.render:
                self.textPos.center = pos
                self.screen.blit(self.render, self.textPos)
            else:
                pass #draw nothing or shit

class minesweeper:
    size = 10
    amountBombs = 20

    def __init__(self, _screen) -> None:
        self.screen = _screen
        self.clicked = False

        self.initFont()
        self.setupDraw()

        self.reset()
        self.placeBombs()

    def initFont(self):
        self.font = pygame.font.SysFont('Comic Sans MS',int(settings.CUBESIZE * 0.6))

    def reset(self):
        self.game = [[Cell(self.screen, self.font) for _ in range(self.size)] for __ in range(self.size)]  #-1 = bomb | rest = number

    def placeBombs(self):
        for i in range(self.amountBombs):
            while True:
                x = random.randint(0, self.size-1)
                y = random.randint(0, self.size-1)

                if self.game[x][y].value != -1:
                    break

            for j in range(3):
                j -= 1
                for k in range(3):
                    k -= 1
                    if x+k < self.size and y + j < self.size and x + k >= 0 and y + j >= 0 and self.game[x+k][y+j].value != -1: #check for bomb
                        self.game[x+k][y+j].value += 1
                        self.game[x+k][y+j].renderText()

            self.game[x][y].value = -1
            self.game[x][y].renderText()

    def update(self, dt, keys, mouse):
        if pygame.mouse.get_pressed()[0] and not self.clicked:
            self.clicked = True

            i, j = self.getMouseFieldIndex(mouse)

            if i != -1 and j != -1:
                self.game[i][j].shown = True

        if self.clicked and not pygame.mouse.get_pressed()[0]:
            self.clicked = False

    def getMouseFieldIndex(self, pos):
        x = pos[0] - self.startX
        y = pos[1] - self.startY

        if x >= 0 and y >= 0 and x <= settings.CUBESIZE * self.size and y <= settings.CUBESIZE * self.size:
            i = math.floor(x / settings.CUBESIZE)
            j = math.floor(y / settings.CUBESIZE)

            return i, j

        return -1, -1

    def setupDraw(self):
        if self.size % 2 == 0:
            self.startX = settings.WIDTH / 2 - (settings.CUBESIZE * math.floor(self.size / 2))
            self.startY = settings.HEIGHT/ 2 - (settings.CUBESIZE * math.floor(self.size / 2))
        else:
            self.startX = settings.WIDTH / 2 - settings.CUBESIZE / 2 - (settings.CUBESIZE * math.floor(self.size / 2))
            self.startY = settings.HEIGHT/ 2 - settings.CUBESIZE / 2 - (settings.CUBESIZE * math.floor(self.size / 2))

    def drawRect(self, pos):
        pygame.draw.rect(self.screen, settings.WHITE, (pos[0], pos[1], settings.CUBESIZE, settings.CUBESIZE), width=1)

    def draw(self):
        for i in range(self.size):
            for j in range(self.size):
                posX = self.startX + settings.CUBESIZE * i
                posY = self.startY + settings.CUBESIZE * j
                
                self.drawRect((posX, posY))
                self.game[i][j].show([posX, posY])
