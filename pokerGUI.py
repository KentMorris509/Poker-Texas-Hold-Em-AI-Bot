import tkinter as tk
from tkinter import messagebox
import random
from trainingbot import DummyBot, Hand
from perceptron import Perceptron
import pandas as pd
import os

# Utility function to map card numbers to names
def get_card_name(card):
    card_dict = {
        11: "J",
        12: "Q",
        13: "K",
        14: "A",
    }
    card_number = card[0]
    card_suit = card[1]
    suit_dict = {
        1: "♠",
        2: "♥",
        3: "♦",
        4: "♣",
    }
    return f"{card_dict.get(card_number, card_number)}{suit_dict[card_suit]}"

# Basic GUI setup for Poker Texas Hold'em
class PokerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Poker Texas Hold'em")
        self.geometry("400x400")

        self.perceptrons = self.load_perceptrons()  # Load trained perceptrons
        self.dummy_bot = DummyBot()  # Initialize the bot
        self.opponent_hand = []
        self.community_cards = []
        
        self.create_widgets()

    def load_perceptrons(self):
        # Load trained perceptrons (customize this logic based on your data and models)
        perceptrons = [Perceptron() for _ in range(4)]  # Preflop, Flop, Turn, River
        perceptrons[0].fit(pd.read_csv("preflop.csv").iloc[:, :-1], pd.read_csv("preflop.csv").iloc[:, -1])
        perceptrons[1].fit(pd.read_csv("flop.csv").iloc[:, :-1], pd.read_csv("flop.csv").iloc[:, -1])
        perceptrons[2].fit(pd.read_csv("turn.csv").iloc[:, :-1], pd.read_csv("turn.csv").iloc[:, -1])
        perceptrons[3].fit(pd.read_csv("river.csv").iloc[:, :-1], pd.read_csv("river.csv").iloc[:, -1])
        
        return perceptrons
    
    def create_widgets(self):
        # Create poker game widgets
        self.player_hand_label = tk.Label(self, text="Player Hand:")
        self.flop_label = tk.Label(self, text="Flop:")
        self.turn_label = tk.Label(self, text="Turn:")
        self.river_label = tk.Label(self, text="River:")
        self.opponent_hand_label = tk.Label(self, text="Opponent Hand:")
        
        self.deal_button = tk.Button(self, text="Deal", command=self.deal)
        self.result_label = tk.Label(self, text="")

        # Pack widgets
        self.player_hand_label.pack(pady=5)
        self.flop_label.pack(pady=5)
        self.turn_label.pack(pady=5)
        self.river_label.pack(pady=5)
        self.opponent_hand_label.pack(pady=5)
        self.deal_button.pack(pady=10)
        self.result_label.pack(pady=5)
        
    def deal(self):
        # Simulate poker game
        self.dummy_bot = DummyBot()  # Reinitialize the bot to start a new game
        self.dummy_bot.generate_hand_and_table()  # Deal bot's starting hand and flop
        
        # Display initial starting hand
        player_hand = self.dummy_bot.get_hand()
        player_hand_str = ", ".join([get_card_name(card) for card in player_hand])
        self.player_hand_label.config(text=f"Player Hand: {player_hand_str}")

        # Display the flop
        flop = self.dummy_bot.get_table()  # The first three community cards
        flop_str = ", ".join([get_card_name(card) for card in flop])
        self.flop_label.config(text=f"Flop: {flop_str}")

        # Use perceptron to decide the next step based on flop data
        flop_features = [card[0] for card in flop]  # Example feature extraction
        flop_decision = self.perceptrons[1].predict([flop_features])
        if flop_decision == 1:
            self.result_label.config(text="Perceptron says: Play on Flop")
        else:
            self.result_label.config(text="Perceptron says: Fold on Flop")
        
        # Display the turn
        self.dummy_bot.generate_cards()  # Add a card for the turn
        turn = self.dummy_bot.get_table()[-1]
        turn_str = get_card_name(turn)
        self.turn_label.config(text=f"Turn: {turn_str}")

        # Determine turn decision
        turn_features = flop_features + [turn[0]]  # Extend with the turn card
        turn_decision = self.perceptrons[2].predict([turn_features])
        if turn_decision == 1:
            self.result_label.config(text="Perceptron says: Play on Turn")
        else:
            self.result_label.config(text="Perceptron says: Fold on Turn")
        
        # Display the river
        self.dummy_bot.generate_cards()  # Add a card for the river
        river = self.dummy_bot.get_table()[-1]
        river_str = get_card_name(river)
        self.river_label.config(text=f"River: {river_str}")

        # Determine river decision
        river_features = turn_features + [river[0]]  # Include the river card
        river_decision = self.perceptrons[3].predict([river_features])
        if river_decision == 1:
            self.result_label.config(text="Perceptron says: Play on River")
        else:
            self.result_label.config(text="Perceptron says: Fold on River")

        # Generate opponents and determine the winner
        self.dummy_bot.generate_opponent()  # Generate opponent hands
        opponent_hand = self.dummy_bot.get_opponents()[0]
        opponent_hand_str = ", ".join([get_card_name(card) for card in opponent_hand])
        self.opponent_hand_label.config(text=f"Opponent Hand: {opponent_hand_str}")
        
        winner = self.dummy_bot.decide_winner()  # Determine the actual winner
        self.result_label.config(text="Player Wins!" if winner == 1 else "Opponent Wins!")
        
# Create and run the GUI application
if __name__ == "__main__":
    app = PokerGUI()
    app.mainloop()