import time

start = time.time()
print("hello")

for i in range(40000):
    if(i == 20000):
        import time
        start = time.time()
    end = time.time()
    print(end - start)
