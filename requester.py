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
        if self.debug_verbosity > 0:
            print("sending request to " + req.full_url)
        if self.debug_verbosity > 1:
            print('body: ' + body.decode('utf-8'))
        if self.debug_verbosity > 2:
            print("headers: " + str(req.headers))

    def __init__(self,public_key, private_key, checksignature="", paysignature="", statussignature="", cancelsignature='', context=None, d_verb = 0):
        f = open(public_key)
        self.publickey = OpenSSL.crypto.load_publickey(OpenSSL.crypto.FILETYPE_PEM, f.read())
        f.close()
        f = open(private_key)
        self.privatekey = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, f.read())
        f.close()

        self.checkUrl = self.baseUrl + checksignature
        self.payUrl = self.baseUrl + paysignature
        self.statusUrl = self.baseUrl + statussignature
        self.cancelUrl = self.baseUrl + cancelsignature
        if context is not None:
            self.context = self.base_context.copy()
            self.context.update(context)
        else:
            self.context = {}
        print (self.context)
        self.debug_verbosity = d_verb

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
        return result.read()

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
        return result.read()

    def status(self, operationid):
        current_req = Request(self.statusUrl + operationid, headers=self.context['headers'])
        current_req.add_header('X-SIGNATURE', self.make_signature(operationid.encode('utf-8')))
        print('requesting: ' + current_req.full_url + "\nheaders: " + str(current_req.headers))

    def cancel(self, operationid):
        current_req = Request(self.cancelUrl, headers = self.context['headers'])
        data = dumps({ 'operationId' : operationid})
        b_data = data.encode('utf-8')
        current_req.add_header('X-SIGNATURE', self.make_signature(b_data))
        self.debug_out(current_req, b_data)
        result = urlopen(current_req, b_data)
        return result.read()
