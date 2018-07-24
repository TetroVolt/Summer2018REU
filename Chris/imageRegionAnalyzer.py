import pandas as pd
import os
import numpy as np
from functools import reduce
from sklearn.feature_selection import VarianceThreshold
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import seaborn as sns

def summarize_df(df):
	columns = ['Area','EulerNumber','Perimeter','PARatio','SatArea','SatEulerNumber','SatPerimeter','SatPARatio']
	polymers = df.index.unique()
	series = []
	for polymer in polymers:
		attr = []
		for col in columns:
			attr.append(pd.Series({col+'Sum': df.loc[polymer,col].sum(),
						   		   col+'Mean': df.loc[polymer,col].mean(),
						   		   col+'Std': df.loc[polymer,col].std(),
						  		   col+'Min': df.loc[polymer,col].min(),
						   		   col+'Max': df.loc[polymer,col].max()}))
		attr.append(pd.Series({'Count':df.loc[polymer,'Area'].count()}))
		series.append(reduce((lambda x,y: x.append(y)), attr))
	# df_sum is a dataframe to keep track of the summary statistics of the features for each image
	df_summ = pd.DataFrame(series,index=polymers)

	summ = pd.read_csv('summary.txt')
	summ = summ.set_index('Polymer')
	return df_summ.join(summ,how='outer')

def get_properties_df():
	path = r"C:\Users\chris\Documents\csreu\dewetting\175microns"
	dirs = os.listdir(path)
	dfs = []
	for file in dirs:
		if file[:7] == 'summary':
			df = pd.read_csv(file)
			df['Category'] = file[-5]
			dfs.append(df)
		
	# merged dataframe
	df = reduce(lambda df1,df2: pd.concat([df1,df2]),dfs)
	df = df.set_index(['Polymer'])
	print('Step 1 complete')
	return df.astype(float)

def dataframe_to_excel():
	df = get_properties_df()
	df = df.loc[:,df.apply(pd.Series.nunique) != 1] # removes columns with zero variance
	writer = pd.ExcelWriter('output.xlsx') # file name
	df.to_excel(writer,'Summary')
	writer.close()
	print('Step 2 complete')
	return df

	
if __name__ == '__main__' :
	#df = dataframe_to_excel();
	df = pd.read_csv('features.csv')
	df = df.reset_index()
	#df.info(memory_usage='deep')
		
	# produces scatter matrix
	#X = df[['Polymer','WhiteDensity_unweighted', 'WhiteDensity_weighted', 'Entropy', 'IntensitySum', 'IntensityStd', 'IntensityMean', 'IntensityMed', 'Skew']]
	#y = df['Category']
	sns.set(style='ticks')
	df = df.rename(index=str, columns={'grayscale_ent': 'gs.ent', 'grayscale_ent_devN2': 'gs.ent.l', 'grayscale_std':'gs.std', 'grayscale_std_devN2':'gs.std.l', 'grayscale_skew':'gs.skew', 'grayscale_skew_devN2':'gs.skew.l','saturation_ent':'sat.ent','saturation_ent_devN2':'sat.ent.l','saturation_std':'sat.std', 'saturation_std_devN2':'sat.std.l', 'saturation_skew':'sat.skew', 'saturation_skew_devN2':'sat.skew.l'})
	# df = df.drop(columns=['White_w', 'IntMean', 'IntMed', 'IntStd'])
	sns.pairplot(df,hue='labels', vars=['gs.ent', 'gs.ent.l', 'gs.std', 'gs.std.l', 'gs.skew', 'gs.skew.l'])
	plt.show()
	sns.pairplot(df,hue='labels', vars=['sat.ent', 'sat.ent.l', 'sat.std', 'sat.std.l', 'sat.skew', 'sat.skew.l'])
	plt.show()
	sns.pairplot(df,hue='labels', x_vars=['gs.ent', 'gs.ent.l', 'gs.std', 'gs.std.l', 'gs.skew', 'gs.skew.l'], y_vars=['sat.skew.l','sat.skew','sat.std.l','sat.std','sat.ent.l','sat.ent'])
	plt.show()


	#cmap = cm.get_cmap('gnuplot')
	#scatter = pd.plotting.scatter_matrix(X,y, marker='o', s=40, hist_kwds={'bins':15}, figsize=(24,24), cmap=cmap)
	
	

	""" produces 3D figure
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	ax.scatter(df_stat['Area']['std'], df_stat['Eccentricity']['sum'], df_stat['Area']['count'], marker = 'o', s=100)
	ax.set_xlabel('area, std')
	ax.set_ylabel('eccentricity, sum')
	ax.set_zlabel('count')
	plt.show()
	"""

	