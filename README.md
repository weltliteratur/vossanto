---
title: Vossianische Antonomasien
date: 2016-06-12
---

# English: POS tagging with NLTK

- see [[vossanto.py]]

# German: POS tagging with the Stanford tagger

why not NLTK:

- https://stackoverflow.com/questions/20332762/pos-tagging-german-texts-using-nltk

Hence, Stanford:

- http://nlp.stanford.edu/software/tagger.shtml

From the documentation (after adopting the shell script to use Java 8):

    ./stanford-postagger.sh models/wsj-0-18-left3words-distsim.tagger sample-input.txt

A test with German text:

    ./stanford-postagger.sh models/german-hgc.tagger german-input.txt

*Problem*: seems to have problems with Umlauts :-(


Create a default configuration file with comments

    java -classpath stanford-postagger.jar:lib/* edu.stanford.nlp.tagger.maxent.MaxentTagger \
        -genprops > myPropsFile.prop

# Examples

## 2000

- *SOFTWARE* is the *DNA* of the *high-technology age* (2000/01/01/1165197)
- *Virginia Gonzalez*  is the *Dorothea Dix* of *Mexico* (har/01/16/1168831)
- *Lorne Michaels*, the *Flo Ziegfeld* of *sketch comedy* (2000/02/06/1174188)
- *Much Music* is the *Canadian version* of *MTV* (2000/02/06/1174454)

## 2001

- *Youngman* is the *King* of *One Liners* (2001/01/07/1260710)
- *Palm Springs* is the *Hamptons* of *Los Angeles* (2001/01/14/1262501)
- *Las Vegas* is the *Detroit* of the *New Century* (2001/01/26/1265880)
- *William Woys Weaver* is the *Julia Child* of *long-lost vegetables* (2001/03/15/1277939)
- *Peggy Spina* is the *Brenda Blethyn* of *tap* (2001/03/13/1277631)
- *Celia Cruz*, the *Queen* of *Salsa* (2001/03/16/1278191)

## 2002

- *the North American International Auto Show*, the *Cannes Film Festival* of the *auto industry* (2002/01/06/1357245)
- *today's National Enquirer* is the *Las Vegas* of *journalism* (2002/01/13/1359135)
- *Eldredge* is the *Cadillac* among *Ferraris* (2002/02/12/1367217)
- *J Mascis* is the *Neil Young* of *Generation X* (2002/03/22/1377696)

## 2003

- *Eric Bergoust*, the *Babe Ruth* of *freestyle aerials* (2003/01/23/1458686)
- *New Jersey's Vince Lombardi* is the *Yosemite* of *rest stops* (2003/02/02/1461651)
- *Bob Irsay*, the *Caesar* of *sports carpetbaggers* (2003/02/06/1462734)
- *The Emerson Quartet*, the *Fab Four* of the *string world* (2003/02/15/1465110)
- *Mille Lacs* is the *Yankee Stadium* of *ice fishing* (2003/02/21/1466539)
- *Olivier Award*, the *London equivalent* of the *Tony* (2003/03/02/1468848)
- *Las Cruces*, the *Mesilla Valley* of *southern New Mexico* (2003/03/09/1470804)

## 2004

- *Arturo Gatti* is the *Oscar De La Hoya* of *New Jersey* (2004/02/22/1560800)
- *Steinway*, the *Mercedes* of *pianos* (2004/02/29/1562589)
- *Azim Premji* is the *Bill Gates* of *India* (2004/03/21/1568087)
