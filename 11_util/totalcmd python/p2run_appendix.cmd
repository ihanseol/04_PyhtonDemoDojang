@echo off

cd /d d:\05_send

echo ******************************************************************
echo *   Run Appendix_01                                              *
echo ******************************************************************


python "c:\Program Files\totalcmd\ini\02_python\03_GroundWater Ussage\17_Appendix_01\pyhwpx_Appendix_01_hwp_file_refactored.py"

cls

echo ******************************************************************
echo *   Run Appendix_02                                              *
echo ******************************************************************

python "c:\Program Files\totalcmd\ini\02_python\03_GroundWater Ussage\17_Appendix_02\pyhwpx_Appendix_02_hwp_file_refactored.py"

cls

echo ******************************************************************
echo *   Run Appendix_06                                              *
echo ******************************************************************

python "c:\Program Files\totalcmd\ini\02_python\03_GroundWater Ussage\17_Appendix_06\pyhwpx_Appendix_06_hwp_file_refactored.py"

del a*.xlsx








