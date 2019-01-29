import os
import pdfminer.high_level
import pdfminer.layout
import unidecode
import math

maxWordCountThresh = 60

# converts a pdf file to txt (in place with same name)


def convertPdf(absPath):
    print('converting pdf at {} to txt format'.format(absPath))

    # open input and output files
    with open(absPath, 'rb') as inFile, open(absPath[:-4] + '.txt', 'w') as outFile:
        # read PDF
        pdfminer.high_level.extract_text_to_fp(
            inFile, outFile, laparams=pdfminer.layout.LAParams())

# converts a string to a list of tokens
# each token is a list of the following format:
# [text, isWord]


def tokenize(text):
    # verify text length
    assert(len(text))

    # special characters
    specialChars = [' ', '"', "'", ',', '.',
                    '?', '!', ':', ';', '(', ')', '\n', '\t', '-']

    # convert from unicode
    text = unidecode.unidecode(text)

    # process text
    tokens = []
    tokenStart = 0
    wordToken = text[0].isalpha()  # begin with word token?
    for i in range(0, len(text)):
        if wordToken:
            # end word tokens on special characters
            if text[i] in specialChars:
                # check for apostrophe in word (adjacent chars are in alphabet)
                if text[i] == "'":  # note conversion because of unicode
                    # check index bound
                    if i != tokenStart and i + 1 < len(text):
                        if text[i-1].isalpha() and text[i+1].isalpha():
                            continue
            else:
                continue
        else:
            # end non-word tokens on letters
            if not text[i].isalpha():
                continue

        # add new token
        token = [text[tokenStart:i], wordToken]
        tokens.append(token)
        tokenStart = i
        wordToken = not wordToken

    # return tokens
    return tokens


def main():
        # enumerate classes from directories in /data
    classDir = os.path.abspath('../data/')
    classes = next(os.walk(classDir))[1]

    # enumerate .pdf files for each class
    classHistograms = []
    for c in classes:
        thisDir = classDir + '/' + c + '/'

        # enumerate files in class directory
        files = next(os.walk(thisDir))[2]

        # convert pdf files to txt
        for f in files:
            absPath = classDir + '/' + c + '/' + f
            if f[-4:] == '.pdf' and not os.path.isfile(absPath[:-4] + '.txt'):
                convertPdf(absPath)

        # enumerate txt files
        files = next(os.walk(thisDir))[2]
        files = [i for i in files if i[-4:] == '.txt']
        for i in range(0, len(files)):
            files[i] = classDir + '/' + c + '/' + files[i]

        # create dictionary from each each txt file
        histograms = []
        for name in files:
            # read entire file
            contents = ''
            with open(name, 'r') as fp:
                for line in fp.readlines():
                    contents += line

            # tokenize and extract words
            tokens = tokenize(contents)
            words = []
            for token in tokens:
                if token[1] == True:
                    words.append(token[0])

            # fill histogram
            # note: case insensitive
            thisHist = {}
            for w in words:
                if w in thisHist:
                    thisHist[w.lower()] += 1
                else:
                    thisHist[w.lower()] = 1

            # enforce maximum word thresh
            rmList = []
            for k in thisHist:
                if thisHist[k] >= maxWordCountThresh:
                    rmList.append(k)
            for k in rmList:
                del thisHist[k]

            # keep histogram
            histograms.append(thisHist)

        # identify common words for this class
        thisClassWords = []
        if len(histograms) >= 1:
            # start with words in first histogram
            thisClassWords = [k for k in histograms[0]]
            if len(histograms) > 1:
                # keep intersection of all histograms
                for i in range(1, len(histograms)):
                    nextWords = [k for k in histograms[1]]
                    thisClassWords = [
                        k for k in thisClassWords if k in nextWords]

        # retain histogram counts for class-class battles
        thisClassHist = {}
        for k in thisClassWords:
            thisClassHist[k] = 0
            for h in histograms:
                thisClassHist[k] += h[k]

        # keep class histogram
        classHistograms.append(thisClassHist)

    # remove words that exist in more than two histograms
    wordCount = {}
    for i in range(0, len(classHistograms)):
        for k in classHistograms[i]:
            if k in wordCount:
                wordCount[k] += 1
            else:
                wordCount[k] = 1

    for k in wordCount:
        if wordCount[k] >= 2:
            for h in classHistograms:
                if k in h:
                    del h[k]

    # map each word to the class it occurs the most times in
    # iterate keys of histogram combinations
    # if key exists in both, delete key in both histogram and words
    for i in range(0, len(classHistograms)):
        for j in range(0, len(classHistograms) - 1):
            if i == j:
                continue
            commonKeys = [k for k in classHistograms[i]
                          if k in classHistograms[j]]
            for k in commonKeys:
                # loop precedence wins for equal counts
                if classHistograms[i][k] <= classHistograms[j][k]:
                    del classHistograms[i][k]
                else:
                    del classHistograms[j][k]

    # build injective classication map
    classWords = []
    for h in classHistograms:
        thisList = [k for k in h]
        classWords.append(thisList)

    # write classes
    for i in range(0, len(classes)):
        with open('../result/' + classes[i] + '.txt', 'w') as fp:
            for w in classWords[i]:
                fp.write(w + '\n')

    # log
    for i in range(0, len(classes)):
        print('Wrote {} words for {} class'.format(
            len(classWords[i]), classes[i]))


if __name__ == "__main__":
    main()
