#!/usr/bin/env python3

from datetime import datetime
import os
import xml.etree.ElementTree as ET

import matplotlib
import matplotlib.pyplot as plt

START = datetime(2020, 12, 1, 5)
PUZZLES = 25
DATADIR = '/home/marxin/Downloads/aoc2020'
THRESHOLD = 100
THRESHOLD2 = 1000

puzzles = {}
thresholds = {}

def parse_file(path, offset):
    for line in open(path).readlines():
        if '/2020/day' in line:
            root = ET.fromstring(line)
            day = int(root.text)
            if not day in puzzles:
                puzzles[day] = [(0, 0, 0)]
                thresholds[day] = [0, 0, 0, 0]
            both = int(root[0].text)
            first = int(root[1].text) + both
            tick = offset.total_seconds() / 60**2
            puzzles[day].append((tick, first, both))
            if thresholds[day][0] == 0 and first >= THRESHOLD:
                thresholds[day][0] = tick
            if thresholds[day][1] == 0 and both >= THRESHOLD:
                thresholds[day][1] = tick
            if thresholds[day][2] == 0 and first >= THRESHOLD2:
                thresholds[day][2] = tick
            if thresholds[day][3] == 0 and both >= THRESHOLD2:
                thresholds[day][3] = tick

def generate_users_for_puzzle(p):
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot([x[0] for x in puzzles[p]], [x[1] for x in puzzles[p]], label='One star')
    ax.plot([x[0] for x in puzzles[p]], [x[2] for x in puzzles[p]], label='Two stars')
    ax.legend()
    ax.set_title('Day 1 - stars for users')
    ax.set_xlabel('Time (in hours)')
    ax.set_ylabel('Users')
    ax.grid(True)
    plt.savefig(f'puzzle{p:02d}-users.svg')

def generate_first_N(N, index):
    width = 0.35
    fig, ax = plt.subplots(figsize=(10, 5))
    labels = [f'Day {x}' for x in puzzles.keys()]

    name = 'one star' if index % 2 == 0 else 'two stars'
    y = [x[index] for x in thresholds.values()]
    ax.bar(labels, y, label=f'First {N} ({name})')
    ax.legend()
    ax.set_ylabel('Time (in hours)')
    name = 'one-star' if index % 2 == 0 else 'two-stars'
    filename = f'first-{N}-{name}.svg'
    plt.savefig(filename)

for f in sorted(os.listdir(DATADIR)):
    stamp = f.split('.')[0]
    datestamp = datetime.fromisoformat(stamp)
    if datestamp > START:
        parse_file(os.path.join(DATADIR, f), datestamp - START)

for puzzle in puzzles.keys():
    generate_users_for_puzzle(puzzle)

# generate first N bars
generate_first_N(THRESHOLD, 0)
generate_first_N(THRESHOLD, 1)

generate_first_N(THRESHOLD2, 2)
generate_first_N(THRESHOLD2, 3)

with open('README.md', 'w') as readme:
    for day in puzzles.keys():
        readme.write('# Day 1\n')
        readme.write(f'![](/puzzle{day:02d}-users.svg "Day {day}")\n')
    readme.write('# Advent of Code 2020 Statistics\n')
    readme.write('## First 100 users\n')
    readme.write('![](/first-100-one-star.svg "First 100 users (one star)")\n')
    readme.write('![](/first-100-two-stars.svg "First 100 users (two stars)")\n')
    readme.write('## First 1000 users\n')
    readme.write('![](/first-1000-one-star.svg "First 1000 users (one star)")\n')
    readme.write('![](/first-1000-two-stars.svg "First 1000 users (two stars)")\n')
