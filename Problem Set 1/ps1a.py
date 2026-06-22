###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    cow_weight = {}
    with open(filename, 'r') as file:
        for line in file:
            if line[-1] == '\n':
                line = line[:-1] #remove whitespace \n
            
            #append name, weight to dictionary
            name, weight = line.split(',') 
            cow_weight[name] = float(weight)
            
    return cow_weight

# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    #sort dictionary keys (biggest weight to smallest) 
    cows_left = dict(
                     sorted(cows.items(),  # key-value tuples
                            key=lambda cow: cow[1], #ordering on weight
                            reverse=True) #largest first 
                    )  
    #check if all cows can be transported 
    global_max = list(cows_left.values())[0]
    if global_max > limit:
        raise ValueError('Max weight exceeded, trip not possible.')       
            
    trips = []
    #1st loop gets each trip 
    while len(cows_left) != 0:
        trip = []
        weight_limit = limit 
        other_cows = dict(cows_left)
        
        #loop to greedily get max cows on given trip
        for cow in list(cows_left.keys()):
            cow_weight = cows_left[cow]
            
            if cow_weight <= weight_limit:
                trip.append(cow)
                weight_limit -= cow_weight
                del cows_left[cow]
                
        trips.append(trip)
        
    return trips

# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    #get partition generator for cows dict
    cow_partitions = get_partitions(cows)
    
    minimum_trips = float('inf')
    minimum_partition = None
    #loop through each partition
    for cow_trips in cow_partitions:
        num_trips = len(cow_trips)
        if num_trips >= minimum_trips:
            pass
        else:
            #check if trip is under weight limit
            for cow_trip in cow_trips:
                trip_weight = sum([cows[cow] for cow in cow_trip])
                if trip_weight > limit:
                    break
            #update valid minimum trip partition
            if trip_weight <= limit:
                minimum_trips = num_trips
                minimum_partition = cow_trips
            
    return minimum_partition 

# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    cow_dict = load_cows('ps1_cow_data.txt')
    
    #time greedy algorithm (loop 10000x as compute too quick)
    start = time.time()
    for i in range(10000):
        greedy_cow_transport(cow_dict,limit=10)
    end = time.time()
    print(f'Time for greedy algorithm is {(end - start)/10000:0.8f}s') #mean time 
    
    #time brute force algorithm
    start = time.time()
    brute_force_cow_transport(cow_dict,limit=10)
    end = time.time()
    print(f'Time for brute force algorithm is {end - start:0.8f}s')
    
