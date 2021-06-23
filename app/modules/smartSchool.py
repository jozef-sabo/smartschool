from datetime import date
import numpy as np
'''
    Tabulka:
    id[0] , sensor_type[1] , sensor_value[2] , sensor_unit[3] , room_number[4] , date_time[5]
'''

def createDate(year, month, day, hour):
    if day == '0':
        mydate = date(int(year), int(month), int(day))
        # mydate = np.datetime64(year+'-'+month)
    elif hour == 'x': # iba datum
        mydate = date(int(year), int(month), int(day))
        # mydate = np.datetime64(year+'-'+month+'-'+day)
    else:
        mydate = np.datetime64(year+'-'+month+'-'+day+'T'+hour)

    return mydate


# data vo formate: datetime[0], value[1]
def movingAvg(np_data):
    result = []
    if not np_data:
        return np_data
    for idx in range(len(np_data)-2):
        point3avg = round((np_data[idx][1] + np_data[idx+1][1] + np_data[idx+2][1]) / 3, 2)
        # print(np_data[idx][1] , np_data[idx+1][1] , np_data[idx+2][1])
        # print(point3avg)
        result.append([np_data[idx+1][0], point3avg])
        # np_data[idx+1][1] = point3avg
    return result


def eliminateNoise(values, std_factor=3):
    if not values:
        return values
    values = np.array(values)
    mean = np.mean(values[:, 1])
    standard_deviation = np.std(values[:, 1])

    if standard_deviation == 0:
        return values

    final_values = [element for element in values if element[1] > mean - std_factor * standard_deviation]
    final_values = [element for element in final_values if element[1] < mean + std_factor * standard_deviation]

    return final_values


def sigma(values, std_factor=3):
    if not values:
        return [0, 0]
    values = np.array(values)
    mean = np.mean(values[:, 1])
    standard_deviation = np.std(values[:, 1])

    spodna = mean - std_factor * standard_deviation
    dolna = mean + std_factor * standard_deviation

    return [spodna, dolna]

# def filterByDateTime(np_data, myDate):
#     result = []
#     for row in np_data:

#         # if day == '0':
#         #     mydate = np.datetime64(year+'-'+month)
#         #     current = np.array(row[0], dtype='datetime64[M]') # array s iba reg_date
#         # elif hour == '0': # iba datum
#         #     mydate = np.datetime64(year+'-'+month+'-'+day)
#         #     current = np.array(row[0], dtype='datetime64[D]') # array s iba reg_date
#         # else:
#         #     mydate = np.datetime64(year+'-'+month+'-'+day+'T'+hour)

#         current = np.array(row[0], dtype='datetime64[D]') # array v presnosti na den
#         # print(row[0],"  -- ", mydate)
#         if current == myDate:
#             result.append((row[0], row[1]))
#     return np.array(result)


# def filterByRoom(np_data, room):
#     result = []
#     for row in np_data:
#         if room == row[4]:
#             result.append((row[5], row[1], row[2]))
#     return np.array(result)


def parsePlot(np_data):
    # returns data in format [[minute of the day][value]]
    result = []
    if not np_data:
        return np_data
    for row in np_data:
        row = list(row)

        result.append([round(((int(row[0].strftime("%M"))+int(row[0].strftime("%H"))*60)/60), 2),
                       row[1]])
    return result


# funkcia pre candlestick chart
def parseCandle(np_data):
    result = []
    if not np_data:
        return np_data
    # returns data in format [[hour],[value_1, value_2,...,value_n]]
    for row in np_data:
        row = list(row)
        row[0] = int(row[0].strftime("%H"))
        if not result:
            result.append([row[0]])
            result[0].append([row[1]])
            continue
        for element in result:
            if element[0] == row[0]:
                element[1].append(row[1])
                continue
            if element == result[-1]:
                result.append([row[0]])
                result[-1].append([row[1]])
                break
    # returns data in format [[hour], [open - Q3, high - maximum, low - minimum, close - Q1]]
    for element in result:
        # element[1] = [np.quantile(element[1], .75),
        #               maxi(element[1]),
        #               mini(element[1]),
        #               np.quantile(element[1], .25)]
        element[1] = [element[1][0],
                      round(np.amax(element[1]), 1),
                      round(np.amin(element[1]), 1),
                      element[1][-1]]

    return result


# def processData(data, year, month, day, hour):
#     # date hour v data v poradi: 'Y-M-D hh:mm:ss'
#     # predpoklad: numpy 2dim pole x(datum) y1(teplota) y2(vlhkost), .isnull() == 0
#     if day == '0':
#         mydate = np.datetime64(year+'-'+month)
#         dates = np.array(data[:, 5], dtype='datetime64[M]') # array s iba reg_date
#     elif hour == '0': # iba datum
#         mydate = np.datetime64(year+'-'+month+'-'+day)
#         dates = np.array(data[:, 5], dtype='datetime64[D]') # array s iba reg_date
#     else:
#         mydate = np.datetime64(year+'-'+month+'-'+day+'T'+hour)
#         dates = np.array(data[:, 5], dtype='datetime64[h]') # array s iba reg_date

#     result = np.empty((0, 6), dtype=None)

#     for i in range(dates.shape[0]):
#         if dates[i] == mydate:
#             result = np.append(result, np.array([data[i]]), axis=0)

#     return result


def a0volt(np_data):
    if not np_data:
        return np_data
    result = []
    for line in np_data:
        line = list(line)
        result.append([line[0], round(line[1]/1024*5.0, 3)])

    return result


# val - stlpec z processed_data
# => processed_data[:,0] = temp ; processed_data[:,1] = humid
def avg(val):
    if not avg:
        return val
    sum = 0
    if len(val) == 0:
        return None
    for value in val:
        sum += value[1]
    return round(sum/len(val), 1)


def maxi(val):
    if not val:
        return val
    maximum = (val[0][0], val[0][1])
    for row in val:
        if row[1] > maximum[1]:
            maximum = (row[0], row[1])
    return maximum


# def mini(val):
#     return round(np.amin(val), 1)


# def dev(val):
#     return round(np.std(val.astype(np.float64)), 1)


# def printResults(val):
#     return str("MIN: " + str(min(val)) + "  MAX: " + str(max(val)) + "  AVG: " + str(avg(val)) + "  DEV: " + str(dev(val)))


# def pearson(val1, val2):
#     # dva stlpce s processed_data
#     return np.corrcoef(val1.astype(np.float64), val2.astype(np.float64))
