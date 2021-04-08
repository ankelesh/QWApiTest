import time

CONTEXT = {
    'headers' : {
    "X-MERCHANT": "alias1"
}
}

WALLET_ID =  "3736911111"
AMOUNT = "10"
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
    "price": 110.23,
    "discount": 15.89,
    "amount": 94.34,
    "tax": 11.02
}
ID_DATA = {
    "walletId": WALLET_ID,
    "invoiceId": "11223344556677889900",
    "customerId": "info@una.md",
    "when": int(time.time() * 1000),
    "clientIp": "123.123.123.123"
}

CHECK_URL = '/merchant/checkout/check'
PAY_URL = '/merchant/checkout/pay'
STATUS_URL = '/merchant/checkout/status/'