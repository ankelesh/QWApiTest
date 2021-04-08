from urllib.request import Request, urlopen
from json import dumps
import OpenSSL
import base64


class Requester:

    base_context = {'headers': {

        }
    }
    json_header = ('Content-Type', 'application/json')
    baseUrl = "https://api.stg.qwallet.md"

    def make_signature(self, data):
        signature = OpenSSL.crypto.sign(self.privatekey, data, 'sha256')
        signature = base64.b64encode(signature)
        return signature

    def debug_out(self, req, body):
        print("sending request to " + req.full_url)
        print("headers: " + str(req.headers))
        print('body: ' + body.decode('utf-8'))

    def __init__(self,public_key, private_key, checksignature="", paysignature="", statussignature="", context=None ):
        f = open(public_key)
        self.publickey = OpenSSL.crypto.load_publickey(OpenSSL.crypto.FILETYPE_PEM, f.read())
        f.close()
        f = open(private_key)
        self.privatekey = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, f.read())
        f.close()

        self.checkUrl = self.baseUrl + checksignature
        self.payUrl = self.baseUrl + paysignature
        self.statusUrl = self.baseUrl + statussignature
        if context is not None:
            self.context = self.base_context.copy()
            self.context.update(context)
        else:
            self.context = {}
        print (self.context)

    def check(self, walletid, amount, ccy = "498"):
        data = {
            "walletId" : walletid,
            "amount" : amount,
            "ccy" : ccy
        }
        b_data = dumps(data).encode('utf-8')
        current_req = Request(self.checkUrl, headers=self.context['headers'])
        current_req.add_header(*self.json_header)
        current_req.add_header('X-SIGNATURE', self.make_signature(b_data))
        self.debug_out(current_req, b_data)
        result = urlopen(current_req, b_data)
        return result

    def pay(self, idlist, receipt, items):
        req_body = idlist.copy()
        req_body["check"] = receipt.copy()
        req_body["check"]["items"] = items
        b_data =  dumps(req_body).encode('utf-8')
        current_req = Request(self.payUrl, headers=self.context['headers'])
        current_req.add_header(*self.json_header)
        current_req.add_header('X-SIGNATURE', self.make_signature(b_data))
        self.debug_out(current_req, b_data)
        result = urlopen(current_req, b_data)
        return result

    def status(self, operationid):
        current_req = Request(self.statusUrl + operationid, headers=self.context['headers'])
        result = urlopen(current_req)
        return result
