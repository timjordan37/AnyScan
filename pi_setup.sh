#!/bin/bash

# pi_setup - A script to configure a KaliPi for development of ASU Group 9 Capstone
# First argument must be new system user name
# Second argument must be GitHub account email
# Third argument specifies Github SSH setup

##### Constants
GIT_CLONE_PATH="https://github.com/curtis2point0/grp9cap18.git"
GIT_SSH_PATH="git@github.com:curtis2point0/grp9cap18.git"

##### Functions

function pause(){
	read -p "$*"
}

##### Main
if [ "$#" -lt 2 ]; then
	echo "You must specify at least first 2 arguments"
	exit 1
else
	# update OS and install needed packages
	apt-get update
	apt-get upgrade
	# delete default credentials
	rm /etc/ssh/ssh_host_*
	dpkg-reconfigure openssh-server
	service ssh restart
	# reset sudo password
	passwd
	# create new user and add to sudoers
	adduser $1
	usermod -aG sudo $1
	# create git repo folder
	mkdir /home/$1/git
	# Generate ssh key for GitHub account if desired - must add to Github account manually
	if [ "$3" != "" ]; then
		sudo ssh-keygen -t rsa -b 4096 -C "$2"
		eval "$(ssh-agent -s)"
		ssh-add .ssh/id_rsa
		cat .ssh/id_rsa.pub
		pause "Press [Enter] after navigating to your GitHub account and adding the new ssh key printed above."
		cd /home/$1/git
		ssh -T git@github.com
		git clone $GIT_SSH_PATH
		cd
	else
		cd /home/$1/git
		git clone $GIT_CLONE_PATH
		cd
	fi
	
	apt-get install python3
	apt-get install python3-pip
	apt-get install gedit
	apt autoremove
	apt-get install libtiff5-dev libjpeg62-turbo-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev libharfbuzz-dev libfribidi-dev tcl8.6-dev tk8.6-dev python3-tk
fi
pip3 install -r /home/$1/git/grp9cap18/requirements.txt
