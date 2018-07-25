# 로그인
키움OpenAPI에서 제공해주는 기능을 사용하기 위해선 반드시 키움 서버에 연결이 되어있어야 합니다. 

로그인창을 이용하여 키움서버에 접속할 수 있습니다.

로그인 프로세스 이해하기
----------------------
아래는 키움OpenAPI에서 로그인이 진행되는 절차입니다.  

#### 1.로그인 창 호출
![로그인 프로세스1](https://postfiles.pstatic.net/MjAxODA3MjVfODYg/MDAxNTMyNDk4ODY2OTk1.cRjLYGqlPDpbbQjmJXpkncs8eMWuO2lwitmSskTu9yEg.qK35IDoEAWiRvINEKw4pD6J1M1U8VPe54qKIW7llr7Eg.PNG.rkdwnsdud555/1.png?type=w773)
>사용자 작성 코드에서 api함수(CommConnect())를 호출하여 로그인 창을 띄울 수 있습니다. 
>kiwoomOS를 이용할 경우 login()함수를 호출하면 됩니다.

#### 2.로그인 시도
![로그인 프로세스2](https://postfiles.pstatic.net/MjAxODA3MjVfMjA0/MDAxNTMyNDk4ODY3MDc0.l_JvWKt8fkJi7IUTg8nhat53uSdTYutwI0pYdrH1aSkg.Ds1z5hQ1RwqATH5m0e4aIEEQecS9X52mUnr_fdMBiesg.PNG.rkdwnsdud555/2.png?type=w773)
>앞에서 실행한 로그인 창에서 로그인 버튼을 통해 키움서버에 접속을 시도합니다.

#### 3.로그인 결과 전달
![로그인 프로세스3](https://postfiles.pstatic.net/MjAxODA3MjVfMTgg/MDAxNTMyNDk4ODY3MDY4.4Y9SnXyOF34t6zBkSzX_7x7lhEZ4x2FSkTbI5SlV5OMg.DBYEfXxtxJ0ehZ1OTMTmZzztwvr1LgK2SdRXIpXoIP8g.PNG.rkdwnsdud555/3.png?type=w773)
>키움서버가 ocx로 로그인 시도에 대한 결과를 전달합니다. ocx와 키움서버 사이에서 진행되는 절차로 별도의 코드를 작성할 필요는 없습니다.

#### 4.로그인 결과 Event
![로그인 프로세스4](https://postfiles.pstatic.net/MjAxODA3MjVfMTI2/MDAxNTMyNDk4ODY3MDYx.Pv460zyo-e9SmS7u2eFosxbugvCdATuyC6X3qPY2_k0g.2Z2zt95QEVVWH3Qrd0GH9dyBcJ5xKLHuV8qBiqg8rycg.PNG.rkdwnsdud555/4.png?type=w773)
>ocx는 키움서버로부터 받은 로그인 시도 결과를 사용자 작성코드로 전달하기 위해 Event함수를 호출합니다.

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
