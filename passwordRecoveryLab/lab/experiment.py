import time
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from generator.number import generate_numeric
from lab.verifier import LocalVerifier

def run_experiment(secret):
    verifier = LocalVerifier(secret)
    password_length = len(secret)
    attempts = 0
    start = time.perf_counter()

    for candidate in generate_numeric(password_length):
        attempts +=1
        if verifier.verify(candidate):
            elapsed = time.perf_counter()-start
            speed = attempts/elapsed

            print("\n===============================")
            print("        Password Recoery lab")
            print("=================================")

            print(f"Password: {candidate}")
            print(f"Attempts: {attempts}")
            print(f"Time: " ,round(elapsed,4) , "second")
            print(f"Speed:" ,round(speed,2), "attempts/sec")

            return True
    print("Password was not found")
    return False

if __name__ == "__main__":   
    secret = "506787"
    run_experiment(secret)

