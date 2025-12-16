import pygame

class food(pygame.sprite.Sprite):
    

    def __init__(self, color, radius, x, y, id, Time_of_death, Time_of_reproduction):
        super().__init__()
        self.image = pygame.Surface([radius * 2, radius * 2])
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.ID = id
        self.time_of_death = Time_of_death
        self.time_of_reproduction = Time_of_reproduction
