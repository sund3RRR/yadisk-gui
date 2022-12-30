#!/bin/bash
mkdir temp

if [[ $(which rpm)=="/usr/bin/rpm" ]]; then
    wget http://repo.yandex.ru/yandex-disk/yandex-disk-latest.x86_64.rpm -i $PWD/temp
    pkexec sh -c "rpm -i $PWD/yandex-disk-latest.x86_64.rpm"
elif [[ $(which apt)=="/usr/bin/apt" ]]; then
    wget http://repo.yandex.ru/yandex-disk/yandex-disk-latest.x86_64.deb -i $PWD/temp
    pkexec sh -c "dpkg -i $PWD/yandex-disk-latest.x86_64.deb"
fi

rm -rf temp/