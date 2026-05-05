import requests
import time
import datetime

TARGET_URL = "http://192.168.6.129:8080"
NUM_REQUESTS = 20
DELAY_SECONDS = 1
SUCCESS_COUNT = 0
FAIL_COUNT = 0

def send_requests():
    global SUCCESS_COUNT , FAIL_COUNT
    
    print(f"Starting HTTp Traffic Generator")
    print(f"Target: {TARGET_URL}")
    print(f"Sending {NUM_REQUESTS} requests with {DELAY_SECONDS}s delay ")
    print("-" * 50)

    for i in range(1, NUM_REQUESTS + 1):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            start_time = time.time()
            response = requests.get(TARGET_URL, timeout=5)
            end_time = time.time()
            duration = round((end_time - start_time) * 1000, 2)

            if response.status_code == 200:
                SUCCESS_COUNT += 1
                print(f"[{timestamp}] Requests {i}: SUCCESS | Status: {response.status_code} | Time: {duration}ms")
            else:
                FAIL_COUNT += 1
                print(f"[{timestamp}] Request {i}: FAIL | Status: {response.status_code} | Time: {duration}ms")
        except requests.exceptions.ConnectionError:
            FAIL_COUNT += 1
            print(f"[{timestamp}] Request {i}: ERROR | Could not connect to {TARGET_URL}")

        except requests.exceptions.Timeout:
            FAIL_COUNT += 1
            print(f"[{timestamp}] Request{i} TIMEOUT | Server did not respond within 5 seconds")

        time.sleep(DELAY_SECONDS)

    print("-" * 50)
    print(f"RESULTS: {NUM_REQUESTS} requests sent")
    print(f"SUCCESS: {SUCCESS_COUNT}")
    print(f"FAILED: {FAIL_COUNT + (NUM_REQUESTS - SUCCESS_COUNT - FAIL_COUNT)}")

if __name__ == "__main__":
    send_requests()