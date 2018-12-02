from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QAxContainer import *
from kiwoomOS.kwos import *
#from KWOS import KiwoomOS

main_window = uic.loadUiType("main_window.ui")[0]

class MyWindow(QMainWindow, main_window):
    conditionResult = {}

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.kwos = KiwoomOS(self.kiwoom)

        self.kwos.addOnLogin(self.kwos_onLogin)
        self.kwos.addOnReceiveCondition(self.kwos_onReceiveCondition)
        self.kwos.addOnReceiveRealCondition(self.kwos_OnReceiveRealCondition)

        self.loginButton.clicked.connect(self.login_button_clicked)

        self.conditionItemTableWidget.setColumnCount(3)
        self.conditionItemTableWidget.setHorizontalHeaderLabels(["종목코드", "종목명", "현재가"])

    def kwos_onLogin(self, stockItemList, conditionList):
        self.conditionList = conditionList
        self.conditionModel = QStandardItemModel()
        self.conditionListView.setModel(self.conditionModel)
        for condition in conditionList:
            self.conditionModel.appendRow(QStandardItem(condition['조건식명']))

        self.conditionListView.selectionModel().selectionChanged.connect(self.selection_changed)

    def kwos_onReceiveCondition(self, condition, item_list):
        conditionName = condition['조건식명']
        if conditionName not in self.conditionResult:
            self.conditionResult[conditionName] = item_list

        self.setConditionResult(item_list)

        code_list = []
        for item in item_list:
            code = item['종목코드']
            code_list.append(code)
        self.kwos.addRealData(code_list)  # 검색 종목 리스트 실시간 등록

    def kwos_OnReceiveRealCondition(self, condition, strCode, type):
        conditionName = condition['조건식명']
        if conditionName in self.conditionResult:
            if type == '편입':
                self.conditionResult[conditionName].append({
                    '종목코드': strCode
                })
            elif type == '이탈':
                pass

    def setConditionResult(self, itemList):
        self.conditionItemTableWidget.setRowCount(len(itemList))

        for i in range(len(itemList)):
            종목코드 = itemList[i]['종목코드']
            종목명 = self.kwos.getStockItemName(종목코드)
            현재가 = itemList[i]['현재가']
            self.conditionItemTableWidget.setItem(i, 0, QTableWidgetItem(종목코드))
            self.conditionItemTableWidget.setItem(i, 1, QTableWidgetItem(종목명))
            self.conditionItemTableWidget.setItem(i, 2, QTableWidgetItem(str(현재가)))

    def selection_changed(self):
        if not self.conditionListView.selectionModel(): #종목 리스트 모델 설정 전일 경우
            return None

        selectedItem = self.conditionListView.selectionModel().selection().indexes()
        if(selectedItem):
            conditionName = selectedItem[0].data()
            if len(conditionName) > 0:
                if conditionName in self.conditionResult:
                    self.setConditionResult(self.conditionResult[conditionName])
                else:
                    condition = next(filter(lambda con: con['조건식명'] == conditionName, self.conditionList))
                    if condition:
                        self.kwos.startConditionMonitoring(conditionName, condition['조건식인덱스'])

    def login_button_clicked(self):
        self.kwos.login()

if __name__ == "__main__":
    app = QApplication([])
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()