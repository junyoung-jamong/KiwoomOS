from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QAxContainer import *
from kiwoomOS.kwos import *

main_window = uic.loadUiType("main_window.ui")[0]

class MyWindow(QMainWindow, main_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.kwos = KiwoomOS(self.kiwoom)
        self.kwos.addOnLogin(self.kwos_on_login) #로그인 결과 Event 등록
        self.kwos.addOnReceiveReal(self.kwos_on_receive_real)

        self.loginButton.clicked.connect(self.login_button_clicked) #로그인 버튼 클릭 Event 등록
        self.addRealButton.clicked.connect(self.addReal_button_clicked)  #실시간등록 버튼 클릭 Event 등록

    def login_button_clicked(self):
        print('로그인 버튼 클릭')
        self.kwos.login() #로그인 창 호출

    def addReal_button_clicked(self):
        itemCode = '005930'
        print(itemCode)
        self.kwos.addRealData(itemCode)

    #로그인 결과 Event
    def kwos_on_login(self, stockItemList, conditionList):
        #종목 리스트
        self.stockItemList = stockItemList

        for stockItem in stockItemList:
            self.stockItemListWidget.addItem(stockItem['종목명'])

    #실시간 데이터 수신Event
    def kwos_on_receive_real(self, code, data):
        print(code, data)

if __name__ == "__main__":
    app = QApplication([])
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()