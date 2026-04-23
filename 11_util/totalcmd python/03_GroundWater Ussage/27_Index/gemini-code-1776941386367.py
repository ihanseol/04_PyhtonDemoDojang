import sys
import glob
import os
import shutil
import time
import psutil
from pyhwpx import Hwp


class HwpTocManager:
    def __init__(self, source_dir, template_src, template_dest, toc_targets):
        self.source_dir = source_dir
        self.template_src = template_src
        self.template_dest = template_dest
        self.toc_targets = toc_targets

    @staticmethod
    def terminate_all_hwp():
        for proc in psutil.process_iter(['name']):
            try:
                if 'hwp' in proc.info['name'].lower():
                    proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

    @staticmethod
    def get_first_file(path, extension):
        pattern = os.path.join(path, f"*{extension}")
        files = glob.glob(pattern)
        for f in files:
            if os.path.isfile(f):
                return f
        return None

    @staticmethod
    def progress_bar(iteration, total, prefix='', suffix='', length=30, fill='█'):
        percent = f"{100 * (iteration / float(total)):.1f}"
        filled_length = int(length * iteration // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}   ')
        sys.stdout.flush()

    @staticmethod
    def copy_file(source, destination):
        try:
            shutil.copy2(source, destination)
            print(f"Success: {source} -> {destination}")
        except FileNotFoundError:
            print("Error: 원본 파일을 찾을 수 없습니다.")
        except PermissionError:
            print("Error: 권한이 없습니다.")
        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    def delete_insert_field(hwp):
        pset = hwp.HParameterSet.HDeleteCtrls
        hwp.HAction.GetDefault("DeleteCtrls", pset.HSet)
        pset.CreateItemArray("DeleteCtrlType", 1)
        pset.DeleteCtrlType.SetItem(0, 17)
        hwp.HAction.Execute("DeleteCtrls", pset.HSet)

    def get_pages_with_text_scan(self, hwp, search_text):
        pages = set()
        if not hwp.init_scan():
            return []
        try:
            while True:
                state, text = hwp.get_text()
                if state <= 1:
                    break

                if search_text in text:
                    hwp.move_pos(201)
                    page_no = hwp.KeyIndicator()[3]
                    pages.add(page_no)
            return sorted(list(pages))
        finally:
            hwp.release_scan()

    def extract_toc_pages(self, file_path):
        hwp = Hwp(visible=False)
        hwp.open(file_path)
        results = {}
        total = len(self.toc_targets)

        print(f"--- 파일 분석 시작: {file_path} ---")
        for i, target in enumerate(self.toc_targets):
            self.get_pages_with_text_scan(hwp, target)
            self.progress_bar(i + 1, total, prefix='Progress:', suffix='Complete', length=50)
            current_page = hwp.KeyIndicator()[3]
            results[target] = current_page

        hwp.quit()
        return results

    def make_duplicate_list(self, target_list):
        new_list = []
        target_indices = {4, 7, 11, 12}

        for i, data in enumerate(target_list, start=1):
            new_list.append(data)
            if i in target_indices:
                new_list.append(data)

        return new_list

    def write_table_of_contents(self, target_list):
        print("\n-- Enter write_table_of_contents(target_list) --", flush=True)

        hwp = Hwp(visible=False)
        hwp.open(self.template_dest)

        field_list = [i for i in hwp.get_field_list(0, 0x02).split("\x02")]
        new_list = self.make_duplicate_list(target_list)

        previous_field = "save_field"
        total_len = len(new_list)

        for i, (field, data) in enumerate(zip(field_list, new_list), 1):
            self.progress_bar(i, total_len, prefix='Progress:', suffix='Writing Data...', length=50)
            time.sleep(.05)
            suffix = "{{1}}" if field == previous_field else "{{0}}"
            field_tag = f"{field}{suffix}"

            hwp.MoveToField(field_tag)
            hwp.PutFieldText(field_tag, data)

            previous_field = field

        print()
        self.delete_insert_field(hwp)
        hwp.save()
        hwp.quit()

    def run(self):
        self.terminate_all_hwp()
        self.copy_file(self.template_src, self.template_dest)

        file_name = self.get_first_file(self.source_dir, "hwp")
        if not file_name:
            print(f"Error: {self.source_dir} 경로에 hwp 파일이 없습니다.")
            return

        toc_results = self.extract_toc_pages(file_name)

        print("\n--- 최종 목차 요약 ---")
        for text, pg in toc_results.items():
            print(f"{text}: {pg}")

        result_values = list(toc_results.values())
        self.write_table_of_contents(result_values)


if __name__ == "__main__":
    # 설정값 초기화
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
        "<  부   록  >"
    ]

    SOURCE_DIR = "d:\\05_Send"
    TEMPLATE_SRC = r"c:\Program Files\totalcmd\hwp\목차.hwp"
    TEMPLATE_DEST = r"d:\06_Send2\목차.hwp"

    # 인스턴스 생성 및 실행
    manager = HwpTocManager(SOURCE_DIR, TEMPLATE_SRC, TEMPLATE_DEST, TOC_TARGETS)
    manager.run()