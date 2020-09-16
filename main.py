import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# 1st step: importing data from xml file_________________________________________

tree = ET.parse('post.xml')
root = tree.getroot()


def etree_to_dict(tree):
    posts = []
    for i in range(len(tree)):
        posts.append(tree[i].attrib)
    return posts


posts = etree_to_dict(root)

# 2nd step: Adding RFM variables _________________________________________

# 2.1 Recency

posts = sorted(posts, key=lambda i: i['CreationDate'])

number_Of_Segments = 5
number_Of_Items_In_Segments = int(len(posts) / 5)

global list_Counter
list_Counter = 0
target_Segmentation = []

for i in range(number_Of_Segments):
    for j in range(number_Of_Items_In_Segments):

        posts[list_Counter]['Recency'] = i + 1

        if 'OwnerUserId' in posts[list_Counter]:
            target_Segmentation.append({'ID': posts[list_Counter]['OwnerUserId'], 'Recency': i + 1})

        list_Counter += 1

# set highest Recency as user's Recency

target_Temp = []
for x in target_Segmentation:
    temp = 0
    for y in target_Segmentation:
        if x['ID'] == y['ID']:
            temp = max(x['Recency'], y['Recency'])
    target_Temp.append({'ID': x['ID'], 'Recency': temp})

# Remove duplicates in target

seen = set()
new_l = []
for d in target_Temp:
    t = tuple(d.items())
    if t not in seen:
        seen.add(t)
        new_l.append(d)

target_Segmentation = new_l

# 2.2 Frequency

# Counting frequency of each customer
for x in posts:
    sum_Of_score = int(x['Score'])
    if 'OwnerUserId' in x:
        frequency_Repeat = 0
        for y in posts:
            if 'OwnerUserId' in y:
                if x['OwnerUserId'] == y['OwnerUserId']:
                    frequency_Repeat += 1
                    sum_Of_score = sum_Of_score + int(y['Score'])

        for z in target_Segmentation:
            if z['ID'] == x['OwnerUserId']:
                z['Frequency'] = frequency_Repeat

                z['MonetaryValue'] = int(sum_Of_score / frequency_Repeat)
    else:
        pass

# turning frequency to Frequency variable of RFM
number_Of_Segments = 5
number_Of_Items_In_Segments = int(len(target_Segmentation) / 5)

target_Segmentation = sorted(target_Segmentation, key=lambda i: i['Frequency'])
list_Counter = 0

for i in range(number_Of_Segments):
    for j in range(number_Of_Items_In_Segments):
        target_Segmentation[list_Counter]['Frequency'] = i + 1
        list_Counter += 1

# 2.3 Monetary value
target_Segmentation = sorted(target_Segmentation, key=lambda i: i['MonetaryValue'])

list_Counter = 0
for i in range(number_Of_Segments):
    for j in range(number_Of_Items_In_Segments):
        target_Segmentation[list_Counter]['MonetaryValue'] = i + 1
        list_Counter += 1

# RFM measure's saved in target segmentation

# 3rd step: Adding RFM Score _________________________________________

# RFM score formulation = 5 * Monetary value + 3 * Frequency + 2 * Recency

for i in target_Segmentation:
    i['Score'] = 5 * i['MonetaryValue'] + 3 * i['Frequency'] + 2 * i['Recency']

# 4th step: Clustering _________________________________________

Data = target_Segmentation
df = pd.DataFrame(Data, columns=['MonetaryValue', 'Frequency', 'Recency', 'Score'])

# 4.1 Elbow method to find optimal k
# distortions = []
# K = range(1,10)
# for k in K:
#     kmeanModel = KMeans(n_clusters=k)
#     kmeanModel.fit(df)
#     distortions.append(kmeanModel.inertia_)
#
# plt.figure(figsize=(16,8))
# plt.plot(K, distortions, 'bx-')
# plt.xlabel('k')
# plt.ylabel('Distortion')
# plt.title('The Elbow Method showing the optimal k')
# plt.show()

# 4.2 K-means clustering with opitaml k from elbow method
kmeans = KMeans(n_clusters=3).fit(df)
list_Counter = 0
Clusters = []
Clusters = kmeans.labels_
for i in range(len(target_Segmentation)):
    target_Segmentation[i]['Cluster'] = Clusters[i]

cluster1_Id = []
cluster2_Id = []
cluster3_Id = []
cluster1_Score = []
cluster2_Score = []
cluster3_Score = []
for i in target_Segmentation:
    if i['Cluster'] == 0:
        cluster1_Id.append(int(i['ID']))
        cluster1_Score.append(int(i['Score']))
    elif i['Cluster'] == 1:
        cluster2_Id.append(int(i['ID']))
        cluster2_Score.append(int(i['Score']))
    else:
        cluster3_Id.append(int(i['ID']))
        cluster3_Score.append(int(i['Score']))

for i in range(len(cluster1_Id)):
    if cluster1_Id[i] > 1000:
        cluster1_Id[i] = 0

for i in range(len(cluster2_Id)):
    if cluster2_Id[i] > 1000:
        cluster2_Id[i] = 0

for i in range(len(cluster3_Id)):
    if cluster3_Id[i] > 1000:
        cluster3_Id[i] = 0

plt.scatter(cluster1_Id, cluster1_Score, label="stars")
plt.scatter(cluster2_Id, cluster2_Score, label="circle")
plt.scatter(cluster3_Id, cluster3_Score, label='square')

plt.xlabel('Id')
plt.ylabel('Score')

plt.title('Customer Segmentation Clustering')
plt.legend()
plt.show()
