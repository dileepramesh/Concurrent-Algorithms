import threading, time, random

#
# Main class which implements the Lamport's Bakery algorithm
#
class Bakery (threading.Thread):
    # Constructor
    def __init__(self):
        threading.Thread.__init__(self)
        self.pid = 0
        self.pending_req = 0
    
    # Utility methods to set the thread ID
    def set_pid(self, pid):
        self.pid = pid
        
    # This routine contains the Request CS, Enter CS and Release CS sections
    def cs(self, task):
        
        global choosing
        global num
        global n
        tid = self.pid
        
        # Request CS
        print("Thread-" + str(self.pid) + " requesting CS")
        
        # Pseudo code:
        # choosing[i]:=1
        # num[i]:= 1+max{num[j]: j=1..n}
        # choosing[i]:=0 
        # 
        # for j:=1..n: 
        #     await choosing[j]=0
        #     await num[j]=0 or (num[j],j) >= (num[i],i)

        choosing[tid] = 1
        num[tid] = 1 + max(num)
        choosing[tid] = 0

        for j in range(n):
            while (choosing[j] != 0):
                pass
                
            while (num[j] != 0 and (num[j], j) < (num[tid], tid)):
                pass
                
        # Execute CS
        task(self)
            
        # Exit CS
        print("Thread-" + str(self.pid) + " exiting CS")
        num[tid] = 0
        
    # 
    # Main routine for this thread. This continuously invokes the cs()
    # method untils all the pending requests run out.
    #
    def main(self):
        
        # Print the count of pending requests for this thread
        print("Pending Requests for " + "Thread-" + str(self.pid) + ": " + str(self.pending_req))
        
        # Routine called when CS is acquired
        def cs_task (self):
            # Log a message for now
            print("Thread-" + str(self.pid) + " in CS")
            
        # Process the requests one at a time
        for i in range(self.pending_req):
            
            # Call the CS routine
            self.cs(cs_task)
            
            # Sleep for sometime
            r = random.randint(0, 2)
            time.sleep(r)
        
        print("Thread-" + str(self.pid) + " terminating")

    # Thread start routine
    def run(self):
        
        # Just invoke the main routine
        self.main()

# Setup routine to map thread objects to requests
def setup (thread_list = [], m = 0):

    # Global variables shared by all the threads
    global choosing
    global num
    global n
    
    choosing, num = [], []
    
    n = len(thread_list)
    
    # Initialize the shared variables
    for i in range(n):
        choosing.append(0)
    
    for i in range(n):
        num.append(0)

    # Invoke the start routine for each thread
    for i in range(n) :
        thread = thread_list[i]
        thread.start()

    # 
    # Wait for the threads to complete execution before moving onto 
    # the the Lamport's fast algorithm
    # 
    for i in range(n) :
        thread = thread_list[i]
        thread.join()

# End of File
