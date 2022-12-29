class scatter:
	import matplotlib.pyplot as plt
	
	def __init__(self, title, xLabel, yLabel):
		self.title = title
		self.xLabel = xLabel
		self.yLabel = yLabel
		
	def build(self, dataframe, x, y, val):
		fig = self.plt.figure(figsize = (8,8))
		ax = fig.add_subplot(1,1,1) 
		ax.set_xlabel(self.xLabel, fontsize = 15)
		ax.set_ylabel(self.yLabel, fontsize = 15)
		ax.set_title(self.title, fontsize = 20)
		targets = [0, 1]
		colors = ['r', 'g']
		for target, color in zip(targets,colors):
			indicesToKeep = dataframe[val] == target
			ax.scatter(dataframe.loc[indicesToKeep, x]
					   , dataframe.loc[indicesToKeep, y]
					   , c = color
					   , s = 50)
		ax.legend(targets)
		ax.grid()
		
	def show(self):
		self.plt.show()
	
	def save(self, filename):
		self.plt.savefig("img/"+filename+".png")
