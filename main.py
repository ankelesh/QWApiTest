from requester import Requester
import testvalues
from urllib import error
from json import loads



if __name__ == '__main__':
    m_rec = Requester("publickey.crt", 'pkcs8.key', testvalues.CHECK_URL, testvalues.PAY_URL, testvalues.STATUS_URL, testvalues.CANCEL_URL, testvalues.CONTEXT, 2)

    # changes test behaviour
    TEST_OPERATION = 'cancel'
    #TEST_OPERATION = 'pay'

    try:
        print(m_rec.check(testvalues.WALLET_ID, testvalues.AMOUNT, testvalues.CCY))
        print('-'* 80)
        res = m_rec.pay(testvalues.ID_DATA, testvalues.RECEIPT_DATA, testvalues.ITEM_LIST)
        decoded = loads(res)
        print(res)
        oid = decoded['operationId']


        if TEST_OPERATION == 'cancel':
            res = m_rec.cancel(oid)
            print(res)
        elif TEST_OPERATION == 'pay':
            input("press enter after payment confirm")

        print('-' * 80)
        print(m_rec.status(oid))
        print('-' * 37 + 'SUCCESS' + '-' * 36)
    except error.HTTPError as e:
        print (e)

