# secret santa generator
import csv
import random
import smtplib, ssl

def get_player_info(all_info):
    name = input("Name: ")
    email = input("Email: ")
    wishlist = input("Wishlist items: ")
    print("\n")
    all_info[name]=[email, wishlist]
    

def get_player_info_csv(all_info):
    filename = input("Please enter csv file name: ")
    filename = filename + ".csv"
    print("Reading csv file...\n")
    with open(filename) as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for name, email, wishlist in reader:
            all_info[name]=[email, wishlist]


def get_secret_santa(all_info):
    info_copy = all_info.copy()
    print("Matching all players to their secret santa...\n")
    for key in all_info.keys():
        recipient_notfound = True
        while recipient_notfound:
            recipient = random.choice(list(info_copy.keys()))
            if (recipient != key):
                info_copy.pop(recipient)
                recipient_notfound = False
        all_info[key].append(recipient)
        all_info[key].append(all_info.get(recipient)[1])


def output_secret_santa_as_txt(all_info):
    f= open("secret_santa_list.txt","w+")
    num=0
    for key, values in all_info.items():
        num += 1
        player = key
        recipient = values[-2]
        f.write("Player {}: {}, Recipient: {}\n".format(num, player, recipient))
    f.close()
    print("Output players list with respective recipient into secret_santa_list.txt\n")
            
def send_email(all_info):
    message = """Subject: Secret Santa Recipient

Hi {name},

Please prepare a present for {recipient}. {recipient}'s wishlist items: {wishlist}.

Best regards,
Secret Santa Generator"""

    from_address = input("Enter broadcaster email address: ")
    password = input("Type your password and press enter: ")

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(from_address, password)
        for key, values in all_info.items():
            email = values[0]
            recipient = values[-2]
            wishlist = values[-1]
            name = key
            server.sendmail(
                from_address,
                email,
                message.format(name=name,recipient=recipient,wishlist=wishlist),
            )
    print("Emails sent!")

def main():
    print("----Welcome to Secret Santa Generator!----")
    print("(1) Enter player details")
    print("(2) Read player details from csv file")
    while True:
        value = input('Enter choice (1) or (2): \n')
        try:
            choice = int(value)
        except ValueError:
            print('Please enter a valid number.')
            continue
        if 1 <= choice <= 2:
           break
        else:
           print('Invalid option. Please enter 1 or 2.')
    
    players_info = {}

    if (choice == 1):
        while True:
            value_ = input('Enter number of players: ')
            try:
                num_players = int(value_)
            except ValueError:
                print('Please enter a valid number.')
                continue
            if 2 <= num_players <= 100:
               break
            else:
               print('Invalid range, please enter number from 2-100.')
        print("\n")
        for i in range(0, num_players):
            print("Enter player {} info: ".format(i+1))
            get_player_info(players_info)
        #print(players_info)
    elif (choice == 2):
        get_player_info_csv(players_info)
        #print(players_info)

    get_secret_santa(players_info)
    #print(players_info)
    output_secret_santa_as_txt(players_info)
    send_email(players_info)


main()
    
    
