import cx_Oracle

class database_login:
    address=''
    username=''
    password=''
    def __init__(self,address,username,password):
        self.address=address
        self.username=username
        self.password=password
    def login(self):
        return cx_Oracle.connect(self.username, self.password, self.address)

        #cx_Oracle.connect('BJYJY', 'abc@123', '10.10.31.115:1521/orcl')
