


# Written by Oren Ben-Moshe, 308249754
# This program will take an input file that should include x, dx, y, dy and will process
# the data given into one final linear fit graph. It will, in addition, provide the fitting parameters
# a, b, da, db, and chi^2 and chi^2 reduced.

# PLEASE NOTE: In order to run the program, it is necessary to have the PyPlot addon installed for the PyCharm project.
# In addition, all of the equations provided for this project were all given in the project instructions PDF.


def fit_linear(filename):

    # First, we have to check if the data is given as columns or as rows.

    colsorrows = columns_or_rows(filename)

    if not colsorrows:
        V_dic = columns_handle(filename)
    elif colsorrows:
        V_dic = rows_handle(filename)

    # Next, we have to make sure all uncertainties are positive and that the data sets match.

    datamatch = check_1(V_dic)

    # If the data is not good to use, an error will be printed. Otherwise, the program continues.

    if datamatch == True:

        ab_values = find_ab(V_dic)
        chi_squared(V_dic, ab_values)
        graph(V_dic, ab_values)

    elif type(datamatch) == str:
        print(datamatch)




def rows_handle(filename):

    # This is the rows handling function.
    # It is going to read from the file and return a dictionary that includes x, y, dx, dy,
    # Axis titles and the data length.

    file_pointer = open(filename, 'r')
    data = file_pointer.read()
    file_pointer.close()

    splitdata = data # Making a 2nd set of the data, the second one will be used to create the dictionary.

    splitdata = splitdata.splitlines()

    # Using caseload method to make handling easier (reason for the 2nd copy of data)
    # Converting the data into a list of lines.

    data = data.casefold()
    data = data.splitlines()
    file_pointer.close()

    # Defining the dictionary that will be returned to the main function

    rows_dic = {'x': [], 'dx': [], 'y': [], 'dy': []}

    def append_1(f_str, w_line):

        # This inside function accepts the iterated line and a string.
        # Using the string which corresponds to a key this function will append the line contents to the dic.

        for i in w_line.split(' ')[1:]:

            # Getting rid of leftover string characters so we do not append them.

            try:
                rows_dic[f_str].append(float(i))
            except ValueError:
                continue

    for line in data:

        # Checking which line we need to refer to and appending to the right key.

        if line.startswith('x'):
            if line.startswith('x axis'):

                # Using the index from the line in the first data set we use splitdata to add to our main dic.

                rows_dic["".join(splitdata[data.index(line)].split(' ')[0:2])] = " ".join(
                    splitdata[data.index(line)].split(' ')[2:])

            else:
                append_1('x', line)

        if line.startswith('y'):
            if line.startswith('y axis'):

                # Using the index from the line in the first data set we use splitdata to add to our main dic.

                rows_dic["".join(splitdata[data.index(line)].split(' ')[0:2])] = " ".join(
                    splitdata[data.index(line)].split(' ')[2:])

            else:
                append_1('y', line)

        if line.startswith('dx'):
            append_1('dx', line)

        if line.startswith('dy'):
            append_1('dy', line)

    # Adding the data set length value to the dic.

    Tlen = len(rows_dic['x'])
    rows_dic['Tlen'] = Tlen


    return rows_dic


def check_1(V_dic):

    # This function takes the dictionary from columns_handle or rows_handle.
    # It will print an error and return False if the data lengths do not match or if
    # we have negative uncertainties. Otherwise, it will return True.

    Tlen = V_dic['Tlen']
    if len(V_dic['y']) != Tlen or len(V_dic['dx']) != Tlen or len(V_dic['dy']) != Tlen:
        return "Input file error: Data lists are not the same length."

    # Checking if all uncertainties are positive

    for d in V_dic['dx']:
        if float(d) <= 0:
            return "Input file error: Not all uncertainties are positive."

    for d in V_dic['dy']:
        if float(d) <= 0:
            return "Input file error: Not all uncertainties are positive."

    else:
        return True



def columns_handle(filename):  # notice the input - "filename"

    # This is the columns handling function.
    # It is going to read from the file and return a dictionary that includes x, y, dx, dy,
    # Axis titles and the data length.

    file_pointer = open(filename, 'r')
    data = file_pointer.read()
    file_pointer.close()

    splitdata = data # Making a 2nd set of the data, the second one will be used to create the dictionary.
    splitdata = splitdata.splitlines()
    data = data.casefold()
    data = data.splitlines()

    d_names = data[0].split(' ')

    # Using the above list we'll make a new dic with corresponding keys.

    cols_dic = {d_names[0]: [], d_names[1]: [], d_names[2]: [], d_names[3]: []}

    # The function will iterate through the line-list, appending flouts to our dic.
    # It will keep going until it receives an error, which means it has reached the graph axis titles.
    # Using the error index, it will know where to take the axis titles from.

    for line in data[1:]:
        try:
            float(line[0])
            line = line.split(' ')
            for i in range(len(line)):
                try:
                    cols_dic[d_names[i]].append(float(line[i]))
                except ValueError:
                    continue

        except ValueError:
            stoped = data.index(line)
            break
        except IndexError:
            stoped = data.index(line) + 1

            break

    # Using the index of the error, we know where we should take the axis titles from.
    # We'll use the ones in splitdata, which wasn't casefolded.

    for line2 in splitdata[stoped:]:
        line2 = line2.split(' ')
        cols_dic["".join(line2[0:2])] = " ".join(line2[2:])

    # Adding the data set length value to the dic.

    Tlen = len(cols_dic['x'])
    cols_dic['Tlen'] = Tlen

    return cols_dic



def columns_or_rows(filename):

    # This function will read the content of given file, strips "tabs" that might be there from Excel
    # data pasting and then the function will replace the old content with the newer one.
    # The function will then determine which type of data was entered.
    # If theres an error, it will call columns_handle. Otherwise, it will call rows_handle.

    file_pointer = open(filename, 'r+')
    data = file_pointer.read()
    data = data.replace('\t', ' ')  # removing any tabs left from excel
    file_pointer.seek(0)
    file_pointer.truncate()  # removing original data
    file_pointer.seek(0)
    file_pointer.write(data)  # writing new data without tabs
    file_pointer.close()
    data = data.casefold()  # changing all letters to lowercase so it'll be easier to handel
    data = data.splitlines()  # splitting the text into a list of lines

    f_line = data[0].split(' ')  # looking at the first line without spaces

    # This function checks if there are any numbers in the first line of the text.
    # In order to do so, it will try and convert the first line into a floating number.
    # Based on its' success we would know which type of file was given to it.

    for n in f_line:
        try:
            float(n)
            return True
        except ValueError:
            continue
    return False


def find_ab(V_dic):

    # This function accepts a dictionary and returns the linear fit, as a list.

    sum_1 = 0  # sum of 1/dy
    sum_2 = 0  # sum of xy/dy
    sum_3 = 0  # sum of x/dy
    sum_4 = 0  # sum of y/dy
    sum_5 = 0  # sum of x^2/dy
    d_len = V_dic['Tlen']  # length of data set

    for i in range(d_len):

        # Please note that all of the mentioned equations are listed in the project instructions page.
        # Calculating vars of equations (4), (5).
        # The variables are calculated using equation (6)

        sum_1 += (1 / ((V_dic['dy'][i]) * (V_dic['dy'][i])))
        sum_2 += ((V_dic['x'][i] * V_dic['y'][i]) / ((V_dic['dy'][i]) * (V_dic['dy'][i])))
        sum_3 += ((V_dic['x'][i]) / ((V_dic['dy'][i]) * (V_dic['dy'][i])))
        sum_4 += ((V_dic['y'][i]) / ((V_dic['dy'][i]) * (V_dic['dy'][i])))
        sum_5 += (((V_dic['x'][i]) * (V_dic['x'][i])) / ((V_dic['dy'][i]) * (V_dic['dy'][i])))

    # Equation (4)
    a = (((sum_2 / sum_1) - ((sum_3 / sum_1) * (sum_4 / sum_1))) / (
            (sum_5 / sum_1) - ((sum_3 / sum_1) * (sum_3 / sum_1))))
    da_s = ((1 / (sum_1 * ((sum_5 / sum_1 - (
            (sum_3 / sum_1) * (sum_3 / sum_1))))))) ** .5

    # Equation (5)
    b = sum_4 / sum_1 - a * sum_3 / sum_1
    db_s = (((da_s) * (da_s)) * ((sum_5)) * (1 / sum_1)) ** (.5)

    return [a, b, da_s, db_s]


def chi_squared(V_dic, ab_value):

    # The function accepts a dir list. It takes the vars from the dir and calculates chi^2 and chi^2 reduced.
    # The calculations are done using equations (3), (7) from the project instructions page.

    a = ab_value[0]
    b = ab_value[1]
    da = ab_value[2]
    db = ab_value[3]
    chi = 0
    Tlen = V_dic['Tlen'] # this is the data set length

    for i in range(Tlen):
        chi += ((V_dic['y'][i] - (a * V_dic['x'][i] + b)) / (V_dic['dy'][i])) ** 2

    if Tlen >= 3:
        chi_red = (chi / (Tlen - 2))
        print('a = ' + str(a) + ' +- ' + str(da))
        print('b = ' + str(b) + ' +- ' + str(db))
        print("chi2 = " + str(chi))
        print("chi2_reduced = " + str(chi_red))

    # Not accepting less than two input values

    elif Tlen <= 3:
        print('a = ' + str(a) + ' +- ' + str(da))
        print('b = ' + str(b) + ' +- ' + str(db))
        print("chi2 = " + str(chi))
        print("Chi squared cannot be calculated for less than two input values")


def graph(V_dic, ab_value):

    # This is the final graphing function.
    # It will take a&b values from the list/dictionary given, give the graphs a theme and add the axis title,
    # and finally it will add those up into a file called 'fit_linear.svg'

    a = ab_value[0]
    b = ab_value[1]

    import matplotlib.pyplot as plt
    import numpy as np

    x = np.linspace(min(V_dic['x']), max(V_dic['x']))

    fit_linear = plt.plot(x, a * x + b, linestyle='-', )
    plt.setp(fit_linear, color='r', linewidth=0.7)
    plt.errorbar(V_dic['x'], V_dic['y'], V_dic['dy'], V_dic['dx'], fmt='none', ecolor='blue')

    try:
        plt.ylabel(V_dic['yaxis:'])
    except KeyError:
        plt.ylabel('Y axis')
    try:
        plt.xlabel(V_dic['xaxis:'])
    except KeyError:
        plt.xlabel('X axis')

    plt.savefig('fit_linear.svg', dpi=None, facecolor='w', edgecolor='w',
                orientation='portrait', papertype=None, format='svg',
                transparent=False, bbox_inches=None, pad_inches=0.1,
                frameon=None, metadata=None)
    plt.show()
