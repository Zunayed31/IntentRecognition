import googlemaps, re, g4f, json, polyline, math

gmaps = googlemaps.Client(key='AIzaSyDVS9S2Txb-yhzTW2YkB7ZSSIMUw5EIGsU')

#################################################################################
# Function to create points for the base route
def calcRoute(og, ds, arr):
    route = gmaps.directions(og, ds)
    points = polyline.decode(route[0]['overview_polyline']['points'])
    max = math.floor(len(points) / 20)
    if max == 0:
        max = 1
    for k in range(0, len(points), max):
        if len(pointsArr[arr]) < 20:
            pointsArr[arr].append(points[k])

#################################################################################
# Function to create points for the base route (different approach)
# def calcRoute2(og, ds, arr):
#     route = gmaps.directions(og, ds)
#     points = polyline.decode(route[0]['overview_polyline']['points'])
#     for k in range(0, len(points)):
#         pointsArr[arr].append(points[k])

#################################################################################
# Function to create points for the observation route
def obsCalcRoute(og, ds, arr, way):
    route = gmaps.directions(og, ds, waypoints=way)
    points = polyline.decode(route[0]['overview_polyline']['points'])
    max = math.floor(len(points) / 20)
    if max == 0:
        max = 1
    for k in range(0, len(points), max):
        if len(pointsArr[arr]) < 20:
            pointsArr[arr].append(points[k])

#################################################################################
# Function to create points for the observation route (different approach)
# def obsCalcRoute2(og, ds, arr, way):
#     route = gmaps.directions(og, ds, waypoints=way)
#     points = polyline.decode(route[0]['overview_polyline']['points'])
#     for k in range(0, len(points)):
#         pointsArr[arr].append(points[k])

#################################################################################
# Calculating the difference between the points
def similarity(arr1, arr2, intendArr):
    flag = False
    bonus = 0
    sum = 0
    if intendArr:
        for l in range(0, len(intendArr)):
            for point in arr2: 
                if abs(intendArr[l][0] - point[0]) <= 0.005 and abs(intendArr[l][1] - point[1]) <= 0.005:
                    flag = True
                    bonus += 1
                    break

    for i in range(min((len(arr1)),len(arr2))):
        sum += max(abs(arr1[i][0]),abs(arr2[i][0])) - min(abs(arr1[i][0]),abs(arr2[i][0]))
        sum += max(abs(arr1[i][1]),abs(arr2[i][1])) - min(abs(arr1[i][1]),abs(arr2[i][1]))
    
    if flag:
        sum = sum - (0.05 * (1 + bonus*(0.5)))
        if sum <= 0:
            sum = 0.0 

    return round(sum, 2)  

#################################################################################
# # Calculating similiraty by checking the number of points that are the same
# def similarity2(arr1, arr2):
#     set1 = set(arr1)
#     set2 = set(arr2)
#     common = len(set1.intersection(set2))
#     percent = (common/(max(len(arr1),len(arr2))))*100
#     return percent

# Reading the JSON file
with open('goals_data2.json') as f:
    data = json.load(f)

file = open("results2.txt", "w")

# Setting up variables
truePositiveG2 = 0
falsePositiveG2 = 0
truePositiveG5 = 0
falsePositiveG5 = 0
truePositiveG10 = 0
falsePositiveG10 = 0
truePositiveG15 = 0
falsePositiveG15 = 0
pattern = r'\((-?\d+\.\d+), (-?\d+\.\d+)\)'


# Main loop
for i in range(0, len(data)):
    origin = data[i]['initial']
    goals = data[i]['goals']
    obs = data[i]['observations']
    loop = len(goals)
    pointsArr = []
    compArr = []
    intendMessage = f"""Find me 3 key waypoint needed to go through along the shortest and fastest route between {origin} and {data[i]['intent_goal']}.
                Give these waypoints as (latitude,longitude). """
    intendResponse = g4f.ChatCompletion.create(
        model="airoboros-70b",
        provider=g4f.Provider.DeepInfra,
        messages=[{"role": "user",
                    "content": intendMessage}],
        stream=False,
    )

    intendMatches = re.findall(pattern, intendResponse)
    intendCoordinates = [(float(lat), float(lon)) for lat, lon in intendMatches]
    while len(intendCoordinates) > 1:
        intendCoordinates.pop()


    for x in range(loop):
        pointsArr.append([])
        pointsArr.append([])
    for j in range (0, len(goals)):
        destination = data[i]['goals'][j]
        calcRoute(origin, destination, j)
        obsCalcRoute(origin, destination, j+len(goals), obs)
        compArr.append([destination,similarity(pointsArr[j],pointsArr[j+loop], intendCoordinates)])
    # print(data[i]['id'])
    minName = min(compArr, key=lambda x: x[1])[0]
    print(compArr)
    file.write(str(compArr) + '\n')
    if minName == data[i]['intent_goal'] or (compArr[j][1] == 0):
        if ".2." in data[i]['id']:
            truePositiveG2 += 1
        elif ".5." in data[i]['id']:
            truePositiveG5 += 1
        elif ".10." in data[i]['id']:
            truePositiveG10 += 1
        elif ".15." in data[i]['id']:
            truePositiveG15 += 1
    else:
        if ".2." in data[i]['id']:
            falsePositiveG2 += 1
        elif ".5." in data[i]['id']:
            falsePositiveG5 += 1
        elif ".10." in data[i]['id']:
            falsePositiveG10 += 1
        elif ".15." in data[i]['id']:
            falsePositiveG15 += 1

    

print('####################################################')
print("Goals: 2")
print("True positives: " + str(truePositiveG2))
print("False positives: " + str(falsePositiveG2))
print("Percentage: " + str(truePositiveG2/(truePositiveG2+falsePositiveG2)))
print('####################################################')
print("Goals: 5")
print("True positives: " + str(truePositiveG5))
print("False positives: " + str(falsePositiveG5))
print("Percentage: " + str(truePositiveG5/ (truePositiveG5+falsePositiveG5)))
print('####################################################')
print("Goals: 10")
print("True positives: " + str(truePositiveG10))
print("False positives: " + str(falsePositiveG10))
print("Percentage: " + str(truePositiveG10/(truePositiveG10+falsePositiveG10)))
print('####################################################')
print("Goals: 15")
print("True positives: " + str(truePositiveG15))
print("False positives: " + str(falsePositiveG15))
print("Percentage: " + str(truePositiveG15/(truePositiveG15+falsePositiveG15)))
