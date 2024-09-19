import datetime
from sys import argv

KBH=False
Modes=('I','Y','A','P','M')
Sharings=('N','Y','NO','YES','0','1','F','T','FALSE','TRUE')
GameMode=''
ShareYN=None
LoopGameloop=False
Keyboards={
"QWERTY": ('Q','W','E','R','T','Y','U','I','O','P','A','S','D','F','G','H','J','K','L','Z','X','C','V','B','N','M'),
"ABC":    ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'),
"AZERTY": ('A','Z','E','R','T','Y','U','I','O','P','Q','S','D','F','G','H','J','K','L','M','W','X','C','V','B','N'),
"WORKMAN":('Q','D','R','W','B','J','F','U','P','A','S','H','T','G','Y','N','E','O','I','Z','X','M','C','V','K','L'),
"FREQ":   ('E','T','A','O','I','N','S','H','R','D','L','C','U','M','W','F','G','Y','P','B','V','K','J','X','Q','Z'),
"NONE":   None
}

Quittables= ('QUIT','EXIT','CANCEL')
Attempables=('-A','--ATTEMPTS')
Helpables=  ('-H','--HELP','/?','-?')
Playables=  ('-HTP','--HOW-TO-PLAY')
Linkables=  ('-L','--LINKS')
KBables=    ('-K','-KB','--KEYBOARD')
Historics=  ('-KBH','--KEYBOARD-HISTORY')
Modables=   ('-M','--MODE')
Shareable=  ('-S','--SHARE')
Colourables=('-C','-COL','--COLOURS','--COLOUR','--COLORS','--COLOR')
Attempts=6

ColourNames=('NORMAL','8COL','256COL','HICON','NYTHICON',
						 'WORDLE','8COLOR','256COLOR','HICONTRAST','NYTHICONTRAST',
						 'CLASSIC','8COLOUR','256COLOUR','HIGHCONTRAST','NYTHIGHCONTRAST')
LtRst= '\x1b[0m'#Resets the colours to default.
LtRstW='\x1b[0;1;38;2;248;248;248m'#Resets the colours to white/bright.
LtC=   '\x1b[48;2;83;141;78m'#Changes the colour to green.
LtN=   '\x1b[48;2;181;159;59m'#Changes the colour to yellow/orange.
LtW=   '\x1b[48;2;58;58;60m'#Changes the colour to dark grey.
LtU=   '\x1b[48;2;81;83;84m'#Changes the colour to light grey.
LtEE=  '\x1b[38;2;255;0;0m'#Changes the colour to red.
OWL= '\r\x1b[1A'#"Over Writes" the current line.

def Quinput(Request=""):
		Response=input(Request).upper().strip()
		if Response in Quittables:
				exit(OWL+LtEE+"Game quit."+' '*16+LtRst)
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
-HTP\t--HOW-TO-PLAY\tExit the program and display a how-to-play screen.
-L\t--LINKS\t\tExit the program and display links to the Wordle sub-websites, including help and solution sites.
-A\t--ATTEMPTS\tChange the number of maximum attempts to make it easier or harder. Default is 6.
-M\t--MODE\t\tSelect your mode.
OPTIONS:
\t(I)nfinite
\tNew (Y)ork Times today
\tA Wordle from the NYT (A)rchives
\t(P)ass&Play
\t(M)arathon

-KBH\t--KEYBOARD-HISTORY\tDoesn't clear the contents of previous word's keyboards.
-K\t--KEYBOARD\tSelect a keyboard to display during the game. Default is ABC.
OPTIONS: (In order of)
\tABC\tThe alphabet.
\tQWERTY\tA QWERTY keyboard
\tAZERTY\tAn AZERTY keyboard
\tWORKMAN\tA workman keyboard
\tFREQ\tFrequency of the letters in English
\tNONE\tNo keyboard display

-C\t--COLOURS\tChanges the colour modes the game runs in.
OPTIONS: (COLOUR=COLOR=COL, HIGH=HI, 256-COL=256COL)
\tCLASSIC\t\tThe normal colour scheme of the game. All correct and same as the website.
\t8-COLOUR\tFor terminals that only support 8 colours. Not recommended unless needed.
\t256-COLOUR\tFor terminals that only support up to the 256 colour palatte.
\tHIGH-CONTRAST\tIncreases vibrance of the colours to make them easier to see in a terminal.
\tNYT-HI-CONTRAST\tAdds the official high contrast colour palatte of Wordle.

Type 'QUIT' while the program's running to exit.
Arguments do not have to be capitalized.
If colours are not displaying properly, try the colours option.""")

		if i in Colourables:
				DisplayColours=argv[argv.index(i)+1].replace('-','')
				if DisplayColours in ColourNames:
						DisplayColours=ColourNames.index(DisplayColours)%5
				else:
						DisplayColours=0
				match DisplayColours:
						case 0:pass
						case 1:
								LtRstW='\x1b[0;1;37m'
								LtC=   '\x1b[42m'
								LtN=   '\x1b[43m'
								LtW=   '\x1b[40;37m'
								LtU=   LtW
								LtEE=  '\x1b[31m'
						case 2:
								LtRstW='\x1b[0;1;38;5;255m'
								LtC=   '\x1b[48;5;107m'
								LtN=   '\x1b[48;5;184m'
								LtW=   '\x1b[48;5;238m'
								LtU=   '\x1b[48;5;240m'
								LtEE=  '\x1b[38;5;9m'
						case 3:
								LtRstW='\x1b[0;1;38;5;255m'
								LtC=   '\x1b[48;5;46m'
								LtN=   '\x1b[48;5;226m'
								LtW=   '\x1b[48;5;232m'
								LtU=   '\x1b[48;5;246m'
								LtEE=  '\x1b[38;5;9m'
						case 4:
								LtC=   '\x1b[38;5;0;48;2;245;121;58m'
								LtN=   '\x1b[38;5;0;48;2;133;192;249m'
								LtW=   '\x1b[38;5;15;48;5;232m'

		if i in Playables:
				exit(f"""How To Play:
Guess the Wordle in 6 tries. Each guess must be a valid 5-letter word.
The color of the tiles will change to show how close your guess was to the word.

Examples:
{LtRstW+LtC}W{LtRstW}EARY
{LtRst}W is in the word and in the correct spot.
{LtRstW}P{LtN}I{LtRstW}LLS{LtRst}\nI is in the word but in the wrong spot.
{LtRstW}VAG{LtW}U{LtRstW}E{LtRst}\nU is not in the word in any spot.

In Infinite mode, you play a random word. In NYT mode, you play today's Wordle. In Archive, you play any Wordle from the past.
In Pass&Play, you choose words for your opponent to guess, until one of you fails.
In Marathon mode, you play as many games as you can without failing, and the last answer becomes your first guess for the next word.""")

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
		if i in Shareable:ShareYN=argv[argv.index(i)+1]

		if i in Historics:KBH=True
		if i in KBables:
				try:
						KBDisplay=Keyboards[argv[argv.index(i)+1]]
				except:
						print(LtEE+"Invalid keyboard option, using ABC."+LtRst)
PossibleAnswers=open("ANSWERS.TXT").read().split('\n')
WordleList=list()#Done to make a deep copy, or else both lists get modified.
WordleList.extend(PossibleAnswers)
WordleList.extend(open("GUESSABLES.TXT").read().split('\n'))
def ValidWord(ShowWord=True):
		Word=Quinput()
		while True:
				if len(Word)!=5:
						print(OWL+' '*5+LtEE+"||Wrong word length||"+LtRst+OWL)
				elif Word not in WordleList:
						print(OWL+' '*5+LtEE+"||Invalid word||"+LtRst+' '*5+OWL)
				else:
						if ShowWord:
								print(OWL+Word+' '*22)
						else:
								print(OWL+"#####"+' '*22)
						return Word
				Word=Quinput()

def RandFromTime(ListLen):
		return int(datetime.datetime.now().timestamp()*1000000)%ListLen

RandomWord=PossibleAnswers[RandFromTime(len(PossibleAnswers))]

if GameMode in Modes:
		pass
else:
		GameMode=Quinput("Which mode do you want to play?\n(I)nfinite, New (Y)ork Times, NYT (A)rchive, (P)ass&Play, (M)arathon\n")
		while GameMode not in Modes:
				GameMode=print(OWL+' '+LtEE+"||Invalid mode||"+LtRst+OWL)#Gonna make some function for this whole mess. Later.
				GameMode=Quinput()
		print(OWL+GameMode+' '*16)

if GameMode=='P':
		ShareYN=False
		print(f"Choose your opponent's word and{LtEE} don't show them.{LtRst}")
		RandomWord=ValidWord(False)
		LoopGameloop=True
elif GameMode=='M':
		LapCount=0
		ShareYN=False
		LoopGameloop=True
elif GameMode!='I':
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
WordGuess=None
if ShareYN!=False:ShareText=str()
if KBDisplay:KBColours=['']*26
while Attempt<Attempts:
		if GameMode=='M' and Attempt==0 and WordGuess!=None:
				print('-----\n')
		else:
				WordGuess=ValidWord()
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
						if ShareYN!=False:ShareText+='⬛'#Black square character
				elif ColIn==1:
						ColouredWord+=LtC+CurLet
						if ShareYN!=False:ShareText+='🟩'#Green square emoji
				else:
						ColouredWord+=LtN+CurLet
						if ShareYN!=False:ShareText+='🟨'#Yellowish sqare emoji.
		if ShareYN!=False:ShareText+='\n'
		# print(KBColours)
		print(OWL+LtRstW+ColouredWord+LtRst+' '*21,end='')
		if KBDisplay:
				print(LtU,end='')
				for i in range(len(KBDisplay)):
						print(KBColours[i]+KBDisplay[i]+LtRst+LtU,end='')
				if not KBH and Attempt!=0:print(LtRst+'\x1b[1A\x1b[26D'+' '*26+'\x1b[1B')#Moves cursor up, back 26 characters, writes 26 spaces, back down, and to the bottom left.
				else:
						print(LtRst)
		else:print()
		ColouredWord=str()
		Attempt+=1
		if Colourrr==[1,1,1,1,1]:
				if not LoopGameloop:
						print(f"You win! That took {Attempt+1} attempt(s).")
						OWLSHARE=False
						if ShareYN not in Sharings:
								OWLSHARE=True
								ShareYN=Quinput("Do you want to share? (Y)es/(N)o\n")
						while ShareYN not in Sharings:
								ShareYN=print(OWL+' '*5+LtEE+"||Invalid||"+LtRst+OWL)
								ShareYN=Quinput()
						if OWLSHARE:print(OWL+ShareYN+' '*20)
						if Sharings.index(ShareYN)%2==1:
								if GameMode!='I':
										WordleGameText="Wordle "+NYT['days_since_launch']
								else:
										WordleGameText="Infinite Wordle"
								print(f"You can copy the below text, normally with Ctrl-Shift-C, but it will change depending on your terminal.\nIt may look garbled or strange, but it should copy correctly.\n{WordleGameText} {Attempt+1}/{Attempts}\n{ShareText}")#I would copy it automatically, but it depends so much by system that it's not worth it and it would be its own program.
						break
				else:
						if GameMode=='P':
								Attempt=0
								print(LtRstW+"Change!"+LtRst)
								RandomWord=ValidWord(False)
								if KBDisplay:KBColours=['']*26
						elif GameMode=='M':
								Attempt=0
								LapCount+=1
								RandomWord=PossibleAnswers[RandFromTime(len(PossibleAnswers))]
								if KBDisplay:KBColours=['']*26
		if Attempt==Attempts and Colourrr!=[1,1,1,1,1]:
				print("Sorry, you ran out of attemps.",end='') #Add system to see answer.
				if GameMode=='P':print(" The other player wins.")
				elif GameMode=='M':print(f" You made it {LapCount} round(s).")
