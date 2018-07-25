# 로그인
키움OpenAPI에서 제공해주는 기능을 사용하기 위해선 반드시 키움 서버에 연결이 되어있어야 합니다. 

로그인창을 이용하여 키움서버에 접속할 수 있습니다.

로그인 창 호출하기
----------------
login()함수를 이용하여 키움OpenAPI의 로그인창을 호출할 수 있습니다.
```
kwos.login()
```

로그인창 호출 결과:

![로그인창](https://postfiles.pstatic.net/20160917_142/rkdwnsdud555_1474046676886JObIO_PNG/12.png?type=w2)

전체 코드:
```
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from kiwoomOS.kwos import KiwoomOS

app = QApplication([])
kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
kwos = KiwoomOS(kiwoom)
kwos.login()
app.exec_()
```

로그인 결과 Event
----------------
로그인 창을 이용해서 키움서버 접속에 성공하였을 때 OnLogin() 이벤트가 호출됩니다.

이벤트 함수는 addOnLogin() 함수를 통해 등록할 수 있습니다.
```
def kwos_on_login(stockItemList, conditionList):
  print('키움서버에 접속되었습니다.')

kwos.addOnLogin(kwos_on_login)
```

로그인 이벤트는 호출 시 2개의 값이 전달됩니다.
> * 상장된 종목정보리스트(stockItemList)
>   * [{'종목코드': '000020', '종목명': '동화약품', '전일가': 10700, '상장주식수': 27931470, '상장일': '19760324', '감리구분': '정상', '종목상태': '증거금40%|담보대출|신용가능'}, {'종목코드': '000030', '종목명': '우리은행', '전일가': 16500, '상장주식수': 676000000, '상장일': '20141119', '감리구분': '정상', '종목상태': '증거금20%|담보대출|신용가능'}, ...]
>
> * 사용자 조건검색식 리스트(conditionList)
>   * [{'조건식인덱스': 0, '조건식명': '조건식명1'}, {'조건식인덱스': 1, '조건식명': '조건식명2'}, ...]

전체 코드:
```
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from kiwoomOS.kwos import KiwoomOS

def kwos_on_login(stockItemList, conditionList):
  print('키움서버에 접속되었습니다.')
  
app = QApplication([])
kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
kwos = KiwoomOS(kiwoom)
kwos.addOnLogin(kwos_on_login)
kwos.login()
app.exec_()
```

종목정보 리스트와 사용자 조건검색식 리스트는 로그인한 후 다음 함수를 통해서도 접근할 수 있습니다.
#### 종목정보 리스트 요청
```
kwos.getStockItemList()
```
#### 사용자 조건검색식 리스트 요청
```
kwos.getConditionList()
```

로그인 접속/사용자 관련 함수
--------------------------
#### 접속 상태
```
kwos.getLoginState()
```
> True : 연결 | False : 연결안됨

#### 계좌비밀번호 창 호출
```
kwos.showAccountWindow()
```
![계좌비밀번호 창](https://postfiles.pstatic.net/MjAxODA3MjVfMTcg/MDAxNTMyNDk1NjU0NDY0.Ti1Eza9o7J6Q9f54WpqEyToomunKEkorTIOKMsXMCcEg.zgyIPGfYZSPSIK_Y_cwgto-FnRZpVtbTYdAJIMheEDcg.PNG.rkdwnsdud555/ing.png?type=w773)

#### 서버 구분
```
kwos.getServerState()
```
> '모의서버' | '실서버'

#### 계좌번호 리스트
```
kwos.getAccountList()
```
> ['801650212', '804031234', ...]

#### 사용자 아이디
```
kwos.getUserId()
```
> 'jamong'

#### 사용자 이름
```
kwos.getUserName()
```
> '자몽'

샘플 프로그램 (login.py)
-----------------------
![샘플 프로그램](https://postfiles.pstatic.net/MjAxODA3MjVfMjI2/MDAxNTMyNDkxMDI4NDAw.WD7CyrljMh-EbpqQfAKpKCil4rSYwnO3SDBDJbYYA-gg.1i6BfadpSnS38UcVWMV6kEcbK1vtSSr510Wx75VaqLcg.PNG.rkdwnsdud555/img2.png?type=w773)
