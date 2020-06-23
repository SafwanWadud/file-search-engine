pageFreqCache = {}#nested dictionary cache to store all words and their frequencies for every page

def mostFreq(freqDict):
    highestFreq = -1
    mostFreq = None
    for page in freqDict:
        if freqDict[page] > highestFreq:
            highestFreq = freqDict[page]
            mostFreq = page
    return mostFreq

def totalWords(wordFreq):
    total = 0
    for word in wordFreq:
        total += wordFreq[word]
    return total

#returns the page(file) that has the most occurrences of the search word
def mostOccurences(pages, searchWord):
    pageFreq = {}#frequency dictionary for current searchword (keys = pages, values = frequency of the search word)
    pageFreqRatio = {}
    for page in pages:
        if page not in pageFreqCache:
            infile = open(page,'r')
            words = infile.read().split('\n')
            pageFreqCache[page] = {}
            for word in words:
                if word not in pageFreqCache[page]:
                    pageFreqCache[page][word]=1
                else:
                    pageFreqCache[page][word]+=1

        if searchWord not in pageFreqCache[page]:
            pageFreq[page] = 0
            pageFreqRatio[page] = 0
        else:
            pageFreq[page] = pageFreqCache[page][searchWord]
            pageFreqRatio[page] = pageFreqCache[page][searchWord]/totalWords(pageFreqCache[page])

    mostFreqPage =  mostFreq(pageFreq)
    highestRatioPage =  mostFreq(pageFreqRatio)

    print('Max page (Count): ', mostFreqPage)
    print('Max Count: ', pageFreq[mostFreqPage])
    print('Max page (Ratio): ', highestRatioPage)
    print('Max Ratio: ', round(pageFreqRatio[highestRatioPage],4))

def main():
    infile = open('pages.txt','r')
    pages = infile.read().split('\n')
    pages.pop(-1)
    infile.close()
    while True:
        searchWord = input('Enter a word to search for (Enter q to quit): ')
        if searchWord == 'q': break
        mostOccurences(pages, searchWord)


if __name__ == "__main__":
    main()
