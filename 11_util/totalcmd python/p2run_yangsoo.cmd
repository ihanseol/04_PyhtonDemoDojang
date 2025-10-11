@echo off

:: cd /d d:\05_send
cd /d "c:\Program Files\totalcmd\ini\02_python\03_GroundWater Ussage\23_QT_YangSoo All Step\"

:: ** Step 2: Activate the desired environment **
:: conda run -n py311 

call conda activate py311
timeout /t 2 >nul

echo == "Yangsoo_test_qt.py" ==
python "c:\Program Files\totalcmd\ini\02_python\03_GroundWater Ussage\23_QT_YangSoo All Step\yangsoo_test_qt.py"
::pause



