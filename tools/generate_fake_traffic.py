import requests
import time
from concurrent.futures import ThreadPoolExecutor

# API URL
URL = "http://localhost:8000/gameslist/?size=10&page=1"

# Number of requests to send
NUM_REQUESTS = 10000  # Change this to your desired request count
CONCURRENT_WORKERS = 1000  # Number of parallel requests

# Function to send a single GET request
def send_request():
    try:
        response = requests.get(URL)
        return response.status_code, response.elapsed.total_seconds()
    except requests.exceptions.RequestException as e:
        return "ERROR", str(e)

# Measure execution time
start_time = time.time()

# Using ThreadPoolExecutor to send requests in parallel
with ThreadPoolExecutor(max_workers=CONCURRENT_WORKERS) as executor:
    results = list(executor.map(lambda _: send_request(), range(NUM_REQUESTS)))

end_time = time.time()

# Analyze results
success_count = sum(1 for status, _ in results if status == 200)
error_count = NUM_REQUESTS - success_count
average_time = sum(time for _, time in results if isinstance(time, float)) / max(success_count, 1)

# Print Summary
print(f"\n📊 Test Summary:")
print(f"✅ Successful Requests: {success_count}")
print(f"❌ Failed Requests: {error_count}")
print(f"⚡ Average Response Time: {average_time:.4f} sec")
print(f"⏳ Total Test Duration: {end_time - start_time:.2f} sec")
