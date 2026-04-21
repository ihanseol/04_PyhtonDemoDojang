import time
import sys


def progress_bar(iteration, total, prefix='', suffix='', length=30, fill='█'):
    percent = f"{100 * (iteration / float(total)):.1f}"
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    # \r를 사용하여 커서를 줄 시작으로 이동
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')
    sys.stdout.flush()


# 사용 예시
items = list(range(0, 50))
l = len(items)

for i, item in enumerate(items):
    time.sleep(0.1)
    progress_bar(i + 1, l, prefix='Progress:', suffix='Complete', length=50)
print()  # 종료 후 줄바꿈
