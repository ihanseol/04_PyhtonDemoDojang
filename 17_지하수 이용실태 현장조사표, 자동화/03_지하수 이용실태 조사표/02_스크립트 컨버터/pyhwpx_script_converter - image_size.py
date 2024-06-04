from pyhwpx import Hwp

hwp = Hwp()
hwp.clipboard_to_pyfunc()

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
