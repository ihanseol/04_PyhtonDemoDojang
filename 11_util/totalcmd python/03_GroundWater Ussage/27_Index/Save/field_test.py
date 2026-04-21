import time
import sys
import glob
import os
import shutil
from pyhwpx import Hwp
from pathlib import Path

TOC_TARGETS = [
    "영향조사 결과의 요약",
    "지하수 이용방안",
    "조사서 작성에 관한 사항",
    "II. 수문지질현황 및 원수의 개발가능량",
    "2. 조사지역의 지하수 함양량, 개발가능량 조사",
    "3. 신규 지하수 개발가능량 산정",
    "III. 적정취수량 및 영향범위 산정",
    "2. 적정취수량과 영향반경",
    "3. 잠재오염원과 영향범위",
    "4. 지하수의 개발로 인하여 주변지역에 미치는 영향의 범위 및 정도",
    "IV. 수질의 적정성 평가",
    "Ⅴ. 시설설치계획",
    "2. 사후 관리방안",
    "<  참 고 문 헌  >",
    "<  부    록  >"
]

hwp = Hwp()
hwp.open(r"d:\06_Send2\목차.hwp")

field_list = [i for i in hwp.get_field_list(0, 0x02).split("\x02")]
print(len(field_list), field_list)
# hwp.MoveToField("i1{{0}}")
# hwp.MoveToField("i2{{0}}")
hwp.MoveToField("i4{{0}}")
hwp.MoveToField("i4{{1}}")






