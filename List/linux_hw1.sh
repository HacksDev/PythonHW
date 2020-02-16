#!/bin/bash
# Make sure only root can run script
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi;

# Create main ftp folder.
BASE_DIR=/var/ftp;
mkdir -p $BASE_DIR;


# Create group that includes superusers.
groupadd ftpadmins;
# Create group that includes ftp users.
groupadd ftpusers;

# Create superuser;
useradd -d $BASE_DIR -G ftpadmins ftpmod;

# Create users;
useradd -m -d $BASE_DIR/u1 -G ftpusers u1;
chown u1 $BASE_DIR/u1;
chgrp ftpadmins $BASE_DIR/u1;
useradd -m -d $BASE_DIR/u2 -G ftpusers u2;
chown u2 $BASE_DIR/u2;
chgrp ftpadmins $BASE_DIR/u2;
useradd -m -d $BASE_DIR/u3 -G ftpusers u3;
chown u3 $BASE_DIR/u3;
chgrp ftpadmins $BASE_DIR/u3;


# Set super group as owner
chgrp ftpadmins $BASE_DIR;
chgrp ftpadmins $BASE_DIR/*;

# Set permission rules
chmod u+rwx,g+rwx,o-rwx $BASE_DIR/*;
chmod g+s $BASE_DIR/*;
# With using ACL: setfacl -R -d -m u::rwx,g::rwx,o::--- $BASE_DIR/*

# How to check it...
# 1. docker run -it --name=ubuntu ubuntu:latest
# 2. apt update
# [2.1] apt install acl nano
# 3. Write this into scriptname.sh file.
# 4. chmod 777 scriptname.sh
# 5. ./scriptname.sh
# 6. su - u1 # to change account
