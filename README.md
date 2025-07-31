# coding-case-julia

## SHORT LOCATION

### REQUIREMENTS
* Python 3.12
* Docker environment

### Running and using the docker container
+ The project is set up to run inside a docker environment.
+ In a terminal from inside this project's root directory run:
```bash
docker-compose up -d --build
```
+ This command builds and runs the docker environment in a detached mode
+ You can now test the service manually by calling this url: http://localhost:8000/docs#
+ From here you can test the single routes

### Testing the docker container
+ There is an integration test set up to be run inside a docker environment
+ The testcase is setup inside the docker-compose.testing.yml
+ To run the test call the following command from the terminal:
```bash
docker compose -f docker-compose.testing build
docker compose -f docker-compose.testing up --build
```
+ It will build and run the testing environment
+ You can follow the logs on the terminal

### Known errors and issues
+ You can pass other geo graphical locations than cities into the post request and get a result if this location exist
+ There can be more than one result for a inserted city, but only the first result is return currently
+ The used geo api can be throttled. Requests that worked in first place might fail in a second call. This is part of the *terms of use* of https://photon.komoot.io
