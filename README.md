# Rara Mini Api Server

The project is to build a simple auth server with django. And django rest framework with handle rest apis. The api will handle JWT Token authentication using asymmetric private and public keys. 

## Features
- JWT Token authentication
- JWKS endpoint

## Installation

You can start the setup by creating virtual environment. And activating the virtual environment. Then, you can install dependencies using pip:
```
pip install -r requirements.txt
```
Now, you have required packages. You can create your *public key* and *private key*.
_Example_:
```
mkdir certs
openssl genrsa -out certs/private.pem 4096 
openssl rsa -in certs/private.pem -pubout -out certs/public.pem
```
*Note:- private and public key directory will be added to settings.

To add the environment variable for *SECRET_KEY*, you can either add the environment variable. Or, you can create a `.env` file in root directory of the project i.e, in same level as `manage.py`. In the `.env` file, you can set environment variable as:
```
SECRET_KEY=YOUR_DJANGO_SECRET_KEY
```
*Note:- If you don't set *SECRET_KEY* environment variable, application will still run with the default *SECRET_KEY*. But, you MUST add your secret key yourself.

Now you can migrate to create tables:
```
python manage.py migrate
```
As our tables are created, you can now create sample user. By:
```
python manage.py shell < script.py 
```
*Note:- Sample user have following credentials: `email=tester@gmail.com` and `password=tester`. Or, you can change that from *script.py*

Run server and test it out. Also, run test with:
```
python manage.py test && flake8
```

## Configuration

In *settings.py*, you can add your configuration yourself:

```
MY_JWT_CONF = {
    'JWT_ALGORITHM': 'RS256',
    'JWT_HEADER_PREFIX': 'Bearer',
    'JWT_EXPIRATION_TIME_DELTA': datetime.timedelta(seconds=600),
    'JWT_PRIVATE_KEY_PATH': 'certs/private.pem',
    'JWT_PUBLIC_KEY_PATH': 'certs/public.pem',
    'JWT_JWKS_ENDPOINT': 'http://localhost:8000/api/certs/',
    'JWT_DECODE_MONOLITH': True,
}
```
*Note:- `JWT_DECODE_MONOLITH: True` will decode jwt using *public.pem*. `JWT_DECODE_MONOLITH: False`  will decode jwt using jwks endpoint from `JWT_JWKS_ENDPOINT`.


