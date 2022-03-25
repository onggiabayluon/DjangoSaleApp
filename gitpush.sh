# Colors
red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`

# git checkout -b "$1"
if [ "$1" != "" ]
then
  echo -e "${green}>>> Git checkout -b "$1" \n"
  git checkout -b "$1"
# else 
#   git checkout master
#   echo -e "${green}>>> Git checkout master"
fi

# git add .
echo -e "${green}>>> Git add . \n"
git add .

# git commit -m "$2"
echo -e "${green}>>> Git commit -m "$2" \n"
git commit -m "$2"

# git push
echo -e "${green}>>> Git push origin head \n"
git push origin head