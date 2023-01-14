import subprocess, time

yd = subprocess.Popen(["yandex-disk", "token"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=0,
                universal_newlines=True)

while yd.poll() == None:
    print(yd.stdout.readline())
    time.sleep(0.5)

print(yd.poll())