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
myDate = smartSchool.createDate('2021', '04', '12', 'x')
print(myDate)
# print(smartSchool.filterTodayData(tempAll))
# temperature example
# print(tempAll)
# temp_06_04_2021 = smartSchool.filterByDateTime(humdAll, myDate) # do not use '0' as it is a valid hour_Idx
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


db_data = fetchData.fetch()

temp_all = smartSchool.filterByType(db_data, "Temperature")
    # temp_today = mainData.smartSchool.filterTodayData(temp_all)
temp_06_04_2021 = smartSchool.filterByDateTime(temp_all, myDate)
temp_06_04_2021_line = smartSchool.parsePlot(temp_06_04_2021)

humid_all = smartSchool.filterByType(db_data, "Humidity")
    # humid_today = mainData.smartSchool.filterTodayData(humid_all)
humid_06_04_2021 = smartSchool.filterByDateTime(humid_all, myDate)
humid_06_04_2021_line = smartSchool.parsePlot(humid_06_04_2021)

dp_all = smartSchool.filterByType(db_data, "DewPoint")
    # dp_today = mainData.smartSchool.filterTodayData(dp_all)
dp_06_04_2021 = smartSchool.filterByDateTime(dp_all, myDate)
dp_06_04_2021_line = smartSchool.parsePlot(dp_06_04_2021)

a0_all = smartSchool.filterByType(db_data, "A0")
    # a0_today = mainData.smartSchool.filterTodayData(a0_all)
a0_06_04_2021 = smartSchool.filterByDateTime(a0_all, myDate)
a0_06_04_2021_volt = smartSchool.a0volt(a0_06_04_2021)
a0_06_04_2021_line = smartSchool.parsePlot(a0_06_04_2021_volt)


temp_av = smartSchool.avg(temp_06_04_2021_line)
humid_av = smartSchool.avg(humid_06_04_2021_line)
dp_av = smartSchool.avg(dp_06_04_2021_line)
a0_av = smartSchool.avg(a0_06_04_2021_line)
print(a0_06_04_2021_line)
print(a0_av)
x = smartSchool.createDate('2021', '04', '27', 'x')
print(x.strftime("%a, %d %b %Y %H:%M:%S"))