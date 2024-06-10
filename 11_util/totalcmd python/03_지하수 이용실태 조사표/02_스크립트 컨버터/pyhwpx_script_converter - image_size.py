from pyhwpx import Hwp

hwp = Hwp()
hwp.clipboard_to_pyfunc()

"""
    
    function OnScriptMacro_script14()
    {
        HAction.GetDefault("PictureSaveAsAll", HParameterSet.HSaveAsImage.HSet);
        with (HParameterSet.HSaveAsImage)
        {
        }
        HAction.Execute("PictureSaveAsAll", HParameterSet.HSaveAsImage.HSet);
        
        
        HAction.GetDefault("FileSaveAs_S", HParameterSet.HFileOpenSave.HSet);
        with (HParameterSet.HFileOpenSave)
        {
            FileName = "C:\\Users\\minhwasoo\\Desktop\\iyong_empty_complete.hwp";
            Format = "HWP";
        }
        HAction.Execute("FileSaveAs_S", HParameterSet.HFileOpenSave.HSet);
    }



def save_s(hwp):
    pset = hwp.HParameterSet.HSaveAsImage
    hwp.HAction.GetDefault("PictureSaveAsAll", pset.HSet)
    hwp.HAction.Execute("PictureSaveAsAll", pset.HSet)

    hwp.HAction.GetDefault("FileSaveAs_S", hwp.HParameterSet.HFileOpenSave.HSet)  # 다른이름으로 저장 액션 생성
    hwp.HParameterSet.HFileOpenSave.filename =   # 원래파일명#페이지.hwp로 저장
    hwp.HParameterSet.HFileOpenSave.Format = "HWP"  # 포맷은 Native HWP
    hwp.HAction.Execute("FileSaveAs_S", hwp.HParameterSet.HFileOpenSave.HSet)  # 다른이름저장 실행
    hwp.HAction.Run("Delete")  # 현재문서 페이지 조판부호 삭제


"""

"""



    function OnScriptMacro_지하수이용실태이미지사이즈()
    {
        HAction.GetDefault("ShapeObjDialog", HParameterSet.HShapeObject.HSet);
        with (HParameterSet.HShapeObject)
        {
            Width = 45637;
            CreateItemArray("OptLockProperties", 1);
            OptLockProperties.Item(0) = 16395;
        }
        HAction.Execute("ShapeObjDialog", HParameterSet.HShapeObject.HSet);
        
        
        HAction.GetDefault("ShapeObjDialog", HParameterSet.HShapeObject.HSet);
        with (HParameterSet.HShapeObject)
        {
            Height = 65196;
            CreateItemArray("OptLockProperties", 1);
            OptLockProperties.Item(0) = 16397;
        }
        HAction.Execute("ShapeObjDialog", HParameterSet.HShapeObject.HSet);
    }
    
    
    def script_macro():
        pset = hwp.HParameterSet.HShapeObject
        hwp.HAction.GetDefault("ShapeObjDialog", pset.HSet)
        pset.Width = 45637
        pset.CreateItemArray("OptLockProperties", 1)
        pset.OptLockProperties.Item(0) = 16395
        hwp.HAction.Execute("ShapeObjDialog", pset.HSet)
        
                
        hwp.HAction.GetDefault("ShapeObjDialog", pset.HSet)
        pset.Width =  65196
        pset.CreateItemArray("OptLockProperties", 1)
        pset.OptLockProperties.Item(0) = 16397
        hwp.HAction.Execute("ShapeObjDialog", pset.HSet)
    
    
"""
