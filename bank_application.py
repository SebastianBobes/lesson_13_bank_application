# sa adaugam clienti noi
# sa verificam balanta pentru fiecare client
# sa modificam balanta clientilor(transfer intre clienti)
# extras de cont, printeaza datele intr un fisier nou

# sa schimb fct login, optiunea de forget passwd, daca isi introduce corect numarul de telefon si user-ul
# sau o functie separata pentru resetare parola
from caesar import encrypt
from caesar import decrypted
import json
import random
import string
import pwinput

OKBLUE = '\033[94'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


def get_all_clients(path: str = "clients.json") -> list:
    with open(path, "r") as f:
        clients = json.loads(f.read())
        clients = clients['clients']
    return clients


def get_client(username: str, path: str = "clients.json") -> dict:
        with open(path, "r") as f:
            clients = json.loads(f.read())
            clients = clients['clients']
            for client in clients:
                if username == client['id']:
                    return client



def add_client(new_client: dict, path: str, auth_path: str = "auth.json"):
    # generate new ID
    id = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    new_client["id"] = id

    with open(path, "r+") as file:
        clients = json.loads(file.read())
        file.seek(0)
        clients["clients"].append(new_client)
        file.write(json.dumps(clients, indent=4))

    with open(auth_path, "r+") as f:
        users = json.loads(f.read())
        new_passwd = ''.join(random.choices(string.digits, k=3))
        add_user_passwords(username=new_client['id'], password=new_passwd)
        users[id] = encrypt(new_passwd)
        print(f"Clientul {new_client['nume']} cu user-ul {id} are parola: {new_passwd}")
        f.seek(0)
        f.write(json.dumps(users, indent=4))



def forgot_or_change_password(username):
    print("Ai intrat in meniul pentru schimmbare a parolei. "
          "Vei primi cateva intrebari pentru a ne asigura ca tu esti detinatorul contului.")
    clients = get_all_clients()
    dict = get_client(username=username)
    print(dict)
    k = 0
    while k <= 3:
        x = input("Care este numarul tau de telefon?")
        if x == dict['telefon']:
            k = 0
            break
        else:
            k += 1
        if k == 3:
            print(f"{FAIL}Ai raspuns de 3 ori gresit!{ENDC}")
            exit()

    k = 0
    while k <= 3:
        x = input("Care este orasul in care locuiesti?")
        if x == dict['oras']:
            new_passwd = input("Dati o noua parola:")
            new_passwd2 = input("Repetati parola:")
            while new_passwd != new_passwd2:
                new_passwd2 = input("Parolele nu se potrivesc! Incercati din nou:")
            with open("auth.json", 'r+') as f:
                dict = json.loads(f.read())
                dict[username] = encrypt(new_passwd)
                f.seek(0)
                f.write(json.dumps(dict, indent=4))
                print(f"{OKGREEN}Parola a fost schimbata cu succes!{ENDC}")
                add_user_passwords(username=username, password=new_passwd)
                break
        else:
            k += 1
        if k == 3:
            print(f"{FAIL}Ai raspuns de 3 ori gresit!{ENDC}")
            exit()




def login(path: str = "auth.json") -> str:
    with open(path, "r") as f:
        credentials = json.loads(f.read())



    username = input("Introduceti user ul: ")
    while username not in credentials:
        username = input("Wrong user. ")

    passwd = input("Citeste parola:")
    # # passwd = pwinput.pwinput(prompt='PW: ', mask='*')
    # passwd = maskpass.askpass(mask="*")
    for k in range(2):
        if passwd != decrypted(credentials[username]):
            passwd = input("Parola gresita: ")
            if k == 1:
                choice=int(input("""Parola a fost introdusa incorect de 3 ori!
                                1. FORGOT PASSWORD
                                2.EXIT """))
                match choice:
                    case 1:
                        forgot_or_change_password(username)
                        pass
                    case 2:
                        exit()
                    case _:
                        exit()

    return username





def check_balance(user: str, path: str = "clients.json") -> list:
    balances = []
    clients = get_all_clients(path)
    if user == "admin":
        for client in clients:
            balances.append(f"Nume {client['nume']} are in cont {client['balanta']} lei")
    else:
        for client in clients:
            if user == client["id"]:
                balances.append(f"Nume {client['nume']} are in cont {client['balanta']} lei")
                break
    return (balances)




def wire_money(sender: str, recipient: str, clients: list, path: str = "clients.json"):
    money = int(input("Introduceti suma de bani pe care vreti sa o trimiteti: "))
    clients_info = get_client(username=sender, clients=clients)
    recipient_info = get_client(username=recipient, clients=clients)
    while clients_info['balanta'] < money or money < 0:
        money = input(f"{FAIL}Suma este prea mare. Introduceti alta suma sau exit:{ENDC} ")
        if money == "exit":
            exit()
        else:
            money = int(money)
    if clients_info and recipient_info:
        recipient_info['balanta'] += money
        clients_info['balanta'] -= money

        with open(path, "w") as f:
            client_dict = {"clients": clients}
            f.write(json.dumps(client_dict, indent=4))

        print(f"{OKGREEN}Money transfer was successful{ENDC}")
    else:
        print(f"{FAIL}Something went wrong!Sender or receiver not found!{ENDC}")

def see_all_decrypted_and_crypted_passwords(path1: str = "auth.json", path2: str = "passwords.json"):
    with open(path1, "r") as f:
        dict = json.loads(f.read())
        dict2 = {}
        for k, v in dict.items():
            dict2[k]={"encrypted": v, "decrypted": decrypted(v)}
        with open(path2, "w") as f:
            f.write(json.dumps((dict2), indent=4 ))

def add_user_passwords(username:str,password:str, path = "passwords.json"):
    with open(path, "r+") as f:
        dict = json.loads(f.read())
        dict[username] = {"encrypted": password, "decrypted": decrypted(password)}
        f.seek(0)
        f.write(json.dumps((dict), indent=4))





if __name__ == '__main__':
    MENU = """
    1. Adauga client.
    2. Verifica balanta.
    3. Transfer de balanta.
    4. Extras de cont.
    5.Sign out.
    6.Exit
    7.Schimbare parola.
        """
    see_all_decrypted_and_crypted_passwords()
    username = login()
    user_pick = input(MENU + " ")

    while user_pick.lower() != "exit":
        match user_pick:

            case "1":
                if username == "admin":
                    client_info = input("Introduceti datele clientului in ordinea data: nume, "
                                        "telefon, oras, balanta:"
                                        " ")
                    client_info = client_info.split()
                    new_client = {"nume": client_info[0], "telefon": client_info[1], "oras": client_info[2],
                                  "balanta": int(client_info[3])}

                    add_client(new_client, path="clients.json")
                else:
                    print("Nu ai autorizatie!")

            case "2":

                balances = check_balance(username)
                print("\n".join(balances))

            case "3":
                if username == "admin":
                    print("You are not allowed to send money!")
                else:
                    clients = get_all_clients()
                    print("\n\n")
                    clients_usernames = []
                    for index, client in enumerate(clients):
                        print(f"{index + 1}. {client['nume']}-{client['id']}")
                        clients_usernames.append(client['id'])
                    recipient = input("Type in the user you want to send money to: ")
                    while recipient == username or recipient not in clients_usernames:
                        recipient = input("Wrong receiver.Pleas input again.")
                    wire_money(sender=username, recipient=recipient, clients=clients)

            case "4":
                if username == "admin":
                    print("Nu poti face extras de cont cu user-ul actual:")
                else:
                    client = get_client(username)
                    with open(f"{client['nume']}.json", "w") as file:
                        file.write(json.dumps(client, indent=4))
                    pass

            case "5":
                username = login()
                pass
            case "6":
                exit()
            case "7":
                forgot_or_change_password(username)



        print("\n\n")
        user_pick = input(MENU + " ")

