import time
from random import randint
CONTEXT = {
    'headers' : {
    "X-MERCHANT": "alias1"
}
}

WALLET_ID =  "37369111111"
AMOUNT = 9
CCY = "498"
ITEM_LIST = [
    {
        "price":"10",
        "title" : "Test product 1",
        "subtitle":"coninfo test"
    }
]
RECEIPT_DATA = {
    "ccy": "498",
    "price": 12,
    "discount": 1,
    "amount": 9,
    "tax": 1
}
ID_DATA = {
    "walletId": WALLET_ID,
    "invoiceId": "1122334455667788" + str(randint(1000, 9999)),
    "customerId": str(randint(100000, 999999)),
    "when": int(time.time() * 1000),
    "clientIp": "123.123.123.123"
}

CHECK_URL = '/merchant/checkout/check'
PAY_URL = '/merchant/checkout/pay'
STATUS_URL = '/merchant/checkout/status/'
CANCEL_URL = '/merchant/checkout/cancel'