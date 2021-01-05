function OnScriptMacro_사이즈1()
{
	HAction.GetDefault("PrintToPDFEx", HParameterSet.HPrint.HSet);
	with (HParameterSet.HPrint)
	{
		PrinterPaperSize = PrintPaper("");
		PrinterPaperWidth = 59528;
		PrinterPaperLength = 84188;
		Collate = 1;
		UserOrder = 0;
		PrintToFile = 0;
		UsingPagenum = 1;
		ReverseOrder = 0;
		Pause = 0;
		PrintImage = 1;
		PrintDrawObj = 1;
		PrintClickHere = 0;
		PrintAutoFootnoteLtext = "^f";
		PrintAutoFootnoteCtext = "^t";
		PrintAutoFootnoteRtext = "^P쪽 중 ^p쪽";
		PrintAutoHeadnoteLtext = "^c";
		PrintAutoHeadnoteCtext = "^n";
		PrintAutoHeadnoteRtext = "^p";
		PrintFormObj = 1;
		PrintMarkPen = 0;
		PrintBarcode = 1;
		PrintPronounce = 0;
	}
	HAction.Execute("PrintToPDFEx", HParameterSet.HPrint.HSet);
	HAction.GetDefault("FileSaveAs_S", HParameterSet.HFileOpenSave.HSet);
	with (HParameterSet.HFileOpenSave)
	{
		FileName = "C:\\to_pdf\\문서(1).pdf";
		Format = "PDF";
		Attributes = 0;
	}
	HAction.Execute("FileSaveAs_S", HParameterSet.HFileOpenSave.HSet);
}

