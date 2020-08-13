import subprocess,random,os,time

dirname = os.path.dirname(os.path.abspath(__file__))
print(dirname)

while True:

    wait_period = random.randint(15, 20)
    subprocess.call(["python",f"{dirname}" + '\\villaDianaWatcher.py'])
    print(f"Success. Waiting for {wait_period} seconds")
    time.sleep(wait_period)
