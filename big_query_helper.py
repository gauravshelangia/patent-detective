from google.cloud import bigquery
import pandas as pd

class BigQueryHelper(object):
	"""
	Helper class to interact with bigquery provides read only operations
	"""

	def __init__(self, active_project, dataset_name):
		self.project_name = active_project
		self.dataset_name = dataset_name
		self.client = bigquery.Client()
		self.dataset_ref = self.client.dataset(self.dataset_name, project=self.project_name)

	def get_tables(self):
	    """
	    Fetch all tables under dataset of active project specified during initialization.
	    In case you want all table meta-data then change x.table_id to x.__dict__
	    """
	    return [table.table_id for table in self.client.list_tables(self.dataset_ref)]

	def get_table_headers(self,table_name):
		"""
		Return list of header of a table
		"""
		rows = client.list_rows('.'.join([self.active_project, self.dataset_name, table_name]), max_results=0)
		return [field.name for field in rows.schema]

	def create_download_link(df, title = "Download CSV file", filename = "data.csv"):
		"""
		This method will create a download link for a given dataframe
		"""
		csv = df.to_csv()
		b64 = base64.b64encode(csv.encode())
		payload = b64.decode()
		html = '<a download="{filename}" href="data:text/csv;base64,{payload}" target="_blank">{title}</a>'
		html = html.format(payload=payload,title=title,filename=filename)
		return HTML(html)

	def get_data_as_df(self,query):
		query_job = self.client.query(query)
		return query_job.result().to_dataframe()


		
        
