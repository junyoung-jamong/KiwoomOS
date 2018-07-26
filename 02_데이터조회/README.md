# TR데이터 조회
TR(Transaction)데이터 조회를 통해 주식가격 및 정보, 거래량 순위, 증권사별매매상위, 계좌평가현황 등 주식과 관련된 정보를 키움 서버에 요청할 수 있습니다.
 키움API에서는 220가지 이상의 TR데이터를 제공하고 있습니다. 각 TR데이터마다 고유한 optCode를 가지며, 각기 다른 INPUT값을 요구합니다. 

![TR데이터 리스트](https://postfiles.pstatic.net/MjAxODA3MjZfMjA3/MDAxNTMyNjAzNTAwMTI5.zv0JvsrSjp9jKCafaGwHBG5ihkHsuWbNJ-Oeb5sB_R4g.Ew6sKckUQtzAmUt2KC_dO-K1ZG2WRB-TI65UKB4CEeYg.PNG.rkdwnsdud555/img2.png?type=w773)

TR데이터 조회 프로세스 이해하기
-----------------------------



TR데이터 조회 요청
-----------------
TR데이터를 조회하기 위해서는 해당 TR에서 요구하는 INPUT값을 등록해줘야합니다. **setInput()** 함수를 사용해 입력값을 등록할 수 있습니다.
 TR조회에 필요합 입력값을 모두 등록했다면 **requestTr()** 함수를 사용해 tr데이터 조회 요청을 할 수 있습니다.

TR code가 opt10003인 **체결정보요청** TR을 요청한다고 가정해보겠습니다. 

![TR데이터 예제](https://postfiles.pstatic.net/MjAxODA3MjZfNTMg/MDAxNTMyNjAzNTAwMTI1.kMltOvd0zsvpNaI7bj0YUyoW6NiEre5kh3dUSOdlsd0g.LlwTFLSW3w_M6QbkJBbq80f_nNfU8ZGDiU3Y1oWL7nAg.PNG.rkdwnsdud555/img3.png?type=w773)

opt10003 TR데이터는 [INPUT]값으로 종목코드를 입력해야합니다. 따라서 아래와 같이 setInput(key, value)함수를 사용합니다. 이 TR데이터는 '종목코드' 하나의 입력값만을 요구하기 때문에 setInput()을 한 번만 사용하면 됩니다.
```
kwos.setInput('종목코드', '005930')
```
> * 매개변수1 : 입력항목 이름
> * 매개변수2 : 입력항목 값


이제, 필요한 입력값을 모두 설정했으니 requestTr(rqName, optCode)함수를 사용해 TR조회 요청을 합니다.
```
kwos.requestTr('체결정보', 'opt10003')
```
> * 매개변수1 : 사용자 구분자(데이터 수신 시에 요청 구분 목적으로 사용됨)
> * 매개변수2 : optCode

전체코드:
```
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from kiwoomOS.kwos import KiwoomOS

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.kwos = KiwoomOS(kiwoom)
        self.kwos.addOnLogin(self.kwos_on_login)
        self.kwos.login()

    def kwos_on_login(self, stockItemList, conditionList):
        print('키움서버에 접속되었습니다.')
        self.kwos.setInput('종목코드', '005930') #input값 설정
        self.kwos.requestTr('체결정보', 'opt10003') #TR데이터 조회요청

if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()
```

TR데이터 수신 Event
------------------

전체코드:
```
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from kiwoomOS.kwos import KiwoomOS

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.kwos = KiwoomOS(kiwoom)
        self.kwos.addOnLogin(self.kwos_on_login)
        self.kwos.addOnReceiveTr(self.kwos_on_receive_tr)
        self.kwos.login()

    def kwos_on_receive_tr(self, rqName, trCode, hasNext):
        print('rqName =', rqName)
        count = self.kwos.getTrCount(trCode)

        for index in range(count):
            시간 = self.kwos.getTrData(trCode, '시간')
            현재가 = self.kwos.getTrData(trCode, '현재가')
            전일대비 = self.kwos.getTrData(trCode, '전일대비')
            대비율 = self.kwos.getTrData(trCode, '대비율')
            체결거래량 = self.kwos.getTrData(trCode, '체결거래량')
            누적거래량 = self.kwos.getTrData(trCode, '누적거래량')
            누적거래대금 = self.kwos.getTrData(trCode, '누적거래대금')
            체결강도 = self.kwos.getTrData(trCode, '체결강도')
            print(시간, 현재가, 전일대비, 대비율, 체결거래량, 누적거래량, 누적거래대금, 체결강도)


    def kwos_on_login(self, stockItemList, conditionList):
        print('키움서버에 접속되었습니다.')
        self.kwos.setInput('종목코드', '005930')
        self.kwos.requestTr('체결정보', 'opt10003')

if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()
```

- - -
출력:
```
키움서버에 접속되었습니다.
rqName = 체결정보
155938 +46900 +750 +1.63 +436 7339112 342397065500 132.40
155938 +46900 +750 +1.63 +436 7339112 342397065500 132.40
155938 +46900 +750 +1.63 +436 7339112 342397065500 132.40
155938 +46900 +750 +1.63 +436 7339112 342397065500 132.40
155938 +46900 +750 +1.63 +436 7339112 342397065500 132.40
155938 +46900 +750 +1.63 +436 7339112 342397065500 132.40
155938 +46900 +750 +1.63 +436 7339112 342397065500 132.40
...
```

관련 함수
--------

샘플 프로그램(requestTr.py)
--------------------------
![샘플 프로그램](https://postfiles.pstatic.net/MjAxODA3MjZfMTAx/MDAxNTMyNjAyMzEwMDAw.EnHewXclSk3AfdeEn6FkFE1oF88pKHllSobz4Kbpqx8g.vF1wHnsLSpiPfACu5yqeAmgVXHoQoC_o6lBTKz2Be98g.PNG.rkdwnsdud555/img.png?type=w773)
