import os
import PyPDF2

# converts a pdf file to txt (in place with same name)
def convertPdf(absPath):
    print('converting pfd at {} to txt format'.format(absPath))

    # open input and output files
    pdfFile = open(absPath, 'rb')
    outFile = open(absPath[:-4] + '.txt', 'w')
    
    # read PDF
    pdfReader = PyPDF2.PdfFileReader(pdfFile)
    
    # convert pages to text and write
    for p in range(0, 1):
        if p % 10 == 0:
            print('Converting page {} of {}'.format(p, pdfReader.numPages))
        pageObj = pdfReader.getPage(45)
        pageText = pageObj.extractText()
        outFile.write(pageText)

def main():
    # enumerate classes from directories in /data
    classDir = os.path.abspath('../data/')
    classes = next(os.walk(classDir))[1]

    # enumerate .pdf files for each class
    for c in classes:
        thisDir = classDir + '/' + c + '/'

        # enumerate files in class directory
        files = next(os.walk(thisDir))[2]

        # convert pdf files to txt
        for f in files:
            if f[-4:] == '.pdf':
                convertPdf(classDir + '/' + c + '/' + f)
    
        # enumerate txt files

        #print(files)

    #print(classes)

main()