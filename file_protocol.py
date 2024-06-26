import json
import logging
import shlex
import base64

from file_interface import FileInterface

"""
* class FileProtocol bertugas untuk memproses 
data yang masuk, dan menerjemahkannya apakah sesuai dengan
protokol/aturan yang dibuat

* data yang masuk dari client adalah dalam bentuk bytes yang 
pada akhirnya akan diproses dalam bentuk string

* class FileProtocol akan memproses data yang masuk dalam bentuk
string
"""

class FileProtocol:
    def __init__(self):
        self.file = FileInterface()
        
    def proses_string(self,string_datamasuk=''):
        logging.warning(f"string diproses: {string_datamasuk}")
        c = shlex.split(string_datamasuk)
        try:
            c_request = c[0].strip()
            logging.warning(f"memproses request: {c_request}")
            params = [x for x in c[1:]]
            if c_request == 'UPLOAD':
                filename=params[0]
                filedata=' '.join(params[1:])
                params=[filename, filedata]    
            cl = getattr(self.file,c_request.lower())(params)
            return json.dumps(cl)
        except Exception as e:
            return json.dumps(dict(status='ERROR', data=f'request tidak dikenali'))
                                   

if __name__=='__main__':
    #contoh pemakaian
    fp = FileProtocol()
    # print(fp.proses_string("LIST"))
    # print(fp.proses_string("GET pokijan.jpg"))