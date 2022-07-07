#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  2 13:33:16 2022

@author: maxcai
"""

import numpy as np
import matplotlib.pyplot as plt

R = 1E-9 #Variance of noise, no convariance matrix because both noise values currently satisfy same distribution
Q = 0.2 #Variance of measurement noise
x0 = np.array([[3.1],[0]]) #theta, omega
Sigma0 = np.array([[1,0],[0,1]])
N = 1000 #number of steps
g = 10
l = 1
k = g/l
dt = 1E-2

#B = 0
C = np.array([[1,0]]) #row vector

x = np.zeros((N,2,1))
#u = np.zeros((N,2)) #Control
np.random.seed(seed=10)
epsilon = np.random.normal(0,np.sqrt(R),(N,2,1))
delta = np.random.normal(0,np.sqrt(Q),N)
mu = np.zeros((N,2,1))
Sigma = np.zeros((N,2,2))

#for i in range(N):
#    u[i] = 0.1

t = dt * np.arange(N)
z = np.zeros(N)

def evolve(x):
    output = np.zeros((2,1))
    output[0] = x[0] + dt * x[1] - dt**2 * k * np.sin(x[0])
    output[1] = x[1] - dt * k * np.sin(x[0])
    return output

#simulation
x[0] = x0
for i in range(1,N):
    x[i] = evolve(x[i-1])
    x[i] += epsilon[i]

#measurement
for i in range(0,N):
    z[i] = np.matmul(C, x[i]) + delta[i]
    #only theta is measured
    
#kalman filter (kalman gain)
mu[0] = x0
Sigma[0] = Sigma0
mu_pred = np.zeros((2,1))
for i in range (1,N):
    G = np.array([[1-k*dt**2 * np.cos(mu[i-1,0]),dt],[-k * dt * np.cos(mu[i-1,0]), 1]]) #Jacobian of evolution function
    #prediction
    mu_pred = evolve(mu[i-1])
    Sigma_pred = G @ Sigma[i-1] @ G.T + R
    #kalman gain
    K = Sigma_pred @ C.T * (C @ Sigma_pred @ C.T + Q)**-1
    #measurement
    Sigma[i] = (np.identity(2)- K @ C) @ Sigma_pred
    mu[i] = mu_pred + K @ (z[i]-C @ mu_pred)

#print(np.max(np.abs(mu[:,0]-mu_k[:,0])))
#print((Sigma[-1]-Sigma_k[-1]))

plt.figure(1)

plt.plot(t, z, 'r', label = 'theta measured')
plt.plot(t, x[:,0], 'b', label = 'theta')
plt.plot(t, mu[:,0], 'g', label = 'theta estimate')
#plt.plot(t, x[:,1], 'g', label = 'omega')
plt.plot([0, np.max(t)],[0,0],'k')
plt.legend()
plt.xlabel('t')
plt.title('Pendulum EKF')

plt.figure(2)
plt.plot(t,Sigma[:,0,0],'b',label = 'theta variance')
plt.plot(t,Sigma[:,1,0],'m')
plt.plot(t,Sigma[:,0,1],'g',label = 'theta and omega covariance')
plt.plot(t,Sigma[:,1,1],'r',label = 'omega variance')
plt.legend()
plt.xlabel('t')
plt.title('EKF Covariance')

plt.show()

    