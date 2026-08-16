import time 

secret = "506787"

attempts= 0
start_at = time.time()

for num in range(1_000_000):
    candidate = f"{num:06d}"
    attempts+=1
    if candidate==secret:
        end_time = time.time()

        elapsed = end_time-start_at
        speed = attempts/elapsed 

        print("\n Password found!")
        print("Password: ",candidate)
        print("Attempts: ",attempts)
        print("Time: ",round(elapsed,4),"seconds")
        print("Speed: ",round(speed,2),"attempts/sec")

        break

        