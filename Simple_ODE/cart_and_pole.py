#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 14:35:49 2022

@author: maxcai
"""

import numpy as np
import matplotlib.pyplot as plt


g = 10
l = 1
m1 = 5 #cart mass
m2 = 5 #pendulum mass
x0 = 0
v0 = 0
theta0 = 3
omega0 = 0

dt = 5E-5
t = np.arange(0, 10, dt)
x = np.zeros_like(t)
v = np.zeros_like(t)
theta = np.zeros_like(t)
omega = np.zeros_like(t)
x[0] = x0
v[0] = v0
theta[0] = theta0
omega[0] = omega0

#Euler Forward
for i in range(t.shape[0]-1):
    A = np.array([[m1 + m2, m2 * l * np.cos(theta[i])],[np.cos(theta[i]), l]])
    RHS = np.array([[m2 * l * omega[i]**2 * np.sin(theta[i])],[-g * np.sin(theta[i])]])
    [[ddx],[ddtheta]] = np.linalg.solve(A,RHS)
    #Solves System of Equations for x double dot and theta double dot
    
    x[i+1] = x[i] + v[i] * dt
    theta[i+1] = theta[i] + omega[i] * dt
    v[i+1] = v[i] + ddx * dt
    omega[i+1] = omega[i] + ddtheta * dt

energy = 0.5 * (m1 * np.square(v) + m2 * (l**2 * np.square(omega) + 2*l*omega*v*np.cos(theta)+np.square(v))) - m2*g*l*np.cos(theta)
print("Energy change = ", energy[-1] - energy[0])

plt.figure(1)
plt.plot(t, x,"b", label = 'x')
plt.plot(t, theta, "g", label = "theta")
plt.plot([0, np.max(t)],[0,0],'k')
plt.legend()
plt.xlabel('t')
plt.title('Cart and Pole')
plt.show()

plt.figure(2)
plt.plot(t, energy)
plt.xlabel('t')
plt.ylabel('energy')
plt.show()