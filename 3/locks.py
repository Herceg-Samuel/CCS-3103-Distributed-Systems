import threading

# Shared global resource
global_counter = 0

def increment_without_lock():
    global global_counter
    for _ in range(100000):
        # Read global_counter -> Add 1 -> Write back
        # Threads will interrupt each other here, causing lost increments!
        global_counter += 1

def run_problem_simulation():
    global global_counter
    global_counter = 0 # Reset
    threads = []
    
    print("Starting 10 threads WITHOUT a lock...")
    for _ in range(10):
        t = threading.Thread(target=increment_without_lock)
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join() # Wait for all threads to finish
        
    print(f"Expected Count: 1,000,000")
    print(f"Actual Count:   {global_counter}")
    print(f"Data Lost:      {1000000 - global_counter}")

if __name__ == "__main__":
    run_problem_simulation()