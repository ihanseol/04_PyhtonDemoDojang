"""
파란 동그라미 번호 매기기 스크립트
=====================================
- 입력 : d:\05_Send\*.jpg
- 처리 : 하늘색 영향반경 원 안에 있는 파란 동그라미를 자동 감지 → 번호 표시
- 출력 : 원본파일명_numbered.jpg (같은 폴더에 저장)

필요 라이브러리 설치 (최초 1회):
  pip install opencv-python numpy

  by claude, sonet 4.6
  2026/4/20
"""

import cv2
import numpy as np
import glob
import os


def find_large_circle(image):
    """이미지에서 하늘색 영향반경 큰 원의 중심·반지름 반환"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(
        gray, cv2.HOUGH_GRADIENT, dp=2,
        minDist=image.shape[0] // 2,
        param1=30, param2=30,
        minRadius=int(min(image.shape[:2]) * 0.25),
        maxRadius=int(min(image.shape[:2]) * 0.70),
    )
    if circles is not None:
        circles = np.round(circles[0]).astype(int)
        h, w = image.shape[:2]
        best = min(circles, key=lambda c: (c[0] - w/2)**2 + (c[1] - h/2)**2)
        return int(best[0]), int(best[1]), int(best[2])
    h, w = image.shape[:2]
    return w // 2, h // 2, min(h, w) // 2


def find_blue_circles_inside(image, cx, cy, radius):
    """영향반경 원 안에 있는 파란 마커 목록 반환"""
    b, g, r = cv2.split(image)
    mask = (
        (b.astype(int) > g.astype(int) + 20) &
        (b.astype(int) > r.astype(int) + 30) &
        (b > 100)
    ).astype(np.uint8) * 255

    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    circles = []
    seen = []

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 25 or area > 4000:
            continue
        perimeter = cv2.arcLength(cnt, True)
        if perimeter == 0:
            continue
        circularity = 4 * np.pi * area / (perimeter ** 2)
        if circularity < 0.40:
            continue
        M = cv2.moments(cnt)
        if M["m00"] == 0:
            continue
        x = int(M["m10"] / M["m00"])
        y = int(M["m01"] / M["m00"])
        rr = max(4, int(np.sqrt(area / np.pi)))

        if np.sqrt((x - cx)**2 + (y - cy)**2) > radius * 1.03:
            continue
        if any(np.sqrt((x-ex)**2 + (y-ey)**2) < 18 for ex, ey in seen):
            continue

        circles.append((x, y, rr))
        seen.append((x, y))

    circles.sort(key=lambda c: (c[1] // 30, c[0]))
    return circles


def draw_numbers(image, circles):
    result = image.copy()
    font = cv2.FONT_HERSHEY_SIMPLEX

    for i, (x, y, rr) in enumerate(circles, 1):
        text = str(i)
        font_scale = max(0.22, rr * 0.085)
        thickness = max(1, rr // 7)
        (tw, th), _ = cv2.getTextSize(text, font, font_scale, thickness)
        while (tw > rr * 1.9 or th > rr * 1.6) and font_scale > 0.15:
            font_scale -= 0.02
            (tw, th), _ = cv2.getTextSize(text, font, font_scale, thickness)
        tx, ty = x - tw // 2, y + th // 2
        cv2.putText(result, text, (tx, ty), font, font_scale, (255,255,255), thickness+2, cv2.LINE_AA)
        cv2.putText(result, text, (tx, ty), font, font_scale, (10,10,10), thickness, cv2.LINE_AA)

    count_text = f"Total: {len(circles)}"
    h, w = result.shape[:2]
    cv2.putText(result, count_text, (w-240, 50), font, 1.3, (255,255,255), 6, cv2.LINE_AA)
    cv2.putText(result, count_text, (w-240, 50), font, 1.3, (0,80,220), 2, cv2.LINE_AA)
    return result


def process_file(filepath):
    image = cv2.imread(filepath)
    if image is None:
        print(f"  ERROR 읽기 실패: {filepath}")
        return None
    cx, cy, r = find_large_circle(image)
    circles = find_blue_circles_inside(image, cx, cy, r)
    result = draw_numbers(image, circles)
    base, ext = os.path.splitext(filepath)
    out_path = base + "_numbered" + ext
    cv2.imwrite(out_path, result)
    print(f"  OK {os.path.basename(filepath)} -> {len(circles)}개 -> {os.path.basename(out_path)}")
    return len(circles)


def main():
    input_pattern = r"d:\05_Send\*.jpg"
    files = sorted(glob.glob(input_pattern))
    if not files:
        print(f"파일 없음: {input_pattern}")
        return

    print(f"총 {len(files)}개 파일 처리 시작")
    print("=" * 50)
    summary = []
    for fp in files:
        n = process_file(fp)
        if n is not None:
            summary.append((os.path.basename(fp), n))

    print("\n" + "=" * 50)
    print("[ 처리 완료 요약 ]")
    for fname, count in summary:
        print(f"  {fname:35s}  ->  {count:3d}개")
    total = sum(c for _, c in summary)
    print(f"\n  파일 {len(summary)}개  /  전체 동그라미 {total}개")


if __name__ == "__main__":
    main()