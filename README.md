## Feature
- Restful API Web Service ✅
- Unified Interface for all couriers servies ✅
- Documentation ✅
- Impelementation for (creating a waybill, print waybill label, tracking shipment status) ✅
- Optional cancellation functionality for some couriers. ✅
- Message Broker & Worker ✅
- Simple dummy Integration with Fedex sandbox api ✅
- Testing (Todo)
- Seeds ✅
- Authentication ✅
- Standardized responses & error handling ✅

## Tools
- Python
- Django
- MySQL
- phpMyAdmin
- RabbitMQ
- Docker & Docker-compose

## Documentation
You can either 
- Navigate it through django server at ```/api/schema/swagger-ui ```
- Copy the yaml file content from ``` https://github.com/Hussein-ElAttar/zidship/blob/master/schema.yam1 ``` and paste it in the official swagger editor ```https://editor.swagger.lo/```
## Running the project with docker: 
- clone the repo ```git clone https://github.com/Hussein-ElAttar/zidship.git ```
- cd into project root ```cd zidship```
- Add a ```.env``` file, you can use the data included in ```.env.example``` file
- Start the app: ```docker-compose up```

## API Authentication 
- Use the username & password from the ```.env.example``` file


