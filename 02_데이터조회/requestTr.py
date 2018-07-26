from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QAxContainer import *
from kiwoomOS.kwos import *
from datetime import datetime

main_window = uic.loadUiType("main_window.ui")[0]

class MyWindow(QMainWindow, main_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.kwos = KiwoomOS(self.kiwoom)

        self.kwos.addOnLogin(self.kwos_on_login) #로그인 결과 Event 등록
        self.kwos.addOnReceiveTr(self.kwos_on_receive_tr) #TR데이터 수신 Event 등록

        self.loginButton.clicked.connect(self.login_button_clicked) #로그인 버튼 클릭 Event 등록
        self.requestStockInfoButton.clicked.connect(self.request_stock_info_button_clicked) #종목기본정보 버튼 클릭 Event 등록
        self.requestChartButton.clicked.connect(self.request_chart_button_clicked) #일봉데이터 버튼 클릭 Event 등록
        self.requestContinuousButton.clicked.connect(self.request_continuous_button_clicked) #일봉데이터 연속조회 버튼 클릭 Event 등록
        self.requestBalanceButton.clicked.connect(self.request_balance_button_clicked) #잔고조회 버튼 클릭 Event 등록

        # TR ListView Model
        self.trDataModel = QStandardItemModel()
        self.trDataListView.setModel(self.trDataModel)

    def login_button_clicked(self):
        print('로그인 버튼 클릭')
        self.kwos.login() #로그인 창 호출

    def request_stock_info_button_clicked(self):
        itemCode = self.get_selection_changed()
        if itemCode:
            self.kwos.setInput('종목코드', itemCode)
            self.kwos.requestTr('종목기본정보요청', 'opt10001')
        else:
            QMessageBox.about(self, "종목 선택", "종목을 선택해주세요.")

    def request_chart_button_clicked(self):
        itemCode = self.get_selection_changed()
        if itemCode:
            self.kwos.setInput('종목코드', itemCode)
            self.kwos.setInput('기준일자', datetime.today().strftime('%Y%m%d'))
            self.kwos.setInput('수정주가구분', '1')
            self.kwos.requestTr('주식일봉차트조회요청', 'opt10081')
        else:
            QMessageBox.about(self, "종목 선택", "종목을 선택해주세요.")

    def request_continuous_button_clicked(self):
        itemCode = self.get_selection_changed()
        if itemCode:
            self.kwos.setInput('종목코드', itemCode)
            self.kwos.setInput('기준일자', datetime.today().strftime('%Y%m%d'))
            self.kwos.setInput('수정주가구분', '1')
            self.kwos.requestTr('주식일봉차트조회요청', 'opt10081', 2) #연속조회 시 3번째 파라미터에 2를 입력
        else:
            QMessageBox.about(self, "종목 선택", "종목을 선택해주세요.")

    def request_balance_button_clicked(self):
        account = self.accountComboBox.currentText()
        if len(account) > 0:
            self.kwos.setInput('계좌번호', account)
            self.kwos.setInput('비밀번호', '')
            self.kwos.setInput('상장폐지조회구분', '0')
            self.kwos.setInput('비밀번호입력매체구분', '00')
            self.kwos.requestTr('계좌평가현황요청', 'OPW00004')

    #로그인 결과 Event
    def kwos_on_login(self, stockItemList, conditionList):
        #종목 리스트
        self.stockItemList = stockItemList

        model = QStandardItemModel()
        self.stockItemListView.setModel(model)
        for stockItem in stockItemList:
            model.appendRow(QStandardItem(stockItem['종목명']))

        #계좌번호 리스트
        for account in self.kwos.getAccountList():
            self.accountComboBox.addItem(account)

    #TR데이터 수신 Event
    def kwos_on_receive_tr(self, rqName, trCode, hasNext):
        self.trDataModel.appendRow(QStandardItem('rqName = ' + rqName))
        self.trDataModel.appendRow(QStandardItem('trCode = ' + trCode))
        self.trDataModel.appendRow(QStandardItem('hasNext = ' + str(hasNext)))

        if rqName == '종목기본정보요청':
            itemCode = self.kwos.getTrData(trCode, '종목코드')
            itemName = self.kwos.getTrData(trCode, '종목명')
            price = self.kwos.getTrData(trCode, '현재가')
            changeRate = self.kwos.getTrData(trCode, '등락율')
            volume = self.kwos.getTrData(trCode, '거래량')

            self.trDataModel.appendRow(QStandardItem('종목코드 = ' + itemCode))
            self.trDataModel.appendRow(QStandardItem('종목명 = ' + itemName))
            self.trDataModel.appendRow(QStandardItem('현재가 = ' + price))
            self.trDataModel.appendRow(QStandardItem('등락률 = ' + changeRate))
            self.trDataModel.appendRow(QStandardItem('거래량 = ' + volume))

        elif rqName == '주식일봉차트조회요청':
            count = self.kwos.getTrCount(trCode)
            self.trDataModel.appendRow(QStandardItem('count = ' + str(count)))
            for i in range(count):
                date = self.kwos.getTrData(trCode, '일자', i)
                closePrice = self.kwos.getTrData(trCode, '현재가', i)
                openPrice = self.kwos.getTrData(trCode, '시가', i)
                highPrice = self.kwos.getTrData(trCode, '고가', i)
                lowPrice = self.kwos.getTrData(trCode, '저가', i)
                volume = self.kwos.getTrData(trCode, '거래량', i)

                self.trDataModel.appendRow(QStandardItem('------------------------'))
                self.trDataModel.appendRow(QStandardItem('일자 = ' + date))
                self.trDataModel.appendRow(QStandardItem('현재가 = ' + closePrice))
                self.trDataModel.appendRow(QStandardItem('시가 = ' + openPrice))
                self.trDataModel.appendRow(QStandardItem('고가 = ' + highPrice))
                self.trDataModel.appendRow(QStandardItem('저가 = ' + lowPrice))
                self.trDataModel.appendRow(QStandardItem('거래량 = ' + volume))
                self.trDataModel.appendRow(QStandardItem('------------------------'))

        elif rqName == "계좌평가현황요청":
            count = self.kwos.getTrCount(trCode)
            self.trDataModel.appendRow(QStandardItem('count = ' + str(count)))

            balanceAsset = self.kwos.getTrData(trCode, '예수금')
            totalBuyingAmount = self.kwos.getTrData(trCode, '총매입금액')
            self.trDataModel.appendRow(QStandardItem('예수금 = ' + balanceAsset))
            self.trDataModel.appendRow(QStandardItem('총매입금액 = ' + totalBuyingAmount))

            for i in range(count):
                itemcode = self.kwos.getTrData(trCode, '종목코드', i)
                balanceQnt = self.kwos.getTrData(trCode, '보유수량', i)
                buyingPrice = self.kwos.getTrData(trCode, '평균단가', i)
                estimated = self.kwos.getTrData(trCode, '평가금액', i)
                profit = self.kwos.getTrData(trCode, '손익금액', i)
                profitRate = self.kwos.getTrData(trCode, '손익율', i)

                self.trDataModel.appendRow(QStandardItem('------------------------'))
                self.trDataModel.appendRow(QStandardItem('종목코드 = ' + itemcode))
                self.trDataModel.appendRow(QStandardItem('보유수량 = ' + balanceQnt))
                self.trDataModel.appendRow(QStandardItem('평균단가 = ' + buyingPrice))
                self.trDataModel.appendRow(QStandardItem('평가금액 = ' + estimated))
                self.trDataModel.appendRow(QStandardItem('손익금액 = ' + profit))
                self.trDataModel.appendRow(QStandardItem('손익율 = ' + profitRate))
                self.trDataModel.appendRow(QStandardItem('------------------------'))


    #종목 리스트 뷰에서 선택된 종목의 종목코드를 구하는 함수
    def get_selection_changed(self):
        if not self.stockItemListView.selectionModel(): #종목 리스트 모델 설정 전일 경우
            return None

        selectedItem = self.stockItemListView.selectionModel().selection().indexes()
        if(selectedItem):
            itemName = selectedItem[0].data()
            if len(itemName) > 0:
                stockItem = next(filter(lambda stockItem: stockItem['종목명'] == itemName, self.stockItemList))
                if stockItem:
                    return stockItem['종목코드']
            else:
                return None
        else:
            return None

if __name__ == "__main__":
    app = QApplication([])
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()