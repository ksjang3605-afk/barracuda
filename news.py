# 주피터 노트북에서 실행 : exec(open(r"H:\\Python\\news\\news.py", 'r', encoding = 'utf-8').read())

''' 
# 추후 진행 예정 사항
0. 블로그 스팟  API를 이용해 기사 자동 포스팅 + 파이썬 애니웨어로 자동 포스팅 지원
   - 이걸 인공지능의 바로 전단계로 인식해야 한다. Cursor AI의 활용과 같은...
   - '속보 + 상보 + 종합'를 기본 타입으로 하고 추후 그래픽 추가
1. Django 이후 celery를 통한 스케쥴링
2. KoNLPy를 활용한 AI 기자의 첫 걸음
3. 다양햔 유형의 기사 작성 추가
   - 연금복권 기사
   - 파이썬으로 홈피 화면 캡쳐 첨부하는 기능 자동화
   - 그래픽 기사(번호 관련 그래픽은 많이 있으므로 주로 매장 위주로...)
4. seaborn, plotly를 이용한 그래픽, 통계 기사(마지막 미션) - 어쩌면 이게 text 기사 보다 더 중요하거나 사람들에게 소구할 수 있다.
5. 원하는 시점, 상황에서 특정 회차를 선택해 기사를 작성하는 코드 작성
   - opt = ''로 초기화한 후 if문에서 opt=='pick'이면 선택 회차 기사 작성 함수 호출. 그리고 마지막에 opt는 다시 ''로 초기화
   - opt 값이 바뀌자마자 이를 알아채 함수를 호출할 수 있는 기능이나 패키지가 있는지 확인 필요
6. 모든 코드의 GUI화 - 홈페이지로 가기 위한 관문 중 하나
7. 기사를 만들기 위해 필요한 모든 기능을 각각의 py 파일에 작성한 뒤 이를 'util'이란 이름의 전용 폴더에 넣어서 관리하고 import 하기
'''

import word
import handle
# from io import StringIO
# import seaborn as sns # 그래픽 기사 작성용(추후)
# from plotly import express as px # 그래픽 기사 작성용(추후)

''' 리턴값이 없는 print()의 결과를 변수에 저장해 그대로 출력하기
def return_print(*char):
    io = StringIO()
    print(*char, file = io, end = "")
    
    return io.getvalue()

a = return_print(total6)
'''

######################################################### 기사 작성 ####################################################################

# 제목 
title1 = f"""
로또 {handle.lotto_nums[0]}회 1등 당첨번호 ❛{handle.lotto_nums[2]}, {handle.lotto_nums[3]}, {handle.lotto_nums[4]}, \
{handle.lotto_nums[5]}, {handle.lotto_nums[6]}, {handle.lotto_nums[7]}❜… 보너스 번호 ❛{handle.lotto_nums[10]}❜
"""

title2 = f"""
로또 {handle.lotto_nums[0]}회 1등 당첨번호 ❛{handle.lotto_nums[2]}·{handle.lotto_nums[3]}·{handle.lotto_nums[4]}·\
{handle.lotto_nums[5]}·{handle.lotto_nums[6]}·{handle.lotto_nums[7]}❜… 보너스 번호 ❛{handle.lotto_nums[10]}❜
"""

title3 = f"""
{handle.lotto_nums[0]}회 로또 1등 {handle.lotto_nums[2]}, {handle.lotto_nums[3]}, {handle.lotto_nums[4]}, {handle.lotto_nums[5]}, \
{handle.lotto_nums[6]}, {handle.lotto_nums[7]}┅ 보너스 {handle.lotto_nums[10]}
"""

title4 = f"""
{handle.lotto_nums[0]}회 로또 1등 {handle.lotto_nums[8]}명… 당첨금 각 {handle.change_unit(handle.lotto_nums[9]).split('만')[0]+'만'}원
"""

title5 = f"""
제{handle.lotto_nums[0]}회 로또 1등 {handle.lotto_nums[8]}명… 당첨금 1인당 {handle.change_unit(handle.lotto_nums[9]).split('억')[0]+'억'}원
"""

# 최다 당첨지역은 빈도 수에 상관 없이 1곳만 표기(글자를 최대한 줄여야 하는 타이틀이라는 점을 감안)
title6 = f"""  
{handle.lotto_nums[0]}회 로또 1등 {handle.lotto_nums[8]}명… 각 {handle.change_unit(handle.lotto_nums[9]).split('억')[0]+'억'}원씩·\
{handle.prov_freq[0][0]} {handle.prov_freq[0][1]}곳 최다 당첨지역 
"""

title7 = f"""
로또 1등 {handle.lotto_nums[8]}명, 자동 {handle.lotto_nums[19]}개·수동 {handle.lotto_nums[20]}개… \
{word.eun_plus('당첨금')} {handle.change_unit(handle.lotto_nums[9]).split('억')[0]+'억'}원
"""

'''
print(title1)
print(title2)
print(title3)
print(title4)
print(title5)
print(title6)
print(title7)
'''

# 부제목 
sub1 = f"""
1등 각 {handle.change_unit(handle.lotto_nums[9]).split('억')[0]+'억'}원… \
{word.eun_plus('2등')} {handle.change_unit(handle.lotto_nums[12]).split('만')[0]+'만'}원씩
"""

sub2 = f"""
1등 당첨번호 ❛{handle.lotto_nums[2]}·{handle.lotto_nums[3]}·{handle.lotto_nums[4]}·{handle.lotto_nums[5]}·{handle.lotto_nums[6]}\
·{handle.lotto_nums[7]}❜… 보너스 번호 ❛{handle.lotto_nums[10]}❜
"""

'''
print(sub1)
print(sub2)
'''

# 속보
fast1 = f"""
{handle.date} 제{handle.lotto_nums[0]}회 동행복권 로또 추첨 결과 ❛{handle.lotto_nums[2]}, {handle.lotto_nums[3]}, {handle.lotto_nums[4]}, \
{handle.lotto_nums[5]}, {handle.lotto_nums[6]}, {handle.lotto_nums[7]}❜{word.yi_ga(handle.num_kor(handle.lotto_nums[7]))} {word.ro_plus('1등 당첨번호')} 뽑혔고, \
{word.eun_plus('보너스 번호')} ❛{handle.lotto_nums[10]}❜{word.ro_euro(handle.num_kor(handle.lotto_nums[10]))} 결정됐다.
"""

fast2 = f"""
로또 복권 운영사 {word.eun_plus('동행복권')} ❛제{handle.lotto_nums[0]}회 동행복권 로또❜ 추첨 결과 ❛{handle.lotto_nums[2]}, {handle.lotto_nums[3]}, \
{handle.lotto_nums[4]}, {handle.lotto_nums[5]}, {handle.lotto_nums[6]}, {handle.lotto_nums[7]}❜{word.yi_ga(handle.num_kor(handle.lotto_nums[7]))} \
{word.ro_plus('1등 당첨번호')} 뽑혔다고 {handle.date} 밝혔다. 

2등 {word.eun_plus('보너스 번호')} ❛{handle.lotto_nums[10]}❜{word.da(handle.num_kor(handle.lotto_nums[10]))}
"""

fast3 = f"""
{word.yi_plus('동행복권')} {handle.date} 추첨한 {handle.lotto_nums[0]}회차 로또 {word.yi_plus('1등 당첨번호')} ❛{handle.lotto_nums[2]}, {handle.lotto_nums[3]}, \
{handle.lotto_nums[4]}, {handle.lotto_nums[5]}, {handle.lotto_nums[6]}, {handle.lotto_nums[7]}❜, {word.eun_plus('보너스 번호')} \
❛{handle.lotto_nums[10]}❜{word.ro_euro(handle.num_kor(handle.lotto_nums[10]))} 결정됐다.
"""

fast4 = f"""
{word.eun_plus('동행복권')} {handle.date} 추첨한 로또 {handle.lotto_nums[0]}회 {word.eul_plus('당첨번호')} 공개했다.

로또 {handle.lotto_nums[0]}회 {word.eun_plus('당첨번호')} ❛{handle.lotto_nums[2]}·{handle.lotto_nums[3]}·{handle.lotto_nums[4]}·{handle.lotto_nums[5]}\
·{handle.lotto_nums[6]}·{handle.lotto_nums[7]}❜{word.myeo(handle.num_kor(handle.lotto_nums[7]))} 2등 {word.eun_plus('보너스 번호')} \
❛{handle.lotto_nums[10]}❜{word.da(handle.num_kor(handle.lotto_nums[10]))}
"""

fast5 = f"""
{handle.date} 제{handle.lotto_nums[0]}회 동행복권 로또 추첨 결과 ❛{handle.lotto_nums[2]}, {handle.lotto_nums[3]}, {handle.lotto_nums[4]}, \
{handle.lotto_nums[5]}, {handle.lotto_nums[6]}, {handle.lotto_nums[7]}❜{word.yi_ga(handle.num_kor(handle.lotto_nums[7]))} {word.ro_plus('1등 당첨번호')} 뽑혔고, \
{word.eun_plus('보너스 번호')} ❛{handle.lotto_nums[10]}❜{word.ro_euro(handle.num_kor(handle.lotto_nums[10]))} 결정됐다.

1등 {word.eun_plus('당첨자')} {handle.lotto_nums[8]}{word.ro_plus('명')} 1인당 \
{handle.change_unit(handle.lotto_nums[9]).split('만')[0]+'만'}{word.eul_plus('원')} 지급받는다.
"""

fast6 = f"""
{handle.date} 제{handle.lotto_nums[0]}회 동행복권 로또 추첨 결과 ❛{handle.lotto_nums[2]}, {handle.lotto_nums[3]}, {handle.lotto_nums[4]}, \
{handle.lotto_nums[5]}, {handle.lotto_nums[6]}, {handle.lotto_nums[7]}❜{word.yi_ga(handle.num_kor(handle.lotto_nums[7]))} {word.ro_plus('1등 당첨번호')} 뽑혔고, \
{word.eun_plus('보너스 번호')} ❛{handle.lotto_nums[10]}❜{word.ro_euro(handle.num_kor(handle.lotto_nums[10]))} 결정됐다.

1등 중 {word.eun_plus('자동')} {handle.lotto_nums[19]}명, {word.eun_plus('수동')} {handle.lotto_nums[20]}명이었으며, {word.eun_plus('최다 당첨지역')} \
{word.yi_plus(handle.fast6_prov)} 차지했다.
"""

fast7 = f"""
{handle.date} 진행된 제{handle.lotto_nums[0]}회 로또 복권 추첨에서 {handle.lotto_nums[2]}, {handle.lotto_nums[3]}, {handle.lotto_nums[4]}, \
{handle.lotto_nums[5]}, {handle.lotto_nums[6]}, {handle.lotto_nums[7]}{word.yi_plus('번')} {word.ro_plus('1등 당첨번호')} 뽑혔다.
{word.eun_plus('보너스 번호')} {handle.lotto_nums[10]}{word.da_plus('번')}

로또 당첨금 등 {word.wa_plus('복권')} 관련한 자세한 {word.eun_plus('사항')} 동행복권 홈페이지에서 확인할 수 있다.
"""

fast8 = f"""
{handle.date} 추첨한 제{handle.lotto_nums[0]}회 로또 당첨번호는 ❛{handle.lotto_nums[2]} {handle.lotto_nums[3]} {handle.lotto_nums[4]} \
{handle.lotto_nums[5]} {handle.lotto_nums[6]} {handle.lotto_nums[7]}❜ {word.myeo(handle.num_kor(handle.lotto_nums[7]))} \
{word.eun_plus('보너스 번호')} ❛{handle.lotto_nums[10]}❜{word.da(handle.num_kor(handle.lotto_nums[10]))} 

{word.eun_plus('당첨금 지급기한')} 지급 개시일로부터 {word.da_plus('1년 이내')}
{word.yi_plus('당첨금 지급 마지막 날')} {word.myeon_plus('휴일')} 다음 영업일까지 받을 수 있다. 
동행복권 홈페이지에서 지난 로또 당첨번호 {word.wa_plus('조회')} 당첨복권 판매점 조회도 가능하다. 

{word.eun_plus('로또 판매 시간')} {word.eun_plus('평일에')} {word.yi_plus('제한')} 없으며, 추첨일인 {word.eun_plus('토요일')} 오후 8시에 {word.eul_plus('판매')} \
마감해 일요일 오전 6시까지 {word.yi_plus('판매')} 중단된다.
"""

'''
print(fast1)
print(fast2)
print(fast3)
print(fast4)
print(fast5)
print(fast6)
print(fast7)
print(fast8)
'''

# 상보
detail1 = f"""
{handle.date} 제{handle.lotto_nums[0]}회 동행복권 로또 추첨 결과 {handle.lotto_nums[2]}, {handle.lotto_nums[3]}, {handle.lotto_nums[4]}, \
{handle.lotto_nums[5]}, {handle.lotto_nums[6]}, {handle.lotto_nums[7]}{word.yi_ga(handle.num_kor(handle.lotto_nums[7]))} {word.ro_plus('1등 당첨번호')} 결정됐다.
{word.eun_plus('보너스 번호')} {handle.lotto_nums[10]}{word.da(handle.num_kor(handle.lotto_nums[10]))}

{word.eul_plus('6개 번호')} 모두 맞힌 {word.eun_plus('1등 당첨자')} {handle.lotto_nums[8]}{word.da_plus('명')} \
각각 {handle.change_unit(handle.lotto_nums[9]).split('만')[0]+'만'}{word.eul_plus('원')} 받는다.
{word.wa_plus('5개 번호')} {word.eul_plus('보너스 번호')} 맞힌 {word.eun_plus('2등')} {handle.lotto_nums[11]}{word.ro_plus('명')} {word.eun_plus('당첨금')} \
{handle.change_unit(handle.lotto_nums[12]).split('만')[0]+'만'}{word.da_plus('원')}
{word.eul_plus('5개 번호')} 맞힌 3등 {handle.lotto_nums[13]}{word.eun_plus('명')} 각각 \
{handle.change_unit(handle.lotto_nums[14]).split('만')[0]+'만'}{word.eul_plus('원씩')} 받는다.
{word.eul_plus('4개 번호')} 맞힌 4등 당첨자 {word.eun_plus(handle.fourth)} {word.eul_plus('5만원씩')}, \
{word.eul_plus('3개 번호')} 맞힌 5등 당첨자 {word.eun_plus(handle.fifth)} 5000원씩 가져간다. 

{word.eun_plus('당첨금 지급기한')} 지급 개시일로부터 {word.da_plus('1년 이내')}
{word.yi_plus('당첨금 지급 마지막 날')} {word.myeon_plus('휴일')} 다음 영업일까지 받을 수 있다.
"""

detail2 = f"""
로또복권 운영사 {word.eun_plus('동행복권')} 제{handle.lotto_nums[0]}회 동행복권 로또 추첨 결과 ❛{handle.lotto_nums[2]}, {handle.lotto_nums[3]}, \
{handle.lotto_nums[4]}, {handle.lotto_nums[5]}, {handle.lotto_nums[6]}, {handle.lotto_nums[7]}❜{word.yi_ga(handle.num_kor(handle.lotto_nums[7]))} \
{word.ro_plus('1등 당첨번호')} 뽑혔다고 밝혔다.
{word.eun_plus('보너스 번호')} ❛{handle.lotto_nums[10]}❜{word.da(handle.num_kor(handle.lotto_nums[10]))} 

로또 {word.eun_plus('1등')} 당첨번호 숫자 {word.yi_plus('6개')} 모두 일치해야 한다. 
{word.eun_plus('2등')} 당첨번호 {word.wa_plus('5개')} 보너스 번호, {word.eun_plus('3등')} 당첨번호 5개, {word.eun_plus('4등')} 당첨번호 4개, \
{word.eun_plus('5등')} 당첨번호 {word.eul_plus('3개')} 맞춰야 한다.

{word.eun_plus('수령 금액')} 당첨 인원 수에 따라 달라진다.
{word.eun_plus('당첨금 지급기한')} 지급 개시일로부터 {word.da_plus('1년 이내')}
{word.yi_plus('당첨금 지급 마지막 날')} {word.myeon_plus('휴일')} 다음 영업일까지 받을 수 있다.
"""

detail3 = f"""
제{handle.lotto_nums[0]}회 로또복권 추첨에서 ❛{handle.lotto_nums[2]}, {handle.lotto_nums[3]}, {handle.lotto_nums[4]}, {handle.lotto_nums[5]}, \
{handle.lotto_nums[6]}, {handle.lotto_nums[7]}❜{word.yi_ga(handle.num_kor(handle.lotto_nums[7]))} {word.ro_plus('1등 당첨번호')} 뽑혔다.
{word.eun_plus('보너스 번호')} ❛{handle.lotto_nums[10]}❜{word.da(handle.num_kor(handle.lotto_nums[10]))}

로또복권 운영사 동행복권에 따르면 당첨번호 {word.eul_plus('6개')} 모두 맞힌 1등 {word.eun_plus('당첨자')} {handle.lotto_nums[8]}명으로 \
{handle.change_unit(handle.lotto_nums[9]).split('만')[0]+'만'}원씩 받는다.
당첨번호 {word.wa_plus('5개')} {word.yi_plus('보너스 번호')} 일치한 {word.eun_plus('2등')} {handle.lotto_nums[11]}명으로 \
각 {handle.change_unit(handle.lotto_nums[12]).split('만')[0]+'만'}{word.eul_plus('원씩')}, 당첨번호 {word.eul_plus('5개')} 맞힌 {word.eun_plus('3등')} \
{handle.lotto_nums[13]}명으로 {handle.change_unit(handle.lotto_nums[14]).split('만')[0]+'만'}{word.eul_plus('원씩')} 받는다.

당첨번호 {word.eul_plus('4개')} 맞힌 4등(고정 당첨금 5만원){word.eun_neun('4등')} {handle.fourth}, \
당첨번호 {word.yi_plus('3개')} 일치한 5등(고정 당첨금 5천원){word.eun_neun('5등')} {word.da_plus(handle.fifth)}
"""

detail4 = f"""
로또복권 운영사 {word.eun_plus('동행복권')} 제{handle.lotto_nums[0]}회 로또복권 추첨에서 ❛{handle.lotto_nums[2]}, {handle.lotto_nums[3]}, \
{handle.lotto_nums[4]}, {handle.lotto_nums[5]}, {handle.lotto_nums[6]}, {handle.lotto_nums[7]}❜{word.yi_ga(handle.num_kor(handle.lotto_nums[7]))} \
{word.ro_plus('1등 당첨번호')} 뽑혔다고 {handle.date} 밝혔다.
2등 {word.eun_plus('보너스 번호')} ❛{handle.lotto_nums[10]}❜{word.da(handle.num_kor(handle.lotto_nums[10]))}

당첨번호 {word.eul_plus('6개')} 모두 맞힌 1등 {word.eun_plus('당첨자')} {handle.lotto_nums[8]}명으로 \
{handle.change_unit(handle.lotto_nums[9]).split('만')[0]+'만'}원씩 받는다.
당첨번호 {word.wa_plus('5개')} {word.yi_plus('보너스 번호')} 일치한 {word.eun_plus('2등')} {handle.lotto_nums[11]}명으로 각 \
{handle.change_unit(handle.lotto_nums[12]).split('만')[0]+'만'}{word.eul_plus('원씩')}, 당첨번호 {word.eul_plus('5개')} 맞힌 {word.eun_plus('3등')} \
{handle.lotto_nums[13]}명으로 {handle.change_unit(handle.lotto_nums[14]).split('만')[0]+'만'}{word.eul_plus('원씩')} 받는다.

당첨번호 {word.eul_plus('4개')} 맞힌 4등(고정 당첨금 5만원){word.eun_neun('4등')} {handle.fourth}, \
당첨번호 {word.yi_plus('3개')} 일치한 5등(고정 당첨금 5000원){word.eun_neun('5등')} {word.da_plus(handle.fifth)}
"""

detail5 = f"""
{word.ro_plus('1등 당첨번호')} ❛{handle.lotto_nums[2]}, {handle.lotto_nums[3]}, {handle.lotto_nums[4]}, {handle.lotto_nums[5]}, {handle.lotto_nums[6]}, \
{handle.lotto_nums[7]}❜{word.yi_ga(handle.num_kor(handle.lotto_nums[7]))} 뽑혔다.
2등 {word.eun_plus('보너스 번호')} ❛{handle.lotto_nums[10]}❜{word.da(handle.num_kor(handle.lotto_nums[10]))}

당첨번호 {word.eul_plus('6개')} 모두 맞힌 1등 {word.eun_plus('당첨자')} {handle.lotto_nums[8]}명으로 \
{handle.change_unit(handle.lotto_nums[9]).split('만')[0]+'만'}원씩 받는다.
당첨번호 {word.wa_plus('5개')} {word.yi_plus('보너스 번호')} 일치한 {word.eun_plus('2등')} {handle.lotto_nums[11]}명으로 각 \
{handle.change_unit(handle.lotto_nums[12]).split('만')[0]+'만'}{word.eul_plus('원씩')}, 당첨번호 {word.eul_plus('5개')} 맞힌 {word.eun_plus('3등')} {handle.lotto_nums[13]}명으로 \
{handle.change_unit(handle.lotto_nums[14]).split('만')[0]+'만'}{word.eul_plus('원씩')} 받는다.

당첨번호 {word.eul_plus('4개')} 맞힌 4등(고정 당첨금 5만원){word.eun_neun('4등')} {handle.fourth}, \
당첨번호 {word.yi_plus('3개')} 일치한 5등(고정 당첨금 5000원){word.eun_neun('5등')} {word.da_plus(handle.fifth)}
"""

detail6 = f"""
{word.eun_plus('동행복권')} 제{handle.lotto_nums[0]}회 로또복권 추첨에서 ❛{handle.lotto_nums[2]}, {handle.lotto_nums[3]}, {handle.lotto_nums[4]}, \
{handle.lotto_nums[5]}, {handle.lotto_nums[6]}, {handle.lotto_nums[7]}❜{word.yi_ga(handle.num_kor(handle.lotto_nums[7]))} \
{word.ro_plus('1등 당첨번호')} 뽑혔다고 {handle.date} 밝혔다.
2등 {word.eun_plus('보너스 번호')} ❛{handle.lotto_nums[10]}❜{word.da(handle.num_kor(handle.lotto_nums[10]))}

당첨번호 {word.eul_plus('6개')} 모두 맞힌 1등 {word.eun_plus('당첨자')} {handle.lotto_nums[8]}명으로 \
{handle.change_unit(handle.lotto_nums[9]).split('만')[0]+'만'}원씩 받는다.
당첨번호 {word.wa_plus('5개')} {word.yi_plus('보너스 번호')} 일치한 {word.eun_plus('2등')} {handle.lotto_nums[11]}명으로 \
각 {handle.change_unit(handle.lotto_nums[12]).split('만')[0]+'만'}{word.eul_plus('원씩')}, \
당첨번호 {word.eul_plus('5개')} 맞힌 {word.eun_plus('3등')} {handle.lotto_nums[13]}명으로 \
{handle.change_unit(handle.lotto_nums[14]).split('만')[0]+'만'}{word.eul_plus('원씩')} 받는다. 

당첨번호 {word.eul_plus('4개')} 맞힌 4등(고정 당첨금 5만원){word.eun_neun('4등')} {handle.fourth}, 당첨번호 {word.yi_plus('3개')} 일치한 \
5등(고정 당첨금 5000원){word.eun_neun('5등')} {word.da_plus(handle.fifth)}
"""

# 자동/수동별 매장 전체 숫자만 표기할 때는 동행복권 홈피에 나온 숫자 그대로 handle.lotto_nums[19], handle.lotto_nums[20]를 사용
# 매장명까지 같이 표기할 때는 온라인, 중복 매장을 제외한 len(handle.auto_shop), len(handle.manu_shop)을 사용
detail7 = f"""
{handle.lotto_nums[0]}회({handle.date} 추첨) 로또 1등 당첨 번호는 ❛{handle.lotto_nums[2]}·{handle.lotto_nums[3]}·{handle.lotto_nums[4]}\
·{handle.lotto_nums[5]}·{handle.lotto_nums[6]}·{handle.lotto_nums[7]}❜{word.da(handle.num_kor(handle.lotto_nums[7]))}
{word.eun_plus('보너스 번호')} ❛{handle.lotto_nums[10]}❜{word.da(handle.num_kor(handle.lotto_nums[10]))}

당첨 번호 {word.eul_plus('6개')} 모두 맞힌 {word.eun_plus('1등')} 총 {handle.lotto_nums[8]}명이다.
당첨금액은 각각 {handle.change_unit(handle.lotto_nums[9]).split('만')[0]+'만'}원이다.
당첨 번호 {word.wa_plus('5개')} {word.eul_plus('보너스 번호')} 맞힌 {word.eun_plus('2등')} {handle.lotto_nums[11]}{word.myeo_plus('명')}, \
당첨금은 {handle.change_unit(handle.lotto_nums[12]).split('만')[0]+'만'}원이다.

1등 {word.eun_plus('배출점')} 자동 {handle.lotto_nums[19]}곳이고, {word.eun_plus('수동')} {handle.lotto_nums[20]}곳이다. 

자동 선택 {word.eun_plus('배출점(인터넷 복권판매사이트, 중복 매장 제외)')} {word.da_plus(handle.black_auto_city)}

수동 {len(handle.manu_shop)}{word.eun_plus('곳(인터넷 복권판매사이트, 중복 매장 제외)')} {word.da_plus(handle.black_manu_city)}
"""

'''
print(detail1)
print(detail2)
print(detail3)
print(detail4)
print(detail5)
print(detail6)
print(detail7)
'''

# 종합
total1 = f"""
{word.yi_plus('동행복권')} {handle.date} 진행한 {handle.lotto_nums[0]}회 로또복권 추첨 결과 1등 {word.eun_plus('당첨번호')} \
❛{handle.lotto_nums[2]}·{handle.lotto_nums[3]}·{handle.lotto_nums[4]}·{handle.lotto_nums[5]}·{handle.lotto_nums[6]}·{handle.lotto_nums[7]}❜, \
{word.eun_plus('보너스 번호')} ❛{handle.lotto_nums[10]}❜{word.ro_euro(handle.num_kor(handle.lotto_nums[10]))} 결정됐다.

6개 {word.eul_plus('당첨번호')} 모두 맞힌 1등 {word.eun_plus('당첨자')} 모두 {handle.lotto_nums[8]}{word.ro_plus('명')} \
각 {handle.change_unit(handle.lotto_nums[9]).split('만')[0]+'만'}원의 {word.eul_plus('당첨금')} 받는다. 
당첨번호 {word.wa_plus('5개')} 보너스번호 {word.eul_plus('1개')} 맞힌 {word.eun_plus('2등')} {handle.lotto_nums[11]}{word.myeo_plus('명')}, \
각 {handle.change_unit(handle.lotto_nums[12]).split('만')[0]+'만'}원의 {word.eul_plus('당첨금')} 수령한다.
5개 {word.eul_plus('번호')} 맞힌 3등 {handle.lotto_nums[13]}{word.eun_plus('명')} {handle.change_unit(handle.lotto_nums[14]).split('만')[0]+'만'}원, \
4개 {word.eul_plus('번호')} 맞힌 4등 {word.eun_plus(handle.fourth)} 고정 당첨금 5만원, 3개 {word.eul_plus('번호')} 맞힌 5등 {word.eun_plus(handle.fifth)} 고정 당첨금 {word.eul_plus('5000원')} 가져간다.

1등 당첨 복권 판매점 가운데 {word.eun_plus('자동(인터넷 복권판매사이트, 중복 매장 제외)')} {word.da_plus(handle.black_auto_city)}

수동(인터넷 복권판매사이트, 중복 매장 제외) {len(handle.manu_shop)}{word.eun_plus('곳')} {word.da_plus(handle.black_manu_city)}

{word.eun_plus('당첨금 지급기한')} 지급 개시일로부터 {word.da_plus('1년 이내')} 
{word.yi_plus('당첨금 지급 마지막 날')} {word.myeon_plus('휴일')} 다음 영업일까지 받을 수 있다.
"""

total2 = f"""
{handle.date} 제{handle.lotto_nums[0]}회 동행복권 로또 추첨 결과 {handle.lotto_nums[2]}, {handle.lotto_nums[3]}, {handle.lotto_nums[4]}, \
{handle.lotto_nums[5]}, {handle.lotto_nums[6]}, {handle.lotto_nums[7]}{word.yi_ga(handle.num_kor(handle.lotto_nums[7]))} {word.ro_plus('1등 당첨번호')} 결정됐다.
2등 {word.eun_plus('보너스 번호')} {handle.lotto_nums[10]}{word.da(handle.num_kor(handle.lotto_nums[10]))}

{word.eul_plus('6개 번호')} 모두 맞힌 {word.eun_plus('1등 당첨자')} {handle.lotto_nums[8]}{word.da_plus('명')} 각각 \
{handle.change_unit(handle.lotto_nums[9]).split('만')[0]+'만'}{word.eul_plus('원')} 받는다.
{word.wa_plus('5개 번호')} {word.eul_plus('보너스 번호')} 맞힌 {word.eun_plus('2등')} {handle.lotto_nums[11]}{word.ro_plus('명')} {word.eun_plus('당첨금')} \
{handle.change_unit(handle.lotto_nums[12]).split('만')[0]+'만'}{word.da_plus('원')}
{word.eul_plus('5개 번호')} 맞힌 3등 {handle.lotto_nums[13]}{word.eun_plus('명')} 각각 \
{handle.change_unit(handle.lotto_nums[14]).split('만')[0]+'만'}{word.eul_plus('원씩')} 받는다.

{word.eul_plus('4개 번호')} 맞힌 4등 당첨자 {word.eun_plus(handle.fourth)} {handle.change_unit(handle.lotto_nums[16]).split('만')[0]+'만'}{word.eul_plus('원씩')}, \
{word.eul_plus('3개 번호')} 맞힌 5등 당첨자 {word.eun_plus(handle.fifth)} {handle.lotto_nums[18]}원씩 가져간다. 

1등 당첨자 {handle.lotto_nums[8]}명 중 {handle.lotto_nums[19]}{word.yi_plus('명')} {word.da_plus('자동선택')}

{word.eun_plus('판매점(인터넷 복권판매사이트, 중복 매장 제외)')} {word.da_plus(handle.black_auto_full)}

{word.eun_plus('수동선택')} {handle.lotto_nums[20]}{word.ro_plus('명')} {word.eun_plus('판매점(인터넷 복권판매사이트, 중복 매장 제외)')} {word.da_plus(handle.black_manu_full)}

{word.eun_plus('당첨금 지급기한')} 지급 개시일로부터 {word.da_plus('1년 이내')} 
{word.yi_plus('당첨금 지급 마지막 날')} {word.myeon_plus('휴일')} 다음 영업일까지 받을 수 있다. 
"""

total3 = f"""
제{handle.lotto_nums[0]}회 로또복권 {word.yi_plus('추첨')} 진행된 가운데 {handle.lotto_nums[8]}{word.yi_plus('명')} 1등에 당첨됐다.

{handle.date} 로또복권 운영사 동행복권에 따르면 제{handle.lotto_nums[0]}회 1등 {word.eun_plus('번호')} ❛{handle.lotto_nums[2]}, {handle.lotto_nums[3]}, \
{handle.lotto_nums[4]}, {handle.lotto_nums[5]},{handle.lotto_nums[6]}, {handle.lotto_nums[7]}❜{word.da(handle.num_kor(handle.lotto_nums[7]))}
{word.eun_plus('보너스 번호')} ❛{handle.lotto_nums[10]}❜{word.da(handle.num_kor(handle.lotto_nums[10]))}

당첨번호 {word.eul_plus('6개')} 모두 맞힌 1등 {word.eun_plus('당첨자')} {handle.lotto_nums[8]}{word.ro_plus('명')} 각각 \
{handle.change_unit(handle.lotto_nums[9]).split('만')[0]+'만'}{word.eul_plus('원')} 받는다.
당첨번호 {word.wa_plus('5개')} {word.yi_plus('보너스 번호')} 일치한 {word.eun_plus('2등')} {handle.lotto_nums[11]}{word.ro_plus('명')} \
각각 {handle.change_unit(handle.lotto_nums[12]).split('만')[0]+'만'}{word.eul_plus('원')} 받는다.
당첨번호 {word.eul_plus('5개')} 맞힌 {word.eun_plus('3등')} {handle.lotto_nums[13]}{word.ro_plus('명')} 각각 \
{handle.change_unit(handle.lotto_nums[14]).split('만')[0]+'만'}{word.eul_plus('원씩')} 받는다.

1등 당첨자 중 자동 선택 {handle.lotto_nums[19]}명, 수동 선택 {handle.lotto_nums[20]}명이었다.

자동 당첨자 {word.eun_plus('배출지(인터넷 복권판매사이트, 중복 매장 제외)')} {word.da_plus(handle.white_auto_city)}

수동 당첨자 {word.eun_plus('배출지(인터넷 복권판매사이트, 중복 매장 제외)')} {word.da_plus(handle.white_manu_city)}
"""

total4 = f"""
{handle.date} 로또복권 운영사 {word.eun_plus('동행복권')} 제{handle.lotto_nums[0]}회 로또복권 추첨에서 ❛{handle.lotto_nums[2]}, {handle.lotto_nums[3]}, \
{handle.lotto_nums[4]}, {handle.lotto_nums[5]}, {handle.lotto_nums[6]}, {handle.lotto_nums[7]}❜{word.yi_ga(handle.num_kor(handle.lotto_nums[7]))} \
{word.ro_plus('1등 당첨번호')} 뽑혔다고 밝혔다.
2등 {word.eun_plus('보너스 번호')} '{handle.lotto_nums[10]}'{word.da(handle.num_kor(handle.lotto_nums[10]))}

1등 {word.eun_plus('당첨자')} {handle.lotto_nums[8]}{word.ro_plus('명')} 1인당 {handle.change_unit(handle.lotto_nums[9]).split('만')[0]+'만'}\
{handle.lotto_nums[9] % 10000}원씩 받게 된다.
5개 {word.wa_plus('번호')} {word.eul_plus('보너스 번호')} 맞힌 {word.eun_plus('2등')} {handle.lotto_nums[11]}{word.da_plus('명')} 당첨금은 \
{handle.change_unit(handle.lotto_nums[12]).split('만')[0]+'만'}{handle.lotto_nums[12] % 10000}{word.eul_plus('원')} 받는다.
5개 {word.eul_plus('번호')} 맞힌 3등 {handle.lotto_nums[13]}{word.eun_plus('명')} \
{handle.change_unit(handle.lotto_nums[14]).split('만')[0]+'만'}원, \
4개 {word.eul_plus('번호')} 맞힌 4등 {word.eun_plus(handle.fourth)} 고정 당첨금 5만원, \
3개 {word.eul_plus('번호')} 맞힌 5등 {word.eun_plus(handle.fifth)} 고정 당첨금 5000원을 가져간다.

1등 당첨 복권 판매점 가운데 {word.eun_plus('자동(인터넷 복권판매사이트, 중복 매장 제외)')} {handle.white_auto_city} 등 {handle.lotto_nums[19]}{word.da_plus('곳')}

수동(인터넷 복권판매사이트, 중복 매장 제외) {handle.lotto_nums[20]}{word.eun_plus('곳')} {word.da_plus(handle.white_manu_city)}
"""

total5 = f"""
로또 {handle.lotto_nums[0]}회 {word.yi_plus('당첨번호')} 발표된 가운데 로또 1등 당첨지역에 {word.yi_plus('관심')} 쏠리고 있다.

{handle.date} 동행복권에 따르면 로또 {handle.lotto_nums[0]}회 {word.yi_plus('당첨번호')} {handle.lotto_nums[2]}, {handle.lotto_nums[3]}, \
{handle.lotto_nums[4]}, {handle.lotto_nums[5]}, {handle.lotto_nums[6]}, {handle.lotto_nums[7]}{word.ro_euro(handle.num_kor(handle.lotto_nums[7]))} 나타났다.
2등 {word.eun_plus('보너스 번호')} {handle.lotto_nums[10]}{word.da(handle.num_kor(handle.lotto_nums[10]))}

6개 {word.eul_plus('번호')} 모두 맞힌 1등 {word.eun_plus('당첨자')} {handle.lotto_nums[8]}{word.ro_plus('명')} 각각 \
{handle.change_unit(handle.lotto_nums[9]).split('만')[0]+'만'}원씩 받는다.
5개 {word.wa_plus('번호')} {word.eul_plus('보너스 번호')} 맞힌 {word.eun_plus('2등')} {handle.lotto_nums[11]}{word.ro_plus('명')} \
{word.yi_plus('당첨금')} {handle.change_unit(handle.lotto_nums[12]).split('만')[0]+'만'}원씩, \
5개 {word.eul_plus('보너스 번호')} 맞힌 3등 {handle.lotto_nums[13]}{word.eun_plus('명')} 각각 \
{handle.change_unit(handle.lotto_nums[14]).split('만')[0]+'만'}원씩 받는다.

당첨 {word.eul_plus('방식')} 보면 수동에서 {handle.lotto_nums[20]}명, {handle.total5_mode}

당첨 {word.eul_plus('지역')} 보면 {handle.full_name(handle.most_prov)}에서 1등이 {handle.prov_freq[0][1]}명 나왔다.

이외에 {handle.etc_shop_addr}에서 1등이 나왔다.
"""

total6 = f"""
제 {handle.lotto_nums[0]}회 로또복권 1등 당첨번호 {word.eun_plus('6개')} ❛{handle.lotto_nums[2]}, {handle.lotto_nums[3]}, {handle.lotto_nums[4]}, \
{handle.lotto_nums[5]}, {handle.lotto_nums[6]}, {handle.lotto_nums[7]}❜{word.ro_euro(handle.num_kor(handle.lotto_nums[7]))} 나타났다.
2등 {word.eun_plus('보너스 번호')} ❛{handle.lotto_nums[10]}❜{word.da(handle.num_kor(handle.lotto_nums[10]))}

6개 {word.eul_plus('번호')} 모두 맞힌 1등 {word.eun_plus('당첨자')} 모두 {handle.lotto_nums[8]}{word.ro_plus('명')} 각각 \
{handle.change_unit(handle.lotto_nums[9]).split('만')[0]+'만'}원씩 받는다.
당첨번호 {word.wa_plus('5개')} 보너스 번호 {word.eul_plus('1개')} 맞힌 {word.eun_plus('2등')} {handle.lotto_nums[11]}{word.ro_plus('명')} \
당첨금은 각 {handle.change_unit(handle.lotto_nums[12]).split('만')[0]+'만'}{word.da_plus('원')}

이어 ▲5개 {word.eul_plus('번호')} 맞힌 {word.eun_plus('3등')} {handle.change_unit(handle.lotto_nums[14]).split('만')[0]+'만'}원 \
({handle.lotto_nums[13]}명) ▲4개 {word.eul_plus('번호')} 맞힌 {word.eun_plus('4등')} 5만원({handle.fourth}) \
▲3개 {word.eul_plus('번호')} 맞힌 {word.eun_plus('5등')} 5000원({handle.fifth})씩 받는다.

이번 주 1등 당첨번호 {word.yi_plus('6개')} 모두 일치한 {handle.lotto_nums[8]}명의 구매 방식은 모두 자동 {handle.lotto_nums[19]}명, \
수동 {handle.lotto_nums[20]}{word.ro_plus('명')} 집계됐다.
{word.eun_plus('당첨지역')} {handle.total6_str} 등 총 {len(handle.sorted_prov)}곳이다.

1등 당첨자 {handle.lotto_nums[8]}명 가운데 {word.ro_plus('자동선택')} 구매한 {handle.lotto_nums[19]}곳의 {word.eun_plus('판매점(인터넷 복권판매사이트, 중복 매장 제외)')} {word.da_plus(handle.white_auto_full)}

{word.eun_plus('수동선택')} {handle.lotto_nums[20]}{word.ro_plus('곳')} {word.eun_plus('판매점(인터넷 복권판매사이트, 중복 매장 제외)')} {word.da_plus(handle.white_manu_full)}

이번 {handle.lotto_nums[0]}회차까지 1등 누적 {word.eun_plus('당첨자수')} {handle.wins_cumul_sum}{word.da_plus('명')}
역대 최고 {word.eun_plus('당첨금액')} {word.da_plus(handle.top_money)}

{word.eun_plus('당첨금 지급기한')} 지급 개시일로부터 {word.da_plus('1년 이내')} 
{word.yi_plus('당첨금 지급 마지막 날')} {word.myeon_plus('휴일')} 다음 영업일까지 받을 수 있다. 
"""

total7 = f"""
{handle.date} 추첨한 {handle.lotto_nums[0]}회 로또 1등 {word.eun_plus('당첨 번호')} ❛{handle.lotto_nums[2]}·{handle.lotto_nums[3]}·{handle.lotto_nums[4]}·\
{handle.lotto_nums[5]}·{handle.lotto_nums[6]}·{handle.lotto_nums[7]}❜{word.da(handle.num_kor(handle.lotto_nums[7]))}
{word.eun_plus('보너스 번호')} ❛{handle.lotto_nums[10]}❜{word.da(handle.num_kor(handle.lotto_nums[10]))}

당첨 번호 {word.eul_plus('6개')} 모두 맞힌 {word.eun_plus('1등')} 총 {handle.lotto_nums[8]}{word.da_plus('명')}
이들은 각각 {handle.change_unit(handle.lotto_nums[9]).split('만')[0].replace('억', '억 ')+'만'.replace('만', '만 ')}\
{handle.lotto_nums[9] % 10000}{word.eul_plus('원')} 받는다.
당첨 번호 {word.wa_plus('5개')} 보너스 {word.eul_plus('번호')} 맞힌 {word.eun_plus('2등')} {handle.lotto_nums[8]}{word.ro_plus('명')} \
{word.eun_plus('당첨금')} {handle.change_unit(handle.lotto_nums[12]).split('만')[0]+'만'.replace('만', '만 ')}{handle.lotto_nums[12] % 10000}\
{word.da_plus('원')}
5개 {word.eul_plus('번호')} 맞힌 3등 {handle.lotto_nums[13]}{word.yi_plus('명')} 각 \
{handle.change_unit(handle.lotto_nums[14]).split('만')[0]+'만'.replace('만', '만 ')}{handle.lotto_nums[14] % 10000}원씩을 받는다.

4개 {word.eul_plus('번호')} 맞힌 {word.eun_plus('4등(고정 당청금 5만원)')} 당첨자 {word.da_plus(handle.fourth.replace('만', '만 '))}
3개 {word.eul_plus('번호')} 맞힌 {word.eun_plus('5등 당첨자(고정 당첨금 5000원)')} {word.da_plus(handle.fifth.replace('만', '만 '))}

1등 {word.eun_plus('배출점')} 자동 {handle.lotto_nums[19]}곳, 수동 {handle.lotto_nums[20]}{word.da_plus('곳')}

자동 선택 {word.eun_plus('배출점(인터넷 복권판매사이트, 중복 매장 제외)')} {word.da_plus(handle.white_auto_city)}

수동(인터넷 복권판매사이트, 중복 매장 제외) {handle.lotto_nums[20]}{word.eun_plus('곳')} {word.da_plus(handle.white_manu_city)}

{word.eun_plus('당첨금 지급기한')} 지급 개시일로부터 {word.da_plus('1년(휴일인 경우 익영업일)')}
"""

'''
print(total1)
print(total2)
print(total3)
print(total4)
print(total5)
print(total6)
print(total7)
'''

# 기사 조합(아직은 테스트 중인 상황) - 사실 이렇게 기사 조합을 하면 고생해 만들어놓은 나머지 total과 같은 것들이 빛을 못보고 만다.
news1 = f"""
{title2}
{fast1}
"""

news2 = f"""
{title4}
{fast5}
"""

news3 = f"""
{title2}{sub1}
{detail3}
"""

news4 = f"""
{title4}{sub2}
{detail7}
"""

news5 = f"""
{title2}{sub1}
{total2}
"""

news6 = f"""
{title4}{sub2}
{total5}
"""

############################################### 작성된 최신회차 기사 작성(로또) 마이에 저장하기###########################################

''' MySQL에 저장하는 것은 잠시 보류.. 사실 블로그에 쓰면 블로그 서버에 저장되는 것이니 따로 저장하지 않아도 괜찮다.
data = [latest, title_1, title_2, title_3, title_4, title_5, title_6, title_7, sub_1, sub_2, fast_1, fast_2, fast_3, fast_4, fast_5, fast_6, fast_7, fast_8, detail_1, detail_2, detail_3, detail_4, detail_5, detail_6, detail_7, total_1, total_2, total_3, total_4, total_5, total_6, total_7, news_1, news_2, news_3, news_4, news_5, news_6]
con = pymysql.connect(host='localhost', user='root', password='3605', db=f'{news_db}', charset='utf8mb4', autocommit=True)
print("★★★★★ MySQL(Local Host) beefcake DB(news DB) 접속 성공 ★★★★★")
cursor = con.cursor()
cursor.execute(f"use {news_db}")

sql_insert = "insert into lotto_news(round, title_1, title_2, title_3, title_4, title_5, title_6, title_7, sub_1, sub_2, fast_1, fast_2, fast_3, fast_4, fast_5, fast_6, fast_7, fast_8, detail_1, detail_2, detail_3, detail_4, detail_5, detail_6, detail_7, total_1, total_2, total_3, total_4, total_5, total_6, total_7, news_1, news_2, news_3, news_4, news_5, news_6) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

cursor.execute(sql_insert, (data))
'''