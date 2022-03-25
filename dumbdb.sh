# Colors
red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`

cd saleapp/db

# export db to json file
echo "${green}>>> Start Dumbing file to /saleapp/db/data.json ${reset}"
python ../manage.py dumpdata --format=json --indent=2 --exclude=admin --exclude=sessions > data.json


# cd ..
# cd ..

# # run import.py file to import data into database
# echo -e "\n"
# echo "${green}>>> import.py file to import data into database ${reset}"
# python \saleapp/db/import.py