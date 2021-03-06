# -*- coding: utf-8 -*-
"""q2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UbwzKvpYMd5FXm1GvzfB5jlmheeQOzmU
"""

!apt-get install libenchant1c2a
!pip install pyenchant

import enchant
d = enchant.Dict("en_US")

# The extended Euclidean algorithm (EEA)
def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    gcd = b
    return gcd, x, y

# Modular inverse algorithm that uses EEA
def modinv(a, m):
    if a < 0:
        a = m+a
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None  # modular inverse does not exist
    else:
        return x % m

uppercase ={'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7, 'I':8,
         'J':9, 'K':10, 'L':11, 'M':12, 'N':13, 'O':14, 'P':15, 'Q':16,
         'R':17, 'S':18,  'T':19, 'U':20, 'V':21, 'W':22, 'X':23, 'Y':24,
         'Z':25}

inv_uppercase = {0:'A', 1:'B', 2:'C', 3:'D', 4:'E', 5:'F', 6:'G', 7:'H',
                 8:'I', 9:'J', 10:'K', 11:'L', 12:'M', 13:'N', 14:'O', 15:'P',
                 16:'Q', 17:'R', 18:'S', 19:'T', 20:'U', 21:'V', 22:'W', 23:'X',
                 24:'Y', 25:'Z'}

letter_count = {'A':0, 'B':0, 'C':0, 'D':0, 'E':0, 'F':0, 'G':0, 'H':0, 'I':0,
         'J':0, 'K':0, 'L':0, 'M':0, 'N':0, 'O':0, 'P':0, 'Q':0,
         'R':0, 'S':0,  'T':0, 'U':0, 'V':0, 'W':0, 'X':0, 'Y':0, 'Z':0}

def Affine_Dec(ptext, key):
    plen = len(ptext)
    ctext = ''
    for i in range (0,plen):
        letter = ptext[i]
        if letter in uppercase:
            poz = uppercase[letter]
            poz = (key.gamma*poz+key.theta)%26
            ctext += inv_uppercase[poz]
        else:
            ctext += ptext[i]
    return ctext

class key(object):
    alpha=0
    beta=0
    gamma=0
    theta=0

#a function to count the letters in the ciphertext for the frequency analysis, updates the letter_count dictionary accordingly
def countLetters(ciphertext):
  for idx in range(0, len(ciphertext)):
    if ciphertext[idx].isalpha():
      letter_count[ciphertext[idx]] += 1

#a function to determine the possible alpha and beta pairs to exhaustively search
#arguments: x which is the character in plaintext,
#           y which is the character in ciphertext
#this function only works for a known plain-ciphertext letter pair
def possible_alpha_beta_pairs(x, y):
  alpha_beta_pairs = {1: 0, 3: 0, 5: 0, 7: 0, 9: 0, 11: 0, 15: 0, 17: 0, 19: 0, 21: 0, 23: 0, 25: 0}
  x_num = uppercase[x]
  y_num = uppercase[y]
  for alpha in alpha_beta_pairs.keys():
    k = (x_num * alpha) % 26
    beta = (y_num - k) % 26
    alpha_beta_pairs[alpha] = beta
  return alpha_beta_pairs

#a function that splits a sentence into its words and construct a list of these words
#since the enchant library, check function works with words but not sentences, we need to have a list of words of each possible plain sentence
def list_of_words_in_sentence(sentence):
  list_of_words = []
  word = ""
  for char in sentence:
    if char.isalpha():
      word += char
    else:
      list_of_words.append(word)
      word = ""
  list_of_words.append(word)
  for i in range(0, list_of_words.count("")):
    list_of_words.remove("")
  return list_of_words


ciphertext = "Xpjjbxx lx eng klerm, krlmpob lx eng krgrm: lg lx gcb jnportb gn jneglepb gcrg jnpegx."
ciphertext = ciphertext.upper() #to simplify the process of counting
frequent_in_ptext = "T"

countLetters(ciphertext)

#dedicated to find the frequent letter in ciphertext using letter_count dictionary
for dictkey in letter_count:
  if letter_count[dictkey] == max(letter_count.values()):
    frequent_in_ctext = dictkey

alpha_beta_pairs = possible_alpha_beta_pairs(frequent_in_ptext, frequent_in_ctext)

#for each possible alpha-beta pair (total of 12), we compute the encryption and decryption keys
#using the Affine_Dec function provided by the instructor, we decrypt the ciphertext and split the resulting sentence into its words
#in order to make a language check
#if all of its words are in english, then print the plaintext and corresponding encryption and decryption keys, else omit that one
for dictkey in alpha_beta_pairs.keys():
  key.alpha = dictkey
  key.beta = alpha_beta_pairs[dictkey]
  key.gamma = modinv(key.alpha, 26) # you can compute decryption key from encryption key
  key.theta = 26 - (key.gamma * key.beta) % 26
  
  dtext = Affine_Dec(ciphertext, key)
  list_of_words = list_of_words_in_sentence(dtext)
  in_english = True

  for item in list_of_words:
    if not d.check(item):
      in_english = False
      break

  if in_english:
    print(dtext.lower().capitalize())
    print("Encryption key => alpha =", key.alpha, "and beta =", key.beta)
    print("Decryption key => gamma =", key.gamma, "and theta =", key.theta)