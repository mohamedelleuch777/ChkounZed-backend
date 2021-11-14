#!/bin/bash

COLOR_NORMAL="$(tput sgr0)"
COLOR_RED="$(tput setaf 1)"
COLOR_GREEN="$(tput setaf 2)"
COLOR_YELLOW="$(tput setaf 3)"
COLOR_BLUE="$(tput setaf 4)"
COLOR_CYAN="$(tput setaf 6)"

ADD="no"
MESSAGE=""
BRANCH=""
ORIGIN=""

while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -a|--add)
    ADD="yes"
    shift # past argument
    #shift # past value
    ;;
    -m|--message)
    MESSAGE="$2"
    shift # past argument
    shift # past value
    ;;
    -p|--push)
    ORIGIN="$2"
    BRANCH="$3"
    shift # past argument
    shift # past value1
    shift # past value2
    ;;
    *)    # unknown option
    POSITIONAL+=("$1") # save it in an array for later
    printf "${COLOR_RED}Unknown option passed: ${key}\nExisting...${COLOR_NORMAL}\n"
    exit 1
    shift # past argument
    ;;
esac
done

# Example command:
# ./commit.sh --add -m "message here" -p origin master

if [[ $MESSAGE = "" ]]
then
    printf "${COLOR_RED}Commit message option should be passed by -m or --message\nExisting...${COLOR_NORMAL}\n"
    exit 1
fi

if [[ $ADD = "yes" ]]
then
    git add .
    printf "${COLOR_GREEN}All changes has been added to the commit${COLOR_NORMAL}\n"
fi
git commit -m"$MESSAGE"
printf "${COLOR_GREEN}All changes has been commited${COLOR_NORMAL}\n"

if [[ $ORIGIN = "" ]]
then
    printf "${COLOR_GREEN}Trying to push to default location${COLOR_NORMAL}\n"
    git push
else
    printf "${COLOR_GREEN}Trying to push the branch ${BRANCH} to ${ORIGIN}${COLOR_NORMAL}\n"
    git push ${ORIGIN} ${BRANCH}
fi

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
#tmp=$(sed 's|version: ".*"|version: "'${VER}'"|g' src/components/setting.js); printf "%s" "$tmp" >src/components/setting.js


printf "${COLOR_BLUE}version: ${VER}${COLOR_NORMAL}\n"
printf "${COLOR_RED}Git operations finished...${COLOR_NORMAL}\n" 