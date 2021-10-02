import numpy as np
import pandas as pd
import dtale
import dtale.app as dtale_app
dtale_app.USE_NGROK = True

class txt_style:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def reduce_mem_usage(original_df, conserve=False, inplace=False, report=True, low_card_as_cat=10):
    """ iterate through all the columns of a dataframe and modify the data type
        to reduce memory usage.
        if conserve : avoid loss of precision by disabling float convertion  
        if inplace : don't make a copy, change the passed dataframe
        if report : print reduced amount of memory
        low_card_as_cat : if a numeric variable has a lower cardinality than this threshold it'll be considered categorical, 
                          0 means all numeric variables would stay numeric
    """
    # cases of when to backup or copy data
    if inplace:
        df = original_df
        if not conserve : backup = original_df.copy()
    else:
        df = original_df.copy()
        if not conserve : backup = original_df
    
    start_mem = df.memory_usage().sum() / 1024**2
    if report:
        print(f'Initial memory usage of dataframe is {start_mem:.2f} MB')
    
    # set the right dtype for each column based on the range of its values
    for col in df.columns:
        col_type = df[col].dtype
        if col_type != object and df[col].nunique()>low_card_as_cat:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)
            elif not conserve:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max :
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)
        else:
            df[col] = df[col].astype('category')

    if report:
        end_mem = df.memory_usage().sum() / 1024**2
        print(f'Memory usage after optimization is: {end_mem:.2f} MB')
        print(txt_style.GREEN+txt_style.BOLD+f'Decreased by {100 * (start_mem - end_mem)/start_mem:.1f}%'+txt_style.END)
        if conserve :
            print(txt_style.BLUE+'All values conserved, 0% loss of information'+txt_style.END)
        else:
            print('Mean absolute percentage loss of information in float columns :')
            print(
                100 *
                (backup.select_dtypes(include=['float16', 'float32', 'float64']) -
                 df.select_dtypes(include=['float16', 'float32'])).sum().abs() /
                backup.select_dtypes('float').sum())
    return df

data_filepath = "../input/credit-card-customers/BankChurners.csv"
churn_data = pd.read_csv(data_filepath, index_col='CLIENTNUM', usecols = range(21))
reduced_churn_data = reduce_mem_usage(churn_data, conserve=False)

d = dtale.show(reduced_churn_data, allow_cell_edits=False)
print("Click on the link to explore the data and discover new things!")
d.main_url()