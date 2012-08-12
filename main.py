import sys, random, Bakery, Fast

def main ():
    
    # 
    # Get the configuration parameters from the user. Reset to default
    # values if invalid input is entered.
    #
    try:
        if len(sys.argv) == 3:
            n = int(sys.argv[1])
            m = int(sys.argv[2])
            if (n <= 0 or m <= 0):
                print("Invalid input. Resetting to default parameters.")
                n = 10
                m = 50
        else:
            print("Invalid input. Resetting to default parameters.")
            n = 10
            m = 50
    except(ValueError, IndexError):
        print("Invalid input. Resetting to default parameters.")
        n = 10
        m = 50
        
    # Part 1 - Bakery Algorithm
    
    # Print the banner!
    print("Running Lamport's bakery algorithm")
    print("")
    
    # Initialize the thread list
    thread_list_bakery = []
    
    # Initialize the threads
    for i in range(n) :
        thread = Bakery.Bakery()
        thread.set_pid(i)
        thread_list_bakery.append(thread)

    # Assign requests to threads randomly
    for i in range (m):
        # Pick a random thread and increment its request count
        if (n > 1):
            p = random.randint(0, n - 1)
        else:
            p = 0
        thread = thread_list_bakery[p]
        thread.pending_req = thread.pending_req + 1

    # 
    # Call the setup routine to initialize shared variables.
    # This will also start the threads.
    #
    Bakery.setup(thread_list_bakery, m)
        
    # Part 2 - Fast Mutual Exclusion Algorithm
     
    # Print the banner!
    print("")
    print("Running Lamport's fast mutual exclusion algorithm")
    print("")
    
    # Initialize the thread list
    thread_list_fast = []
    
    # Initialize the threads
    for i in range(n) :
        thread = Fast.Fast()
        thread.set_pid(i)
        thread_list_fast.append(thread)

    # Assign requests to threads randomly
    for i in range (m):
        # Pick a random thread and increment its request count
        if (n > 1):
            p = random.randint(0, n - 1)
        else:
            p = 0
        thread = thread_list_fast[p]
        thread.pending_req = thread.pending_req + 1
        
    # 
    # Call the setup routine to initialize shared variables.
    # This will also start the threads.
    #
    Fast.setup(thread_list_fast, m)
        
# Invoke the driver program
main()

# End of File
