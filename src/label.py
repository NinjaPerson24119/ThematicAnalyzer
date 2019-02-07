import sys
import os
from train import tokenize
import math

colorContrastMultiplier = 8

def main():
  # verify arg
  if len(sys.argv) != 2:
    print("Mising argument 1: absolute path to text to label")
    return

  # get arg as name
  filePath = sys.argv[1]

  # try to load file
  if not os.path.isfile(filePath):
    print("File at {} does not exist".format(filePath))
    return

  # check extension
  if filePath[-4:] != '.txt':
    print("File exists, but must be .txt format")
    return

  # load file to label
  contents = ''
  with open(filePath, 'r') as fp:
    for line in fp.readlines():
      contents += line

  # tokenize input text
  tokens = tokenize(contents)

  # enumerate classes
  classFiles = next(os.walk('../result'))[2]
  if len(classFiles) == 0:
    print("No classes to label from")
    return
  classFiles.remove('.dummy')

  # get class names from filenames
  classNames = []
  for f in classFiles:
    classNames.append(f[:-4])

  # load classes
  classWords = []
  for f in classFiles:
    classContents = ''
    with open('../result/' + f, 'r') as fp:
      for line in fp.readlines():
        classContents += line
    thisClassWords = classContents.split('\n')
    classWords.append(thisClassWords)

  # enumerate colors in 1D line: 256^3
  colors = []
  floorColor = (7*16+7)**3
  colorDist = math.floor((256**3 - floorColor) / (len(classNames) * colorContrastMultiplier))
  for i in range(0, len(classNames)):
    color = floorColor + i * colorDist
    hexString = hex(color)
    colors.append(hexString[2:])

  # try to apply each class
  for token in tokens:
    if token[1] == True:
      for i in range(0, len(classNames)):
        # iterate words to look for
        for w in classWords[i]:
          if token[0] == w:
            token[0] = '<span style="background-color: #{}">{}</span>'.format(colors[i], token[0])
       
  # rebuild text with stylized tokens
  rebuilt = ''
  for token in tokens:
    rebuilt += token[0]

  # write rebuilt text to file
  with open(filePath[:-4] + '.md', 'w') as fp:
    # build legend
    fp.write('Legend:<br />')
    for i in range(0, len(classNames)):
      fp.write('<span style="background-color: #{}">{}</span><br />'.format(colors[i], classNames[i]))
    fp.write('<br />')

    # fix tabs and newlines
    rebuilt = rebuilt.replace('\n', '<br />')
    rebuilt = rebuilt.replace('\t', '&nbsp;'*4)

    # write contents
    fp.write(rebuilt)

if __name__ == "__main__":
   main()