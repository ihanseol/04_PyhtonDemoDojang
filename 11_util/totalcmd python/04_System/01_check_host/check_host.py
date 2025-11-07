import os
import sys

# Windows hosts 파일 경로
HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"


def read_hosts_file(path):
    """hosts 파일을 읽고 유효한 엔트리만 반환"""
    entries = []

    if not os.path.exists(path):
        print(f"오류: hosts 파일을 찾을 수 없습니다: {path}")
        return entries

    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()

                # 빈 줄 또는 주석은 무시
                if not line or line.startswith('#'):
                    continue

                # 주석이 중간에 있는 경우 제거 (예: 192.168.1.1 example.com # comment)
                if '#' in line:
                    line = line.split('#', 1)[0].strip()
                    if not line:
                        continue

                # 공백 기준으로 분리
                parts = line.split()
                if len(parts) < 2:
                    continue  # IP와 호스트명이 없으면 무시

                ip = parts[0]
                hostname = parts[1]

                # IP가 0.0.0.0 또는 127.0.0.1이 아닌 경우만 저장
                if ip not in ('0.0.0.0', '127.0.0.1'):
                    entries.append({
                        'line': line_num,
                        'ip': ip,
                        'hostname': hostname,
                        'original': line
                    })

    except PermissionError:
        print("오류: hosts 파일을 읽기 위해 관리자 권한이 필요합니다.")
        print("이 스크립트를 '관리자 권한으로 실행'하세요.")
        sys.exit(1)
    except Exception as e:
        print(f"파일 읽기 중 오류 발생: {e}")
        sys.exit(1)

    return entries


def main():
    print(f"hosts 파일 읽는 중: {HOSTS_PATH}\n")

    entries = read_hosts_file(HOSTS_PATH)

    if not entries:
        print("조건에 맞는 엔트리가 없습니다. (0.0.0.0, 127.0.0.1을 제외한 DNS 엔트리)")
        return

    print(f"총 {len(entries)}개의 외부 DNS 엔트리 발견:\n")
    print("-" * 60)
    for entry in entries:
        print(f"[{entry['line']:3d}행] {entry['ip']:15} → {entry['hostname']}")
        print(f"     원본: {entry['original']}")
        print()
    print("-" * 60)


if __name__ == "__main__":
    main()