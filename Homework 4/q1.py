# -*- coding: utf-8 -*-
"""q1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ld7Vyxer_g2srtkFZvN4UXS3Vj0Mwm2U
"""

import random
import requests
import math

#-------------function definitions
def phi(n):
  amount = 0
  for k in range(1, n+1):
    if math.gcd(n,k) == 1:
      amount += 1
  return amount

def egcd(a,b):
  x,y,u,v = 0,1,1,0
  while a!=0:
    q,r = b//a, b%a
    m,n = x-u*q, y-v*q
    b,a,x,y,u,v = a,r,u,v,m,n
  gcd = b
  return gcd, x,y 

def modinv(a,m):
  if a < 0:
    a = m+a 
  gcd,x,y = egcd(a,m)
  if gcd!=1:
    return None
  else:
    return x%m
#----------------function definitions are over

API_URL = 'http://cryptlygos.pythonanywhere.com'

my_id = 25359   ## Change this to your ID

endpoint = '{}/{}/{}'.format(API_URL, "RSA_Oracle", my_id )
response = requests.get(endpoint) 	
c, N, e = 0,0,0 
if response.ok:	
  res = response.json()
  #print(res)
  c, N, e = res['c'], res['N'], res['e']    #get c, N, e
else: print(response.json())

######
#-----------solution------------------
r = 22 #this is a random number, but does not really matter what it is. I choose it here :)
r_to_pow_e = pow(r, e, N)
willsent = r_to_pow_e * c
c_ = willsent % N

###### Query Oracle it will return corresponding plaintext
endpoint = '{}/{}/{}/{}'.format(API_URL, "RSA_Oracle_query", my_id, c_)
response = requests.get(endpoint) 	
if response.ok: m_ = (response.json()['m_'])
else: print(response)

inv_r = modinv(r, N)
message = m_ * inv_r
message = message % N
print("message: ",message)

byte_array = message.to_bytes(message.bit_length() // 8 + 1, byteorder= "big")
messagetext = byte_array.decode("utf-8")
print(messagetext)

res = byte_array
###Send your answer to the server.
endpoint = '{}/{}/{}/{}'.format(API_URL, "RSA_Oracle_checker", my_id, res)
response = requests.put(endpoint)
print(response.json())