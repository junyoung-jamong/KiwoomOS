# kiwoomOS
kiwoomOS는 파이썬에서 키움OpenAPI가 제공하는 기능을 보다 더 쉽게 사용할 수 있도록 도와주는 모듈입니다. kiwoomOS를 사용하기 위해서는 키움OpenAPI를 사용하기 위한 준비가 선행되어야 합니다.  

#### 키움OpenAPI를 사용하기 위한 조건
  1. 키움증권 계좌 보유 및 키움증권 아이디 등록
  2. Open API 사용 신청
  3. 키움OpenAPI+ 모듈 설치
 
키움OpenAPI 신청/다운로드 : https://www3.kiwoom.com/nkw.templateFrameSet.do?m=m1408000000



다운로드
--------
kiwoomOS는 pip를 이용해 설치할 수 있습니다.
```
pip install kiwoomOS
```


사용하기
-------
#### KiwoomOS 객체 생성
```
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from kiwoomOS.kwos import KiwoomOS

app = QApplication([])
kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
kwos = KiwoomOS(kiwoom)
app.exec_()
```

KiwoomOS 클래스 객체를 생성해 키움OpenAPI가 제공하는 모든 기능을 사용할 수 있습니다. 
객체 생성 시에 키움API OCX컨트롤 객체를 인자로 전달해줘야 합니다.

```
kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
kwos = KiwoomOS(kiwoom)
```

#### 로그인
login()함수를 호출하여 키움API 로그인 창을 띄울 수 있습니다.
```
kwos.login()
```

예제
```
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from kiwoomOS.kwos import KiwoomOS

def login_event(stockItemList, conditionItemList):
    print(stockItemList)
    print(conditionItemList)

if __name__ == "__main__":
    app = QApplication([])
    kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
    kwos = KiwoomOS(kiwoom)

    kwos.addOnLogin(login_event)
    kwos.login()
    app.exec_()
```
