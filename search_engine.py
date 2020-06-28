import webdev

pageFreqCache = {}#nested dictionary cache to store all words and their frequencies for every page

def crawlWeb():
    canditates = []#contains URLs of pages that the web crawler has discovered and could read/save
    crawled = []#contains URLs that the web crawler has already saved
    maxPages = 5
    outfile = open('pages.txt', 'w')

    canditates.append("http://sikaman.dyndns.org:8888/courses/4601/resources/N-0.html")
    while(len(canditates)!=0 and len(crawled) < maxPages):
        currentURL = canditates.pop(0)
        pageContent = webdev.readurl(currentURL)
        linkedURLs = webdev.getlinks(pageContent)
        for url in linkedURLs:
            if url not in canditates and url not in crawled:
                canditates.append(url)
        pageContent = webdev.striphtml(pageContent)
        filename = currentURL[currentURL.rfind('/')+1:]
        outfile.write(filename+'\n')
        out = open(filename,'w')
        wordList = pageContent.split()
        for word in wordList:
            out.write(word+'\n')
        out.close()
        crawled.append(currentURL)
    outfile.close()

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

    if(pageFreq[mostFreqPage]==0):
        print('No matches found.')
    else:
        print('Max page (Count): ', mostFreqPage)
        print('Max Count: ', pageFreq[mostFreqPage])
        print('Max page (Ratio): ', highestRatioPage)
        print('Max Ratio: ', round(pageFreqRatio[highestRatioPage],4))

def main():
    crawlWeb()
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
