import datetime
#I'm not sure why, but I was averse to adding the randint function just for one thing, so I decided to add pseudo-randomness for the RandomWord
from sys import argv

#These can all be optomized an cleaned up, maybe changed for better viewing experience.
#Should probably add a check or something in case their terminal doesn't have full colour support.
LtRst='\x1b[0m'#Resets the colours to default.
LtRstW='\x1b[0;1;38;2;248;248;248m'#Resets the colours to white/bright.
LtC='\x1b[48;2;83;141;78m'#Changes the colour to green.
LtN='\x1b[48;2;181;159;59m'#Changes the colour to yellow/orange.
LtW='\x1b[48;2;58;58;60m'#Changes the colour to grey.
LtEE='\x1b[38;2;255;0;0m'#Changes the colour to red.
OWL="\r\x1b[1A"#"Over Writes" the current line.

Attempables=('-A','-ATTEMPTS','--ATTEMPTS')#Add a way for the player to continue infinitely.
Verboseables=('-V','-VERBOSE','--VERBOSE')
Helpables=('-H','-HELP','--HELP','/?','-?')
Quittables=('QUIT','EXIT','CANCEL')
Playables=('-HTP','-HOW-TO-PLAY','--HOW-TO-PLAY')
Verbose=False
Attempts=6
for i in argv:
		i=i.upper()
		if i in Attempables:Attempts=int(argv[argv.index(i)+1])
		if i in Verboseables:Verbose=True
		if i in Playables:exit(f"How To Play:\nGuess the Wordle in 6 tries. Each guess must be a valid 5-letter word.\nThe color of the tiles will change to show how close your guess was to the word.\n\nExamples:\n{LtRstW+LtC}W{LtRstW}EARY\n{LtRst}W is in the word and in the correct spot.\n{LtRstW}P{LtN}I{LtRstW}LLS{LtRst}\nI is in the word but in the wrong spot.\n{LtRstW}VAG{LtW}U{LtRstW}E{LtRst}\nU is not in the word in any spot.")
		if i in Helpables:exit("-H\t--HELP /? -?\tExit the program and provide this screen.\n-V\t--VERBOSE\tProvide verbose output, including game ID, game number, date, and solution when exiting.\n-A\t--ATTEMPTS\tChange the number of maximum attempts to make it easier or harder. Default is 6.\n-HTP\t--HOW-TO-PLAY\tExit the program and display a how-to-play screen.\nType 'QUIT' while the program's running to exit.\nArguments do not have to be capitalized.")

DisplayAns=""
def Quinput(Request=""):
		Response=input(Request)
		Response=Response.upper()
		if Response in Quittables:
				exit(OWL+LtEE+"Game quit."+LtRst+DisplayAns)
		return Response

def JSONstr2Dict(InStr):
		JSONLines=InStr[1:-1].split(',')
		JSONDict=dict()
		for i in JSONLines:
				JSONDict[i[:i.find(':')].replace('"','')]=i[i.find(':')+1:].replace('"','')
		return JSONDict
Guessables=list(open("GUESSABLES.TXT").read().split('\n'))#These are on top of the possible ones in Answers.
WordleList=list(open("ANSWERS.TXT").read().split('\n'))
RandomWord=WordleList[int(datetime.datetime.now().timestamp()*1000000)%len(WordleList)]

GameMode=Quinput("Which Wordle do you want to play?\n(I)nfinite, New (Y)ork Times, NYT (A)rchive\n")
Modes=('I','Y','A')
while GameMode not in Modes:
		GameMode=print(OWL+" ||Invalid mode"+OWL)
		GameMode=Quinput()
print(OWL+GameMode+"              ")
if GameMode!='I':
		from urllib import request
		if GameMode=='Y':
				print("Attempting to connect to the New York Times website. This may take a minute.")
				RequestedDay=f"{datetime.date.today():%Y-%m-%d}"
		elif GameMode=='A':
				IDPage=open("IDs.TXT").read()
				RequestedDay=Quinput("Please enter your chosen day in the format YYYY-MM-DD, by ID, or by which Wordle it was. (Wordles started counting at 0). Ex: 2023-02-26, ID1462, or 617.\nThe first Wordle was June 19th, 2021 (2021-06-19, ID1, 0).\n")
				print("Attempting to connect to the New York Times website. This may take a minute.")
				if '-' in RequestedDay:
						pass
				elif 'ID' in RequestedDay:
						RequestedDay=RequestedDay.replace('ID','')
						RequestedDay=IDPage[IDPage.find('|'+RequestedDay)-10:IDPage.find('|'+RequestedDay)]
				else:
						RequestedDay.replace(',','')
						RequestedDay=IDPage[IDPage.find(RequestedDay+'#')+len(RequestedDay)+1:IDPage.find(RequestedDay+'#')+len(RequestedDay)+11]
		try:
				NYT=JSONstr2Dict(str(request.urlopen(f"https://www.nytimes.com/svc/wordle/v2/{RequestedDay}.json").read(),'utf-8'))#There's something wrong about this, it's not always returning correctly. Troubleshoot.
				RandomWord=NYT['solution'].upper()
				print("ID: "+NYT['id'])
				print("Game number: "+NYT['days_since_launch'])
				print("Date: "+RequestedDay)
		except request.URLError:
				print(f"{LtEE}Connection to the NYT website failed{LtRst}, moving to Infinite Wordle mode.")

Attempt=0

if Verbose:DisplayAns=" The answer was "+LtC+RandomWord+LtRst+"."
ShareText=str()
while Attempt<Attempts:
		WordGuess=Quinput()
		if WordGuess not in Guessables and WordGuess not in WordleList:
				print(OWL+"     ||Invalid word"+OWL)
				continue
		Colourrr=[0,0,0,0,0]
		RemainingL=[]
		for i in range(5):
				if WordGuess[i]==RandomWord[i]:
						Colourrr[i]=1
				else:
						RemainingL.append(RandomWord[i])

		for i in range(5):
				if WordGuess[i] in RemainingL:
						if Colourrr[i]!=1:
								Colourrr[i]=2
						RemainingL.remove(WordGuess[i])

		ColouredWord=str()
		for ColIn,CurLet in zip(Colourrr,WordGuess):
				if ColIn==0:
						ColouredWord+=LtW+CurLet
						ShareText+='⬛'#I believe this to be the black square? Probably doesn't show up right in your editor.
				elif ColIn==1:
						ColouredWord+=LtC+CurLet
						ShareText+='🟩'#This should be green.
				else:
						ColouredWord+=LtN+CurLet
						ShareText+='🟨'#Should be the yellowish one.
		ShareText+='\n'
		print(OWL+ColouredWord+LtRst+"              ")
		ColouredWord=str()
		if Colourrr==[1,1,1,1,1]:
				print(f"You win!{DisplayAns} That took {Attempt+1} attempt(s).")
				if Quinput("Share? (Y/N)\n")=='Y':
						if GameMode!='I':
								WordleGameText="Wordle "+NYT['days_since_launch']
						else:
								WordleGameText="Infinite Wordle"
						print(f"You can copy the below text, normally with Ctrl-Shift-C, but it will change depending on your terminal.\nIt may look garbled or strange, but it should copy correctly.\n{WordleGameText} {Attempt+1}/{Attempts}\n{ShareText}")#I would copy it automatically, but it depends so much by system that it's not worth it and it would be its own program.
				break
		Attempt+=1
		if Attempt==Attempts and Colourrr!=[1,1,1,1,1]:
				print("Sorry, you ran out of attemps."+DisplayAns)
