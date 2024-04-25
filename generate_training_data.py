from trainingbot import DummyBot
def main():
    user_in = input("How many records would you like to generate? ")
    record_num = int(user_in.strip().split()[0])
    dummy = DummyBot()
    file_name = input("What would you like the name of the data file to be? ")
    try:
        f = open(file_name, 'w')
        for num in range(record_num):
            #simulate game to create data record
            pass

    except:
        pass