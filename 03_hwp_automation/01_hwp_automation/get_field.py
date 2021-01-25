import re

# re.sub(r'[\w-]+@[\w.]+', 'great', 'test@gmail.com haha test2@gmail.com nice test test', count=1)
def extract_brace(s):
    pattern = r'\{{(\d{1}|\d{2})\}}'
    m = re.sub(pattern,'',s ,0)
    return m

# extract number only
# re.findall(r'\d+', 'hello 42 I\'m a 32 string 30')


def extract_number(s):
    return re.findall(r'\d+',s)[0]


def search(list, platform):
    for i in range(len(list)):
        if list[i] == platform:
            return True
    return False


def uniq_list(list):
    id = []
    for item in list:
        c = extract_brace(item)
        if not search(id, c):
            id.append(c)
    return id


def element_count(list, item):
    c=0
    pattern = re.compile(item)
    for i in list:
        if (pattern.search(i)): c+=1
    return c


def get_index_num(list_a):
    ret = {}
    uniq = uniq_list(list_a)
    for entity in uniq:
        cnt = element_count(list_a, entity)
        # print(f'{i} : {cnt}')
        ret[entity] = cnt

    return ret


if __name__ == '__main__':    # 프로그램의 시작점일 때만 아래 코드 실행
    list_a = ['title{{0}}', 'title{{1}}', 'title{{2}}', 'title{{3}}', 'spoint{{0}}', 'epoint{{0}}', 'title{{4}}',
              'title{{5}}', 'spoint{{1}}', 'epoint{{1}}', 'title{{6}}', 'title{{7}}', 'title{{8}}', 'title{{9}}',
              'title{{10}}', 'title{{11}}', 'title{{12}}', 'title{{13}}', 'title{{14}}']

    c = get_index_num(list_a)
    print(c)



























