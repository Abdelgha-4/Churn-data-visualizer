import warnings
warnings.simplefilter("ignore", category=UserWarning)
import dtale
import os
import pandas as pd
import dtale.app as dtale_app
dtale_app.JUPYTER_SERVER_PROXY = True
app_root, port = f"{os.environ['JUPYTERHUB_SERVICE_PREFIX']}proxy/", 4000
churn_data = pd.read_csv("BankChurners.csv", index_col='CLIENTNUM', usecols = range(21))
d = dtale.show(churn_data, port=port, app_root=app_root, allow_cell_edits=False)
print("Click on the link to explore the data and discover new things!")
print(f"https://hub.gke2.mybinder.org{app_root}{port}/dtale/main/{d._data_id}")