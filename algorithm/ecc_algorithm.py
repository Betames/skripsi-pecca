from tinyec.ec import SubGroup, Curve
from random import randint
import pickle
import os
from algorithm.utilities import utilities


class Ecc:
    def __init__(self):
        self.field = SubGroup(p=65629, g=(4, 46171), n=65538, h=1)
        self.curve = Curve(a=-8, b=31, field=self.field, name="p65629")

        self.encode_map = {}
        self.decode_map = {}
        if os.path.exists("../data/encode_map.pickle") and os.path.exists("../data/decode_map.pickle"):
            self.encode_map = pickle.load(open("data/encode_map.pickle", "rb"))
            self.decode_map = pickle.load(open("data/decode_map.pickle", "rb"))
        else:
            for k in range(1, self.curve.field.n):
                p = k * self.curve.g
                if p.x is None:
                    break
                self.encode_map[k] = p
                self.decode_map['' + str(p.x) + ',' + str(p.y)] = k

            pickle.dump(self.encode_map, open("data/encode_map.pickle", "wb"))
            pickle.dump(self.decode_map, open("data/decode_map.pickle", "wb"))

        self.random_k = randint(1, self.curve.field.n)
        self.random_index = randint(1, self.curve.field.n)

    def encryptDataEC(self, ascii_list, k, k_pub, random_index):
        encrypted_datas = []
        encrypted_points = []
        point_list_size = len(self.encode_map)
        for data in ascii_list:
            index = int((data + random_index) % point_list_size)
            encoded_point = self.encode_map[index]
            if encoded_point.x is None:
                decoded_point = self.decode_map[
                    '' + str(encoded_point.x) + ',' + str(-encoded_point.y % point_list_size)]
                encrypted_datas.append(decoded_point)
            else:
                c2 = encoded_point + k * k_pub
                encrypted_points.append(c2)
                try:
                    decoded_point = self.decode_map['' + str(c2.x) + ',' + str(c2.y)]
                    encrypted_datas.append(decoded_point)
                except Exception:
                    encrypted_datas.append(-1)
        return encrypted_datas

    def decryptDataEC(self, encrypted_datas, k, k_priv, random_index):
        decrypted_datas = []
        point_list_size = len(self.encode_map)
        for data in encrypted_datas:
            encoded_point = self.encode_map[data]
            if encoded_point.x is None:
                decoded_point = self.decode_map[
                    '' + str(encoded_point.x) + ',' + str(-encoded_point.y % point_list_size)]
                decrypted_datas.append(decoded_point)
            else:
                c1 = k * self.curve.g
                c2 = encoded_point - k_priv * c1
                try:
                    decoded_point = self.decode_map['' + str(c2.x) + ',' + str(c2.y)]
                    decoded_point = (decoded_point - random_index) % point_list_size
                    decrypted_datas.append(decoded_point)
                except Exception:
                    decrypted_datas.append(-1)
        return decrypted_datas

    def encryptTextECC(self, plaintext, k, k_priv, random_index):
        k_pub = k_priv * self.curve.g
        plainstr_to_asc_list = utilities.str_to_ascii(plaintext)
        encrypted_ascii_list = self.encryptDataEC(plainstr_to_asc_list, k, k_pub, random_index)
        # print(encrypted_ascii_list)
        encrypted_text = utilities.ascii_to_str(encrypted_ascii_list)
        return encrypted_text

    def decryptTextECC(self, ciphertext, k, k_priv, random_index):
        encrypted_ascii_list = utilities.str_to_ascii(ciphertext)
        decrypted_ascii_list = self.decryptDataEC(encrypted_ascii_list, k, k_priv, random_index)
        # print(decrypted_ascii_list)
        decrypted_text = utilities.ascii_to_str(decrypted_ascii_list)
        return decrypted_text


ecc_class = Ecc()
