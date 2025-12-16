import pygame
import food
import predator
import random
import numpy as np
import queueee as q
import math
import matplotlib.pyplot as plt

green_c = (123, 194, 107)
food_c = (219, 95, 64)
predator_c = (50, 124, 217)
black = (0, 0, 0)
white = (255, 255, 255)
yellow = (252, 186, 3)


pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
timer = 0
dt = 0
global id_counter
id_counter = 1
time_multiplier = 5
minimum_dist_between_instances = 15 ## 15

# Food parameters
Start_food = 80 ## 50
food_LE = {'mean': 28, 'std': 7} ## 30, 7
food_reproduction = {'mean': 22, 'std': 4} ## 22, 4
avg_reproduction_num = {'mean': 4.5} ## 4
reproduction_radius = {'std': 75} ## 75
food_energy = 5 ## 5

# Predator parameters
Start_predators = 4 ## 4
predator_LE = {'mean': 22, 'std': 3} ## 42, 6
predator_reproduction = {'mean': 18, 'std': 2} ## 30, 2.5
avg_reproduction_pred = {'mean': 2} ## 2
reproduction_radius_pred = {'std': 20} ## 20
velocity_mod = {'mean': 18, 'std': 6} ## 35, 5
angular_velocity = {'mean':0, 'std':2} ## 0, 2
max_thirst = 30 ## 20
thirst_rate = 1.5 ## 1.1
vision_radius = 32 ## 32

pygame.display.set_caption('Sim')
font = pygame.font.Font('freesansbold.ttf', 14)

global all_sprites
all_sprites = pygame.sprite.Group()
food_sprites = pygame.sprite.Group()
predator_sprites = pygame.sprite.Group()
Q = q.queueee()



def find_Sprite(id, group):
    found = False
    for sprite in group:
        if sprite.ID == id:
            found = True
            return sprite
    if not found:
        print("no sprite with the given ID")
        return None

def process_event(event):
    id = event['ID']
    typee = event['Type']
    if (typee=='Death'):
        sprite = find_Sprite(id, all_sprites)
        sprite.kill()
    elif(typee=='Reproduction_f'):
        sprite = find_Sprite(id, all_sprites)
        position = sprite.rect.center
        num_of_babies = np.random.poisson(avg_reproduction_num['mean'])
        for i in range(num_of_babies):
            x_pick = random.randint(1,2)
            y_pick = random.randint(1,2)
            if x_pick == 1:
                x = np.random.normal(position[0]+minimum_dist_between_instances,reproduction_radius['std'])
            else:
                x = np.random.normal(position[0]-minimum_dist_between_instances,reproduction_radius['std'])
            
            if y_pick == 1:
                y = np.random.normal(position[1]+minimum_dist_between_instances,reproduction_radius['std'])
            else:
                y = np.random.normal(position[1]-minimum_dist_between_instances,reproduction_radius['std'])
            add_food(x,y)
    elif(typee=='Reproduction_p'):
        sprite = find_Sprite(id, predator_sprites)
        position = sprite.rect.center
        vel = sprite.v
        num_of_babies = np.random.poisson(avg_reproduction_pred['mean'])
        for i in range(num_of_babies):
            x_pick = random.randint(1,2)
            y_pick = random.randint(1,2)
            if x_pick == 1:
                x = np.random.normal(position[0]+minimum_dist_between_instances,reproduction_radius_pred['std'])
            else:
                x = np.random.normal(position[0]-minimum_dist_between_instances,reproduction_radius_pred['std'])
            
            if y_pick == 1:
                y = np.random.normal(position[1]+minimum_dist_between_instances,reproduction_radius_pred['std'])
            else:
                y = np.random.normal(position[1]-minimum_dist_between_instances,reproduction_radius_pred['std'])
            add_predator(x,y,vel)
                

def find_empty_place(x,y):
    found = False
    min_dist = minimum_dist_between_instances
    max_iter = 16
    iter = 0
    while not found:
        iter += 1
        instance_dist = distance_to_intances(x,y, all_sprites)
        inst_below_thresh = [ID for ID in instance_dist if instance_dist[ID]<=min_dist]
        if inst_below_thresh==[]:
            found = True
        else:
            vector = (0,0)
            for ID in inst_below_thresh:
                if iter>=max_iter:
                    return None,None
                else:
                    sprite = find_Sprite(ID, all_sprites)
                    center = sprite.rect.center
                    vector = (vector[0]+(x-center[0]), vector[1]+(y-center[1]))
            x,y = (x + vector[0]/np.linalg.norm(vector),y + vector[1]/np.linalg.norm(vector))
    return x,y


def add_food(x, y):
    global id_counter
    x,y = find_empty_place(x,y)
    if (x!=None and y!=None):
        inside_area = x>minimum_dist_between_instances and x<screen.get_width()-minimum_dist_between_instances and y>minimum_dist_between_instances and y<screen.get_height()-minimum_dist_between_instances
        if inside_area:
            new = food.food(food_c,3,x,y, id_counter, timer + np.random.normal(food_LE['mean'],food_LE['std']), timer + np.random.normal(food_reproduction['mean'], food_reproduction['std']))
            Q.add_event(new.ID, new.time_of_death, 'Death')
            if (new.time_of_death>new.time_of_reproduction):
                Q.add_event(new.ID, new.time_of_reproduction, 'Reproduction_f')
            all_sprites.add(new)
            food_sprites.add(new)
            id_counter+=1

def add_predator(x, y, vel):
    global id_counter
    x,y = find_empty_place(x,y)
    if (x!=None and y!=None):
        inside_area = x>minimum_dist_between_instances and x<screen.get_width()-minimum_dist_between_instances and y>minimum_dist_between_instances and y<screen.get_height()-minimum_dist_between_instances
        if inside_area:
            vel = abs(np.random.normal(vel, velocity_mod['std']))
            orientation = np.random.uniform(0,2*math.pi)
            ang_v = np.random.normal(angular_velocity['mean'], angular_velocity['std'])
            colour = (2*vel,predator_c[1],predator_c[2])
            new = predator.predator(colour,5,x,y, id_counter, timer + np.random.normal(predator_LE['mean'],predator_LE['std']), timer + np.random.normal(predator_reproduction['mean'], predator_reproduction['std']),vel,orientation,ang_v,0)
            
            Q.add_event(new.ID, new.time_of_death, 'Death')
            if (new.time_of_death>new.time_of_reproduction):
                Q.add_event(new.ID, new.time_of_reproduction, 'Reproduction_p')
            all_sprites.add(new)
            predator_sprites.add(new)
            id_counter+=1


def bimodal_normal(mean, std, offset):
    x = np.random.normal(mean,std)
    x = [offset + x, offset - x]
    return random.choice(x)


def distance_to_intances(x,y,group):
    res = {}
    for instance in group:
        id = instance.ID
        distance = math.dist([x,y],instance.rect.center)
        res[id] = distance
    return res

def get_closest_food(predator, food_group):
    x,y = predator.rect.center
    lowest_dist = np.inf
    for instance in food_group:
        distance = math.dist([x,y],instance.rect.center)
        if distance<lowest_dist:
            closest = instance
            lowest_dist = distance
    
    if lowest_dist<=vision_radius:
        return closest
    else:
        return None

def angle_to_food(pred, food):
    x_pred,y_pred = pred.rect.center
    x_food,y_food = food.rect.center
    vector = (x_food-x_pred,y_food-y_pred)
    vector = (vector[0]/np.linalg.norm(vector),vector[1]/np.linalg.norm(vector))
    if vector[1]>=0:
        theta = -np.arccos(vector[0])
    else:
        theta = np.arccos(vector[0])
    theta = theta%(2*math.pi)
    return theta



def random_positions(n):
    x = random.sample(range(minimum_dist_between_instances, screen.get_width()-minimum_dist_between_instances), n)
    y = random.sample(range(minimum_dist_between_instances, screen.get_height()-minimum_dist_between_instances), n)
    return x,y

#initialize_food
xx,yy = random_positions(Start_food)
for i in range(Start_food):
    add_food(xx[i],yy[i])

xx,yy = random_positions(Start_predators)
for i in range(Start_predators):
    add_predator(xx[i],yy[i], velocity_mod['mean'])


next_event = Q.pop()

time_vector = []
food_population_vector = []
pred_population_vector = []
pred_speed_vector = []
data_timer = 0
report_data = 2

while running:
    #if next_event==None:
    #    break

    screen.fill(green_c)
    # pygame.QUIT event means the user clicked X to close your window
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            running = False

    #_______move_predators_________kill_thirsty_predators_and_update_thirst___________
    for pred in predator_sprites:
        pred.thirst += dt * thirst_rate
        ### kill_thirsty_predators___
        if pred.thirst >= max_thirst:
            Q.remove_events_by_ID(pred.ID)
            if next_event['ID']==pred.ID:
                next_event = Q.pop()
            pred.kill()
        ### Move_predators___
        else:
            ##_check for close food
            closest = get_closest_food(pred,food_sprites)
            if closest == None:
                new_ang_vel = np.random.normal(angular_velocity['mean'], angular_velocity['std'])
                pred.update(new_ang_vel,dt,screen.get_width(),screen.get_height(),None)
            else:
                theta = angle_to_food(pred,closest)
                new_ang_vel = np.random.normal(angular_velocity['mean'], angular_velocity['std'])
                pred.update(new_ang_vel,dt,screen.get_width(),screen.get_height(),theta)


        
    #_______evaluate_colisions____
    collisions = pygame.sprite.groupcollide(predator_sprites, food_sprites, False, True)
    for pred in collisions:
        for f in collisions[pred]:
            pred.thirst = max(0, pred.thirst-food_energy)
            
            id = f.ID
            Q.remove_events_by_ID(id)
            if next_event['ID']==id:
                next_event = Q.pop()


    #_______process events________
    if next_event==None:
        break
    next_entity = find_Sprite(next_event['ID'], all_sprites)
    player_pos = next_entity.rect.center
    pygame.draw.circle(screen, yellow, player_pos, 7)
    if (next_event!=None and next_event['Time'] <= timer):
        process_event(next_event)
        next_event = Q.pop()
        #print(next_event)


    all_sprites.draw(screen)

    # Text for the time
    food_n = len(food_sprites.sprites())
    pred_n = len(predator_sprites.sprites())
    aux_speed = 0
    for pred in predator_sprites:
        aux_speed += pred.v
    try:
        aux_speed /= pred_n
    except:
        aux_speed = 0
    timer_surface = font.render("{:.2f}".format(timer), True, black)
    var1_surface = font.render("Food: " + str(food_n), True, black)
    var2_surface = font.render("Pred: " + str(pred_n), True, black)
    var3_surface = font.render("Avg_v: {:.2f}".format(aux_speed), True, black)
    timer_position = (10, 10)
    var1_position = (1180, 10)
    var2_position = (1180, 30)
    var3_position = (1180, 50)
    screen.blit(timer_surface, timer_position)
    screen.blit(var1_surface, var1_position)
    screen.blit(var2_surface, var2_position)
    screen.blit(var3_surface, var3_position)
    

    pygame.display.flip()


    if (data_timer>=report_data):
        time_vector += [timer]
        food_population_vector += [food_n]
        pred_population_vector += [pred_n]
        pred_speed_vector += [aux_speed]
        data_timer=0
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = (clock.tick(60)/1000) * time_multiplier
    timer += dt
    data_timer += dt

pygame.quit()


print("Elapsed simulation time: ", "{:.2f}".format(timer))

plt.figure(figsize=(11, 3))
plt.subplot(131)
plt.plot(time_vector, food_population_vector)
plt.title("Food population")
plt.subplot(132)
plt.plot(time_vector, pred_population_vector)
plt.title("Predator population")
plt.subplot(133)
plt.plot(time_vector, pred_speed_vector)
plt.title("Average predator speed")
plt.show()



