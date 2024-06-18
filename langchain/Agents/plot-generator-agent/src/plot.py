import matplotlib.pyplot as plt

# Data for the number of games won by the Golden State Warriors in the last 2 NBA seasons
seasons = ['2019-2020', '2020-2021']
games_won = [15, 39]

# Create a bar plot
plt.figure(figsize=(10, 6))
plt.bar(seasons, games_won, color='blue')

# Add title and labels
plt.title('Number of Games Won by the Golden State Warriors in the Last 2 NBA Seasons')
plt.xlabel('Season')
plt.ylabel('Number of Games Won')

# Show plot
plt.show()