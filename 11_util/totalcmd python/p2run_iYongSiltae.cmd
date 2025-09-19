@echo off

cd /d d:\05_send

echo Copy Hwp File to Send folder ... 
copy "c:\Program Files\totalcmd\ini\02_python\iyong(field).hwp" "c:\Users\minhwasoo\Desktop\"

echo Run Python
:: python "c:\Program Files\totalcmd\ini\02_python\03_지하수 이용실태 조사표\03_지하수 이용실태 조사표, 만들기\pyhwpx_iyongsiltae_josapyo v4.py"
:: python "c:\Program Files\totalcmd\ini\02_python\03_GroundWater Ussage\03_지하수 이용실태 조사표, 만들기\pyhwpx_iyongsiltae_josapyo v4.py"

python "c:\Program Files\totalcmd\ini\02_python\03_GroundWater Ussage\03_지하수 이용실태 조사표, 만들기\pyhwpx_iyong_siltae_refactor.py"
del c:\Users\minhwasoo\Desktop\iyong(field).hwp





