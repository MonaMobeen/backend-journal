import asyncio
import time
import threading
import multiprocessing
import aiohttp 


# ---------- Threading for I/O-Bound Work ----------
# Threading is useful when a task spends most of its time WAITING
# (e.g. waiting for a network response, a file, or a database) rather
# than actually using the CPU.
def download_file_simulation(file_id):
    print(f"Starting download {file_id}...")
    time.sleep(1)  # simulates waiting for a slow network response
    print(f"Finished download {file_id}.")


def run_with_threading():
    start = time.time()
    threads = []
    for i in range(3):
        thread = threading.Thread(target=download_file_simulation, args=(i,))
        threads.append(thread)
        thread.start()  # starts running immediately, doesn't wait

    for thread in threads:
        thread.join()  # wait here until this thread finishes

    print(f"Threading total time: {time.time() - start:.2f} seconds\n")


run_with_threading()
# Notice: 3 downloads that each take 1 second finish in ~1 second total
# (not 3 seconds), because they were all WAITING at the same time.


# ---------- Multiprocessing for CPU-Bound Work ----------
# Multiprocessing is useful when a task is actually CRUNCHING NUMBERS
# (using the CPU heavily), not just waiting. Each process gets its own
# separate CPU core to work on, unlike threads which share one core.
def cpu_heavy_task(n):
    total = sum(i * i for i in range(n))
    return total


def run_with_multiprocessing():
    start = time.time()
    with multiprocessing.Pool(processes=3) as pool:
        results = pool.map(cpu_heavy_task, [5_000_000, 5_000_000, 5_000_000])
    print(f"Multiprocessing results: {results}")
    print(f"Multiprocessing total time: {time.time() - start:.2f} seconds\n")


if __name__ == "__main__":
    run_with_multiprocessing()


# ---------- async / await ----------
# async/await is another way to handle I/O-bound waiting, but WITHOUT
# creating real separate threads - everything runs on a single thread,
# switching between tasks efficiently while one is waiting.
async def fetch_data_simulation(name, delay):
    print(f"Fetching {name}...")
    await asyncio.sleep(delay)  # non-blocking wait - lets other tasks run meanwhile
    print(f"Finished fetching {name}.")
    return f"{name} data"


async def run_async_example():
    start = time.time()

    # Running these concurrently instead of one after another
    results = await asyncio.gather(
        fetch_data_simulation("Users", 1),
        fetch_data_simulation("Orders", 1),
        fetch_data_simulation("Products", 1),
    )

    print(f"Async results: {results}")
    print(f"Async total time: {time.time() - start:.2f} seconds\n")


asyncio.run(run_async_example())


# ---------- Why async Does NOT Automatically Speed Up CPU-Heavy Code ----------
# async is designed for WAITING efficiently, not for doing more CPU work
# at once. If the code inside an async function is CPU-heavy (no awaiting),
# it still blocks everything else, exactly like normal synchronous code.
async def bad_async_example():
    print("Starting CPU-heavy work inside async (this will NOT run concurrently)...")
    total = sum(i * i for i in range(5_000_000))  # no "await" here - blocks the event loop
    print("Finished CPU-heavy work.")
    return total


# For real CPU-heavy work, use multiprocessing instead of async.

# ---------- Async HTTP Client Example ----------
async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            print(data)


asyncio.run(fetch_data("https://jsonplaceholder.typicode.com/users"))

# ---------- Cancellation and Timeouts ----------
async def slow_operation():
    print("Slow operation started...")
    await asyncio.sleep(5)
    print("Slow operation finished.")  # this line may never be reached
    return "done"


async def run_with_timeout():
    try:
        result = await asyncio.wait_for(slow_operation(), timeout=2)
        print(f"Result: {result}")
    except asyncio.TimeoutError:
        print("Operation timed out after 2 seconds - cancelled automatically.\n")


asyncio.run(run_with_timeout())

# ----------Example #01 Asyncio Event Loop ----------

async def task(name, delay):
    print(f"{name} started")
    await asyncio.sleep(delay)
    print(f"{name} finished")


async def main():
    await asyncio.gather(
        task("Task 1", 2),
        task("Task 2", 1),
        task("Task 3", 3)
    )


asyncio.run(main())


 