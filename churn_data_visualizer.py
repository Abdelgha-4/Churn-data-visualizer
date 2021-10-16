import warnings
warnings.simplefilter("ignore", category=UserWarning)
import pandas as pd
import dtale
import dtale.app as dtale_app
dtale_app.JUPYTER_SERVER_PROXY = True

churn_data = pd.read_csv("BankChurners.csv", index_col='CLIENTNUM', usecols = range(21))
d = dtale.show(churn_data, allow_cell_edits=False)
print("Click on the link to explore the data and discover new things!")
print(f"https://hub.gke2.mybinder.org/user{d._main_url}")
