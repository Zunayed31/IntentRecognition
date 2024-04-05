import g4f, re

initial = 'Kilburn Building'
goal = 'Manchester Picadilly station'
observation = [(53.4675, -2.2336), (53.4672, -2.234), (53.468, -2.2365), (53.4673, -2.238), (53.4674, -2.2392), (53.4712, -2.2394), (53.4729, -2.2363), (53.4772, -2.2362), (53.4775, -2.2313)]

# Set with provider
message = f"""Find me a path that crosses the following {observation} key waypoints along the shortest and fastest route between {initial} and {goal} station.
                Give these waypoints as (latitude, longitude). 
                They do not have to be significant landmarks."""
response = g4f.ChatCompletion.create(
    model="gpt-4",
    provider=g4f.Provider.Bing,
    messages=[{"role": "user",
                "content": message}],
    stream=False,
)

pattern = r'\((-?\d+\.\d+), (-?\d+\.\d+)\)'

# Find all matches of the pattern in the text
matches = re.findall(pattern, response)

# Extract latitude and longitude coordinates and store them in an array
coordinates = [(float(lat), float(lon)) for lat, lon in matches]

# Print the array of coordinates
print(coordinates)

print(response)