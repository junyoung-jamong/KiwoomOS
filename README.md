# kiwoomOS
kiwoomOS는 파이썬에서 키움OpenAPI가 제공하는 기능을 보다 더 쉽게 사용할 수 있도록 돕는 모듈입니다. 

kiwoomOS를 사용하기 위해서는 키움OpenAPI를 사용하기 위한 준비가 선행되어야 합니다.  

#### 키움OpenAPI를 사용하기 위한 조건
  1. 키움증권 계좌 보유 및 키움증권 아이디 등록
  2. Open API 사용 신청
  3. 키움OpenAPI+ 모듈 설치
 
[키움OpenAPI 신청/다운로드](https://www3.kiwoom.com/nkw.templateFrameSet.do?m=m1408000000)



다운로드
--------
kiwoomOS를 설치하는 가장 간단한 방법은 Python 패키지를 관리하는 PyPI를 사용하는 것입니다.
다음과 같이 pip 명령어를 이용해 설치할 수 있습니다.
```
pip install kiwoomOS
```


사용하기
-------
### KiwoomOS 객체 생성
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

### 로그인 
login()함수를 호출하여 키움API 로그인 창을 띄울 수 있습니다.
```
kwos.login()
```
![키움API 로그인창](https://postfiles.pstatic.net/20160917_142/rkdwnsdud555_1474046676886JObIO_PNG/12.png?type=w2)

예제:
```
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from kiwoomOS.kwos import KiwoomOS

def login_event(stockItemList, conditionItemList):
    print('키움서버와 연결되었습니다.')

if __name__ == "__main__":
    app = QApplication([])
    kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
    kwos = KiwoomOS(kiwoom)

    kwos.addOnLogin(login_event)
    kwos.login()
    app.exec_()
```

### 코드 간결화
> 기존 데이터 조회 코드
```
kiwoom.dynamicCall("SetInputValue(QString, QString)", '종목코드', '005930')
kiwoom.dynamicCall("CommRqData(QString,QString,int,QString)", 
                                              '종목기본정보요청', 
                                              'opt10001', 
                                              0, 
                                              _getScreenNumber())
```

> **간결화된 코드**
```
kwos.setInput('종목코드', '005930')
kwos.requestTr('종목기본정보요청', 'opt10001')
```

- - - 

> 기존 사용자조건식리스트 호출과정
```
def _api_onEventConnect(nErrCode):
    kiwoom.dynamicCall("GetConditionLoad()") #사용자 조건식 리스트 요청
    
def _api_onReceiveConditionVer(lRet, msg):
    conditions = kiwoom.dynamicCall("GetConditionNameList()")
    conditions = conditions[:-1]
    conditionArray = conditions.split(';')
  
    conditionList = []
    for condition in conditionArray:
        conditionInfo = condition.split('^')
        conditionList.append({
            '조건식인덱스': int(conditionInfo[0]),
            '조건식명': conditionInfo[1]
        })
    
    print(conditionList)

kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
kiwoom.OnEventConnect.connect(_api_onEventConnect)
kiwoom.OnReceiveConditionVer.connect(_api_onReceiveConditionVer)
kiwoom.dynamicCall("CommConnect()")
```

> **간결화된 코드**
```
def kos_onLogin(stockItemList, conditionList):
    print(conditionList)

kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
kwos = KWOS.KiwoomOS(kiwoom)
kwos.addOnLogin(kos_onLogin)
kwos.login()
```

튜토리얼
--------
  1. [로그인](https://github.com/junyoung-jamong/KiwoomOS/tree/master/01_%EB%A1%9C%EA%B7%B8%EC%9D%B8)
  2. [TR 데이터 요청](https://github.com/junyoung-jamong/KiwoomOS/tree/master/02_%EB%8D%B0%EC%9D%B4%ED%84%B0%EC%A1%B0%ED%9A%8C)
  3. 실시간 데이터 처리
  4. 주문 및 체결/잔고
  5. 사용자 조건
