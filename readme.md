#patent-detective

This project provides some static analysis over public data set of patents available on google bigquery. For more knowledge about dataset refer to this article https://cloud.google.com/blog/products/gcp/google-patents-public-datasets-connecting-public-paid-and-private-patent-data. This project contains a notebook which shows some plots depicting the analysis results. We have used table **publication** to do the analysis. I have also created a big_query helper class which I will be using to fetch the result from big query. Apart from that there is one more python file patent_detective which uses bigquery_helper to fetch data and plot the data using python matplotlib or other libraries.

NOTE: you need to export bigquery credential json file where you want to run jupyter notebook or this above code.
