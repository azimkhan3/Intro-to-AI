import numpy as np
from skimage import io, color
import matplotlib.pyplot as plt
from k_means_adi import Colors, KMeansClustering
from sklearn.neighbors import NearestNeighbors  # for KDTree
from collections import Counter

five_colors = Colors('dogbasic.jpeg')
Image = io.imread('dogbasic.jpeg')
Image = color.convert_colorspace(Image, 'RGB', 'RGB')


def color_distance(rgb1, rgb2):
    redMean = (rgb1[0] + rgb2[0]) / 2  # take the mean of the red
    greenMean = (rgb1[1] + rgb2[1]) / 2
    blueMean = (rgb1[2] + rgb2[2]) / 2
    red = rgb1[0] - rgb2[0]
    green = rgb1[1] - rgb2[1]
    blue = rgb1[2] - rgb2[2]
    return np.sqrt((((512 + redMean) * red * red) / 2) + 4 * green * green + (((767 - redMean) * blue * blue) / 2))


def five_color(Image):
    fiveColorMethod = Image
    for i in range(fiveColorMethod.shape[0]):
        for j in range(fiveColorMethod.shape[1]):
            # initialize original minimum distance as a high number for comparison
            minimumDistance = float('inf')

            minColors = []
            red = fiveColorMethod[i, j, 0]
            blue = fiveColorMethod[i, j, 1]
            green = fiveColorMethod[i, j, 2]
            rgb = [red, blue, green]

            for colors in five_colors:
                numpyColors = np.array(colors)
                Distance = color_distance(numpyColors, rgb)
                if Distance < minimumDistance:
                    minimumDistance = Distance
                    minColors = colors
            R = minColors[0]
            G = minColors[1]
            B = minColors[2]
            fiveColorMethod[i, j, 0] = R
            fiveColorMethod[i, j, 1] = G
            fiveColorMethod[i, j, 2] = B
    return fiveColorMethod


fiveColorImage = five_color(Image)

# initialize BlackWhiteTraining by using rgb2gray using fiveColorImage
BlackWhiteTraining = color.rgb2gray(fiveColorImage[:, 0:int(fiveColorImage.shape[1] / 2), :])

BlackWhitePrediction = color.rgb2gray(Image[:, int(Image.shape[1] / 2):Image.shape[1], :])

ColorTraining = fiveColorImage[:, 0:int(fiveColorImage.shape[1] / 2), :]

RealColor = Image[:, int(Image.shape[1] / 2):Image.shape[1], :]

ColorPrediction = RealColor.copy()


def AverageColor(Image, XPoint, YPoint):
    # using surrounding pixels, get average color for that "patch"
    Patch = 1
    # take 3x3 cells as patch
    NeighboringCells = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    AllRedPixels = Image[XPoint, YPoint, 0]
    AllGreenPixels = Image[XPoint, YPoint, 1]
    AllBluePixels = Image[XPoint, YPoint, 2]
    PixelLength = Image.shape[0]
    PixelWidth = Image.shape[1]
    for cell in NeighboringCells:
        UpdatedXPoint = XPoint - cell[0]
        UpdatedYPoint = YPoint - cell[1]
        # check boundaries and make sure points are within limits
        if UpdatedXPoint < 0 or UpdatedXPoint >= PixelLength or UpdatedYPoint < 0 or UpdatedYPoint >= PixelWidth:
            continue
        AllRedPixels += Image[UpdatedXPoint, UpdatedYPoint, 0]
        AllGreenPixels += Image[UpdatedXPoint, UpdatedYPoint, 1]
        AllBluePixels += Image[UpdatedXPoint, UpdatedYPoint, 2]
        Patch += 1
    AverageReds = int(AllRedPixels / Patch)
    AverageGreens = int(AllGreenPixels / Patch)
    AverageBlues = int(AllBluePixels / Patch)
    return [AverageReds, AverageGreens, AverageBlues]


def AverageBlackAndWhite(Image, xPoint, yPoint):
    Patch = 1  # initially start with first patch
    PixelLength = Image.shape[0]
    PixelWidth = Image.shape[1]
    PixelArea = PixelLength*PixelWidth
    # using surrounding pixels, get average color for that "patch"
    NeighboringCells = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    AllRedPixels = Image[xPoint, yPoint] * 255
    AllGreenPixels = Image[xPoint, yPoint] * 255
    AllBluePixels = Image[xPoint, yPoint] * 255

    for cell in NeighboringCells:
        UpdatedXPoint = xPoint + cell[0]
        UpdatedYPoint = yPoint + cell[1]
        # check boundaries and make sure points are within limits
        if UpdatedXPoint < 0 or UpdatedXPoint >= PixelLength or UpdatedYPoint < 0 or UpdatedYPoint >= PixelWidth:
            continue
        updatedPixelValue = Image[UpdatedXPoint, UpdatedYPoint] * 255
        # increment pixel values for red green and blue pixels with the updated pixel value based on the new points
        AllRedPixels += updatedPixelValue
        AllGreenPixels += updatedPixelValue
        AllBluePixels += updatedPixelValue
        # increment patch to look at next one
        Patch += 1

    # CALCULATE AVERAGE FOR ALL PIXELS (R G B) where average is (total number of color pixel)/(number of patch)

    AverageRedPixels = int(AllRedPixels / Patch)
    AverageGreenPixels = int(AllGreenPixels / Patch)
    AverageBluePixels = int(AllBluePixels / Patch)
    return [AverageRedPixels, AverageGreenPixels, AverageBluePixels]


def BWAverages(Image):
    # initialize a dictionary of averages where keys are points and values are average black and white values for points
    Averages = {}
    for i in range(Image.shape[0]):
        for j in range(Image.shape[1]):
            Averages[(i, j)] = AverageBlackAndWhite(Image, i, j)
    return Averages


def RealVsPredicted(Actual, Prediction):
    # keep track when there is a difference between the true image and the predicted
    incorrectness_factor = 0
    for i in range(Actual.shape[0]):  # parse through length
        for j in range(Actual.shape[1]):  # parse through width
            if not np.array_equal(Actual[i, j], Prediction[i, j]):  # if there is a difference between points
                incorrectness_factor += 1
    area = Actual.shape[0] * Actual.shape[1]
    return (incorrectness_factor / area) * 100  # return incorrectness as a percentage


def BasicAgent(Image, BlackAndWhiteTraining, ColorTraining, ColorPrediction):

    print("Running Basic Agent")
    BlackWhiteAvg = BWAverages(BlackAndWhiteTraining)
    ListedBlackWhiteAvg = np.array(list(BlackWhiteAvg.keys()))

    """K-D TREE IMPLEMENTATION: PICK DIMENSION, FIND MEDIAN, SPLIT DATA, REPEAT
       FOR NEW DATA POINT, FIND REGION CONTAINING POINT AND COMPARE TO ALL POINTS IN THE REGION: """

    kdTree = NearestNeighbors(n_neighbors=6, algorithm='kd_tree')

    for i in range(Image.shape[0]):  # parse through length
        for j in range(Image.shape[1]):  # parse through width
            r = int(Image[i, j] * 255)
            g = int(Image[i, j] * 255)
            b = int(Image[i, j] * 255)
            # initially set match and iteration counter to false
            match = False
            iterate = 0
            # initialize an empty array that will be filled with matching points
            colorMatch = []

            while not match:
                # if color distance is less than or equal to 10, add point to color match list
                colorMatch = [a for a in ListedBlackWhiteAvg if color_distance(BlackWhiteAvg.get(tuple(a)), [r, g, b]) <= 10]
            # if color match list contains 5 or more points, then set match as true and exit the loop
                if len(colorMatch) >= 5:
                    match = True
                else:
                    if iterate > 10:
                        colorMatch = [a for a in ListedBlackWhiteAvg if
                                      color_distance(BlackWhiteAvg.get(tuple(a)), [r, g, b]) <= 30]
                        break
                iterate += 1

            kdTree.fit(colorMatch)
            closestNeighbors = kdTree.kneighbors([[i, j]], 6, return_distance=False)
            closestPoints = [ListedBlackWhiteAvg[y] for (x, y) in np.ndenumerate(closestNeighbors)]
            matchingColors = [BlackWhiteAvg.get(tuple(x))[0] for x in closestPoints]
            # create counter object to initialize count in matchingColors list
            colorCounter = Counter(matchingColors)
            dominantColor = max(colorCounter, key=lambda key: colorCounter[key])

            patch = [tuple(x) for x in closestPoints if BlackWhiteAvg.get(tuple(x))[0] == dominantColor]
            patch.sort()

            TargetRedPatch = ColorTraining[patch[0][0], patch[0][1], 0]
            TargetGreenPatch = ColorTraining[patch[0][0], patch[0][1], 1]
            TargetBluePatch = ColorTraining[patch[0][0], patch[0][1], 2]

            # set RGB prediction as ColorPrediction
            ColorPrediction[i, j, 0] = TargetRedPatch
            ColorPrediction[i, j, 1] = TargetGreenPatch
            ColorPrediction[i, j, 2] = TargetBluePatch

    return ColorPrediction


if __name__ == '__main__':
    ColorPrediction = BasicAgent(BlackWhitePrediction, BlackWhiteTraining, ColorTraining, ColorPrediction)
    print("Color has been predicted")

    # display width and height of figure in inches: set to be 20x20 but you can change it
    plt.figure(figsize=(20, 20))
    # subplot is defined as n-rows, n-columns, index
    plt.subplot(2, 1, 1)
    # create title for subplot
    plt.title('Recolored Image')
    # display recolored image
    plt.imshow(fiveColorImage)

    plt.subplot(2, 2, 3)
    # create title for subplot
    plt.title('Black and White Predicted Image')
    # display black and white predicted image
    plt.imshow(BlackWhitePrediction, cmap="gray")

    plt.subplot(2, 2, 4)
    # create title for subplot
    plt.title('Color Predicted Image')
    # display color predicted of the test data image
    plt.imshow(ColorPrediction)
    # display the percentage incorrectness for the real vs predicted image
    print("Percentage Incorrectness {}".format(RealVsPredicted(RealColor, ColorPrediction)) + "%")
    print("Percentage Correctness {}".format(100 - RealVsPredicted(RealColor, ColorPrediction)) + "%")
    plt.show()
