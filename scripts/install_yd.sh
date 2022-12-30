#!/bin/bash
mkdir temp
cd temp
wget http://repo.yandex.ru/yandex-disk/yandex-disk-latest.x86_64.rpm
ls -la
pkexec sh -c "rpm -ihv $PWD/yandex-disk-latest.x86_64.rpm"
cd ..
rm -rf temp/