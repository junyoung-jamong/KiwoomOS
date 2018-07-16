class KiwoomOS:
    stockItemList = []
    conditionList = []

    _conditionMonitoringState = {}
    _realDataDict = {}
    _realScrNumDict = {}
    _screenNumber = 1000
    _realScreenNumber = 9001

    def __init__(self, kiwoom):
        self.kiwoom = kiwoom
        self.kiwoom.OnEventConnect.connect(self._api_onEventConnect)
        self.kiwoom.OnReceiveConditionVer.connect(self._api_onReceiveConditionVer)

    def _api_onEventConnect(self, nErrCode):
        print('api_onEventConnect()')
        if nErrCode == 0:
            codes = self.kiwoom.dynamicCall("GetCodeListByMarket(QString)", "0")
            codes += self.kiwoom.dynamicCall("GetCodeListByMarket(QString)", "10")
            codes = codes[:-1]

            codeList = codes.split(";")

            for code in codeList:
                self.stockItemList.append({
                    '종목코드': code,
                    '종목명': self.kiwoom.dynamicCall("GetMasterCodeName(QString)", code),
                    '전일가': int(self.kiwoom.dynamicCall("GetMasterLastPrice(QString)", code)),
                    '상장주식수': int(self.kiwoom.dynamicCall("GetMasterListedStockCnt(QString)", code)),
                    '상장일': self.kiwoom.dynamicCall("GetMasterListedStockDate(QString)", code),
                    '감리구분': self.kiwoom.dynamicCall("GetMasterConstruction(QString", code),
                    '종목상태': self.kiwoom.dynamicCall("GetMasterStockState(QString", code)
                })

            self.kiwoom.dynamicCall("GetConditionLoad()")

    def _api_onReceiveConditionVer(self, lRet, msg):
        conditions = self.kiwoom.dynamicCall("GetConditionNameList()")
        conditions = conditions[:-1]
        conditionArray = conditions.split(';')

        for condition in conditionArray:
            conditionInfo = condition.split('^')
            self.conditionList.append({
                '조건식인덱스': int(conditionInfo[0]),
                '조건식명': conditionInfo[1]
            })

        print(self.conditionList)

    #SetInputValue 호출
    def setInput(self, key, value):
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", key, value)

    #CommRqData 호출
    def requestTr(self, rqName, trCode, prevNext=0):
        result = self.kiwoom.dynamicCall("CommRqData(QString,QString,int,QString)",
                                         rqName,
                                         trCode,
                                         prevNext,
                                         self._getScreenNumber())
        if result == 0:
            return True
        else:
            return False

    #GetCommData 호출
    def getTrData(self, trCode, key, index=0):
        return self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString)", trCode, "", index, key).strip()

    #GetRepeatCnt 호출
    def getTrCount(self, trCode):
        return self.kiwoom.dynamicCall("GetRepeatCnt(QString, QString)", trCode, "")

    #실시간 데이터 등록 관리
    def addRealData(self, codeList):
        if self.getLoginState():
            if isinstance(codeList, str):
                codeList = [codeList]

            requestList = ''
            fidList = '9001;302;10;11;25;12;13'
            for code in codeList:
                if code not in self._realDataDict:
                    scrNum = self._getRealScreenNumber()
                    requestList += code + ';'
                    self._realDataDict[code] = scrNum
                    self._realScrNumDict[scrNum].append(code)

                    if len(self._realScrNumDict[scrNum]) == 100:
                        requestList = requestList[:-1]
                        self.kiwoom.dynamicCall("SetRealReg(QString, QString, QString, QString)", scrNum, requestList, fidList, '1')
                        requestList = ''

            if len(requestList) > 0:
                requestList = requestList[:-1]
                self.kiwoom.dynamicCall("SetRealReg(QString, QString, QString, QString)", scrNum, requestList, fidList, '1')



    #SendCondition 호출
    def startConditionMonitoring(self, name, index):
        if name in self._conditionMonitoringState:
            self._conditionMonitoringState[name]['state'] = True
        else:
            scrNum = self._getScreenNumber()
            result = self.kiwoom.dynamicCall("SendCondition(QString, QString, int, int)", scrNum, name, index, 1)
            if result == 1:
                monitoring = {'state': True, 'scrNum': scrNum}
                self._conditionMonitoringState[name] = monitoring

    def stopConditionMonitoring(self, name, index):
        if name in self._conditionMonitoringState:
            self._conditionMonitoringState[name]['state'] = False

    #SendConditionStop 호출
    def removeConditionMonitoring(self, name, index):
        if name in self._conditionMonitoringState:
            self.kiwoom.dynamicCall("SendConditionStop(QString, QString, int)",
                                    self._conditionMonitoringState[name]['scrNum'],
                                    name,
                                    index)
            del self._conditionMonitoringState[name]

    #종목리스트 요청
    def getStockItemList(self):
        if self.getLoginState():
            return self.stockItemList

    #조건식리스트 요청
    def getConditionList(self):
        if self.getLoginState():
            return self.conditionList

    #로그인창 호출
    def login(self):
        if self.kiwoom is not None:
            self.kiwoom.dynamicCall("CommConnect()")

    #로그인 연결상태 여부
    def getLoginState(self):
        if self.kiwoom is not None:
            state = self.kiwoom.dynamicCall("GetConnectState()")
            if state == 1:
                return True
            else:
                return False
        else:
            return False

    #계좌번호 리스트
    def getAccountList(self):
        if self.getLoginState():
            accounts = self.kiwoom.dynamicCall("GetLoginInfo(QString)", "ACCLIST")
            accounts = accounts[:-1]
            accountList = accounts.split(";")
            return accountList

    #사용자 아이디
    def getUserId(self):
        if self.getLoginState():
            userId = self.kiwoom.dynamicCall("GetLoginInfo(QString)", "USER_ID" )
            return userId

    #사용자 이름
    def getUserName(self):
        if self.getLoginState():
            userName = self.kiwoom.dynamicCall("GetLoginInfo(QString)", "USER_NAME")
            return userName

    #서버 구분(모의투자 or 실서버)
    def getServerState(self):
        if self.getLoginState():
            server = self.kiwoom.dynamicCall("GetLoginInfo(QString)", "GetServerGubun")
            if server == 1:
                return '모의투자'
            else:
                return '실서버'

    #화면번호 생성
    def _getScreenNumber(self):
        if self._screenNumber > 5000:
            self._screenNumber = 1000

        self._screenNumber += 1
        return str(self._screenNumber)

    #실시간등록 화면번호
    def _getRealScreenNumber(self):
        if self._realScreenNumber > 9200:
            self._realScreenNumber = 9000

        scrNum = str(self._realScreenNumber)

        if scrNum in self._realScrNumDict:
            if len(self._realScrNumDict[scrNum]) >= 100:
                self._realScreenNumber += 1
                scrNum = str(self._realScrNumDict)
        else:
            self._realScrNumDict[scrNum] = []

        return scrNum