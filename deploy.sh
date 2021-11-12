#!/bin/bash

COLOR_NORMAL="$(tput sgr0)"
COLOR_RED="$(tput setaf 1)"
COLOR_GREEN="$(tput setaf 2)"
COLOR_YELLOW="$(tput setaf 3)"
COLOR_BLUE="$(tput setaf 4)"
COLOR_CYAN="$(tput setaf 6)"

#LOCAL_ADDRESS="http://localhost:8888/prjct_react/gaming_ruler"
LOCAL_ADDRESS="https://www.mobile-battles.com"
REMOTE_ADDRESS="https://www.mobile-battles.com"

FTP_SERVER="access888703219.webspace-data.io"
#FTP_ROOT_DIR="/public_html/mobile-battles.com/"
FTP_ROOT_DIR="/"
FTP_USER="u106260247"
FTP_PASS="Bfzk7xmY4ah%5z7Bfzk7xmY4ah%5z7"

SOURCES="all"
BUILD="no"

while [[ $# -gt 0 ]]
do
key="$1"

# Example command:
# ./deploy.sh -s php
# ./deploy.sh -s all -b

case $key in
    -s|--sources)
    SOURCES="$2"
    shift # past argument
    shift # past value
    ;;
    -b|--build)
    BUILD="yes"
    shift # past argument
    #shift # past value
    ;;
    -bt|--buildtest)
    BUILD="test"
    shift # past argument
    #shift # past value
    ;;
    *)    # unknown option
    POSITIONAL+=("$1") # save it in an array for later
    printf "${COLOR_RED}Unknown option passed: ${key}\nExisting...${COLOR_NORMAL}\n"
    exit 1
    shift # past argument
    ;;
esac
done

#read tag from remote
git fetch --prune --tags
#extract tag from git
#TAGV=`git describe --tags --long`
TAGV=`git tag --sort=committerdate | tail -1`
REV=`git log --oneline | wc -l | tr -d ' '`
VER=${TAGV%-*}-$REV
VER=${VER//[-]/.}

# Strings:
#jq --arg a "${version}" '.version = $a' src/components/settings.js > "tmp" && mv "tmp" src/components/settings1.js
# tmp=$(sed 's|version: ".*"|version: "'${VER}'"|g' src/components/setting.js); printf "%s" "$tmp" >src/components/setting.js
# tmp=$(sed 's|serverUrl: ".*"|serverUrl: "'${REMOTE_ADDRESS}'"|g' src/components/setting.js); printf "%s" "$tmp" >src/components/setting.js
#cp config.ini dist/config.ini

if [[ $BUILD = "yes" ]]
then
    yarn build
elif [[ $BUILD = "test" ]]
then
    yarn  build-test
fi


printf "${COLOR_RED}Starting the website deployment...${COLOR_NORMAL}\n"
if [[ $SOURCES = "js" ]]
then
    printf "${COLOR_YELLOW}Deploying JS is not supported${COLOR_NORMAL}\n"
elif [[ $SOURCES = "php" ]]
then
    printf "${COLOR_GREEN}Deploying only PHP source files (API)${COLOR_NORMAL}\n"
    printf "${COLOR_CYAN}Deploying PHP now...${COLOR_NORMAL}\n"
    scp -r "${PWD}" ${FTP_USER}@${FTP_SERVER}:
fi
# tmp=$(sed 's|serverUrl: ".*"|serverUrl: "'${LOCAL_ADDRESS}'"|g' src/components/setting.js); printf "%s" "$tmp" >src/components/setting.js
printf "${COLOR_RED}Deployment finished...${COLOR_NORMAL}\n"