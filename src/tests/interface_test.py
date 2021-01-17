import pygame

def main():
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600

    pygame.init()
    clock = pygame.time.Clock()
    fps = 60
    size = [1000, 600]
    bg = [255, 255, 255]
    window_surface = pygame.display.set_mode(size)

    screen = pygame.display.set_mode(size)

    image = pygame.image.load('../../drawable/buttons/red_button.png')
    image = pygame.transform.scale(image, (int(WINDOW_WIDTH/3), int(WINDOW_HEIGHT/8)))

    button = Button(image, 50, 100, 50, 100, "test")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        screen.fill(bg)

        button.draw(window_surface)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    sys.exit(0)


def timer_test():
    pygame.init()
    screen = pygame.display.set_mode((128, 128))
    clock = pygame.time.Clock()

    counter, text = 10, '10'.rjust(3)
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    font = pygame.font.SysFont('Consolas', 30)

    while True:
        for e in pygame.event.get():
            if e.type == pygame.USEREVENT:
                counter -= 1
                text = str(counter).rjust(3) if counter > 0 else 'boom!'
            if e.type == pygame.QUIT: break
        else:
            screen.fill((255, 255, 255))
            screen.blit(font.render(text, True, (0, 0, 0)), (32, 48))
            pygame.display.flip()
            clock.tick(60)
            continue
        break


def input_box_test():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    input_box1 = InputBox(100, 100, 140, 32)
    input_box2 = InputBox(100, 300, 140, 32)
    input_boxes = [input_box1, input_box2]
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            for box in input_boxes:
                box.handle_event(event)

        for box in input_boxes:
            box.update()

        screen.fill((30, 30, 30))
        for box in input_boxes:
            box.draw(screen)

        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    input_box_test()
    timer_test()