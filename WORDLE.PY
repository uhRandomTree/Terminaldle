import datetime
from sys import argv

#These can all be optomized an cleaned up, maybe changed for better viewing experience.
#Should probably add a check or something in case their terminal doesn't have full colour support.
LtRst= '\x1b[0m'#Resets the colours to default.
LtRstW='\x1b[0;1;38;2;248;248;248m'#Resets the colours to white/bright.
LtC=   '\x1b[48;2;83;141;78m'#Changes the colour to green.
LtN=   '\x1b[48;2;181;159;59m'#Changes the colour to yellow/orange.
LtW=   '\x1b[48;2;58;58;60m'#Changes the colour to dark grey.
LtU=   '\x1b[48;2;81;83;84m'#Changes the colour to light grey.
LtEE=  '\x1b[38;2;255;0;0m'#Changes the colour to red.
OWL= '\r\x1b[1A'#"Over Writes" the current line.
KBH=False
Modes=('I','Y','A')
GameMode=''
Keyboards={
"QWERTY": ('Q','W','E','R','T','Y','U','I','O','P','A','S','D','F','G','H','J','K','L','Z','X','C','V','B','N','M'),
"ABC":    ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'),
"AZERTY": ('A','Z','E','R','T','Y','U','I','O','P','Q','S','D','F','G','H','J','K','L','M','W','X','C','V','B','N'),
"WORKMAN":('Q','D','R','W','B','J','F','U','P','A','S','H','T','G','Y','N','E','O','I','Z','X','M','C','V','K','L'),
"NONE":   None
}

Quittables= ('QUIT','EXIT','CANCEL')
Attempables=('-A','--ATTEMPTS')#Add a way for the player to continue infinitely.
Helpables=  ('-H','--HELP','/?','-?')
Playables=  ('-HTP','--HOW-TO-PLAY')
Linkables=  ('-L','--LINKS')
KBables=    ('-K','--KEYBOARD')
Historics=  ('-KBH','--KEYBOARD-HISTORY')
Modables=   ('-M','--MODE')
Attempts=6

def Quinput(Request=""):
		Response=input(Request)
		Response=Response.upper()
		if Response in Quittables:
				exit(OWL+LtEE+"Game quit.                "+LtRst)
		return Response

def JSONstr2Dict(InStr):
		JSONLines=InStr[1:-1].split(',')
		JSONDict=dict()
		for i in JSONLines:
				JSONDict[i[:i.find(':')].replace('"','')]=i[i.find(':')+1:].replace('"','')
		return JSONDict

KBDisplay=Keyboards["ABC"]
argv=[i.upper() for i in argv]
for i in argv:

		if i in Helpables:
				exit("""-H\t--HELP /? -?\tExit the program and provide this screen.
-A\t--ATTEMPTS\tChange the number of maximum attempts to make it easier or harder. Default is 6.
-HTP\t--HOW-TO-PLAY\tExit the program and display a how-to-play screen.
-K\t--KEYBOARD\tSelect a keyboard to display during the game. Default is ABC.
OPTIONS: (In order of)
\tABC\tThe alphabet.
\tQWERTY\tA QWERTY keyboard.
\tAZERTY\tAn AZERTY keyboard.
\tWORKMAN\tA workman keyboard.
\tNONE\tNo keyboard display.

Type 'QUIT' while the program's running to exit.
Arguments do not have to be capitalized.""")

		if i in Playables:
				exit(f"""How To Play:
Guess the Wordle in 6 tries. Each guess must be a valid 5-letter word.
The color of the tiles will change to show how close your guess was to the word.

Examples:
{LtRstW+LtC}W{LtRstW}EARY
{LtRst}W is in the word and in the correct spot.
{LtRstW}P{LtN}I{LtRstW}LLS{LtRst}\nI is in the word but in the wrong spot.
{LtRstW}VAG{LtW}U{LtRstW}E{LtRst}\nU is not in the word in any spot.""")

		if i in Linkables:
				print("Attempting to connect to the New York Times website. This may take a minute.")
				from urllib import request
				try:
						NYT=JSONstr2Dict(str(request.urlopen(f"https://www.nytimes.com/svc/wordle/v2/{datetime.date.today():%Y-%m-%d}.json").read(),'utf-8'))
				except request.URLError:
						exit(f"{LtEE}Connection to the NYT website failed{LtRst}, you may attempt to connect manually.")
				exit(f"""The following are help and source links {LtEE}(SPOILERS FOR TODAY'S AND PAST WORDLES){LtRst}:
NYT Wordle Game\t\t\thttps://www.nytimes.com/games/wordle/index.html
Wordle \"API\" for today\t\thttps://www.nytimes.com/svc/wordle/v2/{NYT["print_date"]}.json
NYT Wordle solution page\thttps://www.nytimes.com/{NYT["print_date"].replace('-','/')}/crosswords/wordle-review-{NYT["days_since_launch"]}.html
Word lists source\t\thttps://gist.github.com/cfreshman""")

		if i in Attempables:Attempts=int(argv[argv.index(i)+1])
		if i in Modables:GameMode=argv[argv.index(i)+1]

		if i in Historics:KBH=True
		if i in KBables:
				try:
						KBDisplay=Keyboards[argv[argv.index(i)+1]]
				except:
						print(LtEE+"Invalid keyboard option, using ABC."+LtRst)
WordleList=open("ANSWERS.TXT").read().split('\n')
RandomWord=WordleList[int(datetime.datetime.now().timestamp()*1000000)%len(WordleList)]
WordleList.extend(open("GUESSABLES.TXT").read().split('\n'))
if GameMode in Modes:
		pass
else:
		GameMode=Quinput("Which mode do you want to play?\n(I)nfinite, New (Y)ork Times, NYT (A)rchive\n")
		while GameMode not in Modes:
				GameMode=print(OWL+" ||Invalid mode||"+OWL)
				GameMode=Quinput()
		print(OWL+GameMode+' '*16)

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
# " The answer was "+LtC+RandomWord+LtRst+"." # Add an option to know the word again.
ShareText=str()
if KBDisplay:KBColours=['']*26
while Attempt<Attempts:
		WordGuess=Quinput()
		if len(WordGuess)!=5:
				print(OWL+"     ||Word wrong length||"+OWL)
				continue
		elif WordGuess not in WordleList:
				print(OWL+"     ||Invalid word||     "+OWL)
				continue
		Colourrr=[0,0,0,0,0]
		RemainingL=[]
		for i in range(5):
				if WordGuess[i]==RandomWord[i]:
						Colourrr[i]=1
						if KBDisplay:KBColours[KBDisplay.index(WordGuess[i])]=LtC
				else:
						RemainingL.append(RandomWord[i])
						if KBDisplay:KBColours[KBDisplay.index(WordGuess[i])]=LtW

		for i in range(5):
				if WordGuess[i] in RemainingL:
						if Colourrr[i]!=1:
								Colourrr[i]=2
								if KBDisplay:KBColours[KBDisplay.index(WordGuess[i])]=LtN#Something funky about the highlighting.
						RemainingL.remove(WordGuess[i])

		ColouredWord=str()
		for ColIn,CurLet in zip(Colourrr,WordGuess):
				if ColIn==0:
						ColouredWord+=LtW+CurLet
						ShareText+='⬛'#Black square character
				elif ColIn==1:
						ColouredWord+=LtC+CurLet
						ShareText+='🟩'#Green square emoji
				else:
						ColouredWord+=LtN+CurLet
						ShareText+='🟨'#Yellowish sqare emoji.
		ShareText+='\n'
		# print(KBColours)
		print(OWL+LtRstW+ColouredWord+LtRst+' '*21,end='')
		if KBDisplay:print(LtU,end='')
		else:print()
		if KBDisplay:
				for i in range(len(KBDisplay)):
						print(KBColours[i]+KBDisplay[i]+LtRst+LtU,end='')
				if not KBH:print(LtRst+'\x1b[1A\x1b[26D'+' '*26+'\x1b[1B')#Moves cursor up, back 26 characters, writes 26 spaces, back down, and to the bottom left.
				else:
						print(LtRst)
		ColouredWord=str()
		if Colourrr==[1,1,1,1,1]:
				print(f"You win! That took {Attempt+1} attempt(s).")
				if Quinput("Share? (Y/N)\n")=='Y':
						if GameMode!='I':
								WordleGameText="Wordle "+NYT['days_since_launch']
						else:
								WordleGameText="Infinite Wordle"
						print(f"You can copy the below text, normally with Ctrl-Shift-C, but it will change depending on your terminal.\nIt may look garbled or strange, but it should copy correctly.\n{WordleGameText} {Attempt+1}/{Attempts}\n{ShareText}")#I would copy it automatically, but it depends so much by system that it's not worth it and it would be its own program.
				break
		Attempt+=1
		if Attempt==Attempts and Colourrr!=[1,1,1,1,1]:
				print("Sorry, you ran out of attemps.") #Add system to see answer.
