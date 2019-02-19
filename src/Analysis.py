#-*-coding:utf-8-*


import utils.SQLiteUtils as sqlite
import numpy
from scipy.cluster import hierarchy
import matplotlib.pylab as plt
import matplotlib
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D

# change matplotlib settings to displey chinese
matplotlib.rcParams['font.sans-serif']=['SimHei']
matplotlib.rcParams['axes.unicode_minus']=False

# hierarchical clustering analysis
standardized_champion_data = sqlite.get_standardized_champion_data()
standardized_champion_data = numpy.array(standardized_champion_data)
clustering_matrix = hierarchy.linkage(standardized_champion_data, 'average')    # for each group, use the average among the group to compute the distance
clustering_figure = plt.figure(dpi=200)
champion_info = sqlite.get_champion_info_dict()
key_list = [key for key in champion_info]
label_list = [champion_info[key][0] + " " + champion_info[key][1] + " " + champion_info[key][2] for key in champion_info ]
#print(label_list)
dn = hierarchy.dendrogram(clustering_matrix, orientation='right', labels=label_list)
#plt.savefig('clustering_figure.png')


# once used for display clustering result by text, replaced by PCA in 3-dimensional space
'''
clustering_index = hierarchy.cut_tree(clustering_matrix, n_clusters=6)
#print(clustering_index)
clustering_result = [[], [], [], [], [], [], []]
for i in range(len(clustering_index)):
    key = key_list[i]
    clustering_result[clustering_index[i][0]].append(champion_info[key][0] + " " + champion_info[key][1] + " " + champion_info[key][2])
for clustering_group in clustering_result:
    print(clustering_group)
'''


# principal component analysis
pca = PCA(n_components=3)
pca.fit(standardized_champion_data)
result = pca.transform(standardized_champion_data)
#print(result)
pca_figure = plt.figure()
ax = Axes3D(pca_figure)
ax.scatter(result[:, 0], result[:, 1], result[:,2])
for i in range(result[:,0].size):
    ax.text(result[i,0], result[i,1], result[i,2], champion_info[key_list[i]][2])
#plt.savefig('pca_figure.png')
plt.show()