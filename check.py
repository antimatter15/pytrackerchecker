import xml.parsers.expat
import urllib2
import threading



def check_url(checkurl, checkstring, checkname):
  try:
    opener = urllib2.urlopen(checkurl, timeout = 5)
    if checkstring[0] == "!":
      if checkstring.encode('utf-8')[1:] not in opener.read():
        print "Open",checkname
      else:
        #print "Closed",checkname
        pass
    else:
      if checkstring.encode('utf-8') in opener.read():
        print "Open",checkname
      else:
        #print "Closed",checkname
        pass
  except IOError:
    #print "Broken",checkname
    pass
p = xml.parsers.expat.ParserCreate()

tname = ""
url = ""
check = ""
mode = ""
enabled = ""

def char_data(data):
  global tname, url, check, mode, enabled
  if mode == "name":
    tname += data
  elif mode == "check":
    check += data
  elif mode == "signup":
    url += data
  elif mode == "type":
    enabled += data
    
def end_element(name):
  global tname, url, check, mode, enabled
  mode = ""
  if name == "tracker" and enabled[0] == "T":
    threading.Thread(target=check_url, args=(url, check, tname)).start()
    tname = ""
    url = ""
    enabled = ""
    check = ""
    
    
def start_element(name, attrs):
  global tname, url, check, mode, enabled
  if name == "name":
    mode = "name"
  elif name == "signup":
    mode = "signup"
  elif name == "check":
    mode = "check"
  elif name == "type":
    mode = "type"
p.StartElementHandler = start_element
p.EndElementHandler = end_element
p.CharacterDataHandler = char_data

f = open("trackers.xml")
p.Parse(f.read(),1)
