import sys
import os

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

  # enumerate classes
  classFiles = next(os.walk('../result'))[2]
  if len(classFiles) == 0:
    print("No classes to label from")
    return

  # get class names from filenames
  classNames = []
  for f in classFiles:
    classNames.append(f[:-4])

  # load classes
  classWords = []
  for f in classFiles:
    classContents = ''
    with open('../result/' + f, 'r') as fp
      for line in fp.readlines():
        classContents += line
    thisClassWords = classContents.split('\n')
    classWords.append(thisClassWords)

  #

  # try to apply each class
  for i in range(0, len(classNames)):
    # iterate words to look for
    for w in classWords[i]:
      labelled = 

main()