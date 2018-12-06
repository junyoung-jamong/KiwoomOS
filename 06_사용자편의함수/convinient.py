from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QAxContainer import *
from kiwoomOS.kwos import KiwoomOS

main_window = uic.loadUiType("main_window.ui")[0]

class MyWindow(QMainWindow, main_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()

        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.kwos = KiwoomOS(self.kiwoom)

        self.kwos.addOnLogin(self.kwos_on_login) #로그인 결과 Event 등록
        self.kwos.addOnReceiveTr(self.kwos_on_receive_tr) #TR데이터 수신 Event 등록
        self.kwos.addOnReceiveAccountState(self.kwos_on_receive_account_state)
        self.kwos.addOnReceiveConditionPrice(self.kwos_onReceive_condition_price)

        self.login_btn.clicked.connect(self.login_btn_clicked)
        self.rq_btn.clicked.connect(self.rq_btn_clicked)

    def login_btn_clicked(self):
        self.kwos.login()

    def rq_btn_clicked(self):
        #print(self.kwos.getAccountState())
        #print(self.kwos.getBalanceList())
        index = self.kwos.getConditionIndexByName('테스트등락주')
        print(index)
        name = self.kwos.getConditionNameByIndex(2)
        print(name)

        self.kwos.requestConditionPrice('005930', '테스트등락주')

    def kwos_on_login(self, stock_list, condition_list):
        account_list = self.kwos.getAccountList()
        self.kwos.requestAccountState(account_list[0])

    def kwos_on_receive_tr(self, rqName, trCode, hasNext):
        pass

    def kwos_on_receive_account_state(self, account_state, balance_list):
        print(account_state)
        print(balance_list)

    def kwos_onReceive_condition_price(self, code, condition_name, price, data):
        print(code)
        print(condition_name)
        print(price)
        print(data)

if __name__ == '__main__':
    app = QApplication([])
    myWindow = MyWindow()
    app.exec_()