''' 추가되어야 하는 기능/사항들
2. crawl이 안될 경우 입력해서 db에 저장하는 코드 필요 
- 이건 crawl.py가 아니라 별도의 py 파일로 분리한 뒤 임포트하는 방식으로... 그래야 이름에 맞다.
3. 파이썬 애니웨어를 이용한 스케쥴링
4. copy 기능의 처리 및 input 기능과의 통합 여부 결정
'''

import re
import time
import inspect
import certifi
import pymysql
import requests
from urllib3 import util
from requests import adapters
from bs4 import BeautifulSoup
from datetime import datetime
from tqdm.notebook import tqdm

# 사용하려는 DB 접속하기
def con_db(db_name) : 
    con = pymysql.connect(host = 'localhost', user = 'root', password = '3605', db = f'{db_name}', charset = 'utf8mb4', autocommit = True)
    cursor = con.cursor()

    return [con, cursor]
    
# 동행복권 홈피에 접속해 해당 url의 html 가져오기
def get_html(url) :    
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'Connection': 'Keep-Alive',
        'Keep-Alive': 'timeout = 5, max = 2000'
    }
    
    with requests.Session() as s :
        retries = util.Retry(
            total = 10,
            connect = 10,
            read = 10,
            status_forcelist = [401, 403, 429, 500, 502, 503, 504],
            backoff_factor = 0.5
        )
        
        s.mount('http://', adapters.HTTPAdapter(max_retries = retries))
        s.mount('https://', adapters.HTTPAdapter(max_retries = retries))
        
        resp = s.get(url, headers = headers, verify = certifi.where(), timeout = 3)
        soup = BeautifulSoup(resp.content, 'lxml') 

    return soup

# 로또/연금복권 최신 회차 가져오기(로또 태그 : 'lottoDrwNo', 연금복권 태그 : 'drwNo720')
def get_latest():
    url = 'https://www.dhlottery.co.kr/common.do?method=main'
    soup = get_html(url)

    caller_func = inspect.currentframe().f_back.f_code.co_name

    if 'lotto' in caller_func :
        latest_round = int(soup.select_one('strong#lottoDrwNo').text)

    else : 
        latest_round = int(soup.select_one('strong#drwNo720').text)
    
    return latest_round

# 번호 정보 url은 회차, 날짜, 매장 정보 url은 회차와 trs 태그 정리해 리턴
def get_count_date_trs(url, pick_round) :
    soup = get_html(url)
    
    if 'byWin' in url or 'win720' in url :
        count = int(soup.select_one('h4>strong').text.strip('회'))
        date = datetime.strptime(soup.select_one('p.desc').text, '(%Y년 %m월 %d일 추첨)')
        date = date.strftime('%Y-%m-%d')

        return soup, count, date

    else : 
        count = int(soup.find('option', selected = True, value = f'{pick_round}').text)
        trs = soup.select('#article>div:nth-child(2)>div>div:nth-child(4)>table>tbody>tr')

        return count, trs

# 1 ~ 6등 당첨번호/금액/당첨자 수 등 로또 번호 관련 정보 크롤링(회차, 날짜 포함)  
def get_lotto_nums(pick_round) : 
    url = f'https://dhlottery.co.kr/gameResult.do?method=byWin&drwNo={pick_round}'    
    soup, count, date = get_count_date_trs(url, pick_round)
    
    # 1등 정보 가져오기
    nums = [int(i) for i in soup.find('div', class_ = 'num win').find('p').text.strip().split('\n')]
    num1 = nums[0]
    num2 = nums[1]
    num3 = nums[2]
    num4 = nums[3]
    num5 = nums[4]
    num6 = nums[5]
    wins = int(soup.select('table>tbody>tr>td')[2].get_text())
    money = int(soup.select('table>tbody>tr>td')[3].get_text().strip('원').replace(',', ''))

    # 2등 이하 정보 가져오기
    bonus = int(soup.select_one('div.num.bonus>p').text.strip())
    second_wins = int(soup.select_one('table>tbody>tr:nth-child(2)>td:nth-child(3)').get_text())
    second_money = int(soup.select_one('table>tbody>tr:nth-child(2)>td:nth-child(4)').get_text().strip('원').replace(',', ''))
    third_wins = int(soup.select_one('table>tbody>tr:nth-child(3)>td:nth-child(3)').get_text().replace(',', ''))
    third_money = int(soup.select_one('table>tbody>tr:nth-child(3)>td:nth-child(4)').get_text().strip('원').replace(',', ''))
    fourth_wins = int(soup.select_one('table>tbody>tr:nth-child(4)>td:nth-child(3)').get_text().replace(',', ''))
    fourth_money = int(soup.select_one('table>tbody>tr:nth-child(4)>td:nth-child(4)').get_text().strip('원').replace(',', ''))
    fifth_wins = int(soup.select_one('table>tbody>tr:nth-child(5)>td:nth-child(3)').get_text().replace(',', ''))
    fifth_money = int(soup.select_one('table>tbody>tr:nth-child(5)>td:nth-child(4)').get_text().strip('원').replace(',', ''))

    lotto_nums=[count, date, num1, num2, num3, num4, num5, num6, wins, money, bonus, second_wins, second_money, third_wins, third_money, \
                fourth_wins, fourth_money, fifth_wins, fifth_money]

    return lotto_nums

# 1 ~ 6등 당첨 구분(자동/수동/반자동) 수치 정보 크롤링
def get_lotto_mode(pick_round) : 
    url = f'https://dhlottery.co.kr/gameResult.do?method=byWin&drwNo={pick_round}'
    soup = get_html(url)
    
    mode = soup.select_one('table>tbody>tr:nth-child(1)>td:nth-child(6)').get_text().strip()
    mode = mode.translate({ord(char) : None for char in '등\n\r\t '})[1:]

    # 1등 당첨 구분이 표기된 '비고'란이 공란인 경우
    if mode == '': 
        auto = '0'
        hand = '0'
        semi = '0'
    
    # 자동만 있는 경우
    elif mode[0]=='자' and len(mode) <= 4:
        auto = int(mode[0:4].translate({ord(char) : None for char in '자동수'}))
        hand = '0'
        semi = '0'
    
    # 수동만 있는 경우
    elif mode[0]=='수' and len(mode) <= 4:
        hand = int(mode[0:4].translate({ord(char) : None for char in '수동반'}))
        auto = '0'
        semi = '0'  
    
    # 반자동만 있는 경우
    elif mode[0]=='반' and len(mode) <= 5:
        semi = int(mode[0:5].translate({ord(char) : None for char in '반자동'}))
        auto = '0'
        hand = '0'
    
    # 자동 & 수동이 있는 경우
    elif mode[0] == '자' and '수' in mode and len(mode) <= 9:
        auto = int(mode[0:4].translate({ord(char) : None for char in '자동수'}))
        
        if mode.find('수') == 3:
            hand = mode[3:7]
        else :
            hand = mode[4:8]
        hand = int(hand.translate({ord(char) : None for char in '자동수'}))
        semi = '0'
    
    # 자동 & 반자동이 있는 경우
    elif mode[0] == '자' and '반' in mode and len(mode) <= 9:
        auto = int(mode[0:4].translate({ord(char) : None for char in '자동반'}))
        
        if mode.find('반') == 3:
            semi = mode[3:8]
        else :
            semi = mode[4:9]
        semi = int(semi.translate({ord(char) : None for char in '반자동'}))
        hand = '0'
    
    # 수동 & 반자동이 있는 경우
    elif mode[0] == '수' and '반' in mode and len(mode) <= 9:
        hand = int(mode[0:4].translate({ord(char) : None for char in '수동반'}))
        
        if mode.find('반') == 3:
            semi = mode[3:8]
        else :
            semi = mode[4:9]
        semi = int(semi.translate({ord(char) : None for char in '반자동'}))
        auto = '0'
    
    # 자동, 수동, 반자동 모두 있는 경우
    elif len(mode) >= 10 :
        auto = int(mode[0:4].translate({ord(char) : None for char in '자동수'}))
        
        if mode.find('수') == 3:
                hand = mode[3:7]
        else :
            hand = mode[4:8]
        hand = int(hand.translate({ord(char) : None for char in '수동반'})) # 수동 당첨자 수 가져오기 #
    
        if mode.find('반') == 6:
            semi = mode[6:]
        elif mode.find('반') == 7:
            semi = mode[7:]
        elif mode.find('반') == 8:
            semi = mode[8:] 
        semi = int(semi.translate({ord(char) : None for char in '반자동'})) # 반자동 당첨자 수 가져오기

    return [auto, hand, semi]

# DB에 테이블 생성하기
def create_table(db_name, table_name):    
    cursor = con_db(db_name) 

    if table_name == 'lotto_nums' :    
        print(f'DB에 {table_name} 테이블을 생성합니다.')
    
        lotto_nums_sql = f"create table {table_name}(round int not null auto_increment, date date not null, num1 int, num2 int, num3 int, num4 int,\
                          num5 int, num6 int, wins int, money bigint, bonus int, second_wins int, second_money int, third_wins int, third_money int,\
                          fourth_wins int, fourth_money int, fifth_wins int, fifth_money int, auto int, hand int, semi int,\
                          constraint lotto_nums_pk primary key(round))"
        cursor.execute(lotto_nums_sql)
        
        print(f'{table_name} 테이블 생성을 완료했습니다')

    elif table_name == 'lotto_shop' :
        print(f'DB에 {table_name} 테이블을 생성합니다.')
    
        lotto_shop_sql = f"create table {table_name}(round int not null, shop char(30), mode char(10), prov char(30), city char(50), addr char(100))"
        cursor.execute(lotto_shop_sql) 
        
        print(f'{table_name} 테이블 생성을 완료했습니다')

    elif table_name == 'pens_nums' :
        print(f'DB에 {table_name} 테이블을 생성합니다.')
    
        pens_nums_sql = f"create table {table_name}(round int not null auto_increment, date date not null, fam int, num1 int, num2 int, num3 int,\
                         num4 int, num5 int, num6 int, wins int, bonus1 int, bonus2 int, bonus3 int, bonus4 int, bonus5 int, bonus6 int,\
                         second_wins int, third_wins int, fourth_wins int, fifth_wins int, sixth_wins int, seventh_wins int, bonus_wins int,\
                         constraint pens_nums_pk primary key(round))"
        cursor.execute(pens_nums_sql) 
        
        print(f'{table_name} 테이블 생성을 완료했습니다')

    elif table_name == 'pens_shop' :
        print(f'DB에 {table_name} 테이블을 생성합니다.')
    
        pens_shop_sql = f"create table {table_name}(round int not null, shop char(30), prov char(30), city char(50), addr char(100))"
        cursor.execute(pens_shop_sql) 
        
        print(f'{table_name} 테이블 생성을 완료했습니다')

    return [cursor, table_name]

# 반복문으로 1회차부터 최신회차까지 로또 번호 관련 정보 크롤링한 뒤 생성된 lotto_nums 테이블에 저장하기
def loop_lotto_nums_mode():
    cursor, table_name = create_table('mugshot', 'lotto_nums')    

    for i in tqdm(range(1, get_latest('lottoDrwNo') + 1)):
        lotto_nums = get_lotto_nums(i)
        lotto_mode = get_lotto_mode(i)
        merged = lotto_nums + lotto_mode 
            
        sql_insert = f"insert into {table_name}(round, date, num1, num2, num3, num4, num5, num6, wins, money, bonus, second_wins, second_money, third_wins,\
                      third_money, fourth_wins, fourth_money, fifth_wins, fifth_money, auto, hand, semi) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,\
                      %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    
        cursor.execute(sql_insert, (merged))
    
    print(f"{get_latest('lottoDrwNo')}회차까지 로또 번호 관련 정보를 DB에 저장했습니다")

# loop_lotto_nums_mode()

def get_lotto_shop(pick_round):       
    url = f'https://www.dhlottery.co.kr/store.do?method=topStore&pageGubun=L645&drwNo={pick_round}'
    count, trs = get_count_date_trs(url, pick_round)    

    lotto_shop = []
        
    for tr in trs: 
        temp_data = []        
            
        shop = tr.select('td')[1].text.strip()            
        mode = tr.select('td')[2].text.strip()

        if shop != '인터넷 복권판매사이트' : # 매장명이 '인터넷 복권판매사이트'가 아닌 경우 모든 항목을 그대로 처리
            addr = tr.select('td')[3].text.strip()
            prov = addr.split()[0] # 전체 주소에서 광역지자체만 추출                
            city = addr.split()[0:2] # 전체 주소에서 광역지자체 + 시/구만 추출
            city = ' '.join(city) # 광역지자체 + 시/구 추출 후 다시 공백 기준으로 합치기

            temp_data.append(count)
            temp_data.append(shop)
            temp_data.append(mode)
            temp_data.append(prov)
            temp_data.append(city)
            temp_data.append(addr)

            lotto_shop.append(temp_data)            
        
        else : # 매장명이 '인터넷 복권판매사이트'인 경우 주소가 없으므로 '-'로 처리
            prov = '-'
            city = '-'                
            addr = '-'

            temp_data.append(count)
            temp_data.append(shop)
            temp_data.append(mode)
            temp_data.append(prov)
            temp_data.append(city)
            temp_data.append(addr)

            lotto_shop.append(temp_data)  
            
    return lotto_shop

# 반복문으로 262회차부터 최신회차까지 로또 매장 관련 정보 크롤링해 생성된 lotto_shop 테이블에 저장하기
def loop_lotto_shop():
    no_round = [289, 295, 463]
    cursor, table_name = create_table('mugshot', 'lotto_shop')
    
    for i in tqdm(range(262, get_latest('lottoDrwNo') + 1)): # 로또 매장 정보는 262회차부터 제공
        if i not in no_round :             
            lotto_shop = get_lotto_shop(i)
            
            sql_insert = f"insert into {table_name}(round, shop, mode, prov, city, addr) values (%s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql_insert, lotto_shop)

        else :
            continue
    
    print(f"{get_latest('lottoDrwNo')}회차까지 로또 매장 관련 정보를 DB에 저장했습니다")

# loop_lotto_shop()

def get_pens_nums(pick_round) :
    url = f'https://www.dhlottery.co.kr/gameResult.do?method=win720&Round={pick_round}'
    soup, count, date = get_count_date_trs(url, pick_round)

    nums = soup.select('div.win720_num')[0].get_text().strip().split('\n')
    del nums[1:3] # 결과 리스트에서 불필요한 텍스트 제거
    nums = [int(i) for i in nums] # 리스트 안의 모든 요소를 꺼내 str을 정수로 변환
    fam = nums[0]
    num1 = nums[1]
    num2 = nums[2]
    num3 = nums[3]
    num4 = nums[4]
    num5 = nums[5]
    num6 = nums[6]
    
    wins = int(soup.select('table>tbody>tr>td')[5].get_text())
    second_wins = int(soup.select_one('table > tbody > tr:nth-child(2) > td:nth-child(5)').get_text())
    third_wins = int(soup.select_one('table > tbody > tr:nth-child(3) > td:nth-child(5)').get_text())
    fourth_wins = int(soup.select_one('table > tbody > tr:nth-child(4) > td:nth-child(5)').get_text().replace(',', ''))
    fifth_wins = int(soup.select_one('table > tbody > tr:nth-child(5) > td:nth-child(5)').get_text().replace(',', ''))
    sixth_wins = int(soup.select_one('table > tbody > tr:nth-child(6) > td:nth-child(5)').get_text().replace(',', ''))
    seventh_wins = int(soup.select_one('table > tbody > tr:nth-child(7) > td:nth-child(5)').get_text().replace(',', ''))
    bonus_wins = int(soup.select_one('table > tbody > tr:nth-child(8) > td:nth-child(6)').get_text())
    
    bonuses = soup.select('div.win720_num')[1].get_text().strip().split('\n')
    del bonuses[0:3]
    bonuses = [int(i) for i in bonuses]
    bonus1 = bonuses[0]
    bonus2 = bonuses[1]
    bonus3 = bonuses[2]
    bonus4 = bonuses[3]
    bonus5 = bonuses[4]
    bonus6 = bonuses[5]

    pens_nums = [count, date, fam, num1, num2, num3, num4, num5, num6, wins, bonus1, bonus2, bonus3, bonus4, bonus5, bonus6,
                 second_wins, third_wins, fourth_wins, fifth_wins, sixth_wins, seventh_wins, bonus_wins]

    return pens_nums

def loop_pens_nums():
    cursor, table_name = create_table('mugshot', 'pens_nums')

    for i in tqdm(range(1, get_latest('drwNo720') + 1)):
        pens_nums = get_pens_nums(i)        
            
        sql_insert = f"insert into {table_name}(round, date, fam, num1, num2, num3, num4, num5, num6, wins, bonus1, bonus2, bonus3, bonus4, \
                      bonus5, bonus6, second_wins, third_wins, fourth_wins, fifth_wins, sixth_wins, seventh_wins, bonus_wins) \
                      values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    
        cursor.execute(sql_insert, pens_nums)

    print(f'{get_latest('drwNo720')}회차까지 연금복권 번호 관련 정보를 DB에 저장했습니다')    

# loop_pens_nums()

def get_pens_shop(pick_round):
    url = f'https://www.dhlottery.co.kr/store.do?method=topStore&pageGubun=L720&drwNo={pick_round}'
    count, trs = get_count_date_trs(url, pick_round)

    pens_shop = []
    
    for tr in trs:
        if '조회' not in tr.select('td')[0].text.strip() :
            temp_data = []        
            shop = tr.select('td')[1].text.strip() 

            if shop != '인터넷 복권판매사이트' : # 매장명이 '인터넷 복권판매사이트'가 아닌 경우 모든 항목을 그대로 처리
                addr = tr.select('td')[2].text.strip() 
                addr = addr.split() # 로또 매장과 광역지자체명 표기를 통일하기 위해 문자열을 공백을 기준으로 분리해 리스트화

                if addr[0][0] == '광': # 광역지자체명이 '광주광역시'일 경우에만 연결된 '광역시'라는 문자열을 제거
                    addr[0] = addr[0].replace('광역시', '')
    
                else:
                    addr[0] = addr[0].translate({ord(char) : None for char in '특별시광역시도라청상'})

                addr = ' '.join(addr) # 리스트를 다시 문자열로 변환                                
                prov = addr.split()[0] # 전체 주소에서 광역지자체만 추출
                city = addr.split()[0:2] # 전체 주소에서 광역지자체 + 시/구만 추출
                city = ' '.join(city) # 광역지자체 + 시/구 추출 후 다시 공백 기준으로 합치기

                temp_data.append(count)
                temp_data.append(shop)                
                temp_data.append(prov)
                temp_data.append(city)
                temp_data.append(addr)

                pens_shop.append(temp_data)
                
            else : # 매장명이 '인터넷 복권판매사이트'인 경우 주소를 '-'로 처리
                prov = '-'
                city = '-'
                addr = '-'

                temp_data.append(count)
                temp_data.append(shop)                
                temp_data.append(prov)
                temp_data.append(city)
                temp_data.append(addr)

                pens_shop.append(temp_data)

        else : 
            pass

    return pens_shop

def loop_pens_shop():
    cursor, table_name = create_table('mugshot', 'pens_shop')

    for i in tqdm(range(1, get_latest('drwNo720') + 1)):
        pens_shop = get_pens_shop(i)        

        sql_insert = f"insert into {table_name}(round, shop, prov, city, addr) values (%s, %s, %s, %s, %s)"
        cursor.executemany(sql_insert, pens_shop)

    print(f'{get_latest('drwNo720')}회차까지 연금복권 매장 관련 정보를 DB에 저장했습니다.') 

# loop_pens_shop()

# DB의 로또 정보 체크
def check_lotto(): 
    con, cursor = con_db('mugshot')
    last_round = cursor.execute("select round from lotto_nums") 

    print(f"mugshot DB의 lotto_nums 테이블에 저장된 로또 마지막 회차는 {last_round} 회차입니다.")    

    latest_round = get_latest()

    if last_round == latest_round :
        print(f"현재 로또 번호 및 매장 관련 정보는 가장 최근인 {latest_round} 회차까지 반영되어 있습니다.")
        
        cursor.close()
        con.close()

    else: 
        print(f"현재 로또 번호 및 매장 관련 정보는 가장 최근인 {latest_round} 회차까지 반영되어 있지 않아 업데이트합니다.")
        
        update_lotto(cursor, last_round, latest_round)
        
        cursor.close()
        con.close()

# DB의 로또 정보 업데이트
def update_lotto(cursor, last_round, latest_round) :
    for i in tqdm(range(last_round + 1, latest_round + 1)):
        lotto_nums = get_lotto_nums(i)
        lotto_mode = get_lotto_mode(i)
        merged = lotto_nums + lotto_mode 
        
        lotto_shop = get_lotto_shop(i)
            
        sql_insert = f"insert into lotto_nums(round, date, num1, num2, num3, num4, num5, num6, wins, money, bonus, second_wins, second_money, third_wins,\
                      third_money, fourth_wins, fourth_money, fifth_wins, fifth_money, auto, hand, semi) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,\
                      %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    
        cursor.execute(sql_insert, (merged))

        sql_insert = f"insert into lotto_shop(round, shop, mode, prov, city, addr) values (%s, %s, %s, %s, %s, %s)"
        
        cursor.executemany(sql_insert, lotto_shop)        
    
    print(f"{latest_round}회차까지 로또 번호 및 매장 관련 정보를 업데이트 했습니다.")

# DB의 연금복권 정보 체크
def check_pens(): 
    con, cursor = con_db('mugshot')
    last_round = cursor.execute("select round from pens_nums") 

    print(f"mugshot DB의 pens_nums 테이블에 저장된 연금복권 마지막 회차는 {last_round} 회차입니다.")

    latest_round = get_latest()

    if last_round == latest_round :
        print(f"현재 연금복권 번호 및 매장 관련 정보는 가장 최근인 {latest_round} 회차까지 반영되어 있습니다.")
        
        cursor.close()
        con.close()

    else: 
        print(f"현재 연금복권 번호 및 매장 관련 정보는 가장 최근인 {latest_round} 회차까지 반영되어 있지 않아 업데이트합니다.")
        
        update_pens(cursor, last_round, latest_round)
        
        cursor.close()
        con.close()

# DB의 연금복권 정보 업데이트
def update_pens(cursor, last_round, latest_round) :
    for i in tqdm(range(last_round + 1, latest_round + 1)):
        pens_nums = get_pens_nums(i)
        pens_shop = get_pens_shop(i)
            
        sql_insert = f"insert into pens_nums(round, date, fam, num1, num2, num3, num4, num5, num6, wins, bonus1, bonus2, bonus3, bonus4, \
                      bonus5, bonus6, second_wins, third_wins, fourth_wins, fifth_wins, sixth_wins, seventh_wins, bonus_wins) \
                      values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    
        cursor.execute(sql_insert, pens_nums)

        sql_insert = f"insert into pens_shop(round, shop, prov, city, addr) values (%s, %s, %s, %s, %s)"
        
        cursor.executemany(sql_insert, pens_shop)     
    
    print(f"{latest_round}회차까지 로또 번호 및 매장 관련 정보를 업데이트 했습니다.")

if __name__ == '__main__':
    check_lotto()
    check_pens()