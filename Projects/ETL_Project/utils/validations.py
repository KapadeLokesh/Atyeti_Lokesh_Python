def check_nulls(df,column):
    return df[column].isnull().sum()

def check_duplicates(df,column):
    return df[column].duplicated().sum()

def check_row_count(src,target):
    return len(src) >= len(target)