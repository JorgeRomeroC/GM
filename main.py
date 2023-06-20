import pygame
import random

# inicializamos la libreria pygame
pygame.init()
# cargamos los audios
pygame.mixer.init()

# Cragamos los recurosos del video juego
fondo = pygame.image.load('imagenes/fondo.jpg')
fondo2 = pygame.image.load('imagenes/fondo_bienvenida.jpg')
laser_sonido = pygame.mixer.Sound('sonidos/laser.wav')
explosion_sonido = pygame.mixer.Sound('sonidos/explosion.wav')
golpe_sonido = pygame.mixer.Sound('sonidos/golpe.wav')

# Cargando musica de fondo
pygame.mixer.music.load('sonidos/bg_sonido.mp3')
pygame.mixer.music.play(-1)

# recorremos la lista de explosiones
explosion_list = []
for i in range(1, 13):
    explosion = pygame.image.load(f'explosion/{i}.png')
    explosion_list.append(explosion)

# Manejamos la pantalla y sus dimensiones
width = fondo.get_width()
height = fondo.get_height()
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Guerra de los Mundos')
#   el juego se este constantemente inicializado
run = True
# velocidad del juego
fps = 60
# manejar el tiempo
clock = pygame.time.Clock()
# guadaremos el puntaje del jugador
score = 0
vida = 100
blanco = (255, 255, 255)
negro = (0, 0, 0)
blanco_bienvenida = (255, 255, 255)


# funcion que define el texto de puntaje
def texto_puntuacion(frame, text, size, x, y):
    font = pygame.font.SysFont('Calibri', 20, bold=False)
    text_frame = font.render(text, True, blanco, negro)
    text_rect = text_frame.get_rect()
    text_rect.midtop = (960, 10)
    frame.blit(text_frame, text_rect)


# funcion que definie el texto de bienvenida
def texto_bienvenida(frame, text, size, x, y, color_texto):
    font = pygame.font.SysFont('Calibri', size, bold=False)
    text_frame = font.render(text, True, color_texto)
    text_rect = text_frame.get_rect()
    text_rect.midtop = (x, y)
    frame.blit(text_frame, text_rect)


def mostrar_pantalla_bienvenida():
    window.blit(fondo2, (0, 0))
    texto_bienvenida(window, "¡Bienvenido a la Guerra de los Mundos!", 40, width // 2, height // 2, blanco_bienvenida)
    pygame.draw.rect(window, negro, (width // 2 - 75, height // 2 + 50, 150, 50))
    texto_bienvenida(window, "Jugar", 30, width // 2, height // 2 + 55, blanco_bienvenida)
    pygame.display.flip()


mostrar_pantalla_bienvenida()
pantalla_inicio = True


def barra_vida(frame, x, y, nivel):
    longitud = 200
    alto = 20
    fill = int((nivel / 100) * longitud)
    border = pygame.Rect(670, 10, longitud, alto)
    fill = pygame.Rect(670, 10, fill, alto)
    pygame.draw.rect(frame, (255, 0, 55), fill)
    pygame.draw.rect(frame, negro, border, 3)


class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # cargamos la imagen de  la nave
        self.image = pygame.image.load('imagenes/nave.png').convert_alpha()
        # cargamos la imagen de la nave como un icono en la barra de herramientas
        pygame.display.set_icon(self.image)
        self.rect = self.image.get_rect()
        # establecemos la posicion de la ventana
        self.rect.centerx = width // 2
        self.rect.centery = height - 50
        self.velocidad_x = 0
        self.vida = 100

    # obtenemo la lectura de las teclas del usuario
    def update(self):
        self.velocidad_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.velocidad_x = -5
        elif keystate[pygame.K_RIGHT]:
            self.velocidad_x = 5

        self.rect.x += self.velocidad_x
        if self.rect.right > width:
            self.rect.right = width
        elif self.rect.left < 0:
            self.rect.left = 0

    def disparar(self):
        bala = Balas(self.rect.centerx, self.rect.top)
        grupo_jugador.add(bala)
        grupo_balas_jugador.add(bala)
        laser_sonido.play()


class Enemigos(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('imagenes/alien.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(1, width - 30)
        self.rect.y = 50
        self.velocidad_y = random.randrange(-5, 20)

    def update(self):
        self.time = random.randrange(-1, pygame.time.get_ticks() // 5000)
        self.rect.x += self.time
        if self.rect.x >= width:
            self.rect.x = 0
            self.rect.y += 50

    def disparar_enemigos(self):
        bala = Balas_enemigos(self.rect.centerx, self.rect.bottom)
        grupo_jugador.add(bala)
        grupo_balas_enemigos.add(bala)
        laser_sonido.play()


class Balas(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('imagenes/B2.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        # establecemos la direccion de las balas, hacia arriba
        self.velocidad = -18

    def update(self):
        self.rect.y += self.velocidad
        if self.rect.bottom < 0:
            self.kill()


class Balas_enemigos(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('imagenes/B1.png').convert_alpha()
        self.image = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = random.randrange(10, width)
        self.velocidad_y = 4

    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.bottom > height:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = explosion_list[0]
        img_scala = pygame.transform.scale(self.image, (20, 20))
        self.rect = img_scala.get_rect()
        self.rect.center = position
        self.time = pygame.time.get_ticks()
        self.velocidad_explo = 30
        self.frames = 0

    def update(self):
        tiempo = pygame.time.get_ticks()
        if tiempo - self.time > self.velocidad_explo:
            self.time = tiempo
            self.frames += 1
            if self.frames == len(explosion_list):
                self.kill()
            else:
                position = self.rect.center
                self.image = explosion_list[self.frames]
                self.rect = self.image.get_rect()
                self.rect.center = position


grupo_jugador = pygame.sprite.Group()
grupo_enemigos = pygame.sprite.Group()
grupo_balas_jugador = pygame.sprite.Group()
grupo_balas_enemigos = pygame.sprite.Group()

player = Jugador()
grupo_jugador.add(player)
grupo_balas_jugador.add(player)

for x in range(10):
    enemigo = Enemigos(10, 10)
    grupo_enemigos.add(enemigo)
    grupo_jugador.add(enemigo)

while run:
    while run:
        if pantalla_inicio:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if width // 2 - 75 <= event.pos[0] <= width // 2 + 75 and height // 2 + 50 <= event.pos[1] <= height // 2 + 100:
                        pantalla_inicio = False
            mostrar_pantalla_bienvenida()
        else:

            clock.tick(fps)
            window.blit(fondo, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player.disparar()

            grupo_jugador.update()
            grupo_enemigos.update()
            grupo_balas_jugador.update()
            grupo_balas_enemigos.update()

            grupo_jugador.draw(window)

            # Coliciones  balas_jugador -  enemigo
            colicion1 = pygame.sprite.groupcollide(grupo_enemigos, grupo_balas_jugador, True, True)
            for i in colicion1:
                score += 10
                enemigo.disparar_enemigos()
                enemigo = Enemigos(300, 10)
                grupo_enemigos.add(enemigo)
                grupo_jugador.add(enemigo)

                explo = Explosion(i.rect.center)
                grupo_jugador.add(explo)
                explosion_sonido.set_volume(0.3)
                explosion_sonido.play()

            # Coliciones  jugador - balas_enemigo
            colicion2 = pygame.sprite.spritecollide(player, grupo_balas_enemigos, True)
            for j in colicion2:
                player.vida -= 10
                if player.vida <= 0:
                    run = False
                explo1 = Explosion(j.rect.center)
                grupo_jugador.add(explo1)
                golpe_sonido.play()

                # Coliciones  jugador - enemigo
            hits = pygame.sprite.spritecollide(player, grupo_enemigos, False)
            for hit in hits:
                player.vida -= 100
                enemigos = Enemigos(10, 10)
                grupo_jugador.add(enemigos)
                grupo_enemigos.add(enemigos)
                if player.vida <= 0:
                    run = False
            # Indicador y Score
            texto_puntuacion(window, ('  Puntaje: ' + str(score) + '       '), 30, width - 85, 2)
            barra_vida(window, width - 285, 0, player.vida)

            pygame.display.flip()
pygame.quit()
