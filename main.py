import pygame
from settings import WIDTH, HEIGHT, FPS
from model import GameModel
from view import GameView
from controller import GameController

#Инициализация Экрана и игры
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Typing Dino MVC")
    clock = pygame.time.Clock()

    model = GameModel()
    view = GameView(screen)
    controller = GameController(model, view)

    while True:
        controller.update()
        controller.render()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
