import { useState, useRef, useCallback, useEffect } from 'react';
import {
  processImage,
  defaultParams,
  type DetectionParams,
  type ProcessResult,
  type InfluenceRadius,
} from './imageProcessor';

interface ImageFile {
  file: File;
  name: string;
  preview: string;
}

type InfluenceMode = 'none' | 'setCenter' | 'setEdge';

function App() {
  const [images, setImages] = useState<ImageFile[]>([]);
  const [results, setResults] = useState<Map<string, ProcessResult>>(new Map());
  const [processing, setProcessing] = useState(false);
  const [currentImage, setCurrentImage] = useState<string | null>(null);
  const [params, setParams] = useState<DetectionParams>({ ...defaultParams });
  const [showParams, setShowParams] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [zoom, setZoom] = useState(1);
  const resultImageRef = useRef<HTMLImageElement>(null);

  // Influence radius state
  const [influenceMode, setInfluenceMode] = useState<InfluenceMode>('none');
  const [influenceCenter, setInfluenceCenter] = useState<{ x: number; y: number } | null>(null);
  const [influenceRadiusValue, setInfluenceRadiusValue] = useState<number>(0);
  const [showInfluenceInput, setShowInfluenceInput] = useState(false);
  const [manualCenter, setManualCenter] = useState({ x: 0, y: 0 });
  const [manualRadius, setManualRadius] = useState(0);
  const [showMergeInfo, setShowMergeInfo] = useState(false);

  // Temp influence radius for preview while setting
  const [tempInfluence, setTempInfluence] = useState<InfluenceRadius | undefined>(undefined);

  const getInfluenceRadius = (): InfluenceRadius | undefined => {
    if (influenceCenter && influenceRadiusValue > 0) {
      return { cx: influenceCenter.x, cy: influenceCenter.y, radius: influenceRadiusValue };
    }
    return undefined;
  };

  const totalCircles = Array.from(results.values()).reduce(
    (sum, r) => sum + r.totalCount,
    0
  );
  const totalInside = Array.from(results.values()).reduce(
    (sum, r) => sum + r.insideCount,
    0
  );
  const totalOutside = Array.from(results.values()).reduce(
    (sum, r) => sum + r.outsideCount,
    0
  );

  const handleFiles = useCallback(
    async (files: FileList | File[]) => {
      const newImages: ImageFile[] = [];
      for (const file of Array.from(files)) {
        if (file.type.startsWith('image/')) {
          newImages.push({
            file,
            name: file.name,
            preview: URL.createObjectURL(file),
          });
        }
      }
      if (newImages.length === 0) return;

      setImages((prev) => [...prev, ...newImages]);
      if (newImages.length > 0 && !currentImage) {
        setCurrentImage(newImages[0].name);
      }
    },
    [currentImage]
  );

  const processAllImages = useCallback(async () => {
    setProcessing(true);
    setResults(new Map());
    const newResults = new Map<string, ProcessResult>();
    const ir = getInfluenceRadius();

    for (const imgFile of images) {
      const result = await processSingleImage(imgFile, params, ir);
      if (result) {
        newResults.set(imgFile.name, result);
      }
    }

    setResults(newResults);
    setProcessing(false);
  }, [images, params, influenceCenter, influenceRadiusValue]);

  const processSingleImage = (
    imgFile: ImageFile,
    detectionParams: DetectionParams,
    influenceRadius?: InfluenceRadius
  ): Promise<ProcessResult | null> => {
    return new Promise((resolve) => {
      const img = new Image();
      img.onload = () => {
        try {
          const result = processImage(img, detectionParams, influenceRadius);
          resolve(result);
        } catch (e) {
          console.error('Error processing image:', e);
          resolve(null);
        }
      };
      img.onerror = () => resolve(null);
      img.src = imgFile.preview;
    });
  };

  // Handle image click for setting influence radius
  const handleImageClick = useCallback(
    (e: React.MouseEvent<HTMLImageElement>) => {
      if (influenceMode === 'none') return;

      const img = e.currentTarget;
      const rect = img.getBoundingClientRect();
      const scaleX = img.naturalWidth / rect.width;
      const scaleY = img.naturalHeight / rect.height;
      const x = Math.round((e.clientX - rect.left) * scaleX);
      const y = Math.round((e.clientY - rect.top) * scaleY);

      if (influenceMode === 'setCenter') {
        setInfluenceCenter({ x, y });
        setInfluenceRadiusValue(0);
        setInfluenceMode('setEdge');
      } else if (influenceMode === 'setEdge' && influenceCenter) {
        const dist = Math.round(
          Math.sqrt((x - influenceCenter.x) ** 2 + (y - influenceCenter.y) ** 2)
        );
        setInfluenceRadiusValue(dist);
        setInfluenceMode('none');
      }
    },
    [influenceMode, influenceCenter]
  );

  // Handle mouse move for preview
  const handleImageMouseMove = useCallback(
    (e: React.MouseEvent<HTMLImageElement>) => {
      if (influenceMode !== 'setEdge' || !influenceCenter) {
        setTempInfluence(undefined);
        return;
      }
      const img = e.currentTarget;
      const rect = img.getBoundingClientRect();
      const scaleX = img.naturalWidth / rect.width;
      const scaleY = img.naturalHeight / rect.height;
      const x = Math.round((e.clientX - rect.left) * scaleX);
      const y = Math.round((e.clientY - rect.top) * scaleY);
      const dist = Math.round(
        Math.sqrt((x - influenceCenter.x) ** 2 + (y - influenceCenter.y) ** 2)
      );
      setTempInfluence({ cx: influenceCenter.x, cy: influenceCenter.y, radius: dist });
    },
    [influenceMode, influenceCenter]
  );

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      e.stopPropagation();
      handleFiles(e.dataTransfer.files);
    },
    [handleFiles]
  );

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const clearAll = () => {
    images.forEach((img) => URL.revokeObjectURL(img.preview));
    setImages([]);
    setResults(new Map());
    setCurrentImage(null);
    resetInfluence();
  };

  const resetInfluence = () => {
    setInfluenceCenter(null);
    setInfluenceRadiusValue(0);
    setInfluenceMode('none');
    setTempInfluence(undefined);
    setManualCenter({ x: 0, y: 0 });
    setManualRadius(0);
  };

  const removeImage = (name: string) => {
    setImages((prev) => {
      const img = prev.find((i) => i.name === name);
      if (img) URL.revokeObjectURL(img.preview);
      return prev.filter((i) => i.name !== name);
    });
    setResults((prev) => {
      const next = new Map(prev);
      next.delete(name);
      return next;
    });
    if (currentImage === name) {
      setCurrentImage(null);
    }
  };

  // Auto-select first image when current is removed
  useEffect(() => {
    if (!currentImage && images.length > 0) {
      setCurrentImage(images[0].name);
    }
  }, [images, currentImage]);

  const currentResult = currentImage ? results.get(currentImage) : null;
  const currentImageObj = images.find((i) => i.name === currentImage);

  const cursorStyle =
    influenceMode === 'setCenter'
      ? 'crosshair'
      : influenceMode === 'setEdge'
      ? 'crosshair'
      : 'default';

  // We need to use a state for the preview image
  const [previewSrc, setPreviewSrc] = useState<string | null>(null);

  useEffect(() => {
    if (currentImageObj && (influenceMode !== 'none' || (influenceCenter && influenceRadiusValue > 0))) {
      // For preview, we draw the influence radius on the original image
      const img = new Image();
      img.onload = () => {
        const canvas = document.createElement('canvas');
        canvas.width = img.naturalWidth;
        canvas.height = img.naturalHeight;
        const ctx = canvas.getContext('2d')!;
        ctx.drawImage(img, 0, 0);

        const ir = tempInfluence || (influenceRadiusValue > 0 && influenceCenter
          ? { cx: influenceCenter.x, cy: influenceCenter.y, radius: influenceRadiusValue }
          : null);

        if (ir && ir.radius > 0) {
          ctx.save();
          ctx.strokeStyle = 'rgba(255, 200, 0, 0.8)';
          ctx.lineWidth = Math.max(2, Math.round(img.naturalWidth / 400));
          ctx.setLineDash([
            Math.max(8, Math.round(img.naturalWidth / 150)),
            Math.max(4, Math.round(img.naturalWidth / 300)),
          ]);
          ctx.beginPath();
          ctx.arc(ir.cx, ir.cy, ir.radius, 0, Math.PI * 2);
          ctx.stroke();
          ctx.restore();

          const crossSize = Math.max(6, Math.round(img.naturalWidth / 200));
          ctx.strokeStyle = 'rgba(255, 200, 0, 0.9)';
          ctx.lineWidth = Math.max(1, Math.round(img.naturalWidth / 800));
          ctx.setLineDash([]);
          ctx.beginPath();
          ctx.moveTo(ir.cx - crossSize, ir.cy);
          ctx.lineTo(ir.cx + crossSize, ir.cy);
          ctx.moveTo(ir.cx, ir.cy - crossSize);
          ctx.lineTo(ir.cx, ir.cy + crossSize);
          ctx.stroke();
        } else if (influenceCenter) {
          // Just draw center point
          const crossSize = Math.max(6, Math.round(img.naturalWidth / 200));
          ctx.strokeStyle = 'rgba(255, 200, 0, 0.9)';
          ctx.lineWidth = Math.max(1, Math.round(img.naturalWidth / 800));
          ctx.beginPath();
          ctx.moveTo(influenceCenter.x - crossSize, influenceCenter.y);
          ctx.lineTo(influenceCenter.x + crossSize, influenceCenter.y);
          ctx.moveTo(influenceCenter.x, influenceCenter.y - crossSize);
          ctx.lineTo(influenceCenter.x, influenceCenter.y + crossSize);
          ctx.stroke();
        }

        setPreviewSrc(canvas.toDataURL('image/png'));
      };
      img.src = currentImageObj.preview;
    } else {
      setPreviewSrc(null);
    }
  }, [currentImageObj, influenceCenter, influenceRadiusValue, tempInfluence, influenceMode]);

  const displaySrc = currentResult
    ? currentResult.imageDataUrl
    : previewSrc || (currentImageObj?.preview ?? null);

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Header */}
      <header className="bg-gray-800 border-b border-gray-700 px-4 py-3 shadow-lg">
        <div className="max-w-[1800px] mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="text-3xl">🔵</div>
            <div>
              <h1 className="text-xl font-bold text-blue-300">
                파란 동그라미 카운터
              </h1>
              <p className="text-xs text-gray-400">
                이미지에서 파란색 원을 자동 감지하고 번호를 매깁니다
              </p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            {results.size > 0 && (
              <>
                <div className="bg-green-600/30 border border-green-500/50 rounded-lg px-4 py-2 text-center">
                  <div className="text-xs text-green-300">영향반경 내부</div>
                  <div className="text-2xl font-bold text-green-200">
                    {totalInside}
                  </div>
                </div>
                <div className="bg-orange-600/30 border border-orange-500/50 rounded-lg px-4 py-2 text-center">
                  <div className="text-xs text-orange-300">영향반경 외부</div>
                  <div className="text-2xl font-bold text-orange-200">
                    {totalOutside}
                  </div>
                </div>
                <div className="bg-blue-600/30 border border-blue-500/50 rounded-lg px-4 py-2 text-center">
                  <div className="text-xs text-blue-300">총 감지 수</div>
                  <div className="text-2xl font-bold text-blue-200">
                    {totalCircles}
                  </div>
                </div>
              </>
            )}
          </div>
        </div>
      </header>

      <div className="max-w-[1800px] mx-auto p-4 flex gap-4 h-[calc(100vh-64px)]">
        {/* Left Panel - Controls & File List */}
        <div className="w-80 flex-shrink-0 flex flex-col gap-3 overflow-hidden">
          {/* Drop Zone */}
          <div
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            onClick={() => fileInputRef.current?.click()}
            className="border-2 border-dashed border-gray-600 rounded-xl p-6 text-center cursor-pointer hover:border-blue-500 hover:bg-blue-500/5 transition-all"
          >
            <div className="text-4xl mb-2">📁</div>
            <p className="text-sm text-gray-300 font-medium">
              이미지를 드래그앤드롭하세요
            </p>
            <p className="text-xs text-gray-500 mt-1">또는 클릭하여 선택</p>
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              multiple
              className="hidden"
              onChange={(e) => e.target.files && handleFiles(e.target.files)}
            />
          </div>

          {/* Influence Radius Section */}
          <div className="bg-gray-800 rounded-lg p-3 space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium text-yellow-300">📏 영향반경 설정</span>
              <button
                onClick={resetInfluence}
                className="text-xs text-gray-400 hover:text-red-400"
              >
                초기화
              </button>
            </div>

            {influenceMode === 'none' && !influenceCenter && (
              <div className="space-y-2">
                <button
                  onClick={() => setInfluenceMode('setCenter')}
                  className="w-full bg-yellow-600/30 hover:bg-yellow-600/50 border border-yellow-500/50 text-yellow-300 rounded-lg py-2 text-sm transition-colors"
                >
                  🎯 이미지에서 영향반경 지정
                </button>
                <button
                  onClick={() => setShowInfluenceInput(!showInfluenceInput)}
                  className="w-full bg-gray-700 hover:bg-gray-600 text-gray-300 rounded-lg py-2 text-sm transition-colors"
                >
                  ✏️ 수동 입력
                </button>
              </div>
            )}

            {influenceMode === 'setCenter' && (
              <div className="bg-yellow-900/30 border border-yellow-600/50 rounded-lg p-2 text-xs">
                <p className="text-yellow-300 font-medium">📍 중심점 설정 모드</p>
                <p className="text-gray-400 mt-1">이미지에서 영향반경의 중심을 클릭하세요</p>
                <button
                  onClick={() => setInfluenceMode('none')}
                  className="mt-2 text-gray-400 hover:text-white"
                >
                  취소
                </button>
              </div>
            )}

            {influenceMode === 'setEdge' && influenceCenter && (
              <div className="bg-yellow-900/30 border border-yellow-600/50 rounded-lg p-2 text-xs">
                <p className="text-yellow-300 font-medium">📏 반경 설정 모드</p>
                <p className="text-gray-400 mt-1">
                  중심 ({influenceCenter.x}, {influenceCenter.y})에서 반경 끝점을 클릭하세요
                </p>
                <div className="mt-2 flex items-center gap-2">
                  <label className="text-gray-400">반경:</label>
                  <input
                    type="number"
                    value={influenceRadiusValue || ''}
                    onChange={(e) => setInfluenceRadiusValue(Number(e.target.value))}
                    placeholder="직접입력"
                    className="flex-1 bg-gray-700 rounded px-2 py-1 text-xs text-white"
                  />
                  <button
                    onClick={() => {
                      if (influenceRadiusValue > 0) setInfluenceMode('none');
                    }}
                    className="bg-yellow-600 px-2 py-1 rounded text-xs"
                  >
                    확인
                  </button>
                </div>
                <button
                  onClick={() => {
                    setInfluenceMode('setCenter');
                    setInfluenceRadiusValue(0);
                  }}
                  className="mt-1 text-gray-400 hover:text-white text-xs"
                >
                  ← 중심 다시 설정
                </button>
              </div>
            )}

            {influenceCenter && influenceRadiusValue > 0 && influenceMode === 'none' && (
              <div className="bg-gray-700/50 rounded-lg p-2 text-xs space-y-1">
                <div className="flex justify-between text-gray-300">
                  <span>중심:</span>
                  <span>({influenceCenter.x}, {influenceCenter.y})</span>
                </div>
                <div className="flex justify-between text-gray-300">
                  <span>반경:</span>
                  <span>{influenceRadiusValue}px</span>
                </div>
                <div className="flex gap-1 mt-1">
                  <button
                    onClick={() => {
                      setInfluenceRadiusValue(0);
                      setInfluenceMode('setCenter');
                    }}
                    className="flex-1 bg-gray-600 hover:bg-gray-500 rounded py-1 text-xs"
                  >
                    재설정
                  </button>
                  <button
                    onClick={() => {
                      setInfluenceRadiusValue(0);
                      setInfluenceMode('setEdge');
                    }}
                    className="flex-1 bg-gray-600 hover:bg-gray-500 rounded py-1 text-xs"
                  >
                    반경만 변경
                  </button>
                </div>
              </div>
            )}

            {showInfluenceInput && (
              <div className="bg-gray-700 rounded-lg p-3 space-y-2 text-xs">
                <div className="flex gap-2">
                  <div className="flex-1">
                    <label className="text-gray-400 block mb-1">중심 X</label>
                    <input
                      type="number"
                      value={manualCenter.x}
                      onChange={(e) => setManualCenter({ ...manualCenter, x: Number(e.target.value) })}
                      className="w-full bg-gray-600 rounded px-2 py-1 text-white"
                    />
                  </div>
                  <div className="flex-1">
                    <label className="text-gray-400 block mb-1">중심 Y</label>
                    <input
                      type="number"
                      value={manualCenter.y}
                      onChange={(e) => setManualCenter({ ...manualCenter, y: Number(e.target.value) })}
                      className="w-full bg-gray-600 rounded px-2 py-1 text-white"
                    />
                  </div>
                </div>
                <div>
                  <label className="text-gray-400 block mb-1">반경 (px)</label>
                  <input
                    type="number"
                    value={manualRadius}
                    onChange={(e) => setManualRadius(Number(e.target.value))}
                    className="w-full bg-gray-600 rounded px-2 py-1 text-white"
                  />
                </div>
                <button
                  onClick={() => {
                    setInfluenceCenter({ x: manualCenter.x, y: manualCenter.y });
                    setInfluenceRadiusValue(manualRadius);
                    setShowInfluenceInput(false);
                  }}
                  className="w-full bg-yellow-600 hover:bg-yellow-500 rounded py-1.5 text-white text-xs"
                >
                  적용
                </button>
              </div>
            )}
          </div>

          {/* Parameters Toggle */}
          <button
            onClick={() => setShowParams(!showParams)}
            className="flex items-center justify-between bg-gray-800 rounded-lg px-4 py-2 text-sm hover:bg-gray-750 transition-colors"
          >
            <span>⚙️ 감지 파라미터 설정</span>
            <span>{showParams ? '▲' : '▼'}</span>
          </button>

          {showParams && (
            <div className="bg-gray-800 rounded-lg p-4 space-y-3 text-xs">
              <div>
                <label className="text-gray-400 block mb-1">
                  색상 범위 (Hue): {params.hueMin}° ~ {params.hueMax}°
                </label>
                <div className="flex gap-2">
                  <input
                    type="range"
                    min="0"
                    max="360"
                    value={params.hueMin}
                    onChange={(e) =>
                      setParams((p) => ({ ...p, hueMin: Number(e.target.value) }))
                    }
                    className="flex-1"
                  />
                  <input
                    type="range"
                    min="0"
                    max="360"
                    value={params.hueMax}
                    onChange={(e) =>
                      setParams((p) => ({ ...p, hueMax: Number(e.target.value) }))
                    }
                    className="flex-1"
                  />
                </div>
                <div
                  className="h-2 mt-1 rounded-full"
                  style={{
                    background:
                      'linear-gradient(to right, #ff0000, #ffff00, #00ff00, #00ffff, #0000ff, #ff00ff, #ff0000)',
                  }}
                />
              </div>

              <div>
                <label className="text-gray-400 block mb-1">
                  최소 채도 (Saturation): {params.satMin}%
                </label>
                <input
                  type="range"
                  min="0"
                  max="100"
                  value={params.satMin}
                  onChange={(e) =>
                    setParams((p) => ({ ...p, satMin: Number(e.target.value) }))
                  }
                  className="w-full"
                />
              </div>

              <div>
                <label className="text-gray-400 block mb-1">
                  최소 명도 (Brightness): {params.brightMin}%
                </label>
                <input
                  type="range"
                  min="0"
                  max="100"
                  value={params.brightMin}
                  onChange={(e) =>
                    setParams((p) => ({ ...p, brightMin: Number(e.target.value) }))
                  }
                  className="w-full"
                />
              </div>

              <div>
                <label className="text-gray-400 block mb-1">
                  최소 픽셀 수 (노이즈 필터): {params.minCirclePixels}
                </label>
                <input
                  type="range"
                  min="1"
                  max="5000"
                  step="5"
                  value={params.minCirclePixels}
                  onChange={(e) =>
                    setParams((p) => ({ ...p, minCirclePixels: Number(e.target.value) }))
                  }
                  className="w-full"
                />
              </div>

              <div>
                <label className="text-gray-400 block mb-1">
                  최대 픽셀 수: {params.maxCirclePixels}
                </label>
                <input
                  type="range"
                  min="100"
                  max="500000"
                  step="100"
                  value={params.maxCirclePixels}
                  onChange={(e) =>
                    setParams((p) => ({ ...p, maxCirclePixels: Number(e.target.value) }))
                  }
                  className="w-full"
                />
              </div>

              <div>
                <label className="text-gray-400 block mb-1">
                  중복 병합 기준: {Math.round(params.mergeOverlapRatio * 100)}%
                </label>
                <input
                  type="range"
                  min="0"
                  max="100"
                  step="5"
                  value={Math.round(params.mergeOverlapRatio * 100)}
                  onChange={(e) =>
                    setParams((p) => ({
                      ...p,
                      mergeOverlapRatio: Number(e.target.value) / 100,
                    }))
                  }
                  className="w-full"
                />
                <p className="text-gray-500 mt-1">
                  두 원의 중심 거리가 (반경 합 × {params.mergeOverlapRatio}) 보다 가까우면 병합
                </p>
              </div>

              <div>
                <label className="text-gray-400 block mb-1">라벨 크기</label>
                <div className="flex gap-2">
                  {(['small', 'medium', 'large'] as const).map((size) => (
                    <button
                      key={size}
                      onClick={() => setParams((p) => ({ ...p, showLabelSize: size }))}
                      className={`flex-1 py-1 rounded text-xs ${
                        params.showLabelSize === size
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-700 text-gray-300'
                      }`}
                    >
                      {size === 'small' ? '작게' : size === 'medium' ? '보통' : '크게'}
                    </button>
                  ))}
                </div>
              </div>

              <button
                onClick={() => setParams({ ...defaultParams })}
                className="w-full py-1 bg-gray-700 rounded text-gray-300 hover:bg-gray-600"
              >
                기본값으로 초기화
              </button>
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex gap-2">
            <button
              onClick={processAllImages}
              disabled={images.length === 0 || processing}
              className="flex-1 bg-blue-600 hover:bg-blue-500 disabled:bg-gray-700 disabled:text-gray-500 rounded-lg py-3 font-medium transition-colors text-sm"
            >
              {processing ? '⏳ 처리 중...' : '🔍 감지 시작'}
            </button>
            <button
              onClick={clearAll}
              disabled={images.length === 0}
              className="bg-red-600/20 hover:bg-red-600/40 disabled:bg-gray-700 disabled:text-gray-500 text-red-300 rounded-lg px-4 py-3 text-sm transition-colors"
            >
              🗑️
            </button>
          </div>

          {/* Image List */}
          <div className="flex-1 overflow-y-auto space-y-1 pr-1">
            {images.length === 0 && (
              <div className="text-center text-gray-500 text-sm py-8">
                이미지가 없습니다
              </div>
            )}
            {images.map((img) => {
              const result = results.get(img.name);
              const isActive = currentImage === img.name;
              return (
                <div
                  key={img.name}
                  onClick={() => setCurrentImage(img.name)}
                  className={`flex items-center gap-3 p-2 rounded-lg cursor-pointer transition-colors ${
                    isActive
                      ? 'bg-blue-600/30 border border-blue-500/50'
                      : 'bg-gray-800 hover:bg-gray-750 border border-transparent'
                  }`}
                >
                  <img
                    src={img.preview}
                    alt={img.name}
                    className="w-12 h-12 object-cover rounded"
                  />
                  <div className="flex-1 min-w-0">
                    <div className="text-sm truncate text-gray-200">{img.name}</div>
                    {result && (
                      <div className="text-xs space-y-0.5">
                        <div className="text-green-400">
                          내부: {result.insideCount}개
                        </div>
                        <div className="text-orange-400">
                          외부: {result.outsideCount}개
                        </div>
                        <div className="text-blue-400">
                          총: {result.totalCount}개
                        </div>
                      </div>
                    )}
                  </div>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      removeImage(img.name);
                    }}
                    className="text-gray-500 hover:text-red-400 text-lg"
                  >
                    ×
                  </button>
                </div>
              );
            })}
          </div>
        </div>

        {/* Main Content - Image Display */}
        <div className="flex-1 flex flex-col overflow-hidden bg-gray-800 rounded-xl">
          {currentImage && displaySrc ? (
            <>
              {/* Toolbar */}
              <div className="flex items-center justify-between px-4 py-2 bg-gray-800 border-b border-gray-700">
                <div className="text-sm text-gray-300">
                  📷 {currentImage} —{' '}
                  {currentResult ? (
                    <>
                      <span className="text-green-400 font-medium">
                        내부 {currentResult.insideCount}개
                      </span>
                      {' / '}
                      <span className="text-orange-400 font-medium">
                        외부 {currentResult.outsideCount}개
                      </span>
                      {' / '}
                      <span className="text-blue-400 font-medium">
                        총 {currentResult.totalCount}개
                      </span>
                    </>
                  ) : (
                    <span className="text-gray-400">감지 대기 중</span>
                  )}
                </div>
                <div className="flex items-center gap-3">
                  <button
                    onClick={() => setZoom((z) => Math.max(0.25, z - 0.25))}
                    className="bg-gray-700 px-2 py-1 rounded text-xs hover:bg-gray-600"
                  >
                    ➖
                  </button>
                  <span className="text-xs text-gray-400 w-12 text-center">
                    {Math.round(zoom * 100)}%
                  </span>
                  <button
                    onClick={() => setZoom((z) => Math.min(5, z + 0.25))}
                    className="bg-gray-700 px-2 py-1 rounded text-xs hover:bg-gray-600"
                  >
                    ➕
                  </button>
                  <button
                    onClick={() => setZoom(1)}
                    className="bg-gray-700 px-3 py-1 rounded text-xs hover:bg-gray-600"
                  >
                    리셋
                  </button>
                  <button
                    onClick={() => {
                      if (currentResult) {
                        const a = document.createElement('a');
                        a.href = currentResult.imageDataUrl;
                        a.download = `counted_${currentImage}`;
                        a.click();
                      }
                    }}
                    disabled={!currentResult}
                    className="bg-green-600 hover:bg-green-500 disabled:bg-gray-600 disabled:text-gray-400 px-3 py-1 rounded text-xs"
                  >
                    💾 저장
                  </button>
                </div>
              </div>

              {/* Image Display with Scroll */}
              <div className="flex-1 overflow-auto p-4 flex items-start justify-center">
                <div
                  style={{ transform: `scale(${zoom})`, transformOrigin: 'top center' }}
                  className="inline-block transition-transform"
                >
                  <img
                    ref={resultImageRef}
                    src={displaySrc}
                    alt={`Result: ${currentImage}`}
                    className="max-w-none shadow-2xl rounded"
                    style={{
                      imageRendering: zoom > 2 ? 'pixelated' : 'auto',
                      cursor: cursorStyle,
                    }}
                    onClick={handleImageClick}
                    onMouseMove={handleImageMouseMove}
                    onMouseLeave={() => setTempInfluence(undefined)}
                  />
                </div>
              </div>

              {/* Circle Details */}
              {currentResult && currentResult.circles.length > 0 && (
                <div className="border-t border-gray-700 bg-gray-850 px-4 py-2 max-h-48 overflow-y-auto">
                  {/* Summary */}
                  <div className="flex gap-4 mb-2 pb-2 border-b border-gray-700">
                    <div className="flex items-center gap-2 text-xs">
                      <span className="w-3 h-3 rounded-full bg-green-500 inline-block" />
                      <span className="text-green-300 font-medium">
                        영향반경 내부: {currentResult.insideCount}개
                      </span>
                    </div>
                    <div className="flex items-center gap-2 text-xs">
                      <span className="w-3 h-3 rounded-full bg-orange-500 inline-block" />
                      <span className="text-orange-300 font-medium">
                        영향반경 외부: {currentResult.outsideCount}개
                      </span>
                    </div>
                    <div className="flex items-center gap-2 text-xs">
                      <span className="w-3 h-3 rounded-full bg-blue-500 inline-block" />
                      <span className="text-blue-300 font-medium">
                        총 합계: {currentResult.totalCount}개
                      </span>
                    </div>
                    <button
                      onClick={() => setShowMergeInfo(!showMergeInfo)}
                      className="text-xs text-gray-400 hover:text-white ml-auto"
                    >
                      {showMergeInfo ? '목록 접기 ▲' : '상세 목록 ▼'}
                    </button>
                  </div>

                  {showMergeInfo && (
                    <div className="space-y-2">
                      {currentResult.insideCount > 0 && (
                        <div>
                          <div className="text-xs text-green-400 font-medium mb-1">
                            🟢 영향반경 내부 ({currentResult.insideCount}개)
                          </div>
                          <div className="flex flex-wrap gap-1">
                            {currentResult.circles
                              .filter((c) => c.insideInfluence)
                              .map((c) => (
                                <span
                                  key={`in-${c.id}`}
                                  className="inline-flex items-center gap-1 bg-green-800/40 border border-green-600/30 rounded-full px-2 py-0.5 text-xs"
                                >
                                  <span className="w-2.5 h-2.5 rounded-full bg-green-500 inline-block" />
                                  ●{c.id}{' '}
                                  <span className="text-gray-400">
                                    ({c.cx},{c.cy}) r={c.radius}
                                  </span>
                                </span>
                              ))}
                          </div>
                        </div>
                      )}
                      {currentResult.outsideCount > 0 && (
                        <div>
                          <div className="text-xs text-orange-400 font-medium mb-1">
                            🟠 영향반경 외부 ({currentResult.outsideCount}개)
                          </div>
                          <div className="flex flex-wrap gap-1">
                            {currentResult.circles
                              .filter((c) => !c.insideInfluence)
                              .map((c) => (
                                <span
                                  key={`out-${c.id}`}
                                  className="inline-flex items-center gap-1 bg-orange-800/40 border border-orange-600/30 rounded-full px-2 py-0.5 text-xs"
                                >
                                  <span className="w-2.5 h-2.5 rounded-full bg-orange-500 inline-block" />
                                  ○{c.id}{' '}
                                  <span className="text-gray-400">
                                    ({c.cx},{c.cy}) r={c.radius}
                                  </span>
                                </span>
                              ))}
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              )}
            </>
          ) : currentImage && currentImageObj && !results.has(currentImage) ? (
            /* Original image preview before processing */
            <div className="flex-1 flex flex-col items-center justify-center">
              <div className="text-center mb-4">
                <div className="text-6xl mb-4">🔵</div>
                <p className="text-gray-300 text-lg font-medium">
                  이미지가 로드되었습니다
                </p>
                <p className="text-gray-500 text-sm mt-1">
                  "감지 시작" 버튼을 눌러 파란 동그라미를 감지하세요
                </p>
                {influenceMode !== 'none' && (
                  <div className="mt-2 bg-yellow-900/30 border border-yellow-600/50 rounded-lg p-3 inline-block">
                    <p className="text-yellow-300 text-sm">
                      {influenceMode === 'setCenter'
                        ? '📍 이미지에서 영향반경 중심을 클릭하세요'
                        : '📏 중심에서 반경 끝점을 클릭하세요'}
                    </p>
                  </div>
                )}
              </div>
              <div className="overflow-auto max-h-[60vh] p-4">
                <img
                  src={previewSrc || currentImageObj.preview}
                  alt={currentImage}
                  className="max-w-full shadow-2xl rounded"
                  style={{ cursor: cursorStyle }}
                  onClick={handleImageClick}
                  onMouseMove={handleImageMouseMove}
                  onMouseLeave={() => setTempInfluence(undefined)}
                />
              </div>
            </div>
          ) : (
            /* Empty state */
            <div className="flex-1 flex flex-col items-center justify-center text-gray-500">
              <div className="text-8xl mb-6 opacity-50">🔵</div>
              <p className="text-xl font-medium mb-2">이미지를 추가해 주세요</p>
              <p className="text-sm">
                왼쪽 패널에 이미지를 드래그앤드롭하거나 클릭하여 선택하세요
              </p>
              <div className="mt-8 bg-gray-700/50 rounded-xl p-6 max-w-md text-sm text-gray-400">
                <h3 className="text-gray-300 font-medium mb-3">💡 사용 방법</h3>
                <ol className="space-y-2 list-decimal list-inside">
                  <li>이미지 파일을 업로드합니다 (JPG, PNG 등)</li>
                  <li>📏 영향반경을 설정합니다 (클릭 또는 수동입력)</li>
                  <li>필요시 파라미터를 조정합니다</li>
                  <li>"감지 시작" 버튼을 누릅니다</li>
                  <li>
                    <span className="text-green-400">영향반경 내부</span>와{' '}
                    <span className="text-orange-400">외부</span> 동그라미가 구분됩니다
                  </li>
                  <li>결과 이미지를 저장할 수 있습니다</li>
                </ol>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
