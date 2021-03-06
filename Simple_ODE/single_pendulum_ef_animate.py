#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 22 16:09:37 2022

@author: maxcai
"""

import numpy as np
import pygame
import sys



#First part numerically integrates Pendulum motion
#dd_theta + g/l sin(theta) = 0

class Pendulum():
    def __init__(self,g=10,l=5,m=1,dt=1E-3,theta0=2,omega0=0):
        self.g = g
        self.l = l
        self.m = m
        self.dt = dt
        self.theta0 = theta0
        self.omega0 = omega0
        
    def time_integrate(self,time=60):
        self.t = np.arange(0, time, self.dt) #To Do: Allow program to run indefinitely
        self.theta = np.zeros_like(self.t)
        self.omega = np.zeros_like(self.t)
        self.energy = np.zeros_like(self.t)
        self.theta[0] = self.theta0
        self.omega[0] = self.omega0
        #Euler Forward
        for i in range(self.t.shape[0]-1):
            self.theta[i+1] = self.theta[i] + self.dt * self.omega[i]
            self.omega[i+1] = self.omega[i] - self.g/self.l * self.dt * np.sin(self.theta[i])
        
        self.energy = 0.5 * self.m * np.square(self.omega) * self.l**2 - (self.m*self.g*self.l*np.cos(self.theta))
        print("Energy change = ", self.energy[-1] - self.energy[0])


#Animates Pendulum


class PendulumSprite(pygame.sprite.Sprite,Pendulum):
    def __init__(self,window):
        pygame.sprite.Sprite.__init__(self)
        Pendulum.__init__(self)
        self.window = window
        
    def update(self,timestep):
        r = 0.3 * min(self.window.get_size())
        x = 0.5 * self.window.get_size()[0] + r * np.sin(self.theta[int(timestep)])
        y = 0.5 * self.window.get_size()[1] + r * np.cos(self.theta[int(timestep)])
        
        #self.rect.topleft = [x,y]
        pygame.draw.line(self.window, (0,0,255),(0.5 * self.window.get_size()[0],0.5 * self.window.get_size()[1]),(x,y),2)
        pygame.draw.circle(self.window, (255,0,0),(x,y),10)
        #Use return statmement for double pendulum coordinate stacking
        #The commented messages are responsible for loading in an image
        

# General setup
pygame.init()
clock = pygame.time.Clock()

# Game Screen
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Pendulum Animation")

print(screen.get_size())
# Creating the sprites and groups
moving_sprites = pygame.sprite.Group()
pendulum1 = PendulumSprite(screen)
pendulum1.time_integrate()
moving_sprites.add(pendulum1)


fps = 50
timestep = 0
while True:
    for event in pygame.event.get():   
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((0,0,0)) #Clears screen for next frame
    moving_sprites.update(timestep)
    pygame.draw.circle(screen, (0,150,0),(0.5 * screen.get_size()[0],0.5 * screen.get_size()[1]),4)
    #Draws center peg
    
    #moving_sprites.draw(screen)
    pygame.display.flip()
    
    #print("index ", timestep)
    #print("time ", t[int(timestep)])
    
    clock.tick(fps)
    timestep += 1/fps/pendulum1.dt
    if timestep >= np.size(pendulum1.t):
        pygame.quit()
        sys.exit()
    
