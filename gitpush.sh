# Colors
red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`

# git checkout -b "$1"
if [ "$1" != "" ]
then
  echo "${green}>>> Git checkout -b "$1""
  git checkout -b "$1"
# else 
#   git checkout master
#   echo "${green}>>> Git checkout master"
fi

# git add .
echo -e "\n"
echo "${green}>>> Git add ."
git add .

# git commit -m "$2"
echo -e "\n"
echo "${green}>>> Git commit -m "$2""
git commit -m "$2"

# git push
echo -e "\n"
echo "${green}>>> Git push origin head"
git push origin head