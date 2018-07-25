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
        self.loginButton.clicked.connect(self.login_button_clicked) #로그인 버튼 클릭 Event 등록
        self.accountWindowButton.clicked.connect(self.account_window_button_clicked) #계좌비밀번호창 버튼 클릭 Event 등록

        # Log ListView Model
        self.logModel = QStandardItemModel()
        self.listView.setModel(self.logModel)

    def login_button_clicked(self):
        print('로그인 버튼 클릭')
        self.kwos.login() #로그인 창 호출

    def account_window_button_clicked(self):
        print('계좌비밀번호창 버튼 클릭')
        self.kwos.showAccountWindow() #계좌비밀번호창 호출

    def kwos_on_login(self, stockItemList, conditionList):
        #사용자 조건식
        self.logModel.appendRow(QStandardItem('사용자조건식 리스트:'))
        for condition in conditionList:
            self.logModel.appendRow(QStandardItem(str(condition)))

        #종목리스트
        self.logModel.appendRow(QStandardItem('종목 리스트:'))
        for stockItem in stockItemList:
            self.logModel.appendRow(QStandardItem(str(stockItem)))

        #로그인 접속 상태
        if self.kwos.getLoginState():
            self.loginStateLabel.setText('접속됨')

        #계좌번호
        accountList = self.kwos.getAccountList()
        for account in accountList:
            self.accountComboBox.addItem(account)

        #서버 구분
        self.serverLabel.setText(self.kwos.getServerState())

        #아이디
        self.idLabel.setText(self.kwos.getUserId())

        #비밀번호
        self.nameLabel.setText(self.kwos.getUserName())

if __name__ == "__main__":
    app = QApplication([])
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()