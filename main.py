from PyQt5.QtWidgets import  *
from PyQt5 import uic
from PyQt5.QAxContainer import *
import kiwoomOS as KOS
main_window = uic.loadUiType("main_window.ui")[0]

class MyWindow(QMainWindow, main_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.kos = KOS.KiwoomOS(self.kiwoom)

        self.kiwoom.OnEventConnect.connect(self.api_OnEventConnect)  # 로그인 결과 Event
        self.kiwoom.OnReceiveTrData.connect(self.api_OnReceiveTrData) # TR요청 수신결과 Event
        self.kiwoom.OnReceiveRealData.connect(self.api_OnReceiveRealData) # 실시간 데이터 수신 Event
        self.kiwoom.OnReceiveTrCondition.connect(self.api_OnReceiveTrCondition) # 조건검색 결과 Event
        self.kiwoom.OnReceiveRealCondition.connect(self.api_OnReceiveRealCondition) #실시간 조건 수신 Event

        self.loginButton.clicked.connect(self.login_button_clicked)
        self.requestTrButton.clicked.connect(self.request_tr_button_clicked)

    def login_button_clicked(self):
        self.kos.login()

    def request_tr_button_clicked(self):
        print('request_tr_button_clicked()')
        self.kos.setInput('종목코드', '005930')
        rqResult = self.kos.requestTr('종목기본정보', 'opt10001')
        print('rqResult = ', rqResult)

    #로그인
    def api_OnEventConnect(self, nErrCode):
        print('nErrCode ', nErrCode)
        if nErrCode == 0:
            print('로그인 성공')
            print(self.kos.getAccountList())
            print(self.kos.getStockItemList())
        else:
            print('로그인 실패')
    
    #TR데이터 수신
    def api_OnReceiveTrData(self, sScrNo, sRQName, sTrcode, sRecordName, sPrevNext, nDataLength, sErrorCode, sMessage, sSplmMsg):
        print(sRQName)
        cnt = self.kos.getTrCount(sTrcode)
        print(cnt)

        price = self.kos.getTrData(sTrcode, '현재가')
        print('price :', price)

    #실시간 데이터 수신
    def api_OnReceiveRealData(self, sCode, sRealType, sRealData):
        print(sCode, sRealType, sRealData)

    #조건검색 결과 수신
    def api_OnReceiveTrCondition(self, sScrNo, strCodeList, strConditionName, nIndex, nNext):
        print(sScrNo, strCodeList, strConditionName, nIndex, nNext)

    #실시간 조건 편입/이탈 수신
    def api_OnReceiveRealCondition(self, strCode, strType, strConditionName, strConditionIndex):
        print(strCode, strType, strConditionName, strConditionIndex)

if __name__ == "__main__":
    print("프로그램 시작")

    app = QApplication([]) #process
    myWindow = MyWindow() #클래스를 이용해 객체를 만들고, 생성자(__init__())를 호출
    myWindow.show()
    app.exec_()

