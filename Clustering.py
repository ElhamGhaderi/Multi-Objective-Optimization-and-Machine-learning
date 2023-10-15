
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
# %matplotlib inline

df = pd.read_csv("BestResultsLog.csv")

X = df.iloc[:,1:17]

X.head()

X.shape

wcss = [None]

for i in range(1,12):

    Kmeans = KMeans(n_clusters = i, init = 'k-means++', random_state = 100)
    Kmeans.fit(X)
    wcss.append(Kmeans.inertia_)


plt.plot(wcss)
plt.show

plt.title('The Elbow M')
plt.xlabel('Number of clusters')
plt.ylabel('wcss')

pca = PCA(n_components=3)
principle_components = pca.fit_transform(X)
pca_DF = pd.DataFrame(data=principle_components, columns = ['pc1', 'pc2','pc3'])

pca.explained_variance_

pca.explained_variance_ratio_

pca_DF.head()

X = pca_DF.iloc[:,:]

X.head()



y_pred = Kmeans.predict(X)

X['cluster'] = y_pred




fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(projection='3d')



ClusterNum = 3
dfNumbered = []
for i in range(ClusterNum):
    dfNumbered.append(X[X.cluster == i])

np.random.seed(120)

colormap = plt.cm.gist_ncar
colorst = [colormap(i) for i in np.linspace(0, 0.5, ClusterNum)]

for i in range(ClusterNum):
    ax.scatter(dfNumbered[i]['pc1'], dfNumbered[i]['pc2'], dfNumbered[i]['pc3'], color = colorst[i], alpha = 0.5, s=100)



plt.title('Three clusters')

ax.set_xlabel("PC 1")
ax.set_ylabel("PC 2")
ax.set_zlabel("PC 3")

plt.legend([i+1 for i in range(ClusterNum)], title="Clusters")
plt.savefig('Final_Clusters.png', format="png", dpi=150)
plt.show()

