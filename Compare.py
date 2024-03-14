import googlemaps, json, polyline, math

gmaps = googlemaps.Client(key='AIzaSyDVS9S2Txb-yhzTW2YkB7ZSSIMUw5EIGsU')

#################################################################################
# Function to create points for the base route
def calcRoute(og, ds, arr):
    route = gmaps.directions(og, ds)
    dd = polyline.decode(route[0]['overview_polyline']['points'])
    max = math.floor(len(dd) / 20)
    if max == 0:
        max = 1
    for k in range(0, len(dd), max):
        if len(pointsArr[arr]) < 20:
            pointsArr[arr].append(dd[k])

#################################################################################
# Function to create points for the observation route
def obsCalcRoute(og, ds, arr, way):
    route = gmaps.directions(og, ds, waypoints=way)
    dd = polyline.decode(route[0]['overview_polyline']['points'])
    max = math.floor(len(dd) / 20)
    if max == 0:
        max = 1
    for k in range(0, len(dd), max):
        if len(pointsArr[arr]) < 20:
            pointsArr[arr].append(dd[k])

#################################################################################
# Calculating the difference between the points
def similarity(arr1, arr2):
    sum = 0
    for i in range(min((len(arr1)),len(arr2))):
        sum += abs(abs(max(arr1[i][0],arr2[i][0])) - abs(min(arr1[i][0],arr2[i][0]))) 
        sum += abs(abs(max(arr1[i][1],arr2[i][1])) - abs(min(arr1[i][1],arr2[i][1]))) 
    return sum    

# Reading the JSON file
with open('goals_data2.json') as f:
    data = json.load(f)

pointsArr = []

# Main loop
for i in range(0, len(data)):
    origin = data[i]['initial']
    goals = data[i]['goals']
    obs = data[i]['observations']
    loop = len(goals)
    pointsArr = []
    compArr = []
    for x in range(loop):
        pointsArr.append([])
        pointsArr.append([])
        compArr.append([])
    for j in range (0, len(goals)):
        destination = data[i]['goals'][j]
        calcRoute(origin, destination, j)
        obsCalcRoute(origin, destination, j+len(goals), obs)
        compArr[j].append(similarity(pointsArr[j],pointsArr[j+loop]))
    print(data[i]['id'])
    print(compArr)
    # print(pointsArr)
    # print(dd)
    # print(route)

# print(pointsArr)
# print(len(pointsArr))

