from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QAxContainer import *
from kiwoomOS.kwos import *

main_window = uic.loadUiType("main_window.ui")[0]

class MyWindow(QMainWindow, main_window):  # QMainWindow와 form_class를 상속받는 MyWindow 클래스 정의
    def __init__(self):  # 생성자 함수 정의
        super().__init__()  # 부모 클래스(QMainWindow, form_class) 생성자 호출
        self.setupUi(self)  # 자동으로 UI 코드를 생성 - (Ui_MainWindow)form_class의 메소드
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")  # 키움API 컨트롤 객체 생성
        self.kwos = KiwoomOS(self.kiwoom)  # kiwoomOS 객체 생성
        self.kwos.addOnLogin(self.kwos_on_login) # 로그인 결과 Event 등록
        self.kwos.addOnReceiveReal(self.kwos_on_receive_real)  # 실시간 데이터 수신 Event 등록

        self.loginButton.clicked.connect(self.login_button_clicked) # 로그인 버튼 클릭 Event 등록
        self.addRealButton.clicked.connect(self.addReal_button_clicked)  # 실시간등록 버튼 클릭 Event 등록

    def login_button_clicked(self):  # 로그인 버튼 클릭 Event 정의
        print('로그인 버튼 클릭')
        self.kwos.login()  # 로그인 창 호출

    def addReal_button_clicked(self):  # 실시간데이터 등록 버튼 클릭 Event 정의
        item_code = self.get_selected_item_code()
        if item_code:
            self.kwos.addRealData(item_code)  # 실시간 등록
            self.realDataListWidget.addItem(item_code + ' 실시간 등록 완료')  #realDataListWidget에 출력

    #로그인 결과 Event
    def kwos_on_login(self, stockItemList, conditionList):
        #종목 리스트
        self.stockItemList = stockItemList

        for stockItem in stockItemList:
            self.stockItemListWidget.addItem(stockItem['종목명'])

    #실시간 데이터 수신Event
    def kwos_on_receive_real(self, code, data):
        self.realDataListWidget.addItem(code + ' - ' + str(data))

    def get_selected_item_code(self):
        if self.stockItemListWidget.currentItem():
            itemName = self.stockItemListWidget.currentItem().text()
            if len(itemName) > 0:
                stockItem = next(filter(lambda stockItem: stockItem['종목명'] == itemName, self.stockItemList))
                if stockItem:
                    return stockItem['종목코드']
                else:
                    return None
            else:
                return None
        else:
            return None

if __name__ == "__main__":
    app = QApplication([])  # QApplication 객체 생성
    myWindow = MyWindow()  # MyWindow 객체 생성 후 myWindow 변수에 (주소)저장
    myWindow.show()  # myWindow 가시화
    app.exec_()  # QApplication 메인 이벤트 루프를 진입하고 exit()가 호출 될 때까지 대기