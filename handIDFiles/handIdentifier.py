# handIdentifier
# Evan Parry
# October 5, 2019
# Last updated October 5, 2019
# Designed for HackTheU Hackathon
#
# This program calculates the numerical rank, probability, and name of a poker hand.


handName = ""
handRank = 10;
handProbability = 0.1

# Searches the hand and counts how many cards there are of each suit.
def countSuits(hand):
    for card in hand:
        index = card[1]
        suitCounters[index][0]+=1  
    
# Searches the hand and counts how many cards there are of each rank.
def countRanks(hand):
    for card in hand:
        index = card[0]-2
        rankCounters[index][0]+=1

# Returns true if the highest ranked card in the sorted hand is four ranks higher than the lowest ranked card,
# making the hand a sequence.
def IsSequence(hand):
    return (hand[0][0] - 3 == hand[3][0])

# Returns the size of the largest group of cards of the same suit.
def BiggestNumberOfSameSuit():
    return suitCounters[0][0]

#Returns the size of the largest group of cards of the same rank.
def BiggestNumberOfSameRank():
    return rankCounters[0][0]

#Returns the size of the second largest group of cards of the same rank.
def SecondBiggestNumberOfSameRank():
    return rankCounters[1][0]

#Returns the rank of a High Card hand based on what that card actually is.
def HighCardRank(hand):
    return 24-hand[0][0]

#Returns the name of a High Card hand based on its rank.
#Because the actual ranking of a High Card hand is based on that card's rank, they aren't all identical.
def HighCardHandName(highestRank):
    cardName = str(highestRank)
    if (highestRank > 10):
        if (highestRank == 14):
            cardName = "Ace"
        elif (highestRank == 13):
            cardName = "King"
        elif (highestRank == 12):
            cardName = "Queen"  
    return "High Card: " + cardName

#Calculates the numerical rank of a given hand
def CalculateHandRank():
    if(BiggestNumberOfSameSuit() == 5):
        if(IsSequence(hand)):
            if(hand[0][0] == 14): #If the highest card in the hand is an ace
                return 1 #Royal Flush
            else:
                return 2 #Straight Flush
        else:
            return 5 #Flush
    elif(IsSequence(hand)):
        return 6 #Straight
    elif(BiggestNumberOfSameRank() == 4):
        return 3 #Four Of A Kind
    elif(BiggestNumberOfSameRank() == 3):
        if(SecondBiggestNumberOfSameRank() == 2):
            return 4 #Full House
        else:
            return 7 #Three Of A Kind
    elif(BiggestNumberOfSameRank() == 2):
        if(SecondBiggestNumberOfSameRank() == 2):
            return 8 #Two Pair
        else:
            return 9 #Pair
    else:
        return HighCardRank(hand) #High Card
        
# Returns the English name of a poker hand given its numerical rank.
def CalculateHandName(handRank):
    if(handRank >= 10):
        return HighCardHandName(handRank)
    index = handRank-1
    return handNameList[index]

# Returns the probability of a poker hand given its numerical rank.
def CalculateHandProbability(handRank):
    index = handRank-1
    return handRankProbabilityList[index]

# Returns a card tuple from a given string. 
# Strings must be formatted to have two digits for the rank (e.g. 03, 12, 04), a comma, then a single digit for the suit.
def CreateCardFromText(stringData):
    rank = int(stringData[0] + stringData[1]) 
    suit = int(stringData[3])
    card = (rank,suit)
    return card

# Card Rank Table
# 2
# 3
# 4
# 5
# 6
# 7
# 8
# 9
# 10
# Jack = 11
# Queen = 12
# King = 13
# Ace = 14

# Suit Table
# 0 = Hearts
# 1 = Spades
# 2 = Diamonds
# 3 = Clubs

# Hand Rank Table 
# 1 = Royal Flush
# 2 = Straight Flush
# 3 = Four Of A kind
# 4 = Full House
# 5 = Flush
# 6 = Straight
# 7 = Three Of A Kind
# 8 = Two Pair
# 9 = Pair
# 10+ = High Card

# I decided to store the hand names and hand probabilities in a pair of lists to make them easier to access later
handNameList = ["Royal Flush", "Straight Flush", "Four Of A Kind", "Full House", "Flush", "Straight", 
                    "Three Of A Kind", "Two Pair", "Pair"]
handRankProbabilityList = [0.000154, 0.00139, 0.0240, 0.1441, 0.1965, 0.3925, 2.1128, 4.7539, 42.2569, 50.1177]

#Read the cards in from the input file.
file = open("pokerHand.txt", "r")
fileLine = file.readline()
card1 = CreateCardFromText(fileLine)
fileLine = file.readline()
card2 = CreateCardFromText(fileLine)
fileLine = file.readline()
card3 = CreateCardFromText(fileLine)
fileLine = file.readline()
card4 = CreateCardFromText(fileLine)
fileLine = file.readline()
card5 = CreateCardFromText(fileLine)

# Sample hand, used for testing
#card1 = (9, 0)
#card2 = (13, 0)
#card3 = (12, 0)
#card4 = (11, 0)
#card5 = (10, 3)

# Add the cards to the hand and sort the hand from the highest ranked card to the lowest.
hand = [card1, card2, card3, card4, card5]
hand.sort(key=lambda tup: tup[0], reverse = True) 

# Diagnostic print statement.
print("The highest ranked card in your hand is: " + str(hand[0]))

# Counters for the different card suits.
numHearts = [0, "Hearts"]
numClubs = [0, "Clubs"]
numDiamonds = [0, "Diamonds"]
numSpades = [0, "Spades"]

# Put the suit counters in a list and set their values using the sorted hand.
suitCounters = [numHearts, numClubs, numDiamonds, numSpades]
countSuits(hand)

# Sort the suit counters from the largest grouping to the smallest grouping.
suitCounters.sort(key=lambda tup: tup[0], reverse = True) 

# Diagnostic print statement.
print("The single largest grouping of suits is: " + str(suitCounters[0]))

# Counters for the different card ranks.
numTwos = [0, 2]
numThrees = [0, 3]
numFours = [0, 4]
numFives = [0, 5]
numSixes = [0, 6]
numSevens = [0, 7]
numEights = [0, 8]
numNines = [0, 9]
numTens = [0, 10]
numJacks = [0, 11]
numQueens = [0, 12]
numKings = [0, 13]
numAces = [0, 14]

# Put the rank counters in a list and set their values using the sorted hand.
rankCounters = [numTwos, numThrees, numFours, numFives, numSixes, 
                numSevens, numEights, numNines, numTens, numJacks, numQueens, numKings, numAces]
countRanks(hand)

# Sort the rank counters from the largest grouping to the smallest grouping.
rankCounters.sort(key=lambda tup: tup[0], reverse = True) 

# Diagnostic print statement.
print("The single largest grouping of ranks is: " + str(rankCounters[0]))

#Calculate the hand's rank
handRank = CalculateHandRank()
handName = CalculateHandName(handRank)
handProbability = CalculateHandProbability(handRank)

print("Your hand rank is: " + str(handRank))
print("Your hand name is: " + str(handName))
print("The probability of getting this hand is: " + str(handProbability))




