import random 
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rc
import matplotlib.cm as cm

rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)
rc('text.latex', preamble=r'\usepackage{amsmath}')

params = {'legend.fontsize': 15,'ytick.labelsize': 19, 
          'axes.labelsize' : 19, 'xtick.labelsize': 19,
          'lines.linewidth': 2,
          'agg.path.chunksize':1000}
plt.rcParams.update(params)
  




def load_words():
  with open('google-10000-english-usa-no-swears-medium.txt') as word_file:
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

from Interactive import GenerateQuestion, GradingSystem

print('In total there are %d words' % (len(length_5)))

steps = []
for answer in length_5:
  countWords = 10000
  Question = GenerateQuestion(seed=None,answer=answer,length_5=length_5)
  ob = GradingSystem(quiet=True,length_5=length_5)
  countWords = ob.PossibleWords()
  guesses = []
  results = []
  while countWords > 1:
    bestWord = ob.bestChoices[0]
    # compute the color
    color = Question.AddOne(bestWord)
    # add this word to the guess
    ob.AddingAGuess(AGuess=bestWord,AResult=color)
    guesses.append(bestWord)
    results.append(color)
    countWords = ob.PossibleWords()
  if not guesses[-1] == answer:
    guesses.append(ob.found[0])
    results.append('GGGGG')
  print('To find [%s] we %s' % (answer, '->'.join(guesses))) 
  print('                   %s' % ('->'.join(results))) 

  steps.append(len(guesses)) # last one 


fig, ax = plt.subplots()
bins = np.arange(1,max(steps)+2)
alphab = list(range(min(steps),max(steps)+2))
frequencies = []
for each in alphab:
  frequencies.append(steps.count(each)/len(steps))
ax.bar(alphab, frequencies,1.0,color='b',edgecolor='k',alpha=0.5)

# ax.hist(steps,bins=bins,alpha=0.5,density=True,stacked=True)
ax.set_xlabel(r'${\rm No \, of \, guesses}$')
ax.legend(loc='best')
fig.tight_layout()
fig.savefig('MeanSteps.png',dpi=300)
print('MeanSteps.png')
plt.close(fig)


  
steps = np.array(steps)  
print('There are %d requires > 6 steps' % (np.sum(steps>6)))
  



