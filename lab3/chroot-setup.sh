#!/bin/sh -x
if id | grep -qv uid=0; then
    echo "Must run setup as root"
    exit 1
fi

create_socket_dir() {
    local dirname="$1"
    local ownergroup="$2"
    local perms="$3"

    mkdir -p $dirname
    chown $ownergroup $dirname
    chmod $perms $dirname
}

set_perms() {
    local ownergroup="$1"
    local perms="$2"
    local pn="$3"

    chown -R $ownergroup $pn
    chmod -R $perms $pn
}

mkdir -p /jail
cp -p index.html /jail
cp -p password.cgi /jail

./chroot-copy.sh zookd /jail
./chroot-copy.sh zookfs /jail
./chroot-copy.sh zooksvc /jail

#./chroot-copy.sh /bin/bash /jail

./chroot-copy.sh /usr/bin/env /jail
./chroot-copy.sh /usr/bin/python /jail

mkdir -p /jail/usr/lib/
cp -r /usr/lib/python2.6 /jail/usr/lib
cp -r /usr/lib/pymodules /jail/usr/lib
cp /usr/lib/libsqlite3.so.0 /jail/usr/lib

mkdir -p /jail/usr/local/lib/
cp -r /usr/local/lib/python2.6 /jail/usr/local/lib

mkdir -p /jail/etc
cp /etc/localtime /jail/etc/
cp /etc/timezone /jail/etc/

mkdir -p /jail/usr/share/zoneinfo
cp -r /usr/share/zoneinfo/America /jail/usr/share/zoneinfo/

create_socket_dir /jail/blnssvc 61014:61014 755
create_socket_dir /jail/logsvc 61010:61010 770
create_socket_dir /jail/authsvc 61015:61015 755

mkdir -p /jail/tmp
chmod a+rwxt /jail/tmp

cp -r zoobar /jail/

python /jail/zoobar/zoodb.py init-person
python /jail/zoobar/zoodb.py init-transfer
python /jail/zoobar/zoodb.py init-balance
python /jail/zoobar/zoodb.py init-auth

#set_perms 61011:61011 755 /jail/zoobar/db

set_perms 61011:61011 755 /jail/zoobar/db/person
set_perms 61010:61010 755 /jail/zoobar/db/transfer
set_perms 61014:61014 755 /jail/zoobar/db/zoobars
set_perms 61015:61015 700 /jail/zoobar/db/auth
