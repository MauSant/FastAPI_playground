# money_transfer_api_fastapi
API for transfer Money with fastapi 

#Dont use the next 2
docker build -t test_fastapi_image .
docker run -d --name fastapi_test_container -p 80:80 test_fastapi_image
 
#Inside the fodler where the Docer and docker-compose is
docker-compose -f docker-compose.local.yml up -d

#DB:
## Use the service name of the docker-compose file, for db.HOST
mysql -h 127.0.0.1 -P 3306 -u mauricio -p


Must install Poetry on python! (pip3.9 install poetry 1.1.13)
