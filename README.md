# Terminaldle
Wordle in the terminal! You can play multiple modes, including — but not limited to — today's and archived Wordles, and Pass&Play against a (nerdy) friend. 

Simply run `WORDLE.PY` with Python, and you're set! The `--help` argument shows this page:
```
-H    --HELP /? -?   Exit the program and provide this screen.
-HTP  --HOW-TO-PLAY  Exit the program and display a how-to-play screen.
-L    --LINKS        Exit the program and display links to the Wordle sub-websites, including help and solution sites.
-A    --ATTEMPTS     Change the number of maximum attempts to make it easier or harder. Default is 6.
-M    --Mode         Select your mode.
OPTIONS:
  (I)nfinite.
  New (Y)ork Times today.
  A Wordle from the NYT (A)rchives.

-KBH  --KEYBOARD-HISTORY  Doesn't clear the contents of previous word's keyboards.
-K    --KEYBOARD          Select a keyboard to display during the game. Default is ABC.
OPTIONS: (In order of)
  ABC      The alphabet.
  QWERTY   A QWERTY keyboard.
  AZERTY   An AZERTY keyboard.
  WORKMAN  A workman keyboard.
  FREQ     Frequency of the letters in English.
  NONE     No keyboard display.

-C   --COLOURS  Changes the colour modes the game runs in.
OPTIONS: (COLOUR=COLOR=COL, HIGH=HI, 256-COL=256COL)
  CLASSIC            The normal colour scheme of the game. All correct and same as the website.
  8-COLOUR           For terminals that only support 8 colours. Not recommended unless needed.
  256-COLOUR         For terminals that only support up to the 256 colour palatte.
  HIGH-CONTRAST      Increases vibrance of the colours to make them easier to see in a terminal.
  NYT-HIGH-CONTRAST  Adds the official high contrast colour palatte of Wordle.

Type 'QUIT' while the program's running to exit.
Arguments do not have to be capitalized.
If colours are not displaying properly, try the colours option.
```
## Usage example
Let's say we want to do today's Wordle. We'll want to share it, and everything else should be as it is in real Wordle.
```
py WORDLE.PY --MODE Y --SHARE YES --KEYBOARD QWERTY
py WORDLE.PY -m y -s 0 -kb qwerty
```
Alright. Let's do every option we can. We want to play marathon mode, our machine only has 256 colour support in it's terminal, we want to make it a little easier, etc.
```
py WORDLE.PY --ATTEMPTS 7 --MODE M --KEYBOARD-HISTORY --KEYBOARD FREQ --COLOURS 256-COLOUR
py WORDLE.PY -a 7 -m m -kbh -k freq -c 256col
py WORDLE.PY -A 7 -m M -kbh --KEYBOARD freq --COLOR 256color
```
## Thanks and credits
All credit, of course, goes to Josh Wardle, for the creation of the game, and The New York Times Games division for maintaining it. The official link can be found [here](https://www.nytimes.com/games/wordle/index.html). I used the Wordle API, at https://www.nytimes.com/svc/wordle/v2/YYYY-MM-DD.json. The word lists, while sourced from the NYT page, was distributed by Cyrus Freshman at their GitHub [page](https://gist.github.com/cfreshman). Your local ANSWERS.TXT and GUESSABLES.TXT should be updated from their page.

Thanks to the guides on ANSI escape codes, which are used heavily and are necessary for the game to work. [Burke Libbey's guide](https://notes.burke.libbey.me/ansi-escape-codes/) and [Christopher Yeh's](https://chrisyeh96.github.io/2020/03/28/terminal-colors.html) were incredibly valuable resources. Thanks to you both! [Burke's Github](https://github.com/burke) (@burke), and [Christopher's](https://github.com/chrisyeh96) (@chrisyeh96).
