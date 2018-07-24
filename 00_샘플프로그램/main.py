from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QAxContainer import *
import datetime
import kiwoomOS as KOS

main_window = uic.loadUiType("main_window.ui")[0]

class MyWindow(QMainWindow, main_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.kos = KOS.KiwoomOS(self.kiwoom)
        self.kos.addOnLogin(self.kos_onLogin)
        self.kos.addOnReceiveTr(self.kos_OnReceiveTr)
        self.kos.addOnReceiveReal(self.kos_OnReceiveReal)
        self.kos.addOnReceiveRealExt(self.kos_OnReceiveRealExt)
        self.kos.addOnAcceptedOrder(self.kos_OnAcceptedOrder)
        self.kos.addOnConcludedOrder(self.kos_OnConcludedOrder)
        self.kos.addOnReceiveBalance(self.kos_OnReceiveBalance)
        self.kos.addOnReceiveCondition(self.kos_OnReceiveCondition)
        self.kos.addOnReceiveRealCondition(self.kos_OnReceiveRealCondition)

        # PyQt GUI Event
        self.loginButton.clicked.connect(self.login_button_clicked)
        self.accountWindowButton.clicked.connect(self.account_window_button_clicked)
        self.requestTrButton.clicked.connect(self.request_tr_button_clicked)
        self.continuousTrButton.clicked.connect(self.continuous_tr_button_clicked)
        self.setRealButton.clicked.connect(self.set_real_button_clicked)
        self.monitoringButton.clicked.connect(self.monitoring_button_clicked)

        self.orderPoisitionComboBox.addItem('매수')
        self.orderPoisitionComboBox.addItem('매도')

        # TR예제 추가
        self.trComboBox.addItem('종목기본정보요청_opt10001')
        self.trComboBox.addItem('주식일봉차트조회요청_opt10081')

        # Log ListView Model
        self.logModel = QStandardItemModel()
        self.logListView.setModel(self.logModel)
        self.logModel.appendRow(QStandardItem('로그창'))

        # 실시간 Log ListView Model
        self.realLogModel = QStandardItemModel()
        self.realDataListView.setModel(self.realLogModel)
        self.realLogModel.appendRow(QStandardItem('실시간 로그창'))

    def login_button_clicked(self):
        self.writeLog('로그인 버튼 클릭')
        self.kos.login()

    def account_window_button_clicked(self):
        self.writeLog('계좌비밀번호 버튼 클릭')
        self.kos.showAccountWindow()

    def request_tr_button_clicked(self):
        self.writeLog('TR요청 버튼 클릭')
        self.requestTR()

    def continuous_tr_button_clicked(self):
        self.writeLog('연속조회 버튼 클릭')
        self.requestTR(2)

    def set_real_button_clicked(self):
        if self.stockItemListView.selectionModel():
            itemName = self.stockItemListView.selectionModel().selection().indexes()[0].data()
            stockItem = next(filter(lambda stockItem: stockItem['종목명'] == itemName, self.stockItemList))
            if stockItem:
                itemCode = stockItem['종목코드']
                self.kos.addRealData(itemCode)

    def stock_item_selection_changed(self):
        itemName = self.stockItemListView.selectionModel().selection().indexes()[0].data()
        self.orderItemEdit.setText(itemName)
        stockItem = next(filter(lambda stockItem: stockItem['종목명'] == itemName, self.stockItemList))
        if stockItem:
            self.orderItemTextLabel.setText(stockItem['종목코드'])

    def requestTR(self, continuous=0):
        rqName = self.trComboBox.currentText()

        if rqName == '종목기본정보요청_opt10001':
            self.kos.setInput('종목코드', '005930')
            rqResult = self.kos.requestTr('종목기본정보요청_opt10001', 'opt10001', continuous)
            self.writeLog(rqName, '요청 시도 결과 =', rqResult)

        elif rqName == '주식일봉차트조회요청_opt10081':
            self.kos.setInput('종목코드', '005930')
            self.kos.setInput('기준일자', datetime.datetime.today().strftime('%Y%m%d'))
            self.kos.setInput('수정주가구분', '1')
            rqResult = self.kos.requestTr('주식일봉차트조회요청_opt10081', 'opt10081', continuous)
            self.writeLog(rqName, '요청 시도 결과 =', rqResult)

    def monitoring_button_clicked(self):
        self.writeLog('조건검색 버튼 클릭')
        index = self.conditionComboBox.currentIndex()

        if index > -1:
            conditionIndex = self.conditionList[index]['조건식인덱스']
            conditionName = self.conditionList[index]['조건식명']
            self.kos.startConditionMonitoring(conditionName, conditionIndex)

    # 로그인 완료 Event
    def kos_onLogin(self, stockItemList, conditionList):
        self.writeLog('kos_onLogin()호출 - 로그인 이벤트')
        self.stockItemList = stockItemList
        self.conditionList = conditionList

        self.writeLog('로그인 상태 :', self.kos.getLoginState())
        self.writeLog('사용자 아이디 :', self.kos.getUserId())
        self.writeLog('사용자 이름 :', self.kos.getUserName())
        self.writeLog('서버구분 :', self.kos.getServerState())

        for condition in conditionList:
            self.conditionComboBox.addItem(condition['조건식명'])

        for account in self.kos.getAccountList():
            self.accountComboBox.addItem(account)

        model = QStandardItemModel()
        self.stockItemListView.setModel(model)
        self.stockItemListView.selectionModel().selectionChanged.connect(self.stock_item_selection_changed)

        for stockItem in stockItemList:
            model.appendRow(QStandardItem(stockItem['종목명']))

    # TR수신 Event
    def kos_OnReceiveTr(self, rqName, trCode, hasNext):
        self.writeLog('kos_OnReceiveTr() 호출 - TR데이터 수신')
        self.writeLog('rqName', rqName)
        self.writeLog('trCode', trCode)
        self.writeLog('hasNext', hasNext)

        if rqName == '종목기본정보요청_opt10001':
            itemCode = self.kos.getTrData(trCode, '종목코드')
            itemName = self.kos.getTrData(trCode, '종목명')
            price = self.kos.getTrData(trCode, '현재가')
            changeRate = self.kos.getTrData(trCode, '등락율')  # 등락률이 맞으나 KOA Studio에 명시된 이름을 정확하게 입력해야 함
            self.writeLog(itemCode, itemName, price, changeRate)

        elif rqName == '주식일봉차트조회요청_opt10081':
            itemCount = self.kos.getTrCount(trCode)
            itemCode = self.kos.getTrData(trCode, '종목코드')
            self.writeLog('itemCount', itemCode)
            self.writeLog(itemCode)
            for i in range(itemCount):
                date = self.kos.getTrData(trCode, '일자', i)
                price = self.kos.getTrData(trCode, '현재가', i)
                volume = self.kos.getTrData(trCode, '거래량', i)
                checkPoint = self.kos.getTrData(trCode, '수정주가구분', i)
                self.writeLog(date, price, volume, checkPoint)

    # 실시간 거래 데이터 수신
    def kos_OnReceiveReal(self, itemCode, realData):
        self.writeRealLog('kos_OnReceiveReal() 호출 - 실시간 데이터 수신')
        self.writeRealLog(itemCode)
        self.writeRealLog(realData)

    # 기타 실시가 데이터 수신
    def kos_OnReceiveRealExt(self, itemCode, realType):
        self.writeRealLog('kos_OnReceiveRealExt() 호출 - 기타 실시간 데이터 수신')
        self.writeRealLog('realType', realType)
        if realType == '주식당일거래원':
            sellEx1 = self.kos.getRealData(itemCode, 141)
            sellEx2 = self.kos.getRealData(itemCode, 142)
            sellEx3 = self.kos.getRealData(itemCode, 143)
            self.writeRealLog(sellEx1, sellEx2, sellEx3)

    # 주문 접수 Event
    def kos_OnAcceptedOrder(self, receipt):
        self.writeRealLog('kos_OnAcceptedOrder() 호출 - 주문접수 결과')
        self.writeRealLog(receipt)

    # 주문 체결 Event
    def kos_OnConcludedOrder(self, conclusion):
        self.writeRealLog('kos_OnConcludedOrder() 호출 - 주문 체결 정보')
        self.writeRealLog(conclusion)

    # 실시간 잔고 Event
    def kos_OnReceiveBalance(self, balance):
        self.writeRealLog('kos_kos_OnReceiveBalance() 호출 - 실시간 잔고 전달')
        self.writeRealLog(balance)

    # 조건검색 종목 Event
    def kos_OnReceiveCondition(self, condition, itemList):
        self.writeLog('kos_OnReceiveCondition() 호출 - 조건검색 결과')
        self.writeLog('condition', condition)
        self.writeLog('itemList', itemList)

    # 실시간 조건검색 Event
    def kos_OnReceiveRealCondition(self, condition, strCode, type):
        self.writeRealLog('kos_OnReceiveRealCondition() 호출 - 실시간 조건 편입/이탈')
        self.writeRealLog('condition', condition)
        self.writeRealLog('type', type)
        self.writeRealLog('strCode', strCode)

    # LogListView에 로그 출력
    def writeLog(self, *log):
        logText = ''
        for i in log:
            logText += str(i) + ' '
        self.logModel.appendRow(QStandardItem(logText))

    # realDataListView에 실시간 로그 출력
    def writeRealLog(self, *log):
        logText = ''
        for i in log:
            logText += str(i) + ' '
        self.realLogModel.appendRow(QStandardItem(logText))


if __name__ == "__main__":
    print("프로그램 시작")
    app = QApplication([])
    myWindow = MyWindow()  # 클래스를 이용해 객체를 만들고, 생성자(__init__())를 호출
    myWindow.show()
    app.exec_()

