###########################
# 6.0002 Problem Set 1b: Space Change
# Name:
# Collaborators:
# Time:
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================

# Problem 1
def dp_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    if target_weight == 1:
        return 1
    if target_weight == 0:
        return 0 
    
    #memoised version 
    try:
        return memo[(target_weight, egg_weights)]
    
    #if weight not already solved, solve
    except KeyError:
        
        
        min_eggs = float('inf')
        for egg_weight in reversed(egg_weights):
            #valid egg_weights to take
            if egg_weight <= target_weight:
                #min eggs required is 1 + min of the weight subtract one of the egg weights
                num_eggs = 1 + dp_make_weight(egg_weights, 
                                              target_weight-egg_weight, 
                                              memo)
                if num_eggs < min_eggs:
                    min_eggs = num_eggs
        #update memo with new solution
        memo[(target_weight, egg_weights)] = min_eggs
        return min_eggs

# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected output: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()
    
    egg_weights = (1, 5, 10, 20)
    n = 99
    print("Egg weights = (1, 5, 10, 20)")
    print("n = 99")
    print("Expected output: 10 (4 * 20 + 1 * 10 + 1 * 5 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()
    
    
    
    
####
# Alternative tabular version
####

def dp_make_weight_tabular(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    #initialise solutions for trivial target weights 
    if target_weight == 1:
        return 1
    if target_weight == 0:
        return 0 
    egg_solved = [0,1]
    
    #solve iteratively for weights 2 and above
    for weight in range(2, target_weight+1):
        min_eggs = float('inf')
        
        #loop to find min eggs required 
        for egg_weight in egg_weights:
            if egg_weight <= weight:
                #min eggs required is 1 + min of the weight subtract one of the egg weights 
                num_eggs = 1 + egg_solved[weight-egg_weight]
                
                if num_eggs < min_eggs:
                    min_eggs = num_eggs
        #append solution for given weight
        egg_solved.append(min_eggs)
    
    #return last value, solution for target weight
    return egg_solved[-1]