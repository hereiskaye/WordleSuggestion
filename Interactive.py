import random 
import numpy as np

def load_words():
  with open('words_alpha.txt') as word_file:
    valid_words = set(word_file.read().split())

  return valid_words


english_words = load_words()
# demo print
# print('fate' in english_words)
# print(type(english_words))
length_5 = set()
for word in english_words:
  if len(word) == 5:
    length_5.add(word)
length_5 = list(length_5)
print('In total there are %d words' % (len(length_5)))


class GenerateQuestion(object):
  def __init__(self,seed=None,quiet=False,answer='saved',length_5=[]):
    if seed:
      random.seed = seed
      self.answer = random.choice(length_5)
    else:
      self.answer = answer
    return
  def AddOne(self,Add):
    colors = '' 
    for i,char in enumerate(Add):
      if self.answer[i] == char:
        colors += 'G'
      elif char in self.answer:
        colors += 'Y'
      else:
        colors += 'K'
    # print(Add)
    # print(colors)
    return colors

# ob = GenerateQuestion()
# color = ob.AddOne('table')
 

class GradingSystem(object):
  def __init__(self,quiet=False,seed=1,length_5=[]):
    self.quiet = quiet
    self.seed = seed
    # Collected info 
    self.contain = ''
    self.notpresent = ''
    self.known = {}
    self.bad = {}
    for i in range(5):
      self.known[i] = ''
      self.bad[i] = ''

    # Info of the dictionary
    self.length_5 = np.array(length_5)
    self.size_5 = np.size(self.length_5)
    self.weight = np.zeros((26,5))
    self.weight.fill(1.) # the self.weight of grade
    self.found = self.length_5[:]
    self.UpdateFrequency()

  def UpdateFrequency(self):
    # sort by self.position
    All = ''.join(self.found)
    self.size = np.size(self.found)
    self.pos = ['','','','','']
    for i in range(5):
      self.pos[i] = All[i::5]
      # print('i=%d, len=%d' % (i, len(self.pos[i])))
    All = ''.join(self.found)
    pos = ['','','','','']
    for i in range(5):
      pos[i] = All[i::5]
      # print('i=%d, len=%d' % (i, len(pos[i])))
    self.alphabet = 'abcdefghijklmnopqrstuvwxyz'
    # how many times a letter appears in certain self.position 
    self.RawFrequency = np.zeros((26,5))
    for i in range(26):
      for j in range(5):
        myCount = self.pos[j].count(self.alphabet[i])
        if myCount == np.size(self.found):
          if not self.quiet:
            print('I have reset [%s] at [%d] to be zero' % (self.alphabet[i],j))
          self.RawFrequency[i,j] = 0 
        else:
          self.RawFrequency[i,j] = myCount

    return 


  def AddingAGuess(self,AGuess=None,AResult=None):
    if not AGuess:
      AGuess = str(input('Input your initial guess >>'))
      AResult = str(input('What did you get? K->grey, G->Green, Y->yellow >>'))
    # update the grading system
    for i,each in enumerate(AGuess):
      if AResult[i] == 'K':
        # this letter is worthless now
        self.weight[self.alphabet.index(AGuess[i]),:] = 0
      elif AResult[i] == 'G':
        # this letter is worthless now here
        self.weight[self.alphabet.index(AGuess[i]),i] = 0
      elif AResult[i] == 'Y':
        # this letter is worthless here and where it's green 
        self.weight[self.alphabet.index(AGuess[i]),i] = 0
        for j,flag in enumerate(AResult): # search for green
          if flag == 'G': 
            self.weight[self.alphabet.index(AGuess[i]),j] = 0
    # update the info
    for i,each in enumerate(AGuess):
      if AResult[i] == 'K':
        self.notpresent += each
      elif AResult[i] == 'G':
        self.known[i] = each
        self.contain += each
      elif AResult[i] == 'Y':
        self.contain += each
        self.bad[i] += each
    self.contain = ''.join(set(self.contain))
    self.notpresent = ''.join(set(self.notpresent))
    if not self.quiet:
      print('self.contain = %s' % self.contain)
      print('self.notpresent = %s' % self.notpresent)
      print('self.known = %s' % self.known)
      print('self.bad = %s' % self.bad)
    return 

  def PossibleWords(self):
    # calculate the size of possible dict
    self.found = []    
    def Check_Word(word):
      for eachChar in self.contain:
        if not eachChar in word:
          return False 
      for eachChar in self.notpresent:
        if eachChar in word:
          return False 
      for key in self.known.keys():
        if len(self.known[key]) >0 and not word[key] == self.known[key]:
          return False 
      for key in self.bad.keys():
        if word[key] in self.bad[key]:
          return False 
      return True
    for word in self.length_5:
      if Check_Word(word):
        self.found.append(word)
    if not self.quiet:
      print('-- there are %5d possible words --' % len(self.found))
      if len(self.found) < 10:
        print(' '.join(self.found))
    if len(self.found) == 1:
      return 1
    self.UpdateFrequency()

    # calculate the best word that provide the most info
    self.weightedFrequency = self.RawFrequency*self.weight
    best_word = ''
    best_grade = 0.
    grades = []
    for word in self.length_5:
      grade = 0.
      for j,char in enumerate(word):
        # chance of getting a green letter
        green = self.weightedFrequency[self.alphabet.index(char),j]/self.size 
        # chance of getting a yellow letter
        yellow = (np.sum(self.weightedFrequency[self.alphabet.index(char)]) - green*self.size)/(self.size*4.)
        # if this position is confirmed green, then set yellow to be zero
        if self.known[j] == char:
          yellow = 0.
        if False:
          print('[%s]->%d,%s green=%e, yellow=%e' % (word,j,char,green,yellow))
          print('self.contain = %s' % self.contain)
          print('self.notpresent = %s' % self.notpresent)
          print('self.known = %s' % self.known)
          print('self.bad = %s' % self.bad)
        grade += 4.*green + 1.*yellow
      # print(word, grade)
      grades.append(grade)
      if grade >= best_grade:
        best_grade = grade
        best_word = word
    grades = np.array(grades)
    gradesinds = grades.argsort()
    sorted_grades = grades[gradesinds[::-1]]
    sorted_length_5 = self.length_5[gradesinds[::-1]]
    if not self.quiet:
      for i in range(5):
        print('top %2d -> %s %.4f' % (i+1, sorted_length_5[i], sorted_grades[i]))
    # print('noisy', sorted_grades[np.where(sorted_length_5 =='noisy')[0]])
    # print('sanes', sorted_grades[np.where(sorted_length_5 =='sanes')[0]])

    self.bestChoices = sorted_length_5
    self.bestGrades = sorted_grades


    return len(self.found) 

'''
ob = GradingSystem(quiet=False)
for i in range(6):
  ob.AddingAGuess()
  words = ob.PossibleWords()
  print('size of words now is %d' % (words))
'''

if __name__ == '__main__':
  PickAAnswer = 'bad'
  while not len(PickAAnswer) in [0,5]: 
    PickAAnswer = input('Would you like to pick a word? If yes, just enter the word, if not, press enter directly')
    if len(PickAAnswer) == 0:
      break
    if len(PickAAnswer) > 0 and len(PickAAnswer)!=5:
      print('check the length of your word please!')
    if not PickAAnswer.lower() in length_5:
      print('sorry but your words in not within the dictionary')
      PickAAnswer = 'bad'
    print('PickAAnswer = [%s]' % PickAAnswer)
    
  if len(PickAAnswer) == 0:
    Question = GenerateQuestion(seed=777,length_5=length_5)
  else:
    Question = GenerateQuestion(seed=None,answer=PickAAnswer.lower(),length_5=length_5)
  print('The program picked [%s]' % Question.answer)

  # now iteration
  words = 10
  ob = GradingSystem(quiet=True,length_5=length_5)
  words = ob.PossibleWords()

  while words > 1:
    wordInput = input('Add a word please                     ->')
    color = Question.AddOne(wordInput)
    ob.AddingAGuess(AGuess=wordInput,AResult=color) 
    print('You get' + ' '*(40-7) + color)
    myWord = ''
    for i in range(5):
      if ob.known[i] == '':
        myWord += '_'
      else:
        myWord += ob.known[i]
    print('The word is now' + ' '*25 + myWord)
    print('You may use %s to fill in the blanks' % (','.join(ob.contain)))

    words = ob.PossibleWords()
