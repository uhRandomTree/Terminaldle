from urllib import request
import datetime
from sys import argv
#I should go through this and make sure things are ints when they're going to be stored for a while, and aren't going through too many conversions.
VerboseMode=False
Verboseables=('-V','-VERBOSE','--VERBOSE')
Helpables=('-H','-HELP','--HELP','/?','-?')
for i in argv:
		if i.upper() in Helpables:exit("This tool is to sync the IDs and game numbers with the Wordle games. This is only useful for Archive mode.\n\n-V --VERBOSE\tProvide verbose output. Otherwise will excecute silently.\n-H --HELP /? -?\tExit the program and provide this screen.\n\nYou can always access the written data in IDs.TXT. The format is GAME#YYYY-MM-DD|ID")
		if i.upper() in Verboseables:VerboseMode=True
IDPage=open("IDs.TXT","w")

DayPerMon=(0,31,0,31,30,31,30,31,31,30,31,30,31,30,31)
Day=19
Mon=6
Year=2021
Today=datetime.date.today()
TDay=Today.day
TMon=Today.month
TYear=Today.year
IDs=list()
Dates=list()
Release=list()
DaysSinceRelease=0
if not VerboseMode:
		print("Silently excecuting. Use the verbose flag (-V) to keep track of execution.")
while ((Day<TDay and (Year<=TYear or Mon<=TMon)) or Mon<TMon and Year<=TYear) or Year<TYear:
		DateString=f"{Year}-{str(Mon).zfill(2)}-{str(Day).zfill(2)}"

		if VerboseMode:
				print("Retrieving data from date "+DateString)
		try:
				TempDat=str(request.urlopen(f"https://www.nytimes.com/svc/wordle/v2/{DateString}.json").read(),'utf-8')
				Dates.append(DateString)
				IDs.append(TempDat[TempDat.find('"id":')+5:TempDat.find(',')])
				Release.append(DaysSinceRelease)
				DaysSinceRelease+=1
				if VerboseMode:
						print("Retrieved ID "+IDs[-1])
						print("Days since release: "+str(Release[-1]))
		except request.URLError:
				if VerboseMode:print(f"WARNING: {DateString} could not be accessed, skipping.")
		if Mon!=2:
				DPM=DayPerMon[Mon]
		else:
				if (Year%4==0 and not Year%100) or Year%400:DPM=29
				else:DPM=28
		if Day>=DPM:
				Day=0
				Mon+=1
		if Mon>12:
				Year+=1
				Mon=1
		Day+=1
if VerboseMode:
		print(Dates)
		print(IDs)
for DateLabel,IDLabel,DaysSince in zip(Dates,IDs,Release):#The DaysSinceRelease is not workin, wonder why.
		IDPage.write(f"{DaysSince}#{DateLabel}|{IDLabel}\n")