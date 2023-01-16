import subprocess

yd = subprocess.Popen(["yandex-disk", "token"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=0)


output = yd.stdout.read(150).decode("UTF-8")
print(output)
words = output.split(" ")

for word in words:
    if "https://" in word:
        link  = word
    if "‘" == word[0] and "’" == word[-1]:
        code = word[1:-2]

print(link, code)
