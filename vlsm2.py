import re

def addToBin(raw):
    arr = []
    for e in list(map(lambda i: format(int(i),"08b"),raw.split("."))):
        for e2 in e:
            arr.append(int(e2))
    return arr

def binToAdd (array):
    array = list(map(lambda i : str(i),array))
    raw = ""
    raw+= str(int("".join(array[0:8]),2))+"."
    raw+= str(int("".join(array[8:16]),2))+"."
    raw += str(int("".join(array[16:24]),2))+"."
    raw += str(int("".join(array[24:32]),2))
    return raw      

def classA (raw):
    number = int(raw.split('.')[0])
    if (number<128):
        return 'A'
    if (number<192):
        return 'B'
    return 'C'

def guessBegin(raw):
    tomponArray = []
    for e in addToBin(raw):
        tomponArray.append(int(e))
    start = 0
    if (classA(raw)=='A'):
        start = 8
    if (classA(raw)=='B'):
        start = 16
    if (classA(raw)=='C'):
        start = 24  
    for e in range (start, len(tomponArray)):
        if (tomponArray[e]==1):
            start = e             
    return start

def fixA(raw, begin):
    tomponArray = [int(i) for i in addToBin(raw)]
    for i in range (begin, len(tomponArray)):
        if (tomponArray[i]==1):
            tomponArray[i]=0
    return binToAdd(tomponArray)

def masque(start):
    array = [1 for i in range (0,start)]
    for i in range(start,32):
        array.append(0)
    return binToAdd(array)

def passerelle (array):
    tomponArray = [i for i in array]
    tomponArray[31] = 1
    return binToAdd(tomponArray)

def first (array):
    tomponArray = [i for i in array]
    tomponArray[30] = 1
    return binToAdd(tomponArray)
    
def last(array, start):
    tomponArray = [i for i in array]
    for i in range (start,31):
        tomponArray[i]=1
    return binToAdd(tomponArray)

def broadcast(array,start):
    tomponArray = [i for i in array]
    for i in range (start,32):
        tomponArray[i]=1
    return binToAdd(tomponArray)

def seg(array,begin,host):
    listAdd = []
    sr =  srNumber(begin,bitPerHost(host))
    nbH = 32-begin-bitPerHost(host)  
    for i in range (srNumber(begin,bitPerHost(host))):
        binI = format(i,"0"+str(nbH)+"b")
        for e in range(len(binI)):
            array[begin+e]=binI[e]
        listAdd.append(binToAdd(array))
    return listAdd

def shiftNb (begin, host):
    return 32-begin-bitPerHost(host)

def bitPerHost(host):
    n=0
    while (2**n<host+2):
        n+=1
    return n

def srNumber(begin, number):
    nb= 2**(32-begin-number)
    if (32-begin-number == 0):
        return 0
    return nb

def calNbrMach (begin):
    return (2**(32-begin))-2

def testMach():
    host = 0
    try: 
        host = int(input("entrer un nombre de machines inferieur à "+str(calNbrMach(begin)-sum(hosts_array))+": "))
    except: 
        return host
    return host

def addMach():
    host = testMach()
    while (host> calNbrMach(begin)-sum(hosts_array) or host<= 0):
        host = testMach()
    hosts_array.append(host)

#*****************************************
pattern = "^((2(([0-4][0-9])|(5[0-5])))|([01]?[0-9]?[0-9]))\.((2(([0-4][0-9])|(5[0-5])))|([01]?[0-9]?[0-9]))\.((2(([0-4][0-9])|(5[0-5])))|([01]?[0-9]?[0-9]))\.((2(([0-4][0-9])|(5[0-5])))|([01]?[0-9]?[0-9]))$"
addresse_raw = ""
addresse_array = []
hosts_array = []
begin = 0
#**************************************

while (re.match(pattern, addresse_raw) == None):
    addresse_raw = input("entrer une addresse ip valide :")

while (begin <8 or begin >30):
    try :
        begin = int(input("masque du reseau :["+str(guessBegin(addresse_raw))+"]"))
    except: 
        begin = 0    

addresse_raw = fixA(addresse_raw,begin)

host = addMach()

choice = input("entrer d'autres machines! [oui/non]")
while (choice == "oui" and sum(hosts_array)<calNbrMach(begin)):
    addMach()
    choice = input("entrer d'autres machines! [oui/non]")
#//////////////////////////////////////////////////////////////
addresse_array = addToBin(addresse_raw)
print ("votre adress est : "+addresse_raw)
print ("adresse classe : "+classA(addresse_raw))
print ("masque  : "+masque(begin))
print ("passerelle : "+passerelle(addresse_array))
print ("1er adress :"+first(addresse_array))
print ("dernier adress :"+last(addresse_array,begin))
print ("adresse de diffusion :"+broadcast(addresse_array,begin))
#*************************************************************
print("segmentation......................")
#print("nbr de sous reseaux possibles: "+str(srNumber(begin,bitPerHost(hosts_array[0]))))
print("-------------------------------------------------------------------------------------------------------------------")
print("| adresse reseau | masque reseau | shift | adresse gateway | 1 adreese res | dernier adresse | addresse broadcast | hosts |")
print("-------------------------------------------------------------------------------------------------------------------")

mapAddress = []
beginArray = []
hostToTrait = hosts_array.pop(0)
sh = shiftNb(begin, hostToTrait)
for e in seg(addresse_array, begin, hostToTrait):
    mapAddress.append({"adress":e,"masque":masque(begin+sh),"shift":begin+sh,"passerelle":passerelle(addToBin(e)),"first":first(addToBin(e)),"last":last(addToBin(e),begin+sh),"broadcast":broadcast(addToBin(e),begin+sh),"hosts":0})
mapAddress[0]["hosts"]= hostToTrait
begin+=sh
beginArray.append(begin)

while (len(hosts_array)!=0):
    hostToTrait =  hosts_array.pop(0)
    test = False

    if (shiftNb(begin,hostToTrait)==0):
        for e in mapAddress :
            if (e.get("hosts")==0 and e.get("shift")==begin):
                e["hosts"]= hostToTrait
                test = True
                break

    if(test==False):
        for b in sorted(beginArray, reverse=True): 
            try: 
                tomponAddress = mapAddress.pop(mapAddress.index(list(filter(lambda i: i.get("shift")==b and i.get("hosts")==0,mapAddress))[0]))
                sh = shiftNb(b, hostToTrait)
                addresse_array = addToBin(tomponAddress.get("adress"))
                listR = seg(addresse_array, b, hostToTrait)
                for e in listR:
                    mapAddress.append({"adress":e,"masque":masque(b+sh),"shift":b+sh,"passerelle":passerelle(addToBin(e)),"first":first(addToBin(e)),"last":last(addToBin(e),b+sh),"broadcast":broadcast(addToBin(e),b+sh),"hosts":0})
                mapAddress[len(mapAddress)-len(listR)]["hosts"]=hostToTrait
                begin= b+sh
                beginArray.append(begin)
                break 
            except:
                continue
                
for e in mapAddress:
    print(e.get("adress").ljust(17," ")+"|"+e.get("masque").ljust(15," ")+"|"+str(e.get("shift")).ljust(7," ")+"|"+e.get("passerelle").ljust(17," ")+"|"+e.get("first").ljust(15," ")+"|"+e.get("last").ljust(17," ")+"|"+e.get("broadcast").ljust(20," ")+ "|"+str(e.get("hosts")))
