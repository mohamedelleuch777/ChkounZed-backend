#!/bin/bash

# example of use:
# ./createGitTag.sh 0.32
# with 0.32 is the tag name

COLOR_NORMAL="$(tput sgr0)"
COLOR_RED="$(tput setaf 1)"
COLOR_GREEN="$(tput setaf 2)"
COLOR_YELLOW="$(tput setaf 3)"
COLOR_BLUE="$(tput setaf 4)"
COLOR_CYAN="$(tput setaf 6)"

printf "${COLOR_YELLOW}Creating the tag: ${1}${COLOR_NORMAL}\n"

git tag ${1}
git push origin --tags