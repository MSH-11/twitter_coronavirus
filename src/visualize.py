#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path',required=True)
parser.add_argument('--key',required=True)
parser.add_argument('--percent',action='store_true')
args = parser.parse_args()

# imports
import os
import json
from collections import Counter,defaultdict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# open the input path
with open(args.input_path) as f:
    counts = json.load(f)

# normalize the counts by the total values
if args.percent:
    for k in counts[args.key]:
        counts[args.key][k] /= counts['_all'][k]

# print the count values
items = sorted(counts[args.key].items(), key=lambda item: (item[1],item[0]), reverse=True)
top_items = items[:10]

for k,v in items:
    print(k,':',v)


# Extracting keys and values for plotting
keys = [item[0] for item in top_items]
values = [item[1] for item in top_items]

# Create a bar graph
plt.bar(keys, values)

if args.input_path[-1] == 'g':
    plt.xlabel('language')
    plt.title(f'Number of Tweets including {args.key} by language')
else:
    plt.xlabel('country')
    plt.title(f'Number of Tweets including {args.key} by country')

plt.ylabel('Count')

# Save the plot to a PNG file
if args.input_path[-1] == 'g':
    plt.savefig(f'{args.key}_language.png')
else:
    plt.savefig(f'{args.key}_country.png')

