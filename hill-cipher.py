# This programs uses the Hill Cipher to encrypt and decrypt a phrase
# Created by John Stromberg

import numpy as np


# gets input and converts it into a matrix of numbers
def word_to_matrix(word):
    word = word.lower()  # hill cipher requires only lower case letters
    int_arr = []
    for letters in word:
        if letters != " ":
            int_arr.append(ord(letters) - 96 - 1)  # turns letters into numbers
    while len(int_arr) % 3 != 0:
        int_arr.append(23)  # adds placeholders x's at the end of the matrix if needed
    # turns that array into a nx1 matrix
    word_mat = np.mat(int_arr)
    word_mat = word_mat.reshape(int(len(int_arr) / 3), 3)  # turns the matrix into an n x 3 matrix
    return word_mat


# Randomly generates a 3x3 key matrix
def key_gen():
    while True:
        curr_key = np.random.randint(27, size=(3, 3))
        key_det = np.linalg.det(curr_key)
        key_det = round(key_det)
        if key_det != 0:  # the matrix must have an inverse
            if key_det % 2 != 0:  # matrix not have any common factors with the modular base
                if key_det % 13 != 0:
                    return curr_key


# takes a matrix and a key and encrypts it using the given key
def encrypt_matrix(word_mat, key_mat):
    encrypt_mat = np.matmul(word_mat, key_mat)  # multiplies the two matrices together
    encrypt_mat = encrypt_mat % 26
    return encrypt_mat


# Calculates the inverse of the given key
def calc_inverse(key_mat):
    key_det = np.linalg.det(key_mat)
    key_det = round(key_det)
    temp_inv = np.linalg.inv(key_mat)

    # Calc the conj
    key_conj = temp_inv * key_det
    key_conj = np.round(key_conj)
    key_conj = key_conj % 26

    # calc the new det
    # this is needed since we have a congruence instead of an equation
    # this is a version of the Euclidean algorithm
    z = 0
    while True:
        if z * key_det % 26 == 1:
            break
        else:
            z = z + 1

    # calc inverse
    inv_key = z * key_conj
    inv_key = inv_key % 26
    return inv_key


# calc the decrypt of a given inverse key and encrypted matrix
def decrypt_matrix(encrypt_mat, inv_key):
    decrypt_mat = np.matmul(encrypt_mat, inv_key)
    decrypt_mat = decrypt_mat % 26
    return decrypt_mat


# takes a matrix of number and turns it into a string
def matrix_to_words(matrix):
    final_string = ""
    row, col = np.shape(matrix)
    decrypt_mat = matrix.reshape((row * col), 1)
    for row in decrypt_mat:
        for i in row:
            final_string += chr(int(i) + 97)
    return final_string


def main():
    while True:
        print("\nEnter a word or phrase to get encrypted:")
        word = input()
        while not all(x.isalpha() or x.isspace() for x in word):  # makes sure there are only letters enters
            print("Input must only be letters, please enter again:")
            word = input()

        # ENCRYPTING----------------------------------------------------------

        word_mat = word_to_matrix(word)
        key_mat = key_gen()
        # if you want a specific key matrix, uncomment this line
        # key_mat = np.array([[1, 4, 0], [7, 11, 2],[0, 5, 1]])
        encrypt_mat = encrypt_matrix(word_mat, key_mat)
        encrypt_word = matrix_to_words(encrypt_mat)

        print("Starting Word: \n", word_mat)
        print("Key Matrix: \n", key_mat)
        print("Encrypted Matrix: \n", encrypt_mat)
        print("Encrypted Message: \n", encrypt_word)

        # DECRYPTING----------------------------------------------------------

        inv_key = calc_inverse(key_mat)
        decrypt_mat = decrypt_matrix(encrypt_mat, inv_key)
        final_word = matrix_to_words(decrypt_mat)

        print("INVERSE KEY: \n", inv_key)
        print("Decrypted Matrix: \n", decrypt_mat)
        print("Final String: \n", final_word)

main()
