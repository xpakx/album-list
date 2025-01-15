import json
from collections import Counter
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib as mpl
import catppuccin

with open('../dist/albumy.json', 'r') as file:
    data = json.load(file)

ratings = [int(item['rating']) for item in data]

rating_counts = Counter(ratings)

ratings_sorted = sorted(rating_counts.items())
ratings_values = [item[0] for item in ratings_sorted]
counts = [item[1] for item in ratings_sorted]

mpl.style.use(catppuccin.PALETTE.mocha.identifier)
color = catppuccin.extras.matplotlib.load_color(catppuccin.PALETTE.mocha.identifier, "flamingo")

plt.bar(ratings_values, counts, tick_label=ratings_values, color=color)
plt.xlabel('Ratings')
plt.ylabel('Frequency')
plt.title('Distribution of Ratings')
plt.xticks(range(1, 11))
plt.show()

