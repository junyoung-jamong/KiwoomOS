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
        self.kiwoom.OnEventConnect.connect(self._api_onEventConnect) #로그인 결과 Event
        self.kiwoom.OnReceiveConditionVer.connect(self._api_onReceiveConditionVer) #조건식 리스트 수신 Event
        self.kiwoom.OnReceiveTrData.connect(self._api_onReceiveTrData) #TR요청 수신결과 Event
        self.kiwoom.OnReceiveRealData.connect(self._api_onReceiveRealData) #실시간 데이터 수신 Event
        self.kiwoom.OnReceiveChejanData.connect(self._api_onReceiveChejanData) #체결 잔고 수신 Event
        self.kiwoom.OnReceiveTrCondition.connect(self._api_onReceiveTrCondition) #조건검색 결과 Event
        self.kiwoom.OnReceiveRealCondition.connect(self._api_onReceiveRealCondition) #실시간 조건 수신 Event

        self.kiwoom.dynamicCall("KOA_Functions(QString, QString)", "SetConditionSearchFlag", "AddPrice")

        self._onLogin_observer = [] #로그인 event
        self._onReceiveTr_observer = [] #TR수신 event
        self._onReceiveReal_observer = [] #실시간 체결 수신 event
        self._onReceiveRealExt_observer = [] #실시간 데이터 수신 event
        self._onAcceptedOrder_observer = [] #주문 접수 event
        self._onConcludedOrder_observer = [] #주문 체결 수신 event
        self._onReceiveBalance_observer = [] #잔고 수신 event
        self._onReceiveCondition_observer = [] #조건검색 수식 event
        self._onReceiveRealCondition_observer = [] #실시간 조건검색 수신 event

    def _api_onEventConnect(self, nErrCode):
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

            self.kiwoom.dynamicCall("GetConditionLoad()") #사용자 조건식 리스트 요청

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

        for event_func in self._onLogin_observer:
            event_func(self.stockItemList, self.conditionList)

    # TR데이터 수신
    def _api_onReceiveTrData(self, sScrNo, sRQName, sTrcode, sRecordName, sPrevNext, nDataLength, sErrorCode,
                            sMessage, sSplmMsg):
        for event_func in self._onReceiveTr_observer:
            event_func(sRQName, sTrcode, sPrevNext)

    # 실시간 데이터 수신
    def _api_onReceiveRealData(self, sCode, sRealType, sRealData):
        if sRealType == '주식체결':
            realData = {
                '체결시간': self.kiwoom.dynamicCall("GetCommRealData(QString, int)", sCode, 20),
                '현재가': self.kiwoom.dynamicCall("GetCommRealData(QString, int)", sCode, 10),
                '전일대비': self.kiwoom.dynamicCall("GetCommRealData(QString, int)", sCode, 11),
                '등락률': self.kiwoom.dynamicCall("GetCommRealData(QString, int)", sCode, 12),
                '최우선매도호가': self.kiwoom.dynamicCall("GetCommRealData(QString, int)", sCode, 27),
                '최우선매수호가': self.kiwoom.dynamicCall("GetCommRealData(QString, int)", sCode, 28),
                '거래량': self.kiwoom.dynamicCall("GetCommRealData(QString, int)", sCode, 15),
                '누적거래량': self.kiwoom.dynamicCall("GetCommRealData(QString, int)", sCode, 13),
                '누적거래대금': self.kiwoom.dynamicCall("GetCommRealData(QString, int)", sCode, 14),
                '시가': self.kiwoom.dynamicCall("GetCommRealData(QString, int)", sCode, 16),
                '고가': self.kiwoom.dynamicCall("GetCommRealData(QString, int)", sCode, 17),
                '저가': self.kiwoom.dynamicCall("GetCommRealData(QString, int)", sCode, 18),
                '전일대비기호': self.kiwoom.dynamicCall("GetCommRealData(QString, int)", sCode, 25),
                '전일거래량대비': self.kiwoom.dynamicCall("GetCommRealData(QString, int)", sCode, 26),
                '거래대금증감': self.kiwoom.dynamicCall("GetCommRealData(QString, int)", sCode, 29),
                '전일거래량대비': self.kiwoom.dynamicCall("GetCommRealData(QString, int)", sCode, 30),
                '거래회전율': self.kiwoom.dynamicCall("GetCommRealData(QString, int)", sCode, 31),
                '거래비용': self.kiwoom.dynamicCall("GetCommRealData(QString, int)", sCode, 32),
                '체결강도': self.kiwoom.dynamicCall("GetCommRealData(QString, int)", sCode, 228),
                '시가총액': self.kiwoom.dynamicCall("GetCommRealData(QString, int)", sCode, 311),
                '장구분': self.kiwoom.dynamicCall("GetCommRealData(QString, int)", sCode, 290),
                'KO접근도': self.kiwoom.dynamicCall("GetCommRealData(QString, int)", sCode, 691),
                '상한가발생시간': self.kiwoom.dynamicCall("GetCommRealData(QString, int)", sCode, 567),
                '하한가발생시간': self.kiwoom.dynamicCall("GetCommRealData(QString, int)", sCode, 568)
            }

            for event_func in self._onReceiveReal_observer:
                event_func(sCode, realData)

        else:
            for event_func in self._onReceiveRealExt_observer:
                event_func(sCode, sRealType)

    # 주문 접수/체결 잔고 수신
    def _api_onReceiveChejanData(self, sGubun, nItemCnt, sFIdList):
        if sGubun == '0':
            orderState = self.kiwoom.dynamicCall("GetChejanData(int)", 913).strip()

            data = {
                '시간': self.kiwoom.dynamicCall("GetChejanData(int)", 908).strip(),
                '계좌번호': self.kiwoom.dynamicCall("GetChejanData(int)", 9201).strip(),
                '주문번호': self.kiwoom.dynamicCall("GetChejanData(int)", 9203).strip(),
                '원주문번호': self.kiwoom.dynamicCall("GetChejanData(int)", 904).strip(),
                '종목코드': self.kiwoom.dynamicCall("GetChejanData(int)", 9001).strip(),
                '종목명': self.kiwoom.dynamicCall("GetChejanData(int)", 302).strip(),
                '주문수량': self.kiwoom.dynamicCall("GetChejanData(int)", 900).strip(),
                '주문가격': self.kiwoom.dynamicCall("GetChejanData(int)", 901).strip(),
                '주문구분': self.kiwoom.dynamicCall("GetChejanData(int)", 905).strip(),
                '매매구분': self.kiwoom.dynamicCall("GetChejanData(int)", 906).strip(),
                '매도매수구분': self.kiwoom.dynamicCall("GetChejanData(int)", 907).strip(),
                '주문업무분류': self.kiwoom.dynamicCall("GetChejanData(int)", 912).strip(),
                '거부사유': self.kiwoom.dynamicCall("GetChejanData(int)", 919).strip()
            }

            if orderState == '접수':
                for event_func in self._onAcceptedOrder_observer:
                    event_func(data)

            elif orderState == '체결':
                data['체결번호'] = self.kiwoom.dynamicCall("GetChejanData(int)", 909).strip()
                data['체결가'] = self.kiwoom.dynamicCall("GetChejanData(int)", 910).strip()
                data['단위체결가'] = self.kiwoom.dynamicCall("GetChejanData(int)", 914).strip()
                data['체결누계금액'] = self.kiwoom.dynamicCall("GetChejanData(int)", 903).strip()
                data['체결량'] = self.kiwoom.dynamicCall("GetChejanData(int)", 911).strip()
                data['단위체결량'] = self.kiwoom.dynamicCall("GetChejanData(int)", 915).strip()
                data['당일매매수수료'] = self.kiwoom.dynamicCall("GetChejanData(int)", 938).strip()
                data['당일매매세금'] = self.kiwoom.dynamicCall("GetChejanData(int)", 939).strip()
                data['현재가'] = self.kiwoom.dynamicCall("GetChejanData(int)", 10).strip()
                data['최우선매도호가'] = self.kiwoom.dynamicCall("GetChejanData(int)", 27).strip()
                data['최우선매수호가'] = self.kiwoom.dynamicCall("GetChejanData(int)", 28).strip()

                for event_func in self._onConcludedOrder_observer:
                    event_func(data)
        elif sGubun == '1':
            data = {
                '계좌번호': self.kiwoom.dynamicCall("GetChejanData(int)", 9201).strip(),
                '종목코드': self.kiwoom.dynamicCall("GetChejanData(int)", 9001).strip(),
                '종목명': self.kiwoom.dynamicCall("GetChejanData(int)", 302).strip(),
                '보유수량': self.kiwoom.dynamicCall("GetChejanData(int)", 930).strip(),
                '매입단가': self.kiwoom.dynamicCall("GetChejanData(int)", 931).strip(),
                '총매입가': self.kiwoom.dynamicCall("GetChejanData(int)", 932).strip(),
                '주문가능수량': self.kiwoom.dynamicCall("GetChejanData(int)", 933).strip(),
                '당일순매수량': self.kiwoom.dynamicCall("GetChejanData(int)", 945).strip(),
                '매수매도구분': self.kiwoom.dynamicCall("GetChejanData(int)", 946).strip(),
                '당일총매도손익': self.kiwoom.dynamicCall("GetChejanData(int)", 950).strip(),
                '예수금': self.kiwoom.dynamicCall("GetChejanData(int)", 951).strip(),
                '기준가': self.kiwoom.dynamicCall("GetChejanData(int)", 307).strip(),
                '손익률': self.kiwoom.dynamicCall("GetChejanData(int)", 8019).strip(),
                '당일유가실현손익': self.kiwoom.dynamicCall("GetChejanData(int)", 990).strip(),
                '당일유가실현손익률': self.kiwoom.dynamicCall("GetChejanData(int)", 991).strip(),
                '당일신용실현손익': self.kiwoom.dynamicCall("GetChejanData(int)", 992).strip(),
                '당일신용실현손익률': self.kiwoom.dynamicCall("GetChejanData(int)", 993).strip(),
                '현재가': self.kiwoom.dynamicCall("GetChejanData(int)", 10).strip(),
                '최우선매도호가': self.kiwoom.dynamicCall("GetChejanData(int)", 27).strip(),
                '최우선매수호가': self.kiwoom.dynamicCall("GetChejanData(int)", 28).strip()
            }
            for event_func in self._onReceiveBalance_observer:
                event_func(data)

        elif sGubun == '4':
            pass

    # 조건검색 결과 수신
    def _api_onReceiveTrCondition(self, sScrNo, strCodeList, strConditionName, nIndex, nNext):
        condition = {'조건식인덱스': nIndex, '조건식명': strConditionName}
        codeList = strCodeList.split(';')
        itemList = []
        for code in codeList:
            if len(code) > 0:
                codeInfo = code.split('^')
                itemList.append({
                    '종목코드': codeInfo[0],
                    '현재가': int(codeInfo[1])
                })

        for event_func in self._onReceiveCondition_observer:
            event_func(condition, itemList)

    # 실시간 조건 편입/이탈 수신
    def _api_onReceiveRealCondition(self, strCode, strType, strConditionName, strConditionIndex):
        if strType == 'I':
            type = '편입'
        else:
            type = '이탈'

        condition = {'조건식인덱스': strConditionIndex, '조건식명': strConditionName}

        for event_func in self._onReceiveRealCondition_observer:
            event_func(condition, strCode, type)

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

    #GetCommRealData 호출
    def getRealData(self, itemCode, fId):
        return self.kiwoom.dynamicCall("GetCommRealData(QString, int)", itemCode, fId)

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

    #SendOrder 호출
    def sendBuyOrder(self, account, itemCode, quantity, price, priceType):
        self.kiwoom.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
                                '신규매수주문',
                                self._getScreenNumber(),
                                account,
                                1,
                                itemCode,
                                quantity,
                                price,
                                self._getOrderPriceType(priceType),
                                ''
                                )

    # SendOrder 호출
    def sendSellOrder(self, account, itemCode, quantity, price, priceType):
        self.kiwoom.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
                                '신규매도주문',
                                self._getScreenNumber(),
                                account,
                                2,
                                itemCode,
                                quantity,
                                price,
                                self._getOrderPriceType(priceType),
                                ''
                                )

    def _getOrderPriceType(self, type):
        if type == '지정가':
            return '00'
        elif type == '시장가':
            return '03'
        elif type == '조건부지정가':
            return '05'
        elif type == '최유리지정가':
            return '06'
        elif type == '최우선지정가':
            return '07'
        elif type == '지정가IOC':
            return '10'
        elif type == '시장가IOC':
            return '13'
        elif type == '최유리IOC':
            return '16'
        elif type == '지정가FOK':
            return '20'
        elif type == '시장가FOK':
            return '23'
        elif type == '최유리FOK':
            return '26'
        elif type == '장전시간외종가':
            return '61'
        elif type == '시간외단일가매매':
            return '62'
        elif type == '장후시간외종가':
            return '81'

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
            server = self.kiwoom.dynamicCall("GetLoginInfo(QString)", "GetServerGubun").strip()
            if server == '1':
                return '모의투자'
            else:
                return '실서버'

    #계좌비밀번호 설정 창 호출
    def showAccountWindow(self):
        if self.getLoginState():
            self.kiwoom.dynamicCall("KOA_Functions(QString, QString)", "ShowAccountWindow", "")

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

    #Add/Remove Event
    def addOnLogin(self, func):
        if func not in self._onLogin_observer:
            self._onLogin_observer.append(func)

    def removeOnLogin(self, func):
        if func in self._onLogin_observer:
            self._onLogin_observer.remove(func)

    def addOnReceiveTr(self, func):
        if func not in self._onReceiveTr_observer:
            self._onReceiveTr_observer.append(func)

    def removeOnReceiveTr(self, func):
        if func in self._onReceiveTr_observer:
            self._onReceiveTr_observer.remove(func)

    def addOnReceiveReal(self, func):
        if func not in self._onReceiveReal_observer:
            self._onReceiveReal_observer.append(func)

    def removeOnReceiveReal(self, func):
        if func in self._onReceiveReal_observer:
            self._onReceiveReal_observer.remove(func)

    def addOnReceiveRealExt(self, func):
        if func not in self._onReceiveRealExt_observer:
            self._onReceiveRealExt_observer.append(func)

    def removeOnReceiveRealExt(self, func):
        if func in self._onReceiveRealExt_observer:
            self._onReceiveRealExt_observer.remove(func)

    def addOnAcceptedOrder(self, func):
        if func not in self._onAcceptedOrder_observer:
            self._onAcceptedOrder_observer.append(func)

    def removeOnAcceptedOrder(self, func):
        if func in self._onAcceptedOrder_observer:
            self._onAcceptedOrder_observer.remove(func)

    def addOnConcludedOrder(self, func):
        if func not in self._onConcludedOrder_observer:
            self._onConcludedOrder_observer.append(func)

    def removeOnConcludedOrder(self, func):
        if func in self._onConcludedOrder_observer:
            self._onConcludedOrder_observer.remove(func)

    def addOnReceiveBalance(self, func):
        if func not in self._onReceiveBalance_observer:
            self._onReceiveBalance_observer.append(func)

    def removeOnReceiveBalance(self, func):
        if func in self._onReceiveBalance_observer:
            self._onReceiveBalance_observer.remove(func)

    def addOnReceiveCondition(self, func):
        if func not in self._onReceiveCondition_observer:
            self._onReceiveCondition_observer.append(func)

    def removeOnReceiveCondition(self, func):
        if func in self._onReceiveCondition_observer:
            self._onReceiveCondition_observer.remove(func)

    def addOnReceiveRealCondition(self, func):
        if func not in self._onReceiveRealCondition_observer:
            self._onReceiveRealCondition_observer.append(func)

    def removeOnReceiveRealCondition(self, func):
        if func in self._onReceiveRealCondition_observer:
            self._onReceiveRealCondition_observer.remove(func)
