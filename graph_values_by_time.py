#!/usr/bin/env python

#TODO: Finish conversion. Pull shared functions out to utils.

import fileinput, glob, os, re, sys
import matplotlib.pyplot as plt
import pylab

#NOTE: So much cleaning up to do.

def create_graph(measurement, data):

    x_vals = []
    y_vals = []
    colors = []

    for value in data:
        x_vals.append(float(value[0]))
        y_vals.append(float(value[1]))

        if value[2] == 'group2':
            color = 800
        elif value[2] == 'group1':
            color = 075

        colors.append(color)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x_vals, y_vals, c=colors, alpha=0.50, s=65)

    file_name = sys.argv[2] + '/' + measurement + '.png'
    plt.savefig(file_name)
    plt.close()


if __name__ == '__main__':

    save_dir(sys.argv[2])
    path = sys.argv[1]


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
        counter = 0

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
                data_pt = (congress, value, party)

                try:
                    data_points[text].append(data_pt)
                except KeyError:
                    data_points[text] = [data_pt]

    for k,v in data_points.items():
        create_graph(k,v)
