import threading, time, random

#
# Main class which implements the Lamport's Fast Mutual Exclusion algorithm
#
class Fast (threading.Thread):
    # Constructor
    def __init__(self):
        threading.Thread.__init__(self)
        self.pid = 0
        self.pending_req = 0
        self.req_cs_1_var = 0
        self.req_cs_2_var = 0
        self.req_cs_3_var = 0
    
    # Utility methods to set the thread ID
    def set_pid(self, pid):
        self.pid = pid
             
    #  
    # Routines to access request for CS. Workaround for goto. 
    # This workaround ensures that the stack space doesn't
    # grow infinitely.
    #

    # Pseudocode:
    # start: b[i]:=1 
    #        x:=i
    def req_cs_1 (self):
        
        global b
        global x
        tid = self.pid
        
        b[tid] = 1
        x = tid
        self.req_cs_1_var = 1
        
    # Pseudocode
    # if y!=0: b[i]:=0 
    #          await y=0 
    #          goto start fi
    def req_cs_2 (self):
        
        global b
        global y
        tid = self.pid
        
        if y != 0 :
            b[tid] = 0
            while (y != 0) :
                pass
            self.req_cs_2_var = 0
            
        self.req_cs_2_var = 1
        
    # Pseudocode
    # y:=i
    # if x!=i: b[i]:=0
    #          for j:=1..n: await b[j]=0 
    #          if y!=i: await y=0
    #                   goto start fi fi
    def req_cs_3 (self):
        
        global b
        global x
        global y
        global n
        tid = self.pid
        
        y = tid
        
        if (x != tid) :
            b[tid] = 0
            for j in range(n) :
                while (b[j] != 0) :
                    pass
                if (y != tid) :
                    while (y != 0) :
                        pass
                    self.req_cs_3_var = 0
        self.req_cs_3_var = 1
        
    # This routine returns 1 if the thread can enter CS, 0 otherwise
    def req_cs (self):
        self.req_cs_1_var = 0
        self.req_cs_1()
        if (self.req_cs_1_var == 1):
            self.req_cs_2_var = 0
            self.req_cs_2()
            if (self.req_cs_2_var == 1):
                self.req_cs_3_var = 0
                self.req_cs_3()
         
        if (self.req_cs_1_var == 1 and self.req_cs_2_var == 1 and self.req_cs_3_var == 1):
            return 1
        else:
            return 0

    # This routine contains the Request CS, Enter CS and Release CS sections
    def cs(self, task):
        
        global b
        global y
        tid = self.pid
        
        # Request CS
        print("Thread-" + str(self.pid) + " requesting CS")
        status = self.req_cs()
        while (status == 0):
            status = self.req_cs()
            
        # Execute CS
        task(self)
            
        # Exit CS
        print("Thread-" + str(self.pid) + " exiting CS")
        b[tid] = 0
        y = 0
                
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
    global b
    global x
    global y
    global n

    b = []
    x, y = 0, 0
    n = len(thread_list)
        
    # Initialize the shared variables
    for i in range(n):
        b.append(0)
    
    x = 0
    y = 0

    # Invoke the start routine for each thread
    for i in range(n) :
        thread = thread_list[i]
        thread.start()

    # Wait for the threads to complete execution
    for i in range(n) :
        thread = thread_list[i]
        thread.join()

# End of File
