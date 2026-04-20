// Types
export interface DetectedCircle {
  id: number;
  cx: number;
  cy: number;
  radius: number;
  pixelCount: number;
  insideInfluence?: boolean;
}

export interface InfluenceRadius {
  cx: number;
  cy: number;
  radius: number;
}

export interface ProcessResult {
  imageDataUrl: string;
  circles: DetectedCircle[];
  totalCount: number;
  insideCount: number;
  outsideCount: number;
  influenceRadius?: InfluenceRadius;
}

// Convert HSL to check if a pixel is "blue enough"
function isBluePixel(
  r: number,
  g: number,
  b: number,
  hueMin: number,
  hueMax: number,
  satMin: number,
  brightMin: number
): boolean {
  const rf = r / 255;
  const gf = g / 255;
  const bf = b / 255;
  const max = Math.max(rf, gf, bf);
  const min = Math.min(rf, gf, bf);
  const l = (max + min) / 2;
  const d = max - min;

  if (d === 0) return false; // achromatic

  const s = l > 0.5 ? d / (2 - max - min) : d / (max + min);

  let h: number;
  if (max === rf) {
    h = ((gf - bf) / d + (gf < bf ? 6 : 0)) / 6;
  } else if (max === gf) {
    h = ((bf - rf) / d + 2) / 6;
  } else {
    h = ((rf - gf) / d + 4) / 6;
  }

  const hueDeg = h * 360;

  const hueInRange = hueDeg >= hueMin && hueDeg <= hueMax;
  const satOk = s * 100 >= satMin;
  const brightOk = l * 100 >= brightMin && l * 100 <= 95;

  return hueInRange && satOk && brightOk;
}

// Connected component labeling using union-find
class UnionFind {
  parent: number[];
  rank: number[];

  constructor(n: number) {
    this.parent = Array.from({ length: n }, (_, i) => i);
    this.rank = new Array(n).fill(0);
  }

  find(x: number): number {
    if (this.parent[x] !== x) {
      this.parent[x] = this.find(this.parent[x]);
    }
    return this.parent[x];
  }

  union(x: number, y: number) {
    const rx = this.find(x);
    const ry = this.find(y);
    if (rx === ry) return;
    if (this.rank[rx] < this.rank[ry]) {
      this.parent[rx] = ry;
    } else if (this.rank[rx] > this.rank[ry]) {
      this.parent[ry] = rx;
    } else {
      this.parent[ry] = rx;
      this.rank[rx]++;
    }
  }
}

export interface DetectionParams {
  hueMin: number;
  hueMax: number;
  satMin: number;
  brightMin: number;
  minCirclePixels: number;
  maxCirclePixels: number;
  showLabelSize: 'small' | 'medium' | 'large';
  mergeOverlapRatio: number; // 0~1, how much overlap to consider as duplicate
}

export const defaultParams: DetectionParams = {
  hueMin: 190,
  hueMax: 260,
  satMin: 25,
  brightMin: 15,
  minCirclePixels: 10,
  maxCirclePixels: 100000,
  showLabelSize: 'small',
  mergeOverlapRatio: 0.4,
};

// Merge overlapping circles
function mergeOverlappingCircles(
  circles: DetectedCircle[],
  overlapRatio: number
): DetectedCircle[] {
  if (circles.length === 0) return circles;

  const merged: boolean[] = new Array(circles.length).fill(false);
  const result: DetectedCircle[] = [];

  // Sort by pixel count descending (keep larger circles)
  const sorted = circles.map((c, i) => ({ ...c, origIndex: i }));
  sorted.sort((a, b) => b.pixelCount - a.pixelCount);

  for (let i = 0; i < sorted.length; i++) {
    if (merged[sorted[i].origIndex]) continue;

    const current = { ...sorted[i] };
    let mergeCount = 1;

    for (let j = i + 1; j < sorted.length; j++) {
      if (merged[sorted[j].origIndex]) continue;

      const other = sorted[j];
      const dist = Math.sqrt(
        (current.cx - other.cx) ** 2 + (current.cy - other.cy) ** 2
      );
      const rSum = current.radius + other.radius;

      // If centers are very close relative to their sizes, merge them
      if (dist < rSum * overlapRatio) {
        // Weighted average position by pixel count
        const totalPixels = current.pixelCount + other.pixelCount;
        current.cx = Math.round(
          (current.cx * current.pixelCount + other.cx * other.pixelCount) /
            totalPixels
        );
        current.cy = Math.round(
          (current.cy * current.pixelCount + other.cy * other.pixelCount) /
            totalPixels
        );
        current.pixelCount = totalPixels;
        current.radius = Math.round(Math.sqrt(totalPixels / Math.PI));
        merged[other.origIndex] = true;
        mergeCount++;
      }
    }

    result.push(current);
  }

  return result;
}

export function processImage(
  img: HTMLImageElement,
  params: DetectionParams,
  influenceRadius?: InfluenceRadius
): ProcessResult {
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d')!;

  canvas.width = img.naturalWidth;
  canvas.height = img.naturalHeight;
  ctx.drawImage(img, 0, 0);

  const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
  const { data, width, height } = imageData;

  // Step 1: Create binary mask of blue pixels
  const mask = new Uint8Array(width * height);
  for (let i = 0; i < width * height; i++) {
    const r = data[i * 4];
    const g = data[i * 4 + 1];
    const b = data[i * 4 + 2];
    if (isBluePixel(r, g, b, params.hueMin, params.hueMax, params.satMin, params.brightMin)) {
      mask[i] = 1;
    }
  }

  // Step 2: Connected component labeling
  const labels = new Int32Array(width * height).fill(-1);
  const uf = new UnionFind(width * height);
  let nextLabel = 0;

  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      const idx = y * width + x;
      if (mask[idx] === 0) continue;

      const neighbors: number[] = [];
      if (x > 0 && mask[idx - 1] === 1) neighbors.push(idx - 1);
      if (y > 0 && mask[idx - width] === 1) neighbors.push(idx - width);

      if (neighbors.length === 0) {
        labels[idx] = nextLabel++;
      } else {
        const minLabel = Math.min(...neighbors.map((n) => labels[n]));
        labels[idx] = minLabel;
        for (const n of neighbors) {
          uf.union(minLabel, labels[n]);
        }
      }
    }
  }

  // Step 3: Resolve labels and group pixels
  const componentMap = new Map<number, { pixels: number[]; sumX: number; sumY: number }>();

  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      const idx = y * width + x;
      if (labels[idx] === -1) continue;
      const root = uf.find(labels[idx]);
      if (!componentMap.has(root)) {
        componentMap.set(root, { pixels: [], sumX: 0, sumY: 0 });
      }
      const comp = componentMap.get(root)!;
      comp.pixels.push(idx);
      comp.sumX += x;
      comp.sumY += y;
    }
  }

  // Step 4: Filter by size and create circles
  let circles: DetectedCircle[] = [];
  let id = 1;

  for (const [, comp] of componentMap) {
    if (
      comp.pixels.length >= params.minCirclePixels &&
      comp.pixels.length <= params.maxCirclePixels
    ) {
      const cx = Math.round(comp.sumX / comp.pixels.length);
      const cy = Math.round(comp.sumY / comp.pixels.length);
      const radius = Math.round(Math.sqrt(comp.pixels.length / Math.PI));

      // Check circularity
      let minX = width, maxX = 0, minY = height, maxY = 0;
      for (const p of comp.pixels) {
        const px = p % width;
        const py = Math.floor(p / width);
        if (px < minX) minX = px;
        if (px > maxX) maxX = px;
        if (py < minY) minY = py;
        if (py > maxY) maxY = py;
      }
      const bw = maxX - minX + 1;
      const bh = maxY - minY + 1;
      const aspectRatio = bw / bh;

      if (aspectRatio > 0.3 && aspectRatio < 3.0) {
        circles.push({
          id: id++,
          cx,
          cy,
          radius,
          pixelCount: comp.pixels.length,
        });
      }
    }
  }

  // Step 5: Merge overlapping/duplicate circles
  circles = mergeOverlappingCircles(circles, params.mergeOverlapRatio);

  // Step 6: Classify inside/outside influence radius
  let insideCount = 0;
  let outsideCount = 0;

  if (influenceRadius && influenceRadius.radius > 0) {
    for (const circle of circles) {
      const dist = Math.sqrt(
        (circle.cx - influenceRadius.cx) ** 2 +
        (circle.cy - influenceRadius.cy) ** 2
      );
      circle.insideInfluence = dist <= influenceRadius.radius;
      if (circle.insideInfluence) {
        insideCount++;
      } else {
        outsideCount++;
      }
    }
  } else {
    // No influence radius defined, all circles are "inside" (unclassified)
    insideCount = 0;
    outsideCount = circles.length;
  }

  // Sort circles: inside first (top-left to bottom-right), then outside
  circles.sort((a, b) => {
    // First sort by inside/outside
    if (a.insideInfluence !== b.insideInfluence) {
      return a.insideInfluence ? -1 : 1;
    }
    // Then by position
    const rowA = Math.floor(a.cy / (a.radius * 2 + 5));
    const rowB = Math.floor(b.cy / (b.radius * 2 + 5));
    if (rowA !== rowB) return rowA - rowB;
    return a.cx - b.cx;
  });

  // Re-assign IDs after sorting, with prefix for inside/outside
  let insideId = 1;
  let outsideId = 1;
  circles.forEach((c) => {
    if (c.insideInfluence) {
      c.id = insideId++;
    } else {
      c.id = outsideId++;
    }
  });

  // Step 7: Draw annotated image
  const outCanvas = document.createElement('canvas');
  outCanvas.width = img.naturalWidth;
  outCanvas.height = img.naturalHeight;
  const outCtx = outCanvas.getContext('2d')!;
  outCtx.drawImage(img, 0, 0);

  // Draw influence radius circle if defined
  if (influenceRadius && influenceRadius.radius > 0) {
    // Dashed yellow circle for influence radius
    outCtx.save();
    outCtx.strokeStyle = 'rgba(255, 200, 0, 0.9)';
    outCtx.lineWidth = Math.max(2, Math.round(img.naturalWidth / 400));
    outCtx.setLineDash([Math.max(8, Math.round(img.naturalWidth / 150)), Math.max(4, Math.round(img.naturalWidth / 300))]);
    outCtx.beginPath();
    outCtx.arc(influenceRadius.cx, influenceRadius.cy, influenceRadius.radius, 0, Math.PI * 2);
    outCtx.stroke();
    outCtx.restore();

    // Draw center crosshair
    const crossSize = Math.max(6, Math.round(img.naturalWidth / 200));
    outCtx.strokeStyle = 'rgba(255, 200, 0, 0.9)';
    outCtx.lineWidth = Math.max(1, Math.round(img.naturalWidth / 800));
    outCtx.setLineDash([]);
    outCtx.beginPath();
    outCtx.moveTo(influenceRadius.cx - crossSize, influenceRadius.cy);
    outCtx.lineTo(influenceRadius.cx + crossSize, influenceRadius.cy);
    outCtx.moveTo(influenceRadius.cx, influenceRadius.cy - crossSize);
    outCtx.lineTo(influenceRadius.cx, influenceRadius.cy + crossSize);
    outCtx.stroke();

    // Label the influence radius
    const irFontSize = Math.max(12, Math.round(img.naturalWidth / 80));
    outCtx.font = `bold ${irFontSize}px Arial, sans-serif`;
    outCtx.textAlign = 'center';
    outCtx.textBaseline = 'bottom';

    // Background for text
    const irText = `영향반경 (r=${Math.round(influenceRadius.radius)})`;
    const textMetrics = outCtx.measureText(irText);
    outCtx.fillStyle = 'rgba(0, 0, 0, 0.7)';
    outCtx.fillRect(
      influenceRadius.cx - textMetrics.width / 2 - 4,
      influenceRadius.cy - influenceRadius.radius - irFontSize - 8,
      textMetrics.width + 8,
      irFontSize + 6
    );
    outCtx.fillStyle = 'rgba(255, 200, 0, 1)';
    outCtx.fillText(
      irText,
      influenceRadius.cx,
      influenceRadius.cy - influenceRadius.radius - 4
    );
  }

  // Determine font size based on circle radius and label size preference
  const sizeMultiplier =
    params.showLabelSize === 'small' ? 0.6 : params.showLabelSize === 'medium' ? 0.8 : 1.0;

  for (const circle of circles) {
    const fontSize = Math.max(8, Math.round(circle.radius * sizeMultiplier));

    // Different labels for inside vs outside
    const prefix = circle.insideInfluence ? '●' : '○';
    const label = `${prefix}${circle.id}`;

    // Color: green for inside, orange for outside
    const bgColor = circle.insideInfluence
      ? 'rgba(0, 180, 80, 0.9)'
      : 'rgba(255, 140, 0, 0.9)';
    const borderColor = circle.insideInfluence
      ? 'rgba(0, 220, 100, 1)'
      : 'rgba(255, 180, 50, 1)';

    // Draw background circle for readability
    outCtx.fillStyle = bgColor;
    outCtx.beginPath();
    outCtx.arc(circle.cx, circle.cy, fontSize * 0.85, 0, Math.PI * 2);
    outCtx.fill();

    // Draw border
    outCtx.strokeStyle = borderColor;
    outCtx.lineWidth = Math.max(1, Math.round(fontSize * 0.12));
    outCtx.beginPath();
    outCtx.arc(circle.cx, circle.cy, fontSize * 0.85, 0, Math.PI * 2);
    outCtx.stroke();

    // Draw number
    outCtx.fillStyle = '#FFFFFF';
    outCtx.font = `bold ${fontSize}px Arial, sans-serif`;
    outCtx.textAlign = 'center';
    outCtx.textBaseline = 'middle';
    outCtx.fillText(label, circle.cx, circle.cy + 1);
  }

  // Draw summary info box at top-right
  if (influenceRadius && influenceRadius.radius > 0) {
    const boxFontSize = Math.max(14, Math.round(img.naturalWidth / 60));
    const lineHeight = boxFontSize * 1.5;
    const boxPadding = boxFontSize * 0.8;
    const boxWidth = boxFontSize * 16;
    const boxHeight = lineHeight * 4 + boxPadding * 2;
    const boxX = img.naturalWidth - boxWidth - 10;
    const boxY = 10;

    // Background
    outCtx.fillStyle = 'rgba(0, 0, 0, 0.8)';
    outCtx.roundRect(boxX, boxY, boxWidth, boxHeight, 8);
    outCtx.fill();
    outCtx.strokeStyle = 'rgba(255, 255, 255, 0.3)';
    outCtx.lineWidth = 1;
    outCtx.roundRect(boxX, boxY, boxWidth, boxHeight, 8);
    outCtx.stroke();

    outCtx.font = `bold ${boxFontSize}px Arial, sans-serif`;
    outCtx.textAlign = 'left';
    outCtx.textBaseline = 'top';

    let yPos = boxY + boxPadding;

    // Title
    outCtx.fillStyle = '#FFFFFF';
    outCtx.fillText('📊 감지 결과', boxX + boxPadding, yPos);
    yPos += lineHeight;

    // Inside count
    outCtx.fillStyle = 'rgba(0, 220, 100, 1)';
    outCtx.fillText(`영향반경 내부: ${insideCount}개`, boxX + boxPadding, yPos);
    yPos += lineHeight;

    // Outside count
    outCtx.fillStyle = 'rgba(255, 180, 50, 1)';
    outCtx.fillText(`영향반경 외부: ${outsideCount}개`, boxX + boxPadding, yPos);
    yPos += lineHeight;

    // Total
    outCtx.fillStyle = '#FFFFFF';
    outCtx.fillText(`총 합계: ${circles.length}개`, boxX + boxPadding, yPos);
  }

  return {
    imageDataUrl: outCanvas.toDataURL('image/png'),
    circles,
    totalCount: circles.length,
    insideCount,
    outsideCount,
    influenceRadius,
  };
}
