# Skeleton Program for the AQA AS Summer 2018 examination
# this code should be used in conjunction with the Preliminary Material
# written by the AQA AS Programmer Team
# developed in a Python 3 environment


# Version Number : 1.6

SPACE = " "
EOL = "#"
EMPTYSTRING = ""


def ReportError(s):
    print("{0:<5}".format("*"), s, "{0:>5}".format("*"))


def StripLeadingSpaces(Transmission):
    TransmissionLength = len(Transmission)
    if TransmissionLength > 0:
        FirstSignal = Transmission[0]
        while (FirstSignal == SPACE and TransmissionLength > 0):  # breaks when it finds first character thats not a space, doesnt return, so only gets rid of leading spaces.
            TransmissionLength -= 1
            Transmission = Transmission[1:]
            if TransmissionLength > 0:
                FirstSignal = Transmission[0]
    if TransmissionLength == 0:
        ReportError("No signal received")  # nothing in the file
    return Transmission


def StripTrailingSpaces(Transmission):
    LastChar = len(Transmission) - 1
    while Transmission[LastChar] == SPACE:
        LastChar -= 1
        Transmission = Transmission[:-1]
    return Transmission


def GetTransmission():
    FileName = input("Enter file name: ")
    try:
        FileHandle = open(FileName, "r")
        Transmission = FileHandle.readline()  # only gets first line of text file
        FileHandle.close()
        Transmission = StripLeadingSpaces(Transmission)
        if (len(Transmission) > 0):  # CHECKS that there is a transmission before calling function, other way round for leadingSpaces                                                      may ASK for change
            Transmission = StripTrailingSpaces(Transmission)
            Transmission = Transmission + EOL
    except:
        ReportError("No transmission found")  # no file
        Transmission = EMPTYSTRING
    return Transmission


def GetNextSymbol(i, Transmission):  # really checks current Symbol, turns series of = into dots, dashes and spaces.
    if Transmission[i] == EOL:  # if end of line
        print()
        print("End of transmission")
        Symbol = EMPTYSTRING
    else:
        SymbolLength = 0
        Signal = Transmission[i]
        while Signal != SPACE and Signal != EOL:  # checks '=' signs next to eachother
            i += 1
            Signal = Transmission[i]
            SymbolLength += 1  # adds 1 for every '='
        if SymbolLength == 1:  # defines symbol just processed
            Symbol = "."
        elif SymbolLength == 3:
            Symbol = "-"
        elif SymbolLength == 0:
            Symbol = SPACE
        else:
            ReportError("Non-standard symbol received")  # number of '=' > 3
            Symbol = EMPTYSTRING
    return i, Symbol


def GetNextLetter(i, Transmission):  # returns a string of symbols (dots dashes and spaces), corresponding to one letter
    SymbolString = EMPTYSTRING
    LetterEnd = False
    while not LetterEnd:
        i, Symbol = GetNextSymbol(i, Transmission)  # gets one symbol (current one)
        if (Symbol == SPACE):  # just processed symbol space, only processes that 3 into 7 spaces (in between words)
            LetterEnd = True
            i += 4
        elif Transmission[i] == EOL:
            LetterEnd = True
        elif (Transmission[i + 1] == SPACE and Transmission[i + 2] == SPACE):  # checks first beause [i+1], checks next one
            LetterEnd = True
            i += 3
        else:
            i += 1
        SymbolString = SymbolString + Symbol
    return i, SymbolString


def Decode(CodedLetter, Dash, Letter, Dot):
    CodedLetterLength = len(CodedLetter)
    Pointer = 0
    for i in range(CodedLetterLength):  # uses Dash, Dot to find index in Letter
        Symbol = CodedLetter[i]
        if Symbol == SPACE:
            return SPACE
        elif Symbol == "-":
            Pointer = Dash[Pointer]  # see disgram in preliminary material
        else:
            Pointer = Dot[Pointer]  # see disgram in preliminary material
    return Letter[Pointer]


def ReceiveMorseCode(Dash, Letter, Dot):
    PlainText = EMPTYSTRING
    MorseCodeString = EMPTYSTRING
    Transmission = GetTransmission()
    LastChar = len(Transmission) - 1
    i = 0
    while i < LastChar:
        i, CodedLetter = GetNextLetter(i, Transmission)  # gets morse code letter (symbol string), e.g. '--.'
        MorseCodeString = MorseCodeString + SPACE + CodedLetter  # adds to final output
        PlainTextLetter = Decode(CodedLetter, Dash, Letter, Dot)  # takes morse code, turns it into plain text
        PlainText = PlainText + PlainTextLetter  # adds to final output
    print(MorseCodeString)
    print(PlainText)


def SendMorseCode(MorseCode):
    PlainText = input("Enter your message (uppercase letters and spaces only): ")

    for char in PlainText:
        if char != char.upper():#this is shit, it should just convert text to uppercase
            exit()

    PlainTextLength = len(PlainText)
    MorseCodeString = EMPTYSTRING
    for i in range(PlainTextLength):
        PlainTextLetter = PlainText[i]
        if PlainTextLetter == SPACE:
            Index = 0
        else:
            Index = ord(PlainTextLetter) - ord("A") + 1  #subtracts the asci value of the current letter from the asci value of "A" 
        CodedLetter = MorseCode[Index]
        MorseCodeString = MorseCodeString + CodedLetter + SPACE
    print(MorseCodeString)


def DisplayMenu():
    print()
    print("Main Menu")
    print("=========")
    print("R - Receive Morse code")
    print("S - Send Morse code")
    print("X - Exit program")
    print()


def GetMenuOption():
    MenuOption = EMPTYSTRING
    while len(MenuOption) != 1:
        MenuOption = input("Enter your choice: ")
    return MenuOption


def SendReceiveMessages():
  Dash = [20,23,0,0,24,1,0,17,0,21,0,25,0,15,11,0,0,0,0,22,13,0,0,10,0,0,0]
  Dot = [5,18,0,0,2,9,0,26,0,19,0,3,0,7,4,0,0,0,12,8,14,6,0,16,0,0,0]
  Letter = [' ','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

  MorseCode = [' ','.-','-...','-.-.','-..','.','..-.','--.','....','..','.---','-.-','.-..','--','-.','---','.--.','--.-','.-.','...','-','..-','...-','.--','-..-','-.--','--..']

  ProgramEnd = False
  while not ProgramEnd:
    DisplayMenu()
    MenuOption = GetMenuOption()
    if MenuOption == "R":
        ReceiveMorseCode(Dash, Letter, Dot)
    elif MenuOption == "S":
        SendMorseCode(MorseCode)
    elif MenuOption == "X":
        ProgramEnd = True


if __name__ == "__main__":
    SendReceiveMessages()
