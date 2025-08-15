# private key

```
openssl genrsa -out jwt-private.pem 2048
```

# public key
```
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
```

# pyjwt
```
pip install "pyjwt[crypto]"
```

# bcrypt
```
pip install bcrypt
```