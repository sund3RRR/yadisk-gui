import subprocess, time

yd = subprocess.Popen(["yandex-disk"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                bufsize=0)
stdout = yd.communicate("token")
while yd.poll() == None:
    print(stdout)
    time.sleep(0.5)

print(yd.poll())