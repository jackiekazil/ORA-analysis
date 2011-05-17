#!/usr/bin/env python

#TODO: Finish conversion. Pull shared functions out to utils.

import fileinput, glob, os, re, sys
import matplotlib.pyplot as plt
import pylab

# sys.argv[1] == location of data
# sys.argv[2] == desired location of output
# sys.argv[3] ==

def find_points(data):
    point_list = []
    for value in data:
        point_list.append((value[0], value[2]))
    return point_list

def get_color(party):
    if group == 'group2':
        color = 800
    elif group == 'group1':
        color = 075
    return color

def create_graph(first_key, first_data, second_key, second_data, include_non_pairs=False):

    x_vals = []
    y_vals = []
    colors = []
    labels = []

    # Find all combos of versions & groups that should be uniquely considered.
    points1 = set(find_points(first_data))
    points2 = set(find_points(second_data))

    # Find the intersection & add those points
    crossover_points = points1.intersection(points2) # Items in both i & j
    points1_only = points1.difference(points2)
    points2_only = points2.difference(points1)

    # Clean up.

    for point in crossover_points:
        for value1 in first_data:
            for value2 in second_data:
                if point[0] == value1[0] == value2[0]:
                    if point[1] == value1[2] == value2[2]:
                        x_vals.append(float(value1[1]))
                        y_vals.append(float(value2[1]))
                        colors.append(get_color(point[1]))
                        labels.append(point[0])

    if include_non_pairs == True:
        for point in points1_only:
            for value1 in first_data:
                 if point[0] == value1[0]:
                    if point[1] == value1[2]:
                        x_vals.append(float(value1[1]))
                        y_vals.append(float(0))
                        colors.append(get_color(point[1]))
                        labels.append(point[0])

        for point in points1_only:
            for value2 in second_data:
                 if point[0] == value2[0]:
                    if point[1] == value2[2]:
                        x_vals.append(float(0))
                        y_vals.append(float(value2[1]))
                        colors.append(get_color(point[1]))
                        labels.append(point[0])


    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(color='#DDDDDD')

    ax.scatter(x_vals, y_vals, label=labels, c=colors, alpha=0.50, s=65)

    ax.set_xlabel(first_key)
    ax.set_ylabel(second_key)

    file_name = sys.argv[2] + '/' + first_key + '_by_' + second_key + '.png'
    plt.savefig(file_name)
    plt.close()

def check_ifequal(list):
    for item in list[1:]:
        if item != list[0]:
            return False
        return True

if __name__ == '__main__':

    save_dir(sys.argv[2])
    path = sys.argv[1]

    print os.listdir(path)

    #Get start & stop points
    for infile in glob.glob( os.path.join(path, '*') ):
        line_before_start = last_line = 0
        for line in fileinput.input(infile):
            line = line.rstrip()
            if not line.strip():
                continue

            l_lstrip = line.lstrip()

            # Get line number of breaking point to start read
            if l_lstrip == 'Network-Level Measure                    Value':
                line_before_start = fileinput.lineno() + 1

            if l_lstrip == 'Node-Level Measure                       Avg        Stddev     Min/Max    Min/Max Nodes':
                last_line = fileinput.lineno()

    data_points = {}
    for infile in glob.glob( os.path.join(path, '*') ):

        # TODO: Make generic
        # Get more info on ORA saving methods.
        # Find all variations in files, then assign colors to each of them.
        version_match = re.search("\d{2,3}", infile)
        version = version_match.group()

        #TODO: regex
        if 'group1' in infile:
            group = 'group1'
        elif 'group2' in infile:
            group = 'group2'
        else:
            print "There is a problem with parsing group names from your file names. Please review your naming conventions and file organization."

        counter = 0 #Line count
        for line in fileinput.input(infile):
            counter+=1

            line = line.rstrip()
            if not line.strip():
                continue

            l_lstrip = line.lstrip()

            if last_line > counter > line_before_start:
                #print counter, len(l_lstrip), line

                line_items = l_lstrip.split()
                value = line_items.pop()
                text = ' '.join(line_items)
                data_pt = (version, value, group)

                try:
                    data_points[text].append(data_pt)
                except KeyError:
                    data_points[text] = [data_pt]

    # Remove data_points sets that all have the same value, b/c they are uninteresting.
    for k,v in data_points.items():
        possible_values = []
        for value in v:
            possible_values.append(value[1])

        if check_ifequal(possible_values) == True:
            del data_points[k]
        else:
            continue

    for k, v in data_points.items():
        print v[2]
    for k1,v1 in data_points.items():
        for k2,v2 in data_points.items():

            #TODO? Offer option to get rid of duplicate graphs where the x & y are flipped.

            # Make sure we aren't creating graphs that plot against themselves.
            if k1 != k2:
                try:
                    create_graph(k1,v1,k2,v2, sys.argv[3])
                except IndexError:
                    create_graph(k1,v1,k2,v2)
