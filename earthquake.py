import urllib.request
import http.cookiejar

#set up cookie opener
cj = http.cookiejar.MozillaCookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

webURL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.atom"
outfilename = "earthquakes.txt"
outfile = open(outfilename, "w")
print ('Magnitude','|','Location','|','Time','|','Depth','|','Longitude','|','Latitude', file = outfile)

try:
    infile = opener.open(webURL)
    newpage = infile.read().decode('utf-8')
except:
    print ("Page not found.")
    newpage = ""

if newpage != "":
    entrylist = newpage.split("<entry>")
    listlength = len(entrylist)
    for i in range(1,listlength):
        rawstring = entrylist[i]
        firstbracketindex = rawstring.find('>M ')
        secondbracketindex = rawstring.find(' - ')
        thirdbracketindex = rawstring.find('- ')
        fourthbracketindex = rawstring.find('</title>')
        fifthbracketindex = rawstring.find('d>',fourthbracketindex)
        sixthbracketindex = rawstring.find('Z</updated')
        sevenbracketindex = rawstring.find('pth<',sixthbracketindex)
        eightbracketindex = rawstring.find(' ',sevenbracketindex)
        ninebracketindex = rawstring.find('point>')
        tenbracketindex = rawstring.find(' ',ninebracketindex)
        elevenbracketindex = rawstring.find('</geor')
        
        if firstbracketindex < secondbracketindex:
            sixthstring = rawstring[tenbracketindex+1:elevenbracketindex]
            longstring = sixthstring.strip()
            fifthstring = rawstring[ninebracketindex+6:tenbracketindex]
            latstring = fifthstring.strip()
            fourthstring = rawstring[sevenbracketindex+12:eightbracketindex]
            depthstring = fourthstring.strip()
            thirdstring = rawstring[fifthbracketindex+13:sixthbracketindex]
            timestring = thirdstring.strip()
            otherstring = rawstring[thirdbracketindex+2:fourthbracketindex]
            locstring = otherstring.strip()
            paddedstring = rawstring[firstbracketindex+3:secondbracketindex]
            magstring = paddedstring.strip()
            if magstring == '?':
                magstring = '1.0'
            magfloat = float(magstring[0:4])
        else:
            print ("Error.")
        print (magfloat,'|',locstring,'|',timestring,'|',depthstring,'|',longstring,'|',latstring, file = outfile)
    
print()
print("Done.")
