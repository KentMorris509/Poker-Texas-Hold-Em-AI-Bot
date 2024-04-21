#python file for creating poker dummy bot in order to create training input data
import random


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