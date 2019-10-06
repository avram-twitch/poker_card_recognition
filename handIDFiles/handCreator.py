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
    if(cardRank == "Jack"):
        cardRank = 11
    elif(cardRank == "Queen"):
        cardRank = 12
    elif(cardRank == "King"):
        cardRank = 13
    elif(cardRank == "Ace"):
        cardRank = 14
        
    
    cardSuit = raw_input("What is this card's suit? ")
    
    #Accounts for text input for the suit
    if(cardSuit == "Hearts"):
        cardSuit = 0
    elif(cardSuit == "Spades"):
        cardSuit = 1
    elif(cardSuit == "Diamonds"):
        cardSuit = 2
    elif(cardSuit == "Clubs"):
        cardSuit = 3
    
    inputString = str(cardRank)+","+str(cardSuit)
    f.write(inputString + "\n")
    
f.close()
    