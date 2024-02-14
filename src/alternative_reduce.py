#!/usr/bin/env python3
import argparse
import os
import json
import matplotlib
# Configure matplotlib to work without a display environment
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import datetime
from collections import defaultdict

# Parse command line arguments for hashtags
parser = argparse.ArgumentParser(description='Analyze and visualize hashtag trends over time.')
parser.add_argument('hashtags', nargs='+', help='Hashtags to analyze (include "#").')
parsed_args = parser.parse_args()

# Prepare a dictionary to hold aggregated counts
aggregate_counts = defaultdict(lambda: defaultdict(int))

# Define the directory containing tweet data
data_directory = 'outputs'

# Identify files within the data directory
file_list = [file_name for file_name in os.listdir(data_directory) if file_name.endswith('.zip.lang')]

# Data extraction and aggregation loop
for file_name in file_list:
    # Parse the date from the filename using a fixed format
    date_portion = file_name[10:18]
    date_parsed = datetime.datetime.strptime(date_portion, '%y-%m-%d').date()

    # Open and load the JSON data
    with open(os.path.join(data_directory, file_name), 'r') as file_handle:
        tweet_data = json.load(file_handle)

        # Sum up the counts for each hashtag on each day
        for tag in parsed_args.hashtags:
            tag_lower = tag.lower()  # Normalize the hashtag to lowercase
            tag_count = sum(tweet_data.get(tag_lower, {}).values())
            aggregate_counts[tag_lower][date_parsed] += tag_count

# Generate a concise filename for the output plot
filename_tags = "_".join(tag.strip('#').lower() for tag in parsed_args.hashtags)[:50]
output_filename = f"trends_{filename_tags}.png"

# Plot configuration
plt.figure(figsize=(10, 6))

# Consolidate all unique dates from the dataset for the x-axis
unique_dates = sorted({day for count_dict in aggregate_counts.values() for day in count_dict})

# Create a plot for each hashtag
for hashtag, day_counts in aggregate_counts.items():
    tweet_counts = [day_counts.get(day, 0) for day in unique_dates]
    plt.plot(unique_dates, tweet_counts, label=hashtag)

# Customize the plot appearance
plt.xlabel('Date')
plt.ylabel('Tweet Volume')
plt.title('Hashtag Popularity Over Time')
plt.legend(loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()

# Save the figure and notify user
plt.savefig(output_filename)
print(f"Generated plot is saved as '{output_filename}'.")

