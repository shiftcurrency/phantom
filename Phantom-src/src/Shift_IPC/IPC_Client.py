import socket
import json
import os
import sys

class Client(object):

    def __init__(self, ipc_path=None, *args, **kwargs):
        if ipc_path is None:
            ipc_path = self.get_default_ipc_path()

        self.ipc_path = ipc_path
        self._socket = self.get_socket()

        super(Client, self).__init__(*args, **kwargs)


    def get_shiftbase(self):
        response = self._make_request("shf_shiftbase", [])
        return response


    def unlock_account(self, account, password):
        response = self._make_request("personal_unlockAccount", [account,password,60])
        return response


    def create_account(self, password):
        response = self._make_request("personal_newAccount", [password])
        return response

    def get_accounts(self):
        response = self._make_request("shf_accounts", [])
        return response


    def send_transaction(self, sender, receiver, amount, nrg, data):

        if nrg and not data:
            trans_params = [{"from": sender, "to": receiver, "value": hex(int(amount)), "gas": hex(int(nrg))}]
        elif nrg and data:
            trans_params = [{"from": sender, "to": receiver, "value": hex(int(amount)), "gas": hex(int(nrg)), "data" : data}]
        else:
            trans_params = [{"from": sender, "to": receiver, "value": hex(int(amount))}]

        response = self._make_request("shf_sendTransaction", trans_params)
        return response


    def construct_json_request(self, method, params):
        request = json.dumps({"jsonrpc": "2.0","method": method, "params": params,"id": "1"})
        return request


    def get_default_ipc_path(self):

        ''' Return the path of shift IPC file depending on OS '''

        if sys.platform == 'darwin':
            ipc_path = os.path.expanduser("~/Library/gshift/gshift.ipc")
        elif sys.platform == 'linux2':
            ipc_path = os.path.expanduser("~/.gshift/gshift.ipc")
        elif sys.platform == 'win32':
            ipc_path = os.path.expanduser("\\~\\AppData\\Roaming\\gshift")
        else:
            raise ValueError(
                "Unsupported platform.  Only darwin/linux2/win32 are "
                "supported.  You must specify the ipc_path"
            )
        return ipc_path


    def get_socket(self):
        _socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        _socket.connect(self.ipc_path)
        # Tell the socket not to block on reads.
        _socket.settimeout(2)
        return _socket


    def _make_request(self, method, params):
        request = self.construct_json_request(method, params)

        for _ in range(3):
            self._socket.sendall(request)
            response_raw = ""

            while True:
                try:
                    response_raw += self._socket.recv(4096)
                except socket.timeout:
                    break

            if response_raw == "":
                self._socket.close()
                self._socket = self.get_socket()
                continue

            break
        else:
            raise ValueError("No JSON returned by socket")

        response = json.loads(response_raw)

        if "error" in response:
            raise ValueError(response["error"]["message"])

        return response