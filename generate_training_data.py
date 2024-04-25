from trainingbot import DummyBot
def main():
    user_in = input("How many records would you like to generate? ")
    record_num = int(user_in.strip().split()[0])
    dummy = DummyBot()
    pre_flop_f = input("What would you like the name of the pre-flop data file to be? ")
    flop_f = input("The flop data file? ")
    turn_f = input("The turn data file? ")
    river_r = input("The river data file? ")
    try:
        pre_flop = open(pre_flop_f, 'w')
        flop_f = open(flop_f, 'w')
        turn_f = open(turn_f, 'w')
        river_r = open(river_r, 'w')
        for _ in range(record_num):
            #simulate game to create data record
            dummy.generate_hand_and_table()
            hand = dummy.get_hand()
            table = dummy.get_table()
            for card in hand:
                pre_flop.write(str(card[0]) + " " + str(card[1]) + "\n")
                flop_f.write(str(card[0]) + " " + str(card[1]) + "\n")
                turn_f.write(str(card[0]) + " " + str(card[1]) + "\n")
                river_r.write(str(card[0]) + " " + str(card[1]) + "\n")
            for card in table:
                flop_f.write(str(card[0]) + " " + str(card[1]) + "\n")
                turn_f.write(str(card[0]) + " " + str(card[1]) + "\n")
                river_r.write(str(card[0]) + " " + str(card[1]) + "\n")
            
            dummy.generate_opponent()
            dummy.generate_opponent()
            dummy.generate_cards()
            card = dummy.get_table()
            turn_f.write(str(card[0]) + " " + str(card[1]) + "\n")
            river_r.write(str(card[0]) + " " + str(card[1]) + "\n")
            
            dummy.generate_cards()
            card = dummy.get_table()
            river_r.write(str(card[0]) + " " + str(card[1]) + "\n")
            
            winner = dummy.decide_winner()
            pre_flop.write(str(winner) + "\n\n")
            flop_f.write(str(winner) + "\n\n")
            turn_f.write(str(winner) + "\n\n")
            river_r.write(str(winner) + "\n\n")


    except:
        pass