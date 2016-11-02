# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 17:10:56 2016

"""
import sys
import getopt
import matplotlib.pyplot as plt
import numpy as np

'''
------------------------------------- USAGE -----------------------------------
Commandline:
    > python filename.py -i [input_data] -o outputfile.extension
From python file:
    import GraphImport
    argv = ['', '-i', [input_data], '-o', outputfile.extension, etc] 
    GraphImport.main(argv)
    
Extra options:
    -x takes [x_begin, x_end] to defines the graph's interval on the x-axis
    -y takes [y_begin, y_end] to defines the graph's interval on the y-axis
    --xti takes an integer to define the interval between ticks on the x-axis
    --yti takes an integer to define the interval between ticks on the x-axis
    --lc takes a string containing either a hexadecimal colorcode or the name
        of that color to define the line's color

If further customization is necessary, parameters in GraphImport.py must be 
changed manually.

-------------------------------------------------------------------------------
'''

###################### Parameters start ###########################

#choose from "line", "dot", "linedot"
graph_style = "linedot" 

#define the scope of the graph. 
#Graph will show in interval <x_start, x_end> where it is inside 
# the y values below
x_start = 0
x_end = 10
y_start = 0
y_end = 10

#If set to True, the graph will not be shown in the scope, defined 
# above, but will zoom automatically
adjust_zoom_to_graph = False 
#Dimensions of the screen (in inches)
frame_width = 10 
frame_height = 6
dots_per_inch = 8 

special_tick_labels = False
#If the special_tick_labels is set to true, the labels in the special_ticks 
# arrays, corresponding with the locations in one of the special_ticks_locations 
# arrays, are shown. Otherwise the integers in the defined scope will 
# be used, with an interval of tick_interval (below)
special_ticks_X_locations = [1]
special_ticks_X = ['$\pi$']
special_ticks_Y_locations = [2]
special_ticks_Y = ['tja']

y_tick_interval = 1
x_tick_interval = 1

#Colour of the line (either the name of the color or the hexadecimal code)
#for example: both 'red' and '#FF0000' would work
line_color = 'red' 
line_width = '2.5' #in pixels

###################### Parameters end #############################


def usage():
    print("\n\n\n", "-"*35, "USAGE", "-"*35, "\n" )
    print(" Commandline excecution:")
    print("\t > python filename.py -i [input_data] -o output_filename\n")
    print("\n", "-"*77, "\n")
    
def valid_tick_array(labels, locations):
    #Checks wether 
    # 1) the locations of the special_tick arrays are of type 'float'
    # 2) the amount of labels is the same as the amount of locations

    labels = [str(i) for i in labels]
    try:
        locations = [float(i) for i in locations]
    except ValueError:
        return False
    return (len(labels) == len(locations))
    
def valid_input_data(data):
    #checks wether data is a list consisting of lists of two numbers    
    if not type(data) is list:
        return False
    for element in data:
        if not ((type(element) is list) and (len(element) == 2)):
            return False 
        elif not (type(element[0]) is int or type(element[0]) is float)\
                or not (type(element[1]) is int or type(element[1]) is float):
            return False
    return True

def seperate_x_y(data):
    #converts data to separate x and y lists
    x = [coordinate[0] for coordinate in data]
    y = [coordinate[1] for coordinate in data]
    return (x, y)

def define_axis():
    axis = plt.gca()
    axis.spines['right'].set_color('none')
    axis.spines['top'].set_color('none')
    
    axis.xaxis.set_ticks_position('bottom')
    axis.spines['bottom'].set_position(('data', 0))
    
    axis.yaxis.set_ticks_position('left')
    axis.spines['left'].set_position(('data', 0))
    
    return axis 
    
def get_options():
    pass
            
def main(argv):
    ''' 
        Gets the data from the commandline (or other pythonfile).
        Checks wether data is valid
    '''
    try:
        opts, args = getopt.getopt(argv[1:], "i:o:x:y:", ["xti=", "yti=", "lc="])      
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    output_file = ""
    for option, argument in opts:
        if option == "-i":
            own_dataset = argument 
            if not valid_input_data(own_dataset):
                print("\n ERROR: invalid input data!")
                usage()
                sys.exit(2)
        elif option == "-o":
            output_file = argument
            if output_file == "":
                print("\n ERROR: invalid outputfile")
                usage()
                sys.exit(2)
        elif option == "-x":
            if(len(argument) == 2):
                x_start = argument[0]
                x_end = argument[1]
            else:
                print("\n ERROR: Invalid input regarding '-x'")
                usage()
                sys.exit(2)
        elif option == "-y":
            if(len(argument) == 2):
                y_start = argument[0]
                y_end = argument[1]
            else:
                print("\n ERROR: Invalid input regarding '-y'")
                usage()
                sys.exit(2)
        elif option == "--xti":
            x_tick_interval = argument
        
        elif option == "--yti":
            y_tick_interval = argument
    
    '''    
    own_dataset consisted of [x, y] lists. separate_x_y() converts it to 
    seperate lists
    '''    
    x, y = seperate_x_y(own_dataset)      
    plt.figure(figsize=(frame_width, frame_height), dpi = dots_per_inch)     
    
    axis = plt.gca()
    axis.spines['right'].set_color('none')
    axis.spines['top'].set_color('none')
    
    axis.xaxis.set_ticks_position('bottom')
    axis.spines['bottom'].set_position(('data', 0))
    
    axis.yaxis.set_ticks_position('left')
    axis.spines['left'].set_position(('data', 0))
    
    plt.xlim(min(x)*1.1, max(x)*1.1)
    plt.ylim(min(y)*1.1, max(y)*1.1)
       
    
    if ( special_tick_labels
            and valid_tick_array(special_ticks_X, special_ticks_X_locations)
            and valid_tick_array(special_ticks_Y, special_ticks_Y_locations) ):
        #Adds the special ticks when necessary and valid
        plt.xticks(special_ticks_X_locations, special_ticks_X)
        plt.yticks(special_ticks_Y_locations, special_ticks_Y)
    else:
        x_tick_locations = np.linspace(x_start, x_end, (abs(x_start)+abs(x_end))/x_tick_interval + 1)
        plt.xticks(x_tick_locations, [str(x) for x in x_tick_locations])
            
        y_tick_locations = np.linspace(y_start, y_end, (abs(y_start)+abs(y_end))/y_tick_interval + 1)
        plt.yticks(y_tick_locations, [str(y) for y in y_tick_locations])
    
    
    if(graph_style == "dot"):
        plt.scatter(x, y, marker="o", color=line_color)
    elif(graph_style == "linedot"):
        plt.plot(x, y, color=line_color, linewidth=line_width, marker="o")
    else:
        plt.plot(x, y, color=line_color, linewidth=line_width, marker="")
        
    plt.savefig(output_file)   # save the figure to file
 
if __name__ == "__main__":
    main(sys.argv)


