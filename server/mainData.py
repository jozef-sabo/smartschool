import fetchData
import smartSchool
import datetime

date = datetime.date.today() 
# dbData = fetchData.fetch(date, '4C', 'humidity')
# humid_filter = smartSchool.eliminateNoise(dbData)
# humid_ma = smartSchool.movingAvg(humid_filter)
# humid_line = smartSchool.parsePlot(humid_ma)
# humid_s = smartSchool.sigma(dbData)
# print(humid_line)
# print(smartSchool.maxi(smartSchool.parsePlot(dbData)))
# fil = smartSchool.eliminateNoise(dbData)
# x = []
# print(smartSchool.eliminateNoise(dbData))
# print(len(dbData))
# print("      ")
# print(len(fil))
# print(smartSchool.movingAvg(dbData))
# print(dbData[-13:])
# print(smartSchool.parsePlot(dbData[-10:]))
# print("db data")
# print(dbData[:10])
# print("                ")
# movingAvg = smartSchool.movingAvg(dbData[:10])
# print("moving avg")
# print(movingAvg)
# print("len db, len moving avg")
# print(len(dbData[:10]), len(movingAvg))
# dbData = fetchData.fetch(date, '3C')
# tempAll = smartSchool.filterByType(dbData, "temperature") # USED
# humdAll = smartSchool.filterByType(dbData, "humidity")
# devpAll = smartSchool.filterByType(dbData, "dewPoint")
# a0a0All = smartSchool.filterByType(dbData, "co2")
# C3All = smartSchool.filterByRoom(dbData, "3C")


# print(dbData)
# print("                  ")
# print(smartSchool.a0volt(a0a0All))
# myDate = smartSchool.createDate('2021', '05', '02', 'x')
# print(myDate)
# # print(smartSchool.filterTodayData(tempAll))
# # temperature example
# # print(tempAll)
# temp_06_04_2021 = smartSchool.filterByDateTime(tempAll, myDate) # do not use '0' as it is a valid hour_Idx
# print(temp_06_04_2021)
# x = smartSchool.parsePlot(temp_06_04_2021)
# print("        and        ")
# print(smartSchool.parseCandle(temp_05_04_2021))

# print("DATE 2021-04-05") # temp_05_04_2021 can by plot as curve - interpolated as well
# print("           " + smartSchool.printResults(temp_06_04_2021[:, 1])) # data of specific day
# for hour_Idx in range(24):
#     if hour_Idx < 10:
#         hour_Idx_string = "0" + str(hour_Idx)
#     else:
#         hour_Idx_string = str(hour_Idx)
#     local = smartSchool.filterByDateTime(temp_06_04_2021, '2021', '04', '06', hour_Idx_string) # candle data of specific hour
#     if local.size != 0:
#         print("HOUR " + hour_Idx_string + " :: " + smartSchool.printResults(local[:, 1]))