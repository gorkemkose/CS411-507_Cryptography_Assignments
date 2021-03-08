import requests # if this lib isn't installed yet --> pip install requests or pip3 intall requests

#Dont forget to open vpn
API_URL = 'http://10.36.52.109:5000' # ATTN: This is the current server (do not change unless being told so) 

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

#a function to count the letters in the ciphertext for the frequency analysis, updates the letter_count dictionary accordingly
def countLetters(ciphertext):
  for idx in range(0, len(ciphertext)):
    if ciphertext[idx].isalpha():
      letter_count[ciphertext[idx]] += 1

def Affine_Dec(ptext, key):
    plen = len(ptext)
    ctext = ''
    for i in range (0,plen):
        letter = ptext[i]
        if letter in turkish_alphabet:
            poz = turkish_alphabet[letter]
            poz = (key.gamma*poz+key.theta)%29
            ctext += inv_turkish_alphabet[poz]
        else:
            ctext += ptext[i]
    return ctext

class key(object):
    alpha=0
    beta=0
    gamma=0
    theta=0

def possible_alpha_beta_pairs(x, y):
  alpha_beta_pairs = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6:0, 7: 0, 8: 0, 9: 0, 10: 0,
                      11: 0, 12:0, 13:0, 14:0, 15: 0, 16:0 ,17: 0, 18:0, 19: 0, 20:0, 21: 0, 22:0, 23: 0, 24:0, 25: 0, 26:0, 27:0, 28:0}
  x_num = turkish_alphabet[x]
  y_num = turkish_alphabet[y]
  for alpha in alpha_beta_pairs.keys():
    k = (x_num * alpha) % 29
    beta = (y_num -k) % 29
    alpha_beta_pairs[alpha] = beta
  return alpha_beta_pairs

if __name__ == '__main__':
    my_id = 25359	# ATTN: change this to your id number. it should be 5 digit number
    
    cipher_text = None
    letter = None

    endpoint = '{}/{}/{}'.format(API_URL, "affine_game", my_id )
    response = requests.get(endpoint) 	#get your ciphertext and most freq. letter
    if response.ok:	#if you get your ciphertext succesfully
        c = response.json()
        cipher_text = c[0]    #this is your ciphertext
        letter = c[1] 	#the most frequent letter in your plaintext

############ write decryption code for affine cipher here ##########

        turkish_alphabet ={'A':0, 'B':1, 'C':2, 'Ç':3, 'D':4, 'E':5, 'F':6, 'G':7, 'Ğ':8, 'H':9, 'I':10,
                'İ': 11, 'J':12, 'K':13, 'L':14, 'M':15, 'N':16, 'O':17, 'Ö':18, 'P':19, 
                'R':20, 'S':21,  'Ş':22, 'T':23, 'U':24, 'Ü':25, 'V':26, 'Y':27,
                'Z':28}

        inv_turkish_alphabet = {0:'A', 1:'B', 2:'C', 3:'Ç', 4:'D', 5:'E', 6:'F', 7:'G', 8:'Ğ', 9:'H',
                    10:'I', 11:'İ', 12:'J', 13:'K', 14:'L', 15:'M', 16:'N', 17:'O', 18:'Ö',
                    19:'P', 20:'R', 21:'S',  22:'Ş', 23:'T', 24:'U', 25:'Ü', 26:'V',
                    27:'Y', 28:'Z'}

        letter_count = {'A':0, 'B':0, 'C':0, 'Ç':0, 'D':0, 'E':0, 'F':0, 'G':0, 'Ğ':0, 'H':0, 'I':0,
                'İ': 0, 'J':0, 'K':0, 'L':0, 'M':0, 'N':0, 'O':0, 'Ö':0, 'P':0, 
                'R':0, 'S':0,  'Ş':0, 'T':0, 'U':0, 'Ü':0, 'V':0, 'Y':0, 'Z':0}

        countLetters(cipher_text)

        for dictkey in letter_count:
            if letter_count[dictkey] == max(letter_count.values()):
                frequent_in_ctext = dictkey

        alpha_beta_pairs = possible_alpha_beta_pairs(letter, frequent_in_ctext)

        for dictkey in alpha_beta_pairs.keys():
            key.alpha = dictkey
            key.beta = alpha_beta_pairs[dictkey]
            key.gamma = modinv(key.alpha, 29) # you can compute decryption key from encryption key
            key.theta = 29 - (key.gamma * key.beta) % 29

            if key.alpha == 21 and key.beta == 18:
                query = Affine_Dec(cipher_text, key)
                break


####################################################################

    elif(response.status_code == 404):
        print("We dont have a student with this ID. Check your id num")
    else:
        print("It was supposed to work:( Contact your TA")


#CHECK YOUR ANSWER HERE
    query = Affine_Dec(cipher_text, key)	# ATTN: change this into the decrypted plaintext to be checked by the server. should be a string

    # Below is the sample code for sending your response back to the server
    endpoint = '{}/{}/{}/{}'.format(API_URL, "affine_game", my_id, query)
    response = requests.put(endpoint)
    if response.ok:
        c = response.json()
        print(c)
    elif (response.status_code == 404):
        print("check paramater types")
    elif(response.status_code == 406):
        print("Nope, Try again")
    elif(response.status_code == 401):
        print("Check your ID number")
    else:
        print("How did you get in here? Contact your TA")
