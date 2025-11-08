import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os
from pathlib import Path


def detect_skew_angle_hough(image):
    """Hough 변환을 사용하여 기울기 각도를 감지합니다."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 엣지 검출
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Hough 라인 변환
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)

    if lines is None:
        return None

    angles = []
    for line in lines:
        rho, theta = line[0]
        angle = np.degrees(theta) - 90

        # 거의 수평이거나 수직인 선만 고려 (-45 ~ 45도)
        if -45 < angle < 45:
            angles.append(angle)

    if angles:
        return np.median(angles)

    return None


def detect_skew_angle_projection(image):
    """투영 프로파일을 사용하여 기울기를 감지합니다."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 이진화
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # 여러 각도에서 수평 투영 계산
    best_angle = 0
    max_variance = 0

    # -10도에서 +10도까지 0.1도 단위로 테스트
    for angle in np.arange(-10, 10, 0.1):
        # 이미지 회전
        h, w = binary.shape
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(binary, M, (w, h), flags=cv2.INTER_CUBIC)

        # 수평 투영 (각 행의 픽셀 합)
        h_proj = np.sum(rotated, axis=1)

        # 분산 계산 (올바른 각도에서 분산이 최대)
        variance = np.var(h_proj)

        if variance > max_variance:
            max_variance = variance
            best_angle = angle

    return best_angle


def detect_skew_angle_morphology(image):
    """형태학적 연산을 사용한 기울기 감지"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 이진화
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # 수평선 강조를 위한 형태학적 연산
    kernel_h = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
    horizontal = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel_h)

    # 라인 검출
    lines = cv2.HoughLinesP(horizontal, 1, np.pi / 180, 100,
                            minLineLength=100, maxLineGap=10)

    if lines is None:
        return None

    angles = []
    for line in lines:
        x1, y1, x2, y2 = line[0]

        # 거의 수평인 선만 고려
        if abs(y2 - y1) < 50:  # y 차이가 작은 선
            angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))

            # -45 ~ 45도 범위로 정규화
            if angle < -45:
                angle += 90
            elif angle > 45:
                angle -= 90

            angles.append(angle)

    if angles:
        # 이상치 제거 (중앙값에서 너무 먼 값 제거)
        median = np.median(angles)
        std = np.std(angles)
        filtered = [a for a in angles if abs(a - median) < 2 * std]

        if filtered:
            return np.median(filtered)

    return None


def detect_skew_angle_combined(image):
    """여러 방법을 조합하여 더 정확한 기울기 각도를 감지합니다."""
    angles = []

    # 방법 1: Hough 변환
    try:
        angle1 = detect_skew_angle_hough(image)
        if angle1 is not None:
            angles.append(angle1)
    except:
        pass

    # 방법 2: 투영 프로파일
    try:
        angle2 = detect_skew_angle_projection(image)
        if angle2 is not None:
            angles.append(angle2)
    except:
        pass

    # 방법 3: 형태학적 연산
    try:
        angle3 = detect_skew_angle_morphology(image)
        if angle3 is not None:
            angles.append(angle3)
    except:
        pass

    if not angles:
        return 0

    # 중앙값 사용 (이상치에 강건)
    final_angle = np.median(angles)

    return final_angle


def rotate_image(image, angle):
    """이미지를 주어진 각도만큼 회전합니다."""
    if abs(angle) < 0.01:  # 각도가 거의 0이면 원본 반환
        return image

    height, width = image.shape[:2]
    center = (width // 2, height // 2)

    # 회전 행렬 생성
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

    # 회전 후 이미지가 잘리지 않도록 새로운 크기 계산
    cos = np.abs(rotation_matrix[0, 0])
    sin = np.abs(rotation_matrix[0, 1])

    new_width = int((height * sin) + (width * cos))
    new_height = int((height * cos) + (width * sin))

    # 회전 행렬의 이동 부분 조정
    rotation_matrix[0, 2] += (new_width / 2) - center[0]
    rotation_matrix[1, 2] += (new_height / 2) - center[1]

    # 이미지 회전
    rotated = cv2.warpAffine(image, rotation_matrix, (new_width, new_height),
                             flags=cv2.INTER_CUBIC,
                             borderMode=cv2.BORDER_CONSTANT,
                             borderValue=(255, 255, 255))

    return rotated


def auto_crop_white_border(image, threshold=250):
    """흰색 여백을 자동으로 제거합니다."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 흰색이 아닌 영역 찾기
    _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY_INV)

    # 컨텐츠가 있는 영역 찾기
    coords = cv2.findNonZero(binary)

    if coords is not None:
        x, y, w, h = cv2.boundingRect(coords)
        # 약간의 여백 추가
        margin = 20
        x = max(0, x - margin)
        y = max(0, y - margin)
        w = min(image.shape[1] - x, w + 2 * margin)
        h = min(image.shape[0] - y, h + 2 * margin)

        return image[y:y + h, x:x + w]

    return image


def deskew_image(input_path, output_path, auto_crop=True):
    """
    이미지의 기울기를 자동으로 보정합니다.

    Args:
        input_path: 입력 이미지 경로
        output_path: 출력 이미지 경로
        auto_crop: 여백 자동 제거 여부

    Returns:
        성공 여부, 감지된 각도
    """
    try:
        # 이미지 로드
        image = cv2.imread(input_path)

        if image is None:
            print(f"  ✗ 이미지를 불러올 수 없습니다: {input_path}")
            return False, 0

        # 기울기 각도 감지
        angle = detect_skew_angle_combined(image)

        # 이미지 회전
        deskewed = rotate_image(image, angle)

        # 여백 자동 제거
        if auto_crop:
            deskewed = auto_crop_white_border(deskewed)

        # 이미지 저장
        cv2.imwrite(output_path, deskewed)

        return True, angle

    except Exception as e:
        print(f"  ✗ 처리 중 오류 발생: {e}")
        return False, 0


def process_folder(input_folder, output_prefix="output_"):
    """
    폴더 내 모든 이미지 파일을 처리합니다.

    Args:
        input_folder: 입력 폴더 경로

        output_prefix: 출력 파일 접두사
    """
    # 입력 폴더 확인
    input_path = Path(input_folder)

    if not input_path.exists():
        print(f"✗ 입력 폴더가 존재하지 않습니다: {input_folder}")
        return

    # 지원하는 이미지 확장자
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}

    # 이미지 파일 찾기 (중복 제거를 위해 set 사용)
    image_files = set()
    for ext in image_extensions:
        image_files.update(input_path.glob(f'*{ext}'))
        image_files.update(input_path.glob(f'*{ext.upper()}'))

    # set을 list로 변환하고 정렬
    image_files = sorted(list(image_files))

    if not image_files:
        print(f"✗ 이미지 파일을 찾을 수 없습니다: {input_folder}")
        return

    print(f"\n{'=' * 60}")
    print(f"이미지 기울기 자동 보정 프로그램")
    print(f"{'=' * 60}")
    print(f"입력 폴더: {input_folder}")
    print(f"출력 접두사: {output_prefix}")
    print(f"발견된 이미지: {len(image_files)}개")
    print(f"{'=' * 60}\n")

    # 통계
    success_count = 0
    fail_count = 0

    # 각 이미지 처리
    for i, input_file in enumerate(image_files, 1):
        filename = input_file.name
        output_filename = output_prefix + filename
        output_path = input_path / output_filename

        print(f"[{i}/{len(image_files)}] 처리 중: {filename}")

        success, angle = deskew_image(str(input_file), str(output_path))

        if success:
            print(f"  ✓ 완료 (각도: {angle:.2f}°) → {output_filename}")
            success_count += 1
        else:
            print(f"  ✗ 실패")
            fail_count += 1

        print()

    # 결과 요약
    print(f"{'=' * 60}")
    print(f"처리 완료!")
    print(f"{'=' * 60}")
    print(f"성공: {success_count}개")
    print(f"실패: {fail_count}개")
    print(f"전체: {len(image_files)}개")
    print(f"{'=' * 60}\n")


# 메인 실행
if __name__ == "__main__":
    # 입력 폴더 설정
    INPUT_FOLDER = r"d:\05_Send"
    OUTPUT_PREFIX = "output_"

    # 폴더 내 모든 이미지 처리
    process_folder(INPUT_FOLDER, OUTPUT_PREFIX)

    print("프로그램이 종료되었습니다.")
    input("엔터를 눌러 종료...")