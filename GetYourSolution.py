import random 
import numpy as np

from Interactive import GradingSystem, length_5

if __name__ == '__main__':

  # now iteration
  words = 10
  ob = GradingSystem(quiet=False,length_5=length_5)
  words = ob.PossibleWords()

  while words > 1:
    ob.AddingAGuess()
    myWord = ''
    for i in range(5):
      if ob.known[i] == '':
        myWord += '_'
      else:
        myWord += ob.known[i]
    print('The word is now' + ' '*25 + myWord)
    print('You may use %s to fill in the blanks' % (','.join(ob.contain)))

    words = ob.PossibleWords()
