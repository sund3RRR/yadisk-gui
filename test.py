import subprocess, time

yd = subprocess.Popen(["yandex-disk", "token"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                bufsize=20)
stdout = yd.communicate()
while yd.poll() == None:
    print(stdout)
    time.sleep(0.5)

print(yd.poll())