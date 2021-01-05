function OnScriptMacro_사이즈1()
{
	HAction.GetDefault("InsertFile", HParameterSet.HInsertFile.HSet);
	with (HParameterSet.HInsertFile)
	{
		FileName = "C:\\to_pdf\\문서 - 복사본 (1).hwp";
		KeepSection = 0;
		KeepCharshape = 0;
		KeepParashape = 0;
		KeepStyle = 0;
	}
	HAction.Execute("InsertFile", HParameterSet.HInsertFile.HSet);

	HAction.GetDefault("FileSaveAsPdf", HParameterSet.HFileOpenSave.HSet);
	with (HParameterSet.HFileOpenSave)
	{
		FileName = "C:\\to_pdf\\지방 쓰는 법.pdf";
		Format = "PDF";
		Attributes = 16384;
	}
	HAction.Execute("FileSaveAsPdf", HParameterSet.HFileOpenSave.HSet);
}

