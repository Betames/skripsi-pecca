from tinyec.ec import SubGroup, Curve
import pickle
import os
from algorithm.utilities import utilities
import time

field = SubGroup(p=65629, g=(4, 46171), n=65538, h=1)
curve = Curve(a=-8, b=31, field=field, name="p65629")

encode_map = {}
decode_map = {}
if os.path.exists("data/encode_map.pickle") and os.path.exists("data/decode_map.pickle"):
    encode_map = pickle.load(open("data/encode_map.pickle", "rb"))
    decode_map = pickle.load(open("data/decode_map.pickle", "rb"))
else:
    for k in range(1, curve.field.n):
        p = k * curve.g
        if p.x is None:
            break
        encode_map[k] = p
        decode_map['' + str(p.x) + ',' + str(p.y)] = k

    pickle.dump(encode_map, open("data/encode_map.pickle", "wb"))
    pickle.dump(decode_map, open("data/decode_map.pickle", "wb"))

# random_k = randint(1, curve.field.n)
random_k = 5443
# random_index = randint(1, curve.field.n)
random_index = 37347


def encryptDataEC(ascii_list, k, k_pub, random_index):
    encrypted_datas = []
    encrypted_points = []
    point_list_size = len(encode_map)
    for data in ascii_list:
        index = int((data + random_index) % point_list_size)
        encoded_point = encode_map[index]
        if encoded_point.x is None:
            decoded_point = decode_map[
                '' + str(encoded_point.x) + ',' + str(-encoded_point.y % point_list_size)]
            encrypted_datas.append(decoded_point)
        else:
            c2 = encoded_point + k * k_pub
            encrypted_points.append(c2)
            try:
                decoded_point = decode_map['' + str(c2.x) + ',' + str(c2.y)]
                encrypted_datas.append(decoded_point)
            except Exception:
                encrypted_datas.append(-1)
    return encrypted_datas


def decryptDataEC(encrypted_datas, k, k_priv, random_index):
    decrypted_datas = []
    point_list_size = len(encode_map)
    for data in encrypted_datas:
        encoded_point = encode_map[data]
        if encoded_point.x is None:
            decoded_point = decode_map[
                '' + str(encoded_point.x) + ',' + str(-encoded_point.y % point_list_size)]
            decrypted_datas.append(decoded_point)
        else:
            c1 = k * curve.g
            c2 = encoded_point - k_priv * c1
            try:
                decoded_point = decode_map['' + str(c2.x) + ',' + str(c2.y)]
                decoded_point = (decoded_point - random_index) % point_list_size
                decrypted_datas.append(decoded_point)
            except Exception:
                decrypted_datas.append(-1)
    return decrypted_datas


def encryptTextECC(plaintext, k, k_priv, random_index):
    k_pub = k_priv * curve.g
    plainstr_to_asc_list = utilities.str_to_ascii(plaintext)
    encrypted_ascii_list = encryptDataEC(plainstr_to_asc_list, k, k_pub, random_index)
    # print(encrypted_ascii_list)
    encrypted_text = utilities.ascii_to_str(encrypted_ascii_list)
    return encrypted_text


def decryptTextECC(ciphertext, k, k_priv, random_index):

    encrypted_ascii_list = utilities.str_to_ascii(ciphertext)
    decrypted_ascii_list = decryptDataEC(encrypted_ascii_list, k, k_priv, random_index)
    # print(decrypted_ascii_list)
    decrypted_text = utilities.ascii_to_str(decrypted_ascii_list)

    return decrypted_text


# f = open("input_text_files/01 lutung kasarung.txt", 'r', encoding='utf-8')
# msg = f.read().replace("\n", "").rstrip("")
# f.close()
# print(msg[:100])
#
# start = time.time()
# encrypt = encryptTextECC(msg, random_k, 10, random_index)
# end = time.time()
# enc_time = utilities.calculateTime(start, end)
# print('enc time: ', enc_time)
# print("enc success")
# # print(encrypt)
#
# start = time.time()
# decrypt = decryptTextECC(encrypt, random_k, 10, random_index)
# end = time.time()
# dec_time = utilities.calculateTime(start, end)
# print("dec time: ", dec_time)
# print("dec success")
# print(decrypt[:100])

# file = open("cipher_text_files/cipher_ecc/cipher04.txt", 'w', encoding='utf-8')
# file.write(encrypt)
# file.close()
#
# file = open("decipher_text_files/decipher_ecc/decipher04.txt", 'w', encoding='utf-8')
# file.write(decrypt)
# file.close()
