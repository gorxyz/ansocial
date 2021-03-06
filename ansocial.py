#!/usr/bin/python3
import os
import time
import asyncio
import random
import threading
import webbrowser
from datetime import datetime
from multiprocessing import Process

from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.toast import toast
from kivy.uix.screenmanager import Screen,ScreenManager

from telethon.sync import TelegramClient
from telethon import TelegramClient, sync, events
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.account import CheckUsernameRequest 
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
from telethon.errors.rpcerrorlist import ApiIdInvalidError
from telethon.errors.rpcerrorlist import HashInvalidError
from telethon.errors.rpcerrorlist import PhoneCodeInvalidError

class Ansocial(MDApp):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_file('kv/ansocial.kv')
        
    def get_api(self):
        webbrowser.open("https://my.telegram.org/auth")

    def github(self):
        webbrowser.open("https://github.com/sudurraaa/Ansocial")

    def login(self):
        self.api_id = self.screen.ids.api_id.text.split()
        self.api_hash = self.screen.ids.api_hash.text.split() 
        self.phone_number = self.screen.ids.phone.text.split()

        try:
            if self.api_id == '' or self.api_hash == '' or self.phone_number == '':
                toast("required field not gived")
            else:
                self.client = TelegramClient(f'sessions/{self.phone_number}', self.api_id, self.api_hash)
                self.client.connect()
                if self.client.get_me():
                    self.screen.current = 'ansocial'
                else:
                    self.client.send_code_request(self.phone_number)
                    self.screen.current = 'verification'
                    toast("please enter verification code")

        except PhoneNumberInvalidError:
            toast("Phone number is invalid")
        except ApiIdInvalidError:
            toast("Api id is invalid")
        except HashInvalidError:
            toast("Hash is invalid")

    def verify(self):
        if self.screen.ids.verify_code.text != '':
            try:
                self.client.sign_in(self.phone_number, self.screen.ids.verify_code.text)
                if self.client.is_user_authorized():
                    self.screen.current = 'ansocial'
                    toast("logined in")

            except PhoneCodeInvalidError:
                toast("verification code is invalid")
        else:
            toast("no verification code founded")
    
    def search(self):
        try:
            self.screen.ids.search_user.opacity = 0
            self.screen.ids.search.opacity = 0
            self.screen.ids.sending_key.opacity = 1 
            self.screen.ids.sending_key.text = "[color=00ff01]KEY SENDED,WAITING KEY[/color]"
            for key in os.listdir("key/"):
                if key.endswith(f'{self.client.get_me().id}.pem'):
                    self.starting_chat(True)
                    #self.thread_chat = Process(target=self.starting_chat, args=(True,))
                    #self.thread_chat.start()
                    #self.thread_chat.join()
                else:
                    friend_id = self.client.get_entity(self.screen.ids.search_user.text).id
                    generate_thread = Process(target=self.generate_key)
                    generate_thread.start()
                    generate_thread.join()
                    self.client.send_file(self.screen.ids.search_user.text, f'{friend_id}.pem')
                    self.starting_chat(False)

        except ValueError:
            toast("user not founded")
            self.screen.ids.sending_key.opacity = 0
            self.screen.ids.search.opacity = 1
            self.screen.ids.send.opacity = 1
            self.screen.ids.search_user.opacity = 1

    def starting_chat(self, key_exists):
        if key_exists is False:
            self.screen.ids.sending_key.text = '[color=00ff00]STARTING ENCRYPTED CHAT[/color]'
            received_key = self.client.get_messages(self.screen.ids.search_user.text, limit=1)
            for messages in received_key:
                if messages.media is not None:
                    self.client.download_media(message=messages,file='key/')
            for key in os.listdir("key/"):
                if key.endswith(f'{self.client.get_me().id}.pem'):
                    self.screen.ids.sending_key.enable = False
                    self.screen.ids.sending_key.opacity = 0
                    self.screen.ids.search.enable = False
                    self.screen.ids.search.opacity = 0
                    self.screen.ids.search_user.enable = False
                    self.screen.ids.search_user.opacity = 0 

                    self.screen.ids.message.pos_hint = {"center_x" : 0.43, "center_y" : 0.1}
                    self.screen.ids.send.pos_hint = {"center_x" : 0.91, "center_y" : 0.1} 
                    self.screen.ids.scroll_chat.pos_hint = {"center_x" : 0.5, "center_y" : 0.85}
                    toast('encrypted chat started')
                    #thread_receive = Process(target=self.receive_message)
                    #thread_receive.start()
                    #thread_receive.join()
            else:
                self.screen.ids.sending_key.text = '[color=#00ff00]KEY SENDED WAITING KEY[/color]'
                for key in os.listdir('key/'):
                    if key.endswith(f'{self.client.get_me().id}.pem'):
                        self.screen.ids.sending_key.enable = False
                        self.screen.ids.sending_key.opacity = 0
                        self.screen.ids.search.enable = False
                        self.screen.ids.search.opacity = 0
                        self.screen.ids.search_user.enable = False
                        self.screen.ids.search_user.opacity = 0 

                        self.screen.ids.message.pos_hint = {"center_x" : 0.43, "center_y" : 0.1}
                        self.screen.ids.send.pos_hint = {"center_x" : 0.91, "center_y" : 0.1} 
                        self.screen.ids.scroll_chat.pos_hint = {"center_x" : 0.5, "center_y" : 0.85}
                        toast('encrypted chat started')

        elif key_exists is True:
            self.screen.ids.sending_key.text = '[color=00ff00]STARTING ENCRYPTED CHAT[/color]'
            time.sleep(2)
            self.screen.ids.sending_key.enable = False
            self.screen.ids.sending_key.opacity = 0
            self.screen.ids.search.enable = False
            self.screen.ids.search.opacity = 0
            self.screen.ids.search_user.enable = False
            self.screen.ids.search_user.opacity = 0 

            self.screen.ids.message.pos_hint = {"center_x" : 0.43, "center_y" : 0.1}
            self.screen.ids.send.pos_hint = {"center_x" : 0.91, "center_y" : 0.1} 
            self.screen.ids.scroll_chat.pos_hint = {"center_x" : 0.5, "center_y" : 0.85}
            toast('encrypted chat started')
        else:
            self.screen.ids.sending_key.text = "[color=#00ff00]ERROR\nSOMETHING WENT WRONG[/color]"

                                
    def generate_key(self):
        self.friend_id = self.client.get_entity(self.screen.ids.search_user.text).id
        key = RSA.generate(2048)
        private_key = key.export_key()
        with open("key/private.pem", "wb") as private_key_out:
            private_key_out.write(private_key)

        public_key = key.public_key().export_key()
        with open("receiver.pem", "wb") as public_key_out:
            public_key_out.write(public_key)

        os.rename("receiver.pem", str(self.friend_id) + '.pem') 

    def send_message(self):
        me = self.client.get_me()
        my_username = me.username
        if my_username is None: my_username = me.phone

        if self.screen.ids.message.text != '':
            encode_thread = Process(target=self.encoding_message, args=(self.screen.ids.message.text,))
            encode_thread.start()
            encode_thread.join()
            #self.encoding_message(self.screen.ids.message.text)
            #threading.Thread(target=self.encode_message, args=(self.screen.ids.message.text,)).start() 
            self.screen.ids.chat_history.text += f'[color=#00ff00]{my_username}[/color][color=#ffffff]: {self.screen.ids.message.text}[/color]\n[color=#00ff00][size=11]{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}[/size][/color]\n' 
            self.screen.ids.message.text = ''
        else:
            toast("cant send empty message")

    def encoding_message(self, message):
        my_id = self.client.get_me().id
        my_key = str(my_id) + '.pem'
        chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        encoded_message_title = ""
        for _ in range(40):
            encoded_message_title += random.choice(chars)
        encoded_message_title += '.bin'

        encoded_file = open(f'encode/{encoded_message_title}', 'wb')
        recipient_key = RSA.import_key(open(f'key/{my_key}').read())
        session_key = get_random_bytes(16)
        
        cipher_rsa = PKCS1_OAEP.new(recipient_key)
        enc_session_key = cipher_rsa.encrypt(session_key)
        
        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(str(message).encode("utf-8"))
        [ encoded_file.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext) ]
        encoded_file.close()

        self.client.send_file(self.screen.ids.search_user.text, f'encode/{encoded_message_title}')


    def receive_message(self):
        self.received_message = self.client.get_messages(self.screen.ids.search_user.text, limit=4)
        while True:
            for message in self.received_message:
                if message.media is not None:
                    if message.file.name.endswith('.bin'):
                        self.decode_message_title = message.file.name
                        self.client.download_media(message.media, file='decode/')
                        decode_thread = Process(target=self.decoding_message, args=(f'decode/{self.decode_message_title}',))
                        decode_thread.start()
                        decode_thread.join()

    def decoding_message(self, decode):
        decode_file = open(decode, 'rb')

        private_key = RSA.import_key(open("private.pem").read())
        enc_session_key, nonce, tag, ciphertext = \
        [ decode_file.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1) ]
        cipher_rsa = PKCS1_OAEP.new(private_key)
        session_key = cipher_rsa.decrypt(enc_session_key)
        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        decode_message = cipher_aes.decrypt_and_verify(ciphertext, tag)
        
        decoded_message = decode_message.decode("utf-8")
        
        self.screen.ids.chat_history.text += f'\n[color=#00ff00]{self.screen.ids.search_user.text}[/color]: [color=#ffffff{decoded_message}[/color\n[color=#00ff00][size=11]{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}[/size][/color]\n' 


    def build(self):
        return self.screen

if __name__ == '__main__':
    Ansocial().run()
