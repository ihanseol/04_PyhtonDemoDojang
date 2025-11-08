import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


def detect_skew_angle(image):
    """이미지의 기울기 각도를 감지합니다."""
    # 그레이스케일 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 이진화 (Otsu's method)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # 노이즈 제거
    kernel = np.ones((3, 3), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    # 윤곽선 검출
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 각도 리스트
    angles = []

    # 각 윤곽선의 최소 회전 사각형 계산
    for contour in contours:
        area = cv2.contourArea(contour)
        # 너무 작은 영역은 무시
        if area < 100:
            continue

        rect = cv2.minAreaRect(contour)
        angle = rect[2]

        # OpenCV의 minAreaRect는 -90 ~ 0 범위로 각도를 반환
        # 이를 -45 ~ 45 범위로 정규화
        if angle < -45:
            angle = 90 + angle

        angles.append(angle)

    # 중앙값을 사용하여 더 안정적인 각도 계산
    if angles:
        median_angle = np.median(angles)
        return median_angle

    return 0


def rotate_image(image, angle):
    """이미지를 주어진 각도만큼 회전합니다."""
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


def deskew_image(input_path, output_path=None, show_result=True):
    """
    이미지의 기울기를 자동으로 보정합니다.

    Args:
        input_path: 입력 이미지 경로
        output_path: 출력 이미지 경로 (None이면 자동 생성)
        show_result: 결과를 화면에 표시할지 여부

    Returns:
        보정된 이미지, 감지된 각도
    """
    # 이미지 로드
    image = cv2.imread(input_path)

    if image is None:
        raise ValueError(f"이미지를 불러올 수 없습니다: {input_path}")

    print(f"원본 이미지 크기: {image.shape[1]} x {image.shape[0]}")

    # 기울기 각도 감지
    angle = detect_skew_angle(image)
    print(f"감지된 기울기 각도: {angle:.2f}도")

    # 이미지 회전
    deskewed = rotate_image(image, angle)
    print(f"보정된 이미지 크기: {deskewed.shape[1]} x {deskewed.shape[0]}")

    # 출력 경로 설정
    if output_path is None:
        import os
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_deskewed{ext}"

    # 이미지 저장
    cv2.imwrite(output_path, deskewed)
    print(f"보정된 이미지 저장 완료: {output_path}")

    # 결과 표시
    if show_result:
        fig, axes = plt.subplots(1, 2, figsize=(15, 8))

        # 원본 이미지
        axes[0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        axes[0].set_title(f'원본 이미지\n(기울기: {angle:.2f}도)', fontsize=12)
        axes[0].axis('off')

        # 보정된 이미지
        axes[1].imshow(cv2.cvtColor(deskewed, cv2.COLOR_BGR2RGB))
        axes[1].set_title('보정된 이미지', fontsize=12)
        axes[1].axis('off')

        plt.tight_layout()
        plt.show()

    return deskewed, angle


# 사용 예시
if __name__ == "__main__":
    # 이미지 파일 경로 지정
    input_image = r"d:\05_Send\image-1.jpg"  # 입력 이미지 경로
    output_image = "output_deskewed.jpg"  # 출력 이미지 경로

    try:
        # 기울기 보정 실행
        deskewed_img, detected_angle = deskew_image(
            input_path=input_image,
            output_path=output_image,
            show_result=True
        )

        print("\n보정 완료!")

    except Exception as e:
        print(f"오류 발생: {e}")
        print("\n사용법:")
        print("1. 'input.jpg' 파일명을 실제 이미지 경로로 변경하세요")
        print("2. 필요한 라이브러리 설치: pip install opencv-python numpy pillow matplotlib")