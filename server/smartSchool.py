from datetime import date
import numpy as np
'''
    Tabulka:
    id[0] , sensor_type[1] , sensor_value[2] , sensor_unit[3] , room_number[4] , date_time[5]
'''

def filter0(dbData):
    result = []
    for line in dbData:
        if line[1] == 0:
            continue
        else: result.append((line[0], line[1]))
        # print(line)
    return np.array(result)


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
def movingAvg(npData):
    result = []
    for idx in range(len(npData)-2):
        point3avg = round((npData[idx][1] + npData[idx+1][1] + npData[idx+2][1]) / 3 , 2)
        print(npData[idx][1] , npData[idx+1][1] , npData[idx+2][1])
        print(point3avg)
        result.append([npData[idx+1][0] , point3avg])
        # npData[idx+1][1] = point3avg
    return result


# def filterByDateTime(npData, myDate):
#     result = []
#     for row in npData:

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


# def filterByRoom(npData, room):
#     result = []
#     for row in npData:
#         if room == row[4]:
#             result.append((row[5], row[1], row[2]))
#     return np.array(result)


def parsePlot(npData):
    # returns data in format [[minute of the day][value]]
    result = []
    for row in npData:
        row = list(row)

        result.append([round(((int(row[0].strftime("%M"))+int(row[0].strftime("%H"))*60)/60), 2), row[1]])
    return result


# funkcia pre candlestick chart
def parseCandle(npData):
    result = []
    # returns data in format [[hour],[value_1, value_2,...,value_n]]
    for row in npData:
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
            elif element == result[-1]:
                result.append([row[0]])
                result[-1].append([row[1]])
                break
    # returns data in format [[hour], [open - Q3, high - maximum, low - minimum, close - Q1]]
    for element in result:
        # element[1] = [np.quantile(element[1], .75), maxi(element[1]), mini(element[1]), np.quantile(element[1], .25)]
        element[1] = [element[1][0], maxi(element[1]), mini(element[1]), element[1][-1]]

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


def a0volt(npData):
    result = []
    for line in npData:
        line = list(line)
        result.append([line[0], round(line[1]/1024*5.0, 3)])

    return result


# val - stlpec z processed_data
# => processed_data[:,0] = temp ; processed_data[:,1] = humid
def avg(val):
    sum = 0
    if len(val) == 0:
        return None 
    for value in val:
        sum += value[1]
    return round(sum/len(val), 1)


def maxi(val):
    return round(np.amax(val), 1)


def mini(val):
    return round(np.amin(val), 1)


def dev(val):
    return round(np.std(val.astype(np.float64)), 1)


def printResults(val):
    return str("MIN: " + str(min(val)) + "  MAX: " + str(max(val)) + "  AVG: " + str(avg(val)) + "  DEV: " + str(dev(val)))


def pearson(val1, val2):
    # dva stlpce s processed_data
    return np.corrcoef(val1.astype(np.float64), val2.astype(np.float64))
