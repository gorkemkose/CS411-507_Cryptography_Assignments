# -*- coding: utf-8 -*-
"""q4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1B3UPph5rTHXsiE_VX9iGGy-NTkSt1YHC
"""

import binascii

def PolDeg(P):
    n = len(P)
    i = n-1
    while (P[i] == 0):
        i = i-1
    return i

def xor(list1, list2):
  XORed = []
  for idx in range(len(list1)):
    if list1[idx] == list2[idx]:
      XORed.append(0)
    else:
      XORed.append(1)
  return XORed 

def decimal2Binary(decimal, degree):
  binary = bin(decimal)
  binary2 = []
  for k in range(len(binary)-1, -1, -1):
    if binary[k] != 'b':
      binary2.append(int(binary[k]))
    else:
      break
  for adding in range(degree - len(binary2)) :
    binary2.append(0)
  binary2.reverse()
  return binary2

def allElementsList(degree):
  allElementsInField = []
  for i in range(0, pow(2,degree)):
    binary = decimal2Binary(i, degree)
    allElementsInField.append(binary)
  return allElementsInField

def generator(degree, paramPoly):
  poly = paramPoly.copy()
  poly.remove(1)

  allElementsInField = allElementsList(degree)
  soon = False #do we encounter the 1 to soon, without generating all elements in group
  count = 0 #how many elements did we generate so far
  generated = [] #list to store the generated elements

  lastElementIdx = degree-1

  for power in range(0, 2**degree):
    C = [0] * degree
    if power < degree: #then everything is normal, no need to substitute any polynomial 
      C[lastElementIdx] = 1
      lastElementIdx -=1
      generated.append(C)
      #print(power, "->", C)
      count +=1
    elif power == degree: #for example a^4 will be equal to a + 1
      C = poly.copy()
      C[0] = 0
      generated.append(C)
      #print(power, "->", C)
      count +=1
    else:
      lastAddedElement = generated[len(generated)-1]
      if lastAddedElement[0] == 1: #xors, just shift by left
        willAdded = lastAddedElement.copy()
        willAdded = willAdded[1:] + willAdded[:1]
        willAdded[len(willAdded)-1] = 0
        willbeXORed = poly.copy()
        willbeXORed[0] = 0
        result = xor(willAdded, willbeXORed)
        #print(power, "->", result)
        generated.append(result)
        count +=1
        if (1 not in result[:len(result)-1]) and result[len(result)-1] == 1 and count < (2**degree)-1:
          soon = True
          break
      else:
        result = lastAddedElement[1:] + lastAddedElement[:1]
        generated.append(result)
        #print(power, "->", result)
        count +=1
        if (1 not in result[:len(result)-1]) and result[len(result)-1] == 1 and count < (2**degree)-1:
          soon = True
          break

  if soon:
    return False
  else:
    myList = []
    generated.remove(decimal2Binary(1, degree))
    allElementsInField.remove(decimal2Binary(0, degree))
    for item in allElementsInField:
      for element in generated:
        if element == item:
          myList.append(item)

    if len(myList) == pow(2, degree) -1:
      return True
    else:
      return False

P1 = [1, 0, 0, 0, 1, 1, 0, 1] #x^7 + x^3 + x^2 + 1
degree1 = PolDeg(P1) #we will compute GF(2^degree) field
is_p1_primitive = generator(degree1, P1)

P2 = [1, 0, 0, 0, 0, 0, 1, 1] #x^7 + x + 1
degree2 = PolDeg(P2)
is_p2_primitive = generator(degree2, P2)

print("P1 ->", is_p1_primitive)
print("P2 ->", is_p2_primitive)