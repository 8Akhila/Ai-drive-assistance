import time

class Timer:
    """
    Simple timer utility to measure performance of different stages.
    """

    def __init__(self):
        self.start_time = None

    def start(self):
        self.start_time = time.time()      # Save current timestamp

    def stop(self, msg="Elapsed"):
        elapsed = time.time() - self.start_time
        print(f"{msg}: {elapsed:.2f}s")    # Print elapsed time nicely
