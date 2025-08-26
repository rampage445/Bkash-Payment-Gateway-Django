# The execution flow 

get_token() -> create_payment() -> execute_payment() 

# How to use it?

1. Create an app(Ex. Payment)
2. use the urls.py and views.py
3. Upon running it will show the tokenized bkash payment ui
4. Just call the get_token() function, it will guide you.

# Don't Forget
1. Make sure you save the transaction history(Ex. you may need to refund). So, I have a Transaction table here.
2. make sure you set these following constants in settings.py. Once you open your merchant account, you will get these credentials.

BKASH_USERNAME = ''
BKASH_PASSWORD = ''
BKASH_APP_KEY = ''
BKASH_SECRET_KEY = ''

BKASH_TOKEN_URL = "https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/token/grant"
BKASH_CREATE_PAYMENT_URL =  "https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/create"
BKASH_EXECUTE_PAYMENT_URL = "https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/execute"