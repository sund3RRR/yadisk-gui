import subprocess, time

yd = subprocess.Popen(["yandex-disk", "token"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                bufsize=0)

for line in yd.stdout:
    print(line.strip())
