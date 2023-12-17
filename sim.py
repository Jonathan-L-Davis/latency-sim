import numpy as np
import statistics as st
import matplotlib.pyplot as plt
import math
import random


# BEHOLD! my python structs
class message:# unused struct
    time_sent = 0
    time_received = -1


class drone:
    messages = []#unused field
    team_mates = [] #integer list of indices
    is_hit = False

class network:
    drones = []
    start_points = []



# will return a list of floats with the percentile delay times.
# [  [] #*percentiles*#,[]#*mean,median,mode*#,{}#maybe more stats if I'm feelin it]

def eval_network(net):
    assert( type(net) == network )
    retMe = []
    max_iters = len(net.drones)-1 # worst case is a drones are in a snake/line, and we start at the end
    
    current_messengers = set(net.start_points)
    next_messengers = set()
    
    counter = []
    
    for x in net.drones:
        counter.append(-1)
    
    #mess = message()
    
    time_received = 0
    print("max iter: ",max_iters)
    while time_received < max_iters and len(current_messengers):
        #print(time_received)
        #print(current_messengers)
        for i,x in enumerate(current_messengers):
            #if len(net.drones[x].messages) == 0:
            #tmp = message()
            if counter[x] < 0 :
                counter[x] = time_received
            next_messengers.update( (net.drones[x].team_mates) )
        #print(next_messengers)
        
        
        #print( len(current_messengers), "," , len(next_messengers) )
        
        current_messengers = next_messengers
        next_messengers = set()
        
        time_received += 1
        
    #print(counter)
    
    # this is where the fun begins
    
    #       ░██████╗████████╗░█████╗░████████╗██╗░██████╗████████╗██╗░█████╗░░██████╗
    #       ██╔════╝╚══██╔══╝██╔══██╗╚══██╔══╝██║██╔════╝╚══██╔══╝██║██╔══██╗██╔════╝
    #       ╚█████╗░░░░██║░░░███████║░░░██║░░░██║╚█████╗░░░░██║░░░██║██║░░╚═╝╚█████╗░
    #       ░╚═══██╗░░░██║░░░██╔══██║░░░██║░░░██║░╚═══██╗░░░██║░░░██║██║░░██╗░╚═══██╗
    #       ██████╔╝░░░██║░░░██║░░██║░░░██║░░░██║██████╔╝░░░██║░░░██║╚█████╔╝██████╔╝
    #       ╚═════╝░░░░╚═╝░░░╚═╝░░╚═╝░░░╚═╝░░░╚═╝╚═════╝░░░░╚═╝░░░╚═╝░╚════╝░╚═════╝░
    
    # python actually makes this easy
    
    stats = []
    percentiles = []
    percentiles.append(np.percentile(counter,0))
    percentiles.append(np.percentile(counter,5))
    percentiles.append(np.percentile(counter,50))
    percentiles.append(np.percentile(counter,95))
    percentiles.append(np.percentile(counter,100))
    stats.append(percentiles)
    
    mean = np.mean(counter)
    stats.append(mean)
    
    mode = st.multimode(counter)
    stats.append(mode)
    print(counter.count(-1) )
    
    #print(stats)
    return stats;


def tree_network(depth, base):
    fill_me = network()
    fill_me.drones = []
    
    assert(type(depth)==int)
    assert(type(base)==int)
    
    total_drones = 0
    last_drone = 0
    larry = []#don't ask
    for i in range(0,depth):
        last_drone = total_drones#purposely one step behind
        total_drones += base**(i)
        for j in range(0,base**(i)):
            larry.append(base**(i))
    
    
    for i in range(0,total_drones):
        fill_me.drones.append(drone())
        fill_me.drones[i].is_hit = False
    
    for i,dron in enumerate(fill_me.drones):
        larry[i] = (math.ceil(math.log(larry[i],base)))# gives us tier of each drone.
    
    
    #print(larry)
    
    #print(total_drones)
    #print(len(fill_me.drones))
    
    if total_drones>0:
        fill_me.start_points.append(0)
    
    
    for i,dron in enumerate(fill_me.drones):
        #print(base)
        if larry[i] < depth-1:
            tmp = []
            for j in range( 0,base ):
                tmp.append( base**larry[i]+i*base+j-( (base**larry[i])-1 if i else 0) )# really don't ask
            fill_me.drones[i].team_mates = tmp
    
    return fill_me

#uses randomness
def mesh_network(num_drones, num_start_drones, connection_density ):
    assert(type(num_drones)==int)
    assert(type(num_start_drones)==int)
    assert(type(connection_density)==float or type(connection_density)==int)
    assert(connection_density >= 0.0 and connection_density <= 1.0 )
    
    fill_me = network()
    fill_me.drones = []
    
    i = 0
    while i < num_drones:
        fill_me.drones.append(drone())
        fill_me.drones[i].team_mates = random.sample(range(0, num_drones), int(num_drones*connection_density))
        #print( fill_me.drones[i].team_mates )
        i += 1
    
    fill_me.start_points = random.sample(range(0, num_drones), num_start_drones)
    #print("???",len(fill_me.drones))
    
    
    #random.sample(range(1, int( num_drones*connection_density )), )
    
    return fill_me

def mixed_network(num_drones, connection_density, tree_factor ):
    assert(type(num_drones)==int)
    #idk what tree factor is, but it feels like it might be useful right now. Something to do with clumping
    return

topology = tree_network(3,10)
print(eval_network(topology))
#print( "?",len( topology.drones ) )



topology2 = mesh_network(1000,1,.01)
#print( "?",len( topology.drones ) )
#print( "?",len( topology2.drones ) )
print(eval_network(topology2))



