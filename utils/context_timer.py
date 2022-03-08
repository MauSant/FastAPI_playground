import time

class Timer(object):
    var1 = 1
    def __enter__(self):
        self.t = time.time()
        return self
    
    def __exit__(self, *args):
        self.t = time.time() - self.t