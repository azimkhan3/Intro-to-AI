from PIL import Image  # Python Imaging Library
import math
import random


class Coordinate:
    # initialize points that will be assigned to clusters to randomly find centroids
    def __init__(self, coordinates):
        self.coordinates = coordinates


class Cluster:
    def __init__(self, center, points):
        self.center = center
        self.pts = points


def euclideanDistance(point1, point2):
    # given two points, find the distance between them.
    dim = len(point1.coordinates)
    euclidean_Distance = math.sqrt(sum([(point1.coordinates[i] - point2.coordinates[i]) ** 2 for i in range(dim)]))
    return euclidean_Distance


def PixelsToPoints(photo):  # convert photo pixels to coordinates
    coordinates = []  # initialize a list of coordinates that parses through the image and retrieves colors
    picture = Image.open(photo)  # Using Image features of PIL (python imaging library)
    picture = picture.convert('RGB')
    width, height = picture.size
    # patchArea = width * height
    for i, patchColor in picture.getcolors(width * height):
        for _ in range(i):
            coordinates.append(Coordinate(patchColor))

    return coordinates


class KMeansClustering:
    def __init__(self, NumberOfClusters, minimumDifference=1):
        self.ClusterCount = NumberOfClusters
        self.minDifference = minimumDifference

    def CenterOfCluster(self, coordinates):
        """Find the center of a given cluster"""
        dimensions = len(coordinates[0].coordinates)
        # list of points ranging from 0 to total count of dimensions
        values = [0.0 for i in range(dimensions)]
        for p in coordinates:
            for i in range(dimensions):
                values[i] += p.coordinates[i]
        # center is found by taking average of all the values (total # of values)/(total number of points)
        ClusterCenter = [(val / len(coordinates)) for val in values]
        return Coordinate(ClusterCenter)

    def ClusterSort(self, clusters, coordinates):
        """Sort points by assigning them to clusters"""
        # initialize list of lists, where a list of points are assigned to a cluster from a list of clusters
        assignPointToCluster = [[] for i in range(self.ClusterCount)]
        index = 0
        minDistance = 0
        for point in coordinates:
            minDistance = float('inf')  # initialize a high value for the minDistance originally
            for i in range(self.ClusterCount):
                # find the distance between point p and the center of cluster
                Distance = euclideanDistance(point, clusters[i].center)
                if Distance < minDistance:
                    index = i

                    minDistance = Distance
            assignPointToCluster[index].append(point)

        return assignPointToCluster

    def matchPoints(self, coordinates):
        # assign points to cluster via cluster sorting process
        clusters = [Cluster(p, [p]) for p in random.sample(coordinates, self.ClusterCount)]

        while True:
            assignPointToCluster = self.ClusterSort(clusters, coordinates)
            # initialize difference
            Difference = 0
            for i in range(self.ClusterCount):
                if not assignPointToCluster[i]:
                    continue
                Original = clusters[i]
                ClusterCenter = self.CenterOfCluster(assignPointToCluster[i])
                Updated = Cluster(ClusterCenter, assignPointToCluster[i])
                clusters[i] = Updated
                Difference = max(Difference, euclideanDistance(Original.center, Updated.center))

            if Difference < self.minDifference:
                break

        return clusters


def Colors(Image):
    # run k-means
    fiveColorCount = 5
    coordinates = PixelsToPoints(Image)
    clusters = KMeansClustering(fiveColorCount).matchPoints(coordinates)
    clusters.sort(key=lambda cluster: len(cluster.pts), reverse=True)
    RGB = [list(map(int, cluster.center.coordinates)) for cluster in clusters]
    print(RGB)
    return RGB
