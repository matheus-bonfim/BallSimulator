import PySimpleGUI as sg
import pygame
import math



WIDTH, HEIGHT = 700, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bola queda livre")

RED = (255,0,0)
BLACK = (0,0,0)

class Bola:

    G = 9.80665
    def __init__(self, vel, angulo, x, y, color, radius, coefRest):
        self.vel = vel
        self.x, self.y = x, y
        self.color = color
        self.radius = radius
        self.angulo = math.radians(angulo)
        if coefRest < 1 :
            self.coefRest = 1 - coefRest
        else: 
            self.coefRest = 0
        self.vel_y = -math.sin(self.angulo) * vel
        self.vel_x = math.cos(self.angulo) * vel
        self.perda = 0
        self.alfa = 1
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

    def update_position(self, tempo, contadorx, directionX, directionY, collision):
        
        self.x += self.vel_x * directionX * self.alfa

        if contadorx == 0:
            if self.vel_x < 0:
                self.alfa = -1 
    
            self.vel_x = self.vel_x - self.coefRest * self.vel_x


        if collision == True:

            if directionY == False:
                
                self.y = self.y - self.vel_instBaixo + self.G*tempo
                self.vel_instCima = -(- self.vel_instBaixo + self.G*tempo)
                if tempo == 0:
                    self.vel_instBaixo = self.vel_instBaixo - self.coefRest * self.vel_instBaixo
                    
            
            if directionY == True: #colide com o chao
                
                self.y = self.y  + self.vel_instCima + self.G*tempo 
                self.vel_instBaixo =  self.vel_instCima + self.G*tempo 
                if tempo == 0:
                    self.vel_instCima = self.vel_instCima - self.coefRest * self.vel_instCima
        else:
            self.y = self.y + self.vel_y + self.G*tempo
            self.vel_instCima = -(self.vel_y + self.G*tempo)
            self.vel_instCima = self.vel_instCima - self.coefRest * self.vel_instCima

            self.vel_instBaixo = self.vel_y + self.G*tempo
            self.vel_instBaixo = self.vel_instBaixo - self.coefRest * self.vel_instBaixo
  
def main(angulo, velocidade, coeficiente):
    run = True
    pao = True
    clock = pygame.time.Clock()
    bolinha = Bola(velocidade, angulo, 10, 400, RED, 10, coeficiente)

    main_font = pygame.font.SysFont("arial", 20)

    info = main_font.render(f"Aperte V para voltar ou X para fechar", 1, (255, 255, 255))
    tempo = 0
    contador = 0
    directionX = 1
    directionY = False
    collision = False
    contadorx = 0
    
    
    G = 10
    coefResBall = 0.47
    while run:
        clock.tick(60)
        WIN.fill(BLACK)

        WIN.blit(info, (20, 750))

        contador += 1
        contadorx += 1
        if contador % 60 == 0:
            print(tempo)
            tempo = tempo + 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if bolinha.x >= WIDTH:
            directionX = -1
            contadorx = 0

        elif bolinha.x <= 0:
            directionX = 1
            contadorx = 0
        
        if bolinha.y >= HEIGHT:
            contador = 0
            collision = True
            directionY = True
            
            

        if bolinha.y <= 0:
            contador = 0
            collision = True
            directionY = False
            

       
        bolinha.draw(WIN)
        bolinha.update_position(contador/60, contadorx, directionX, directionY, collision)
            
        pygame.display.update()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_v]:
            janela()
            run = False

        if keys[pygame.K_x]:
            run = False

    pygame.quit()
    exit()

def AbrirJanela():

    LAYOUT = [[sg.Text("Escolha o ângulo de lançamento.")],
            [sg.Input(size=(5,0), key="angulo")],
            [sg.Text("Escolha a velocidade de lançamento.")],
            [sg.Input(size=(5,0), key="velocidade")],
            [sg.Text("Escolha o coeficiente de restituição de 0 a 1 incluso")],
            [sg.Input(size=(5,0), key="Coef")],
            [sg.Button("OK")]]   
     
    return sg.Window('Simulador de bolinha', layout=LAYOUT, finalize=True)

def janela():
    run = True
    janelinha = AbrirJanela()

    while run:
        window, event, values = sg.read_all_windows()
        
        if window == janelinha:
            if event == sg.WIN_CLOSED: 
                run = False 

            if event == "OK":
                janelinha.hide()
                
                try:
                    angulo = float(values["angulo"])
                    velocidade = float(values["velocidade"])
                    coeficiente = float(values["Coef"])
                except:
                    sg.Popup("Escreva apenas números!")
                    janela()
                pygame.init()
                main(angulo, velocidade, coeficiente)
    exit()
                
janela()