import re

# (괄호 & 괄호 안 내용을 제외한) 조사 바로 앞 글자에 종성, 즉 받침이 있는지 확인
def has_coda(char):
    regex = r'\([^)]*\)' # 괄호가 있을 경우 괄호와 괄호 안의 내용 삭제를 위해 변수 정의
    char = re.sub(pattern = regex, repl='', string = char) # 매개변수로 넘어온 문자열 안에 있는 괄호와 그 내용 삭제
    return (ord(char[-1]) - 44032) % 28 == 0 # 종성이 없으면 True, 있으면 False 리턴

# 조사 바로 앞 글자의 종성이 'ㄹ'인지 확인
def coda_reul(char):
    regex = r'\([^)]*\)'
    char = re.sub(pattern = regex, repl='', string = char)
    return (ord(char[-1]) - 44032) % 28 == 8 # 종성이 'ㄹ'이면 True, 아니면 False 리턴

# 받침 유무에 따라 조사를 다르게 표기하되 조사만 표기. 근데 이걸 굳이 '조사만 VS 단어와 조사 모두 표기'로 나눌 필요가 있을까?
# 애초에 이걸 왜 나누게 됐는지부터 생각해봐야 겠다.
def eun_neun(char):
    return '는' if has_coda(char) else '은'

def yi_ga(char):
    return '가' if has_coda(char) else '이'

def eul_reul(char):
    return '를' if has_coda(char) else '을'

def wa_gwa(char):
    return '와' if has_coda(char) else '과'

def ro_euro(char): # 받침이 'ㄹ'인지를 확인해 'ㄹ'일때도 '로'로 표기
    return '로' if has_coda(char) or coda_reul(char) else '으로'

# 받침 유무에 따라 조사를 다르게 표기하되 해당 단어와 조사를 모두 표기
def eun_plus(char):
    return char + ('는' if has_coda(char) else '은')

def yi_plus(char):
    return char + ('가' if has_coda(char) else '이')

def eul_plus(char):
    return char + ('를' if has_coda(char) else '을')

def wa_plus(char):
    return char + ('와' if has_coda(char) else '과')

def ro_plus(char): # 받침이 'ㄹ'인지를 확인해 'ㄹ'일때도 '로'로 표기
    return char + ('로' if has_coda(char) or coda_reul(char) else '으로')

# 받침 유무에 따라 어미를 다르게 표기하되 어미만 표기
def da(char):
    return '다.' if has_coda(char) else '이다.'

def myeo(char):
    return '며' if has_coda(char) else '이며'

def myeon(char):
    return '면' if has_coda(char) else '이면'

# 받침 유무에 따라 해당 단어와 어미를 모두 표기
def da_plus(char):
    return char + ('다.' if has_coda(char) else '이다.')

def myeo_plus(char):
    return char + ('며' if has_coda(char) else '이며')

def myeon_plus(char):
    return char + ('면' if has_coda(char) else '이면')

if __name__ == '__main__':
    has_coda(char)
    coda_reul(char)
    eun_neun(char)
    yi_ga(char)
    eul_reul(char)
    wa_gwa(char)
    ro_euro(char)
    yi_plus(char)
    eun_plus(char)
    eul_plus(char)
    wa_plus(char)
    ro_plus(char)
    da(char)
    myeo(char)
    myeon(char)
    da_plus(char)
    myeo_plus(char)
    myeon_plus(char)   