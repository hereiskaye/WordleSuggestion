# WordleSuggestion
This project provides you the suggestion to put into the box of wordle puzzle. 

## Source 

The file words_alpha.txt comes from [dwyl's repo](https://github.com/dwyl/english-words/blob/master/words_alpha.txt).
It contains 15918 5-length words. 

## Usage

```
GetYourSolution.py # Give you suggestions based on word inputs and color inputs 
Interactive.py # Generate your own puzzle and play it!
MeanSteps.py # For calculating the effectiveness
```
For the inputs, please always use lower cases, and for the color inputs, please use G->green (right letter right position), Y->yellow (right letter wrong position) and K->black (wrong letter).

## Method

The method is based on ranking all the word with repect to 
  all the possible answers to a particular question.
For example, the score of ''sanes'' is calculated this way:
P(first s is green)*4 + P(first s is yellow)*1 + P(second a is green)*4 + P(second a is yellow)*1 + ....


Therefore, you will always see the same suggestions at the first step. Let's suppose that you input "table" and get the ”GYKKK" (where K stands for black, G for green and Y for yellow),
now the weights will be changed, putting "t" at the first position will be worthless, but t can still be put elsewhere. Similarly, the letters "ble" will be worthless. It would be pointless to put "a" at the the first or second position, because it would provide no extra information at all!


However, the method tend to overestimate words with repeating letters. To avoid this, I simply deduce 0.5 points from the word everytime a letter repeats. 

Some examples could demonstrate the logic behind this method. For example, if you end up with three possible answers: cling, fling, kling, you may need to try three times (if you are unlucky, of course!) to get the right answer! But this program will tell you the following 5 are the best choices: 

```
top  1 -> clonk 0.5065
top  2 -> clink 0.5065
top  3 -> clank 0.5065
top  4 -> clunk 0.5065
top  5 -> clich 0.4985
```
## Effectiveness 

Using the smaller dictionary [first20hours's repo](https://github.com/first20hours/google-10000-english/blob/master/google-10000-english-usa-no-swears-medium.txt), which contain 1367 5-length words, I can confirm that no word require more than 6 steps. The distribution is shown:
![Alt text](MeanSteps.png?raw=true "Title")

However, if I use the larger dictionary [dwyl's repo](https://github.com/dwyl/english-words/blob/master/words_alpha.txt).

