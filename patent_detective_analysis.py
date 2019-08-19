import big_query_helper as bqh
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import operator
import collections


class PatentDetective(object):
	"""docstring for PatentDetective"""
	def __init__(self,active_project, dataset_name, table_name):
		super(PatentDetective, self).__init__()
		self.big_query = bqh.BigQueryHelper(active_project, dataset_name)
		self.table_name = table_name
		

	def avg_inventors_per_country(self):
		"""
		This would return the average inventor per country and number of inventor > 100
		dataset used is = patents-public-data.patents.publications
		"""
		sql_query = '''SELECT AVG(num_inventors), COUNT(*) AS cnt, country_code, filing_year
					FROM (
	  				SELECT ANY_VALUE(ARRAY_LENGTH(inventor)) AS num_inventors, ANY_VALUE(country_code) AS country_code, ANY_VALUE(CAST(FLOOR(filing_date / (5*10000)) AS INT64))*5 AS filing_year
	  					FROM `patents-public-data.patents.publications` AS pubs
	  					WHERE filing_date > 19000000 AND ARRAY_LENGTH(inventor) > 0
	  					GROUP BY application_number	)
					GROUP BY filing_year, country_code
					HAVING cnt > 100
					ORDER BY filing_year'''
		return self.big_query.get_data_as_df(sql_query)

	def plot_avg_invetors_per_country(self):
		avg_inventor = self.avg_inventors_per_country()
		counts = avg_inventor['cnt'].tolist()
		country_codes = avg_inventor['country_code'].tolist()
		plt.bar(country_codes, counts, 10, align='center')
		plt.show()

	def top_terms(self):
		"""
		Return a dictionary of term with count, quering google_patents_research dataset with limit of 1000
		"""
		sql_query = '''SELECT * 
		FROM `patents-public-data.google_patents_research.publications` 
		WHERE ARRAY_LENGTH(top_terms) > 0 LIMIT 1000'''
		result = self.big_query.get_data_as_df(sql_query)
		top_terms_all = result['top_terms']
		terms = [term for term in top_terms_all]
		freq = {} 
		for sublist in terms:
			for item in sublist:
				if (item in freq):
					freq[item] += 1
				else:
					freq[item] = 1
		sorted_freq = sorted(freq.items(), key=operator.itemgetter(1), reverse=True)
		return sorted_freq

	def plot_top_n_terms(self,n):
		"""
		This method would plot the top n terms, from the result of top_terms method
		"""
		top_terms = self.top_terms()
		top_n_terms = top_terms[:n]
		count = []
		terms = []
		for term in top_n_terms:
			terms.append(term[0])
			count.append(term[1])

		y_pos = np.arange(len(terms))
		plt.bar(y_pos, count, align='center', alpha=0.5)
		plt.xticks(y_pos, terms)
		plt.ylabel('Number of times term has been used')
		plt.title('Usage count of top {} terms'.format(n))
		plt.show()


	def most_cited_publications(self):
		"""
		Get top 1000 most sited publications,
		"""
		sql_query = '''
		SELECT publication_number, ARRAY_LENGTH(cited_by) AS cnt 
		FROM `patents-public-data.google_patents_research.publications` 
		WHERE ARRAY_LENGTH(cited_by) > 0 ORDER BY cnt DESC LIMIT 1000;
		'''
		return self.big_query.get_data_as_df(sql_query)

	def plot_most_cited_publication(self, n):
		"""
		Plot top n most cited publication
		"""
		result = self.most_cited_publications()
		result = result.head(n)
		publications = result['publication_number'].tolist()
		citation_count = result['cnt'].tolist()
		y_pos = np.arange(len(publications))
		plt.bar(y_pos, citation_count, align='center', alpha=0.5)
		plt.xticks(y_pos, publications)
		plt.ylabel('Citation count')
		plt.title('top {} most cited publicatios'.format(n))
		plt.show()

	def most_publication_by_country(self):
		sql_query = '''
		SELECT country, COUNT(country) AS cnt 
		FROM `patents-public-data.google_patents_research.publications` GROUP BY country LIMIT 1000;'''
		return self.big_query.get_data_as_df(sql_query)

	def plot_publication_by_country(self, n):
		result = self.most_publication_by_country()
		result = result.head(n)
		countries = result['country'].tolist()
		citation_count = result['cnt'].tolist()
		y_pos = np.arange(len(countries))
		plt.bar(y_pos, citation_count, align='center', alpha=0.5)
		plt.xticks(y_pos, countries)
		plt.ylabel('country count')
		plt.title('top {} most cited publicatios'.format(n))
		plt.show()











		