import wandb
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

wandb.login()


wandb.init(project="ium-projekt", entity="ium-team", group="k-means")

wandb.log({"dataset": wandb.Table(data="TODO")})

k = 3  # Number of clusters

wandb.config.k = k

kmeans = KMeans(n_clusters=k)
kmeans.fit("DATA")
labels = kmeans.labels_

wandb.log({"cluster_assignments": wandb.Histogram(labels)})
inertia = kmeans.inertia_
wandb.log({"inertia": inertia})
wandb.log({"silhouette_score": silhouette_score("DATA", labels)})

wandb.finish()
