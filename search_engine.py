import webdev

def crawlWeb():
    canditates = []#contains URLs of pages that the web crawler has discovered and could read/save
    crawled = []#contains URLs that the web crawler has already saved
    maxPages = 10
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

def updateFreqCache(pages):
    for page in pages:
        if page not in pageFreqCache:
            infile = open(page,'r')
            lines = infile.read().split('\n')
            lines.pop(-1)
            pageFreqCache[page] = {}
            for line in lines:
                word = line.split()[0].upper()
                frequency = int(line.split()[1])
                pageFreqCache[page][word]=frequency

def updatePagePopularity(filename):
    infile = open(filename, 'r')
    line = infile.readline()
    while(line!='\n'):
        page = line.strip()[line.rfind('/')+1:]+'.txt'
        numLinks = float(infile.readline())
        pagePopValue[page] = numLinks
        line = infile.readline()

def similarity(page, words):
    totalFreq = 0
    for word in words:
        if word.upper() not in pageFreqCache[page]: continue
        totalFreq += pageFreqCache[page][word.upper()]
    return 0 if len(pageFreqCache[page])==0 else totalFreq/totalValues(pageFreqCache[page])

def popularity(page):
    return 0 if page not in pagePopValue else pagePopValue[page]

def topSearchResults(pages, words):
    popWeight = 0.2
    relatedWeight = 0.8
    topPages = []
    for i in range(3):
        highestValue = 0
        curTopPage = ''
        for page in pages:
            curValue = similarity(page, words)*relatedWeight + popularity(page)*popWeight
            if curValue > highestValue and page not in topPages:
                highestValue = curValue
                curTopPage = page
        topPages.append(curTopPage)
    return topPages

def main():
    crawlWeb()
    infile = open('pages.txt','r')
    pages = infile.read().split('\n')
    pages.pop(-1)
    infile.close()
    updatePagePopularity('page_popularity.txt')
    updateFreqCache(pages)
    while True:
        searchWords = input('Search (Enter q to quit): ')
        if searchWords.upper() == 'Q': break
        topPages = topSearchResults(pages, searchWords.split())
        print('Top search results:\n'+topPages[0]+'\n'+topPages[1]+'\n'+topPages[2]+'\n')

if __name__ == "__main__":
    main()
