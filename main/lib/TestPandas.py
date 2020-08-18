import pandas as pd

class TestPandas:

	def test_silly():
		df = pd.DataFrame({
			"Name": ["Braund, Mr. Owen Harris",
			         "Allen, Mr. William Henry",
			         "Bonnell, Miss. Elizabeth"],
			"Age": [22, 35, 58],
			"Sex": ["male", "male", "female"]}
		)

		#Each column in a DataFrame is a Series
		agesSeries1 = df["Age"]

		# can create a Series from scratch as well:
		agesSeries2 = pd.Series([22, 35, 58], name="Age")

		results = ["Pandas dataframe - describe"]
		results.append(str(df.describe()))

		results.append("Trying max on a series")
		results.append(str(agesSeries1.max()))
		results.append(str(agesSeries2.max()))

		return results


