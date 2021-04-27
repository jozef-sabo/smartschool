import fetchData
import smartSchool


dbData = fetchData.fetch()
tempAll = smartSchool.filterByType(dbData, "Temperature") # USED
humdAll = smartSchool.filterByType(dbData, "Humidity")
devpAll = smartSchool.filterByType(dbData, "DewPoint")
a0a0All = smartSchool.filterByType(dbData, "A0")
C3All = smartSchool.filterByRoom(dbData, "3C")

# print(a0a0All)
# print("                  ")
# print(smartSchool.a0volt(a0a0All))
myDate = smartSchool.createDate('2021', '04', '06', 'x')
print(myDate)
# print(smartSchool.filterTodayData(tempAll))
# temperature example
# print(tempAll)
temp_06_04_2021 = smartSchool.filterByDateTime(tempAll, myDate) # do not use '0' as it is a valid hour_Idx
# print(temp_06_04_2021)
print(smartSchool.parsePlot(temp_06_04_2021))
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
