import enum

class ErrorCode(enum.Enum):
    PDF_SAVE_MASK_DATA = "[PDF_01_01] Pandas Dataframe, save_mask_data error"
    PDF_DROP_MASK_DATA = "[PDF_01_02] Pandas Dataframe, drop_mask_data error"
    PDF_GET_MASK_DATA = "[PDF_01_03] Pandas Dataframe, get_mask_data error"
    
    
