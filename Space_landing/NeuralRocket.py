import numpy as np
import Rocket as rocket
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
inputs = 12
hidden1 = 10
outputs = 5
generation = 1
spg = 50
maxgen = 100
mutationchance = 0.09
results = np.zeros(spg)
weighting = np.random.rand(spg,(inputs*hidden1)+(hidden1*outputs))

def normalise(v):
    for i in range(len(v)):
        v[i] /= mag(v)
    return v
def mag(v):
    ab = 0
    for i in range(len(v)):
        ab += v[i]**2
    return ab**(1/len(v))
def resize(variable,xs,xf,ys,yf):
    fraction = (variable-xs)/(xf-xs)
    return ys + fraction*(yf-ys)

def getparents(matingpool):
    parent1 = matingpool[np.random.randint(0,len(matingpool))]
    parent2 = matingpool[np.random.randint(0,len(matingpool))]
    x = np.random.randint(len(matingpool[0])-1,size=round(len(weighting[0])/2))
    for index in x:
        parent1[index]=parent2[index].copy()
    return parent1
def mutation(matingpool):
    for x in range(round(mutationchance*len(matingpool))):
        matingpool[np.random.randint(len(matingpool)-1),np.random.randint(len(matingpool[0])-1)] = np.random.rand()
    return matingpool
def neural(observation,weighting,hidden1):
    output = [0,0,0,0,0]
    blobs = [0,0,0,0,0,0,0,0,0,0]

    for j in range(len(blobs)):
        for i in range(len(observation)):
            blobs[j] += observation[i]*weighting[i+j*hidden1]

    for j in range(len(output)):
        for i in range(0,len(blobs)):
            output[j] += blobs[i]*weighting[i + j*10]

    output /= np.linalg.norm(output)
    return output

def run(weighting,position,velocity,orientation,dorientation):
    action = [0,0,0,0,0.00001]
    done = False
    fuel = 60000
    positionarray = np.array([position])
    orientationarray = np.array([orientation])
    totalreward = 0

    while done == False:
        position,velocity,orientation,dorientation,done,reward,fuel = rocket.step(action[0],action[1],action[2],action[3],action[4],position,velocity,fuel,orientation,dorientation)
        positionarray = np.append(positionarray,[position],axis=0)
        orientationarray = np.append(orientationarray,[orientation],axis=0)

        totalreward += reward
        observation = np.vstack((position,velocity,orientation,dorientation))
        observation = np.reshape(observation, 12)

        action = neural(observation,weighting,10)
        action[0] = resize(action[0],0,1,-0.35,0.35)
        action[1] = resize(action[1],0,1,-0.35,0.35)
        action[2] = resize(action[2],0,1,-0.35,0.35)
        action[3] = resize(action[3],0,1,-0.35,0.35)
        if position[2]<1000:
            action[4] = resize(action[4],0,1,0.6,1)
        else:
            action[4] = 0.00001
        if fuel == 1000000:
            #save working config
            pass
    return totalreward,positionarray,orientationarray


for generation in range(maxgen):
    matingpool = np.empty((0,170),dtype=float)
    fuel = 130000
    position = np.array([100,100,3000],dtype=float)
    velocity = np.array([-5,-5,-70],dtype=float)
    orientation = np.array([0,0,1],dtype=float)
    dorientation = np.array([0,0,0],dtype=float)
    positionarray = np.array([position])
    orientationarray = np.array([orientation])
    resultsarrayx = np.empty((0,1))
    resultsarrayy = np.empty((0,1))

    for i_episode in range(0,spg):
        reward,positionarray,orientationarray = run(weighting[i_episode],+position,velocity,orientation,dorientation)
        reward = int(np.ceil(reward))
        results[i_episode] = reward

        resultsarrayx,resultsarrayy = np.append(resultsarrayx,positionarray[-1,0]),np.append(resultsarrayy,positionarray[-1,1])

        if reward != 0:
            for j in range(reward):
                matingpool = np.append(matingpool,np.array([weighting[i_episode]]),axis=0)
    if len(matingpool) < 2:
        matingpool = np.random.rand(10,170)
    
    matingpool = mutation(matingpool)
    for value in range(spg):   
        child = getparents(matingpool)
        weighting[value] = child
    print("____________GENERATION {}____________".format(generation))

np.savetxt('positions.txt',positionarray,delimiter=',',newline='\r')
np.savetxt('orientations.txt',orientationarray,delimiter=',',newline='\r')


x=np.array([])
y=np.array([])
z=np.array([])
for i in range(len(positionarray)-1):
    x = np.append(x,positionarray[i][0])
    y = np.append(y,positionarray[i][1])
    z = np.append(z,positionarray[i][2])
ax.set_xlim3d(-1.5*x[0], 1.5*x[0])
ax.set_ylim3d(1.5*-y[0], 1.5*y[0])
ax.set_zlim3d(0, 1.2*z[0])
ax.plot(x,y,z)


# plt.scatter(resultsarrayx,resultsarrayy)
plt.show()



