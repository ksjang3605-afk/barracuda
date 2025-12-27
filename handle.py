'''추가되어야 하는 기능/사항들
1. 연금복권 및 그래픽 기사 작성을 위한 데이터 처리 함수 추가
2. crawl.py와 함께 파이썬 애니웨어에 넣어서 스케쥴링
3. 
'''

import pymysql
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from collections import Counter

import sys
sys.path.append("H:\\Python\\crawl")
import crawl

# 가장 먼저 crawl 모듈 import 시 자동으로 DB 업데이트부터 진행
crawl.check_lotto() 
crawl.check_pens()

# 로또, 연금복권의 최신 회차 번호 및 매장 정보 및 역대 최다 당첨금, 누적 당첨자 수 계산에 필요한 데이터 DB에서 가져오기
def get_info(db_name) : 
    con, cursor = crawl.con_db(db_name)  
    
    cursor.execute("select * from lotto_nums order by round desc limit 1")
    lotto_nums = cursor.fetchall()
    
    cursor.execute("select round from lotto_shop where round = (select max(round) from lotto_shop) limit 1")
    lotto_max = cursor.fetchone()
    cursor.execute(f"select * from lotto_shop where round = {lotto_max[0]}")
    lotto_shop = cursor.fetchall()

    cursor.execute("select * from pens_nums order by round desc limit 1")
    pens_nums = cursor.fetchall()
    
    cursor.execute("select round from pens_shop where round = (select max(round) from pens_shop) limit 1")
    pens_max = cursor.fetchone()
    cursor.execute(f"select * from pens_shop where round = {pens_max[0]}")
    pens_shop = cursor.fetchall()

    cursor.execute("select * from lotto_nums order by money desc limit 1") 
    top_money = cursor.fetchall()

    cursor.execute("select wins from lotto_nums") 
    wins_col = cursor.fetchall()
    
    cursor.close()
    con.close()
    
    return lotto_nums, lotto_shop, pens_nums, pens_shop, top_money, wins_col

# DB에서 가져온 로또 번호 정보 정리
def set_lotto_nums() :
    lotto_nums, _, _, _, _, _ = get_info('mugshot') # get_info()의 리턴값 6개중 lotto_nums만 받고 나머지는 무시

    if lotto_nums[0][8] != 0 : # 당첨자 수가 0인지 확인
        lotto_nums = [list(i) for i in lotto_nums] # 중첩 튜플을 중첩 리스트로 변환 
        lotto_nums = [x for y in lotto_nums for x in y] # 중첩 리스트 평탄화
        lotto_nums[1] = lotto_nums[1].strftime('%Y-%m-%d') # datetime 형식 날짜를 문자열로 변환
    
        return lotto_nums
    
    else : 
        print(f"현재 가장 최신 정보인 {lotto_nums[0][0]} 회차에는 당첨자가 없어 관련 기사를 작성할 수 없습니다.")

lotto_nums = set_lotto_nums()

def set_lotto_shop() :
    temp_shop = []
    lotto_shop = []
    
    _, shop, _, _, _, _ = get_info('mugshot') # get_info()의 리턴값 6개중 lotto_shop만 받고 나머지는 무시

    for i in range(len(shop)) : # 온라인 매장 제거
        if not shop[i][1].startswith('인터넷') : 
            temp_shop.append(shop[i])
            
    temp_shop = [list(i) for i in temp_shop]

    for i in temp_shop : # 중복 매장 제거 
        if i not in lotto_shop : 
            lotto_shop.append(i)
    
    return lotto_shop

lotto_shop = set_lotto_shop()

# 숫자로 된 인당 당첨금을 만단위로 끊어서 읽기 편하게 문자열로 표기.
def change_unit(number) : 
    res_str= ''

    if number >= 100000000 :
        eok = number // 100000000
        res_str += f"{eok :.0f}억"
        number %= 100000000

    if number >= 10000 :
        man = number // 10000
        res_str += f"{man :.0f}만"
        number %= 10000

    if number > 0 :
        res_str += f"{number :.0f}원"

    elif not res_str :
        res_str = f"{number :.0f}원"

    return res_str.strip()

# 역대 최다 당첨금 계산하기
def set_top_money() :
    _, _, _, _, top_money, _ = get_info('mugshot') # get_info()의 리턴값 6개중 top_money만 받고 나머지는 무시
    top_money = [list(i) for i in top_money]
    top_money = [x for y in top_money for x in y]
    top_money = top_money[9]
    top_money = change_unit(top_money)

    return top_money

top_money = set_top_money()

# 누적 당첨자 수 계산하기
def set_wins_col() :
    wins_cumul_sum = 0
    
    _, _, _, _, _, wins_col = get_info('mugshot') # get_info()의 리턴값 6개중 wins_col만 받고 나머지는 무시
    wins_col = [list(i) for i in wins_col]
    wins_col = [x for y in wins_col for x in y]    

    for i in wins_col :
        wins_cumul_sum += i

    return wins_cumul_sum

wins_cumul_sum = set_wins_col()

# 월, 일 앞자리가 0일 경우 0을 제외한 숫자만 표기 & 기사를 작성하는 시점의 달이 추첨일의 월과 다를 경우 월을 추가하고, 같으면 일만 표기
def set_date(month, day) : 
    if month == str(datetime.now().month) : 
        if day[0] == '0' :
            day = day[1]
            date = day + '일'
            
        else : 
            date = day + '일' 
        
    else :
        if month[0] == '0' or day[0] == '0':
            month = month[1]
            day = day = day[1]
            date = month + '월 ' + day + '일'

        else : 
            date = month + '월 ' + day + '일'

    return date

date = set_date(lotto_nums[1][5:7], lotto_nums[1][8:10])

# 단위가 큰 4등과 5등 당첨자를 읽기 편하게 억/만 단위로 변환
def set_four_five() : 
    fourth = change_unit(lotto_nums[15]).replace('원', '') + '명' 
    fifth = change_unit(lotto_nums[17]).replace('원', '') + '명'

    return fourth, fifth

fourth, fifth = set_four_five()

# 최다 1등 당첨 광역시/도 계산 및 해당 광역시/도의 매장 정보 추출하기
def get_most(lotto_shop) : 
    most_prov = []
    most_shop = []
    
    prov_list = [row[3] for row in lotto_shop] # 최다 당첨 광역시/도 계산을 위해 광역시/도 명칭만 추출
    prov_freq = Counter(prov_list).most_common() # city_list의 모든 요소에 대한 빈도수를 계산해 내림차순으로 정렬

    for i in range(len(prov_freq)):
        if prov_freq[i][1] == prov_freq[0][1] : # prov_freq[0][1]는 최다 당첨지역의 빈도수
            most_prov.append(prov_freq[i][0]) # 최빈값의 빈도수와 같을 경우 해당 지역명을 most_prov 리스트에 추가
    
        elif prov_freq[0][1] == 1 :
            most_prov = prov_list

    for i in range(len(lotto_shop)): 
        if lotto_shop[i][3] in most_prov:
            most_shop.append(lotto_shop[i][1:5]) # 회차를 제외한 나머지 정보만 취합
    
    return prov_list, prov_freq, most_prov, most_shop

    for i in range(len(most_shop)):
        del most_shop[i][0] # 불필요한 회차 삭제
    
    return prov_list, prov_freq, most_prov, most_shop

prov_list, prov_freq, most_prov, most_shop = get_most(lotto_shop)

# 최다 1등 당첨 지역이 아닌 기타 광역시/도 및 해당 광역시/도의 매장 정보 추출하기
def get_etc() : 
    temp_prov = []
    temp_shop_addr = []
    
    etc_prov = []
    etc_shop_addr = []
    
    if prov_freq[0][1] != 1 :
        for i in range(len(lotto_shop)) : 
            if lotto_shop[i][3] not in most_prov :
                temp_prov.append(lotto_shop[i][3])
                temp_shop_addr.append(lotto_shop[i][5])
                
    else :
        for i in range(len(lotto_shop) // 2, len(lotto_shop)) : 
            temp_prov.append(lotto_shop[i][3])
            temp_shop_addr.append(lotto_shop[i][4])

    for i in temp_prov : # 중복 광역시/도명 제거 
        if i not in etc_prov : 
            etc_prov.append(i)

    for i in temp_shop_addr : # 중복 매장 제거 
        if i not in etc_shop_addr : 
            etc_shop_addr.append(i)
            
    etc_shop_addr = ', '.join(etc_shop_addr)

    return etc_prov, etc_shop_addr

etc_prov, etc_shop_addr = get_etc()

# 자동/수동별 매장명, 시도명, 전체 주소 추출하기
def get_auto_manu() : 
    auto_shop = []
    auto_city = []
    auto_full = []
    manu_shop = []
    manu_city = []
    manu_full = []

    for i in range(len(lotto_shop)):
        if lotto_shop[i][2] == '자동' :
            auto_shop.append(lotto_shop[i][1])
            auto_city.append(lotto_shop[i][4])
            auto_full.append(lotto_shop[i][5])

        elif lotto_shop[i][2] == '수동' :
            manu_shop.append(lotto_shop[i][1])
            manu_city.append(lotto_shop[i][4])
            manu_full.append(lotto_shop[i][5])

    return auto_shop, auto_city, auto_full, manu_shop, manu_city, manu_full

auto_shop, auto_city, auto_full, manu_shop, manu_city, manu_full = get_auto_manu()

# 당첨번호 숫자를 한글로 변환
def num_kor(n):
    units = [''] + list('십백')
    nums = '일이삼사오육칠팔구'
    result = []
    i = 0 # 현재 처리 중인 자릿수를 나타내기 위해 0으로 초기화
    
    while n > 0:
        n, r = divmod(n, 10) # 입력된 숫자 n을 10으로 나눠 몫은 n, 나머지는 r에 각각 저장
        if r > 0: # 나머지인 r이 0보다 크면 i와 함께 단위 값을 구하고 이를 임시 리스트인 result에 붙임. 0이면 해당 자리는 건너뜀
            result.append(nums[r - 1] + units[i])
        i += 1 # 자릿수를 하나 늘리기
        
    return ''.join(result[::-1]) # result에는 글자가 일의 자리부터 십의 자리까지 역순으로 들어가 있으므로 이를 뒤집어서 이어 붙임

# 당첨자 배출 광역시/도의 명칭을 풀네임으로 표기
def full_name(win_prov) :
    city = ['서울', '대전', '대구', '부산', '광주', '울산', '세종', '인천']
    prov1 = ['경기', '강원', '제주'] 
    prov2 = ['충남', '충북', '전남', '전북', '경남', '경북'] 
    temp_name_list = []

    if len(win_prov) == 1 :
        win_prov = ' '.join(win_prov)

        if win_prov in city :
            prov_name = win_prov + '시'             
            
        elif win_prov in prov1 :
            prov_name = win_prov + '도'
            
        elif win_prov in prov2 :
            
            if win_prov == '충남' :
                prov_name = '충청남도'
            elif win_prov == '충북' :
                prov_name = '충청북도'
            elif win_prov == '전남' :
                prov_name = '전라남도'
            elif win_prov == '전북' :
                prov_name = '전라북도'
            elif win_prov == '경남' :
                prov_name = '경상남도'
            elif win_prov == '경북' :
                prov_name = '경상북도'

        return prov_name

    else : 
        for i in win_prov :
            
            if i in city :
                temp_name = i + '시' 
                temp_name_list.append(temp_name)
                
            elif i in prov1 :
                temp_name = i + '도'
                temp_name_list.append(temp_name)
                
            elif i in prov2 :
                
                if i == '충남' :
                    temp_name = '충청남도'
                    temp_name_list.append(temp_name)
                    
                elif i == '충북' :
                    temp_name = '충청북도'
                    temp_name_list.append(temp_name)
                    
                elif i == '전남' :
                    temp_name = '전라남도'
                    temp_name_list.append(temp_name)
                    
                elif i == '전북' :
                    temp_name = '전라북도'
                    temp_name_list.append(temp_name)
                    
                elif i == '경남' :
                    temp_name = '경상남도'
                    temp_name_list.append(temp_name)
                    
                elif i == '경북' :
                    temp_name = '경상북도'
                    temp_name_list.append(temp_name)
        
        prov_name = ' '.join(temp_name_list)
        
        return prov_name

# 최다 당첨자 배출 지역 정리
def set_fast6() :
    if len(most_prov) != 1 :
        fast6_prov = ', '.join(most_prov)

    else :
        fast6_prov = most_prov[0]

    return fast6_prov

fast6_prov = set_fast6()

# 매장명 + (시도명)
def black_white_city() :
    black_auto_city = []
    black_manu_city = []
    white_auto_city = []
    white_manu_city = []

    for i in range(len(auto_shop)) : 
        temp1 = f"▲{auto_shop[i]}({auto_city[i]})"
        black_auto_city.append(temp1)

    for i in range(len(manu_shop)) : 
        temp2 = f"▲{manu_shop[i]}({manu_city[i]})"
        black_manu_city.append(temp2)

    for i in range(len(auto_shop)) : 
        temp3 = f"△{auto_shop[i]}({auto_city[i]})"
        white_auto_city.append(temp3)

    for i in range(len(manu_shop)) : 
        temp4 = f"△{manu_shop[i]}({manu_city[i]})"
        white_manu_city.append(temp4)    

    black_auto_city = ' '.join(black_auto_city)
    black_manu_city = ' '.join(black_manu_city)    
    white_auto_city = ' '.join(white_auto_city)
    white_manu_city = ' '.join(white_manu_city) 

    return black_auto_city, black_manu_city, white_auto_city, white_manu_city
    
black_auto_city, black_manu_city, white_auto_city, white_manu_city = black_white_city()

# 매장명 + (전제 주소)
def black_white_full() :
    black_auto_full = []
    black_manu_full = []
    white_auto_full = []
    white_manu_full = []

    for i in range(len(auto_shop)) : 
        temp1 = f"▲{auto_shop[i]}({auto_full[i]})"
        black_auto_full.append(temp1)

    for i in range(len(manu_shop)) : 
        temp2 = f"▲{manu_shop[i]}({manu_full[i]})"
        black_manu_full.append(temp2)

    for i in range(len(auto_shop)) : 
        temp3 = f"△{auto_shop[i]}({auto_full[i]})"
        white_auto_full.append(temp3)

    for i in range(len(manu_shop)) : 
        temp4 = f"△{manu_shop[i]}({manu_full[i]})"
        white_manu_full.append(temp4)    

    black_auto_full = ' '.join(black_auto_full)
    black_manu_full = ' '.join(black_manu_full)    
    white_auto_full = ' '.join(white_auto_full)
    white_manu_full = ' '.join(white_manu_full) 

    return black_auto_full, black_manu_full, white_auto_full, white_manu_full
    
black_auto_full, black_manu_full, white_auto_full, white_manu_full = black_white_full()

def set_total5() : 
    if lotto_nums[21] == 0 :
        total5_mode = "나머지는 모두 자동서 당첨됐다."

    else :
        total5_mode = f"반자동서 {lotto_nums[21]}명, 자동서 {lotto_nums[20]}명이 당첨됐다."

    return total5_mode

total5_mode = set_total5()

def set_total6() : 
    custom_order = ['서울','인천','경기','강원','세종','충북','대전','충남','대구','경북','부산','울산','경남','전북','광주','전남','제주']
    target_prov = []
    sorted_prov_count = []
    total6_str = []
    
    for i in range(len(prov_freq)) : # 이걸 차라리 prov_freq에서 가져오는게 더 낫다.
        target_prov.append(prov_freq[i][0])

    order_map = {name: i for i, name in enumerate(custom_order)}
    sorted_prov = sorted(target_prov, key = lambda name: order_map.get(name, len(order_map)))
    
    for i in range(len(sorted_prov)) : 
        for j in range(len(prov_freq)) : 
            if sorted_prov[i] == prov_freq[j][0] : 
                sorted_prov_count.append(prov_freq[j][1])

    for i in range(len(sorted_prov)) :
        temp_str = f"{sorted_prov[i]} {sorted_prov_count[i]}곳"
        total6_str.append(temp_str)

    total6_str = ', '.join(total6_str)
        
    return sorted_prov, sorted_prov_count, total6_str

sorted_prov, sorted_prov_count, total6_str = set_total6()

# import 되면 name 변수는 main이 아닌 모듈명(process)이 되어 조건이 거짓이 되므로, 블록 내부 함수는 자동으로 실행되지 않고 import한 모듈 안에서 호출될 때만 실행된다.
if __name__ == '__main__': 
    get_info(db_name)
    set_lotto_nums()
    set_lotto_shop()
    change_unit(number)
    set_top_money()
    set_wins_col()
    set_date(month, day)
    set_four_five()
    get_most(lotto_shop)
    get_etc()
    get_auto_manu()
    num_kor(n)
    full_name(win_prov)
    set_fast6()
    black_white_city()
    black_white_full()
    set_total5()
    set_total6()