# TR데이터 조회
TR(Transaction)데이터 조회를 통해 주식가격 및 정보, 거래량 순위, 증권사별매매상위, 계좌평가현황 등 주식과 관련된 정보를 키움 서버에 요청할 수 있습니다.
 키움API에서는 220가지 이상의 TR데이터를 제공하고 있습니다. 각 TR데이터마다 고유한 TR코드를 가지며, 각기 다른 INPUT값을 요구합니다. 

![TR데이터 리스트](https://postfiles.pstatic.net/MjAxODA3MjZfMjA3/MDAxNTMyNjAzNTAwMTI5.zv0JvsrSjp9jKCafaGwHBG5ihkHsuWbNJ-Oeb5sB_R4g.Ew6sKckUQtzAmUt2KC_dO-K1ZG2WRB-TI65UKB4CEeYg.PNG.rkdwnsdud555/img2.png?type=w773)

TR데이터 조회 프로세스 이해하기
-----------------------------



TR데이터 조회 요청
-----------------
TR데이터를 조회하기 위해서는 해당 TR에서 요구하는 INPUT값을 등록해줘야합니다. **setInput()** 함수를 사용해 입력값을 등록할 수 있습니다.
 TR조회에 필요합 입력값을 모두 등록했다면 **requestTr()** 함수를 사용해 tr데이터 조회 요청을 할 수 있습니다.

TR code가 opt10003인 **체결정보요청** TR을 요청한다고 가정해보겠습니다. 

![TR데이터 예제](https://postfiles.pstatic.net/MjAxODA3MjZfNTMg/MDAxNTMyNjAzNTAwMTI1.kMltOvd0zsvpNaI7bj0YUyoW6NiEre5kh3dUSOdlsd0g.LlwTFLSW3w_M6QbkJBbq80f_nNfU8ZGDiU3Y1oWL7nAg.PNG.rkdwnsdud555/img3.png?type=w773)

```
kwos.setInput('종목코드', '005930')
```

```
kwos.requestTr('체결정보', 'opt10003')
```

TR데이터 수신 Event
------------------

관련 함수
--------

샘플 프로그램(requestTr.py)
--------------------------
![샘플 프로그램](https://postfiles.pstatic.net/MjAxODA3MjZfMTAx/MDAxNTMyNjAyMzEwMDAw.EnHewXclSk3AfdeEn6FkFE1oF88pKHllSobz4Kbpqx8g.vF1wHnsLSpiPfACu5yqeAmgVXHoQoC_o6lBTKz2Be98g.PNG.rkdwnsdud555/img.png?type=w773)
