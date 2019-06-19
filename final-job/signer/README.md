# signer
Microservice to digitally sign files. Receives the file through a `POST` request and returns its signature in bytes.

## Requirements
 * `Python3.X` with `virtualenv` installed
 * Setup `.env` file
 * A ` PKCS#12` certificate.  It can be obtained using the following link https://p1.icpedu.rnp.br/default/public/default (the certificate MUST be saved in the root of this the project with the name: `cert.p12`)
 * `Docker` (necessary only for documentation)

### 1. Installing Python dependencies
You should create a `virtualenv` and load it to install the `Python` dependencies
```
$ virtualenv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

### Setting up the `.env` file
You can copy the the `.env.example` file with the `.env` name. Most part of variables are already configured. You need only to to set up the certificate password that you created and the digest (i.e.) the algorithm that you want to use. The available values for the digest variable are:
 * `sha224`
 * `sha256`
 * `sha384`
 * `sha512`
 * `sha3-224`
 * `sha3-256`
 * `sha3-384`
 * `sha3-512`

### Running application
You can run the application using the `run.sh` script:
```
$ ./run.sh
```

The application will be available at the address: `http://$HOST:$PORT`. Both enviroment variables were set in the `.env` file.

### Generating documentation
Documentation uses `swagger-ui` to display information about the routes. With docker installed on your machine, you can do the following:
```
$ docker pull swaggerapi/swagger-ui
$ docker run -p 8080:8080 -e SWAGGER_JSON=/mnt/swagger.json -v $PWD:/mnt swaggerapi/swagger-ui
```

The documentation will be available on your computer on port 8080 in HTML format. Just acess on your browser:
```
http://localhost:8080
```

### Running tests
To run the tests, simply run the `tests.sh` script:
```
$ ./tests.sh
```
