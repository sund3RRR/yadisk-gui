import subprocess, time

yd = subprocess.Popen(["yandex-disk", "token"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True)

while yd.poll() == None:
    print(yd.stdout.readlines())
    time.sleep(0.5)

print(yd.poll())