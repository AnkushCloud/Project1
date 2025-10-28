import requests
import threading
import time
import sys

def generate_load(url, duration=60):
    end_time = time.time() + duration
    requests_count = 0
    
    while time.time() < end_time:
        try:
            response = requests.get(f"{url}/cpu-intensive", timeout=10)
            requests_count += 1
            if requests_count % 10 == 0:
                print(f"Requests sent: {requests_count}")
        except Exception as e:
            print(f"Request failed: {e}")
    
    print(f"Total requests sent: {requests_count}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python stress-test.py <BASE_URL> [DURATION]")
        sys.exit(1)
    
    base_url = sys.argv[1]
    duration = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    
    print(f"Starting load test on {base_url} for {duration} seconds")
    
    # Start multiple threads to generate load
    threads = []
    for i in range(5):  # 5 concurrent threads
        thread = threading.Thread(target=generate_load, args=(base_url, duration))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    print("Load test completed")