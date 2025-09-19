@echo off

cd /d d:\05_send

echo Copy Hwp File to Send folder ... 
copy "c:\Program Files\totalcmd\ini\02_python\03_GroundWater Ussage\01_이미지 로드, 리사이즈\iyong_empty.hwp" "d:\05_Send""

echo Run Python

python "c:\Program Files\totalcmd\ini\02_python\03_GroundWater Ussage\01_이미지 로드, 리사이즈\pyhwpx_iyongsiltae, Image Load and Resize.py"
del d:\05_Send\iyong_empty.hwp






