# handIdentifier
# Evan Parry
# October 6, 2019
# Last updated October 6, 2019
# Designed for HackTheU Hackathon
#
# This program lets the user input values to create a poker hand file.


fileName = raw_input("What do you want to call this file? (do not include .txt extension): ")
fileName += ".txt"
f = open(fileName, "w")

#Creates five lines for five cards.
for i in range(5):
    print("Creating card " + str(i+1))
    cardRank = raw_input("What is this card's rank? ")
    
    #Accounts for text input for the rank
    if(cardRank == "Jack" or cardRank == "jack" or cardRank == "J" or cardRank == "j"):
        cardRank = 11
    elif(cardRank == "Queen" or cardRank == "queen" or cardRank == "Q" or cardRank == "q"):
        cardRank = 12
    elif(cardRank == "King" or cardRank == "king" or cardRank == "K" or cardRank == "k"):
        cardRank = 13
    elif(cardRank == "Ace" or cardRank == "ace" or cardRank == "A" or cardRank == "a"):
        cardRank = 14
        
    
    cardSuit = raw_input("What is this card's suit? ")
    
    #Accounts for text input for the suit
    if(cardSuit == "Hearts" or cardSuit == "hearts" or cardSuit == "H" or cardSuit == "h"):
        cardSuit = 0
    elif(cardSuit == "Spades" or cardSuit == "spades" or cardSuit == "S" or cardSuit == "s"):
        cardSuit = 1
    elif(cardSuit == "Diamonds" or cardSuit == "diamonds" or cardSuit == "D" or cardSuit == "d"):
        cardSuit = 2
    elif(cardSuit == "Clubs" or cardSuit == "clubs" or cardSuit == "C" or cardSuit == "c"):
        cardSuit = 3
    
    inputString = str(cardRank)+","+str(cardSuit)
    f.write(inputString + "\n")
    
f.close()
    