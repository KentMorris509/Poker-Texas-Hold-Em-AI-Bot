#python file for creating poker dummy bot in order to create training input data
import random
from enum import Enum

class Hand(Enum):
    HIGH_CARD = 0
    PAIR = 1
    TWO_PAIR = 2
    THREE_KIND = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_KIND = 7
    STRAIGHT_FLUSH = 8
    ROYAL_FLUSH = 9


class DummyBot:
   
    def __init__(self):
        self.hand = [] #dummy hand
        self.table = [] #cards on table
        self.cur_cards = {} #tracks max 4 of each card value
        self.suits = {} #tracks any repeated card generations
        self.opponents = [] #opponent hand
        

    #generate dummy's hand and flop
    def generate_hand_and_table(self):
        #hand
        for i in range(2):
            card = random.randint(2,14) #14 technically counts as 1 and 14 (ace)
            suit = random.randint(1,4)
            while (card,suit) in self.suits: #check for existing card
                suit = ((suit+1)%4)+1
            self.suits[(card,suit)] = 1
            self.hand.append((card,suit)) 
            self.cur_cards[card] = self.cur_cards.get(card, 0) + 1
        
        #flop
        for i in range(3):
            card = random.randint(2,14)
            suit = random.randint(1,4)
            if card in self.cur_cards:
                while self.cur_cards[card] == 4: #make sure not more than 4 of card number/face
                    card = random.randint(2,14)
            while (card,suit) in self.suits: #check for existing card
                suit = ((suit+1)%4)+1
            self.suits[(card,suit)] = 1
            self.table.append((card,suit))
            self.cur_cards[card] = self.cur_cards.get(card, 0) + 1


    #generate opponent for chance of losing/winning
    def generate_opponent(self):
        self.opponents.append([])
        for i in range(2):
            card = random.randint(2,14) #14 technically counts as 1 and 14 (ace)
            suit = random.randint(1,4)
            if card in self.cur_cards:
                while self.cur_cards[card] == 4: #make sure not more than 4 of card number/face
                    card = random.randint(2,14)
            while (card,suit) in self.suits: #check for existing card
                suit = ((suit+1)%4)+1
            self.suits[(card,suit)] = 1
            self.opponents[-1].append((card,suit)) 
            self.cur_cards[card] = self.cur_cards.get(card, 0) + 1

    #generate another table card each round
    def generate_cards(self):
        card = random.randint(2,14)
        suit = random.randint(1,4)
        if card in self.cur_cards:
            while self.cur_cards[card] == 4: #make sure not more than 4 of card number/face
                card = random.randint(2,14)
        while (card,suit) in self.suits: #check for existing card
            suit = ((suit+1)%4)+1
        self.suits[(card,suit)] = 1
        self.table.append((card,suit))
        self.cur_cards[card] = self.cur_cards.get(card, 0) + 1

    def decide_winner(self):
        if len(self.cur_cards) < 7:
            print("not enough cards")
            return
        else:
            #create own hand
            bot_hand = self.check_hand(self.hand + self.table)
            #create opponent hands
            op_hands = []
            for o in self.opponents:
                op_hands.append(o + self.table)

            #check if opponent has better hand
            for hand in op_hands:
                if hand[0] > bot_hand[0]:
                    return -1
                elif hand[0] == bot_hand[0]:
                    if hand[1] > bot_hand[1]:
                        return -1
                    elif hand[1] == bot_hand[1]:
                        return 0
            #if not, bot wins
            return 1


    def check_hand(self, hand):
        card_nums = [x[0] for x in hand]
        card_nums += [x[0] for x in self.table]
        card_nums.sort()
        card_suits = [x[1] for x in hand]
        card_suits += [x[1] for x in self.table]

        high = card_nums[0]
        combo = Hand.HIGH_CARD
        #check for duplicate combos
        new_val = False
        for i in range(1,len(card_nums)):
            if card_nums[i] > high:
                high = card_nums[i]
            if card_nums[i] == card_nums[i-1] and new_val == False:
                if combo == Hand.HIGH_CARD:
                    combo = Hand.PAIR
                elif combo == Hand.PAIR:
                    combo = Hand.THREE_KIND
                elif combo == Hand.THREE_KIND:
                    combo = Hand.FOUR_KIND
            elif card_nums[i] == card_nums[i-1] and new_val:
                if combo == Hand.HIGH_CARD:
                    combo = Hand.PAIR
                elif combo == Hand.PAIR:
                    combo = Hand.TWO_PAIR
                elif combo == Hand.THREE_KIND:
                    combo = Hand.FULL_HOUSE
            elif card_nums[i] != card_nums[i-1] and combo != Hand.HIGH_CARD:
                new_val = True

        #check for same suit
        suit = card_suits[0]
        flush = True
        for i in range(1,len(card_suits)):
            if card_suits[i] != suit:
                flush = False
        
        #check for straight
        straight = False
        if combo == Hand.HIGH_CARD:
            straight = True
            for i in range(1,len(card_nums)):
                if card_nums[i] != card_nums[i-1]+1:
                    straight = False
                
        if straight and flush:
            if card_nums[-1] == 14:
                combo = Hand.ROYAL_FLUSH
            else:
                combo = Hand.STRAIGHT_FLUSH
        elif combo != Hand.FOUR_KIND and combo != Hand.FULL_HOUSE:
            if flush:
                combo = Hand.FLUSH
            elif straight:
                combo = Hand.STRAIGHT

        return (combo, high)