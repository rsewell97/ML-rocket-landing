import numpy as np
import math as m
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

h = 67  
r = 3.7/2
g = 9.81
s1mass = 25600
dt = 0.1
fuel = 60000

position = np.array([0,0,8000],dtype=float)
velocity = np.array([0,0,-1],dtype=float)
orientation = np.array([0,1,1],dtype=float)
dorientation = np.array([0,0,0],dtype=float)
ddorientation = np.array([0,0,0],dtype=float)
positionarray = np.array([position])
orientationarray = np.array([orientation])
maxallowed = abs(np.linalg.norm(positionarray)*2)
done = False

def normalise(v):
    return v / np.linalg.norm(v)
def mag(v):
    ab = 0.0
    for i in range(len(v)):
        ab += v[i]**2
    return pow(ab, 0.33)
def dot(u,v):
    total =0
    for i in range(len(u)):
        total += u[i]*v[i]
    return total
def angle3d(u,v):
    v1_u = normalise(u)
    v2_u = normalise(v)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))                           #returns cosine of angle between 2 vectors
def costosin(a):
    return np.sqrt(1-a**2)
def rotation_matrix(v, axis, theta):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    """
    axis = np.asarray(axis)
    axis = axis/np.sqrt(np.dot(axis, axis))
    a = np.cos(theta/2.0)
    b, c, d = -axis*np.sin(theta/2.0)
    aa, bb, cc, dd = a*a, b*b, c*c, d*d
    bc, ad, ac, ab, bd, cd = b*c, a*d, a*c, a*b, b*d, c*d
    rotationmatrix = np.array([[aa+bb-cc-dd, 2*(bc+ad), 2*(bd-ac)],
                     [2*(bc-ad), aa+cc-bb-dd, 2*(cd+ab)],
                     [2*(bd+ac), 2*(cd-ab), aa+dd-bb-cc]])
    return np.dot(rotationmatrix, v)
def inertia(fuel):
    return 30000*h*2
def mass(fuel):
    return max(s1mass,s1mass + fuel)
def density():
    return 1.225  #6*np.exp(-position[2]/7000)

def atmospheric_drag(velocity,orientation):

    drag = np.cos(angle3d(-velocity,orientation))*orientation*0.82*density()*(mag(velocity)**2) *3.14*r**2
# 150
#     liftvector = rotation_matrix(orientation,np.cross(velocity,orientation),3.14159/2)    
#     lift = (-0.5*0.3*density()*liftvector*(mag(velocity)**2)) *h*(2*r)*np.sin(2*angle3d(-velocity,orientation))

    restoringtorque = np.array([50*(mag(velocity)**2)*(orientation[0]-normalise(velocity)[0]), 50*(mag(velocity)**2)*(orientation[1]-normalise(velocity)[1]),0])

    # drag = lift + drag
    return drag , -restoringtorque

def enginegimbal(x,y,orientation,throttle,fuel):
    x = np.clip(x,-3.14/15,3.14/15)
    y = np.clip(y,-3.14/15,3.14/15)
    throttle = np.clip(throttle,0,1)

    engineorientation = rotation_matrix(orientation,np.array([0,1,0]),x)
    engineorientation = rotation_matrix(engineorientation,np.array([1,0,0]),y)      #rotates through x and y
    thrustvector = throttle*2*850000 * engineorientation

    return thrustvector

def gridfins(x,y,velocity,fuel):
    if x > 3.14/10:
        x = 3.14/15
    if x < -3.14/10:
        x = -3.14/15
    if y > 3.14/10:
        y = 3.14/15
    if y < -3.14/10:
        y = -3.14/15
    liftx = 0.05*x*0.5*density()*(mag(velocity)**2)*np.cos(angle3d(-velocity,orientation))
    liftx*=5000
    lifty = 0.05*y*0.5*density()*(mag(velocity)**2)*np.cos(angle3d(-velocity,orientation))
    lifty*=5000
    return np.array([liftx,lifty,0])

def step(gridx,gridy,gimbalx,gimbaly,throttle,position,velocity,fuel,orientation,dorientation):
    done = False
    reward =0
    drag , stability = atmospheric_drag(velocity,orientation)
    thrustvector = enginegimbal(gimbalx,gimbaly,orientation,throttle,fuel)
    thrustcom = thrustvector*np.cos(angle3d(thrustvector,orientation))
    thrustrot = thrustvector*np.sin(angle3d(thrustvector,orientation))

    velocitynew = velocity + dt * (np.array([0,0,-g]) + (thrustcom + drag)/mass(fuel))
    positionnew = position + velocitynew * dt

    dorientationnew = dorientation + (gridfins(gridx,gridy,velocity,fuel) - thrustrot + stability)*dt/inertia(fuel)

    orientationnew = orientation + dorientationnew*dt
    orientationnew = normalise(orientationnew)
    fuel -= 2044*throttle

    if (position[2] < h/2) and (position[0]**2+position[1]**2)**0.5 < 30:#and abs(np.linalg.norm(position)) < 5):       #exit conditons
        print("LANDED ON PAD @ {} m/s".format(round(-velocity[2])))
        done = True
        reward = np.clip(60-((position[0]**2+position[1]**2)**0.5)/100,1,60) - np.clip((-velocity[2]),0,60)

        if(velocity[2] > -9):
            reward = 20 + np.clip(60-((position[0]**2+position[1]**2)**0.5)/100,1,60) - np.clip((-velocity[2]),0,59)
            print("DID NOT EXPLODE")
            if(orientation[2]>0.97):
                reward = 200
                print("\n\n\n\n\nLANDED SUCCESSFULLY\n\n\n\n\r")
                fuel = 1000000
    elif (position[2] < h/2):
        string = int(round((position[0]**2+position[1]**2)**0.5))
        print("CRASH LANDED {} m from barge at {}m/s".format(string,round(-velocity[2])))
        done = True
        reward = 0.5*np.clip(60-((position[0]**2+position[1]**2)**0.5)/100,1,60) - np.clip((-velocity[2]),0,59)

    elif (abs(np.linalg.norm(position))> maxallowed):
        done = True
        print("LEFT THE AREA")
        reward = 0

    # if fuel < 0:
    #     print("OUT OF FUEL at {}m".format(round(position[2])))
    #     reward = 1
    #     done = True   
    
    
    return positionnew, velocitynew, orientationnew, dorientationnew, done, reward,fuel


# while done ==False:
#     position, velocity, orientation, dorientation, done, reward,fuel = step(0,0,0,0,0.2,position,velocity,fuel,orientation,dorientation)
#     print(orientation,velocity)
#     positionarray = np.append(positionarray,[position],axis=0)
#     orientationarray = np.append(orientationarray,[orientation],axis=0)
    
# # print("DONE")
# np.savetxt('positions.txt',positionarray,delimiter=',',newline='\r')
# np.savetxt('orientations.txt',orientationarray,delimiter=',',newline='\r')

# x=np.array([])
# y=np.array([])
# z=np.array([])
# for i in range(len(positionarray)-1):
#     x = np.append(x,positionarray[i][0])
#     y = np.append(y,positionarray[i][1])
#     z = np.append(z,positionarray[i][2])
# ax.set_xlim3d(min(-1.5*x[0],-1000), max(1.5*x[0],1000))
# ax.set_ylim3d(min(-1.5*y[0],-1000), max(1.5*y[0],1000))
# ax.set_zlim3d(0, 1.2*z[0])
# ax.plot(x,y,z)
# plt.show()
# #Axes3D.plot()
