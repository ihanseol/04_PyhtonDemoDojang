from pick import pick

from CLASS_AqtWork import AqtProjectInfoInjector
from CLASS_AqtWork import AqtExcelProjectInfoInjector


def process_yangsoo_spec():
    injector = AqtProjectInfoInjector("d:\\05_Send\\", "산수개발(주)")
    injector.Set_Projectinfo("산수개발(주)", "AAA" )


def main():
    title = 'Please choose your Company: '
    options = ['SanSu', 'DaeWoong', 'WooKyung', 'HanIL', 'DongHae', 'HyunYoon', 'JunIL', 'BuYeo', 'TaeYang', 'SamWon',
               'MainGeo']
    my_company = ["산수개발(주)", "대웅엔지니어링 주식회사", "(주) 우경엔지니어링", "주식회사 한일지하수", "(주)동해엔지니어링", "(주)현윤이앤씨", "(주) 전일",
                  "부여지하수개발 주식회사", "(주)태양이엔지", "삼원개발(주)", "마인지오 주식회사"]

    option, index = pick(options, title, indicator='==>', default_index=1)
    company = my_company[index]
    print(option, index, company)

    injector = AqtExcelProjectInfoInjector("d:\\05_Send\\", company)
    injector.process_projectinfo_likesejong(company)


if __name__ == "__main__":
    # process_yangsoo_spec()
    main()
