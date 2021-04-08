from requester import Requester
import testvalues



m_rec = Requester("publickey.crt", 'pkcs8.key', testvalues.CHECK_URL, testvalues.PAY_URL, testvalues.STATUS_URL, testvalues.CONTEXT)
print(m_rec.check(testvalues.WALLET_ID, testvalues.AMOUNT, testvalues.CCY).decode('utf-8'))
print('-'* 80)
print(m_rec.pay(testvalues.ID_DATA, testvalues.RECEIPT_DATA, testvalues.ITEM_LIST))
print('-' * 80)

