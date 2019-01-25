import os
import pdfminer.high_level
import pdfminer.layout

maxWordCountThresh = 1000

# converts a pdf file to txt (in place with same name)
def convertPdf(absPath):
    print('converting pdf at {} to txt format'.format(absPath))

    # open input and output files
    with open(absPath, 'rb') as inFile, open(absPath[:-4] + '.txt', 'w') as outFile:
        # read PDF
        pdfminer.high_level.extract_text_to_fp(inFile, outFile, laparams=pdfminer.layout.LAParams())

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
            
            # remove special characters to isolate words
            special = ['"',"'s",',','.','?','!',':',';','(',')','\n','\t']
            for s in special:
                contents = contents.replace(s, ' ')
            
            # get words
            words = contents.split(' ')

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
                    thisClassWords = [k for k in thisClassWords if k in nextWords]

        # retain histogram counts for class-class battles
        thisClassHist = {}
        for k in thisClassWords:
            thisClassHist[k] = 0
            for h in histograms:
                thisClassHist[k] += h[k]

        # keep class histogram
        classHistograms.append(thisClassHist)

    # map each word to the class it occurs the most times in
    # iterate keys of histogram combinations
    # if key exists in both, delete key in both histogram and words
    for i in range(0, len(classHistograms)):
        for j in range(0, len(classHistograms) - 1):
            if i == j:
                continue
            commonKeys = [k for k in classHistograms[i] if k in classHistograms[j]]
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

main()