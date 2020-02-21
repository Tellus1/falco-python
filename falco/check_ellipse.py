#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 09:07:03 2020

@author: ajriggs
"""

#--Required Inputs
#Nbeam = inputs['Nbeam']  # max aperture radius in samples
#Narray = inputs['Narray'] # Number of samples across in square output array
#radiusX = inputs['radiusX'] # x-radius of ellipse [pupil diameters]
#radiusY = inputs['radiusY'] # y-radius of ellipse [pupil diameters]
#clockingRadians = np.pi/180.*inputs['clockingDegrees']
#
##--Optional inputs
#if not 'centering' in inputs.keys(): inputs['centering'] = 'pixel'
#if not 'xShear' in inputs.keys(): inputs['xShear'] = 0.
#if not 'yShear' in inputs.keys(): inputs['yShear'] = 0.
#if not 'magFac' in inputs.keys(): inputs['magFac'] = 1.
#centering = inputs['centering']
#xShear = inputs['xShear']
#yShear = inputs['yShear']
#magFac = inputs['magFac']

import numpy as np
import matplotlib.pyplot as plt

Nbeam = 100
Narray = 102
radiusX = 0.5
radiusY = 0.3
clockingRadians = 0#np.pi/180.*20.0

centering = 'pixel'
xShear = 0 #0.3
yShear = 0#0.3
magFac = 1.0


if centering == 'pixel':
    x = np.linspace(-Narray/2., Narray/2. - 1, Narray)/float(Nbeam)
elif centering == 'interpixel':
    x = np.linspace(-(Narray-1)/2., (Narray-1)/2., Narray)/float(Nbeam)
    
y = x
x = x - xShear
y = y - yShear
[X, Y] = np.meshgrid(x,y)
dx = x[1] - x[0]
radius = 0.5

RHO = 1/magFac*0.5*np.sqrt(
    1/(radiusX)**2*(np.cos(clockingRadians)*X + np.sin(clockingRadians)*Y)**2
    + 1/(radiusY)**2*(np.sin(clockingRadians)*X - np.cos(clockingRadians)*Y)**2
    )

halfWindowWidth = np.max(np.abs((RHO[1, 0]-RHO[0, 0], RHO[0, 1] - RHO[0, 0])))
pupil = -1*np.ones(RHO.shape)
pupil[np.abs(RHO) < radius - halfWindowWidth] = 1
pupil[np.abs(RHO) > radius + halfWindowWidth] = 0
grayInds = np.array(np.nonzero(pupil==-1))
# print('Number of grayscale points = %d' % grayInds.shape[1])

upsampleFactor = 100
dxUp = dx/float(upsampleFactor)
xUp = np.linspace(-(upsampleFactor-1)/2., (upsampleFactor-1)/2., upsampleFactor)*dxUp
#xUp = (-(upsampleFactor-1)/2:(upsampleFactor-1)/2)*dxUp
[Xup, Yup] = np.meshgrid(xUp, xUp)

subpixel = np.zeros((upsampleFactor,upsampleFactor))

for iInterior in range(grayInds.shape[1]):

    subpixel = 0*subpixel

    xCenter = X[grayInds[0, iInterior], grayInds[1, iInterior]]
    yCenter = Y[grayInds[0, iInterior], grayInds[1, iInterior]]
    RHOup = 0.5*np.sqrt(
    1/(radiusX)**2*(np.cos(clockingRadians)*(Xup+xCenter) + np.sin(clockingRadians)*(Yup+yCenter))**2
    + 1/(radiusY)**2*(np.sin(clockingRadians)*(Xup+xCenter) - np.cos(clockingRadians)*(Yup+yCenter))**2 
    )

    subpixel[RHOup <= radius] = 1
    pixelValue = np.sum(subpixel)/float(upsampleFactor**2)
    pupil[grayInds[0, iInterior], grayInds[1, iInterior]] = pixelValue

plt.figure(2); plt.imshow(pupil); plt.colorbar(); plt.pause(0.1)