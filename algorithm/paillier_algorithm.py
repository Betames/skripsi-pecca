import math
import pickle
import os
import sys
from algorithm.primes import prime_class
import time
from algorithm.utilities import utilities


class Paillier:
    class PrivateKey(object):
        def __init__(self, bits):
            p = prime_class.generate_prime(bits / 2)
            q = prime_class.generate_prime(bits / 2)
            # print('p: ' + str(p), 'q: ' + str(q))
            n = p * q
            self.lam = (p - 1) * (q - 1)
            self.pub = Paillier().PublicKey(bits, n)
            self.mu = self.invmod(self.lam, n)

        def invmod(self, a, p):
            '''
            a * b == 1 mod p
            '''
            r = a
            d = 1
            while True:
                d = ((p // r + 1) * d) % p
                r = (d * a) % p
                if r == 1:
                    break
            return d

    class PublicKey(object):
        def __init__(self, bits, n):
            self.bits = bits
            self.n = n
            self.n_sq = n * n
            self.g = n + 1

    def __init__(self):
        self.encode_dict = {}
        self.decode_dict = {}
        if os.path.exists(utilities.resource_path("data/encode_dict.pickle")) \
                and os.path.exists(utilities.resource_path("data/decode_dict.pickle")):
            self.encode_dict = pickle.load(open(utilities.resource_path("data/encode_dict.pickle"), "rb"))
            self.decode_dict = pickle.load(open(utilities.resource_path("data/decode_dict.pickle"), "rb"))
        else:
            index = 0
            for i in range(0, sys.maxunicode + 1):
                if chr(i).isprintable():
                    self.encode_dict['' + chr(i)] = index
                    self.decode_dict[index] = chr(i)
                    index += 1

            pickle.dump(self.encode_dict, open(utilities.resource_path('data/encode_dict.pickle'), "wb"))
            pickle.dump(self.decode_dict, open(utilities.resource_path('data/decode_dict.pickle'), "wb"))

        # self.private = self.PrivateKey(192)
        # self.public = self.private.pub
        # self.r = self.get_r_value(self.public)

    def encode_to_number(self, plain):
        encoded_number = 0
        for i in range(len(plain)):
            number = int(self.encode_dict[plain[i]]) * (len(self.encode_dict) ** i)
            encoded_number += number
        return encoded_number

    def decode_to_string(self, number):
        num = int(number)
        temp = []
        while num != 0:
            temp.append(self.decode_dict[num % len(self.decode_dict)])
            num //= len(self.decode_dict)
        if len(temp) == 9:
            temp.append(' ')
        # print(temp)
        return ''.join(temp)

    def get_r_value(self, pub):
        while True:
            r = prime_class.generate_prime(round(math.log(pub.n, 2)))
            if 0 < r < pub.n:
                break
        return r

    def encrypt(self, plain, pub, r):

        x = pow(r, pub.n, pub.n_sq)
        cipher = (pow(pub.g, plain, pub.n_sq) * x) % pub.n_sq
        return cipher

    def decrypt(self, cipher, priv):
        pub = priv.pub
        x = pow(cipher, priv.lam, pub.n_sq) - 1
        plain = ((x // pub.n) * priv.mu) % pub.n
        return plain

    def encryptTextPaillier(self, plaintext, pub, r):
        plain_list = list(plaintext)
        divided_plaintext = []
        encoded_number_list = []
        encrypted_number_list = []
        cipher = ""
        if len(plain_list) % 10 != 0:
            for i in range(len(plain_list) // 10 + 1):
                if i * 10 + 10 > len(plain_list):
                    divided_plaintext.append(plain_list[i * 10:len(plain_list)])
                else:
                    divided_plaintext.append(plain_list[i * 10:i * 10 + 10])
        else:
            for i in range(len(plain_list) // 10):
                divided_plaintext.append(plain_list[i * 10:i * 10 + 10])

        # check if len text = 9 in divided_plaintext except the last element
        for idx in range(len(divided_plaintext) - 1):
            if len(divided_plaintext[idx]) == 9:
                divided_plaintext[idx] = divided_plaintext[idx] + ' '

        # remove '\n' from list and remove empty list from list
        if divided_plaintext[-1][-1] == "\n":
            divided_plaintext[-1] = divided_plaintext[-1][:-1]
        if not divided_plaintext[-1]:
            divided_plaintext.pop()
        # print(divided_plaintext)
        for p in divided_plaintext:
            encoded_number = self.encode_to_number(p)
            encoded_number_list.append(encoded_number)
        # print(encoded_number_list)
        for encoded in encoded_number_list:
            encrypted_number = self.encrypt(encoded, pub, r)
            encrypted_number_list.append(encrypted_number)
        # print(encrypted_number_list)
        # v = []
        for enc in encrypted_number_list:
            encrypted_string = self.decode_to_string(enc)
            if len(encrypted_string) == 22:
                encrypted_string = encrypted_string + ' '
            # v.append(encrypted_string)
            cipher += encrypted_string
        # print(v)
        # for i in v:
        #     print(len(i))
        # return cipher, encrypted_number_list
        return cipher

    def decryptTextPaillier(self, cipher, priv):
        cipher_list = list(cipher)
        divided_ciphertext = []
        encoded_num_list = []
        decrypted_number_list = []
        plain = ""

        if len(cipher_list) % 23 != 0:
            for i in range(len(cipher_list) // 23 + 1):
                if i * 10 + 10 > len(cipher_list):
                    divided_ciphertext.append(cipher_list[i * 23:len(cipher_list)])
                else:
                    divided_ciphertext.append(cipher_list[i * 23:i * 23 + 23])
        else:
            for i in range(len(cipher_list) // 23):
                divided_ciphertext.append(cipher_list[i * 23:i * 23 + 23])

        # check if len text = 22 in divided_ciphertext except the last element
        for idx in range(len(divided_ciphertext) - 1):
            if len(divided_ciphertext[idx]) == 22:
                divided_ciphertext[idx] = divided_ciphertext[idx] + ' '

        # remove '\n' from list and remove empty list from list
        if divided_ciphertext[-1][-1] == "\n":
            divided_ciphertext[-1] = divided_ciphertext[-1][:-1]
        if not divided_ciphertext[-1]:
            divided_ciphertext.pop()

        # print(divided_ciphertext)

        for c in divided_ciphertext:
            encoded_num = self.encode_to_number(c)
            encoded_num_list.append(encoded_num)
        # print(encoded_num_list)

        # for encoded in enc_num_list:
        for encoded in encoded_num_list:
            decrypted_number = self.decrypt(encoded, priv)
            decrypted_number_list.append(decrypted_number)
        # print(decrypted_number_list)
        # u = []
        for dec in decrypted_number_list:
            decrypted_string = self.decode_to_string(dec)
            if len(decrypted_string) == 9:
                decrypted_string = decrypted_string + ' '
            # u.append(decrypted_string)
            plain += decrypted_string
        # print(u)
        # for i in u:
        #     print(len(i))
        return plain


paillier_class = Paillier()
paillier_priv_key = paillier_class.PrivateKey(192)
paillier_pub_key = paillier_priv_key.pub
paillier_r = paillier_class.get_r_value(paillier_pub_key)


# f = open("../input_text_files/input1.txt", 'r', encoding='utf-8')
# msg = f.read().replace("\n", "").rstrip("")
#
# print(msg)
#
# start = time.time()
# enc = paillier_class.encryptTextPaillier(msg, paillier_pub_key, paillier_r)
# end = time.time()
# print("enc time: " + str(utilities.calculateTime(start, end)))
# print("enc success")
#
# start = time.time()
# dec = paillier_class.decryptTextPaillier(enc, paillier_priv_key)
# end = time.time()
# print("dec time: " + str(utilities.calculateTime(start, end)))
# print("dec success")
# print(dec)
