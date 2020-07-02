import webdev

def crawlWeb():
    canditates = []#contains URLs of pages that the web crawler has discovered and could read/save
    crawled = []#contains URLs that the web crawler has already saved
    maxPages = 5
    outfile = open('pages.txt', 'w')
    linkFreq = {}

    canditates.append("http://people.scs.carleton.ca/~lanthier/teaching/COMP2401")
    while(len(canditates)!=0 and len(crawled) < maxPages):
        currentURL = canditates.pop(0)
        pageContent = webdev.readurl(currentURL)
        linkedURLs = webdev.getlinks(pageContent)
        for url in linkedURLs:
            if url not in canditates and url not in crawled:
                canditates.append(url)
            if url not in linkFreq:
                linkFreq[url]=0
            linkFreq[url]+=1
        pageContent = webdev.striphtml(pageContent)
        filename = currentURL[currentURL.rfind('/')+1:]+'.txt'
        outfile.write(filename+'\n')
        out = open(filename,'w')
        wordList = pageContent.split()
        wordFreq = {}
        for word in wordList:
            if word not in wordFreq:
                wordFreq[word]=0
            wordFreq[word]+=1
        for word in wordFreq:
            out.write(word+' '+str(wordFreq[word])+'\n')
        out.close()
        crawled.append(currentURL)
    outfile.close()

    outfile = open('page_popularity.txt', 'w')
    totalReferrals = totalValues(linkFreq)
    for url in linkFreq:
        outfile.write(url+'\n')
        outfile.write(str(round(linkFreq[url]/totalReferrals,4))+'\n')
    outfile.close()


pageFreqCache = {}#nested dictionary cache to store all words and their frequencies for every page
pagePopValue = {}

def mostFreq(freqDict):
    highestFreq = -1
    mostFreq = None
    for page in freqDict:
        if freqDict[page] > highestFreq:
            highestFreq = freqDict[page]
            mostFreq = page
    return mostFreq

def totalValues(freqDict):
    total = 0
    for value in freqDict:
        total += freqDict[value]
    return total

#returns the page(file) that has the most occurrences of the search word
def mostOccurences(pages, searchWord):
    pageFreq = {}#frequency dictionary for current searchword (keys = pages, values = frequency of the search word)
    pageFreqRatio = {}
    for page in pages:
        if page not in pageFreqCache:
            infile = open(page,'r')
            lines = infile.read().split('\n')
            lines.pop(-1)
            pageFreqCache[page] = {}
            for line in lines:
                word = line.split()[0]
                frequency = int(line.split()[1])
                pageFreqCache[page][word]=frequency
        if searchWord not in pageFreqCache[page]:
            pageFreq[page] = 0
            pageFreqRatio[page] = 0
        else:
            pageFreq[page] = pageFreqCache[page][searchWord]
            pageFreqRatio[page] = pageFreqCache[page][searchWord]/totalValues(pageFreqCache[page])

    mostFreqPage =  mostFreq(pageFreq)
    highestRatioPage =  mostFreq(pageFreqRatio)

    '''
    if(pageFreq[mostFreqPage]==0):
        print('No matches found.')
    else:
        print('Max page (Count): ', mostFreqPage)
        print('Max Count: ', pageFreq[mostFreqPage])
        print('Max page (Ratio): ', highestRatioPage)
        print('Max Ratio: ', round(pageFreqRatio[highestRatioPage],4))
        '''

def updatePagePopularity(filename):
    infile = open(filename, 'r')
    page = ''
    numLinks = 0
    line = infile.readline()
    while(line!='\n'):
        page = line.strip()[line.rfind('/')+1:]+'.txt'
        numLinks = int(infile.readline())
        pagePopValue[page] = numLinks
        line = infile.readline()

def similarity(page, words):
    totalFreq = 0
    for word in words:
        totalFreq += pageFreqCache[page][word]
    return totalFreq/totalValues(pageFreqCache[page])

def popularity(page):
    return pagePopValue[page]

def main():
    crawlWeb()
    infile = open('pages.txt','r')
    pages = infile.read().split('\n')
    pages.pop(-1)
    infile.close()
    updatePagePopularity('page_popularity.txt')
    while True:
        searchWords = input('Enter a word to search for (Enter q to quit): ')
        if searchWord == 'q': break
        mostOccurences(pages, searchWord)


if __name__ == "__main__":
    main()
