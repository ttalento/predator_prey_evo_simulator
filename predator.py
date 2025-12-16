import pygame
import math
class predator(pygame.sprite.Sprite):
    

    def __init__(self, color, radius, x, y, id, Time_of_death, Time_of_reproduction, velocity, orientation, angular_v, Thirst):
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
        self.v = velocity
        self.theta = orientation
        self.omega = angular_v
        self.thirst = Thirst

    def update(self, next_angular_v, dt, width, height, custom_theta):
        x,y = self.rect.center
        if custom_theta==None:
            self.theta = (self.theta + self.omega*dt)%(2*math.pi)
            if x<6:
                if self.theta>math.pi/2 or self.theta<3*math.pi/2:
                    self.theta = math.pi - self.theta
                #self.omega = 0
            if x>width-6:
                if self.theta<math.pi/2 or self.theta>3*math.pi/2:
                    self.theta = math.pi - self.theta
                #self.omega = 0
            if y<6:
                if self.theta<math.pi:
                    self.theta = - self.theta
                #self.omega = 0
            if y>height-6:
                if self.theta>math.pi:
                    self.theta = - self.theta
                #self.omega = 0
        else:
            self.theta = custom_theta

        v_x = self.v*math.cos(self.theta)
        v_y = -self.v*math.sin(self.theta)
        self.rect.center = (x + v_x*dt, y + v_y*dt)
        self.omega = next_angular_v

        

    def reflect(self, wall_type):
        if wall_type=='vertical':
            self.theta = math.pi - self.theta
        else: # 'horizontal'
            self.theta = -self.theta
