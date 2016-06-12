
# Vossianische Antonomasien

siehe
[Der Umblätterer: Vossianische Antonomasie](http://www.umblaetterer.de/category/vossianische-antonomasie/)

## Howto

### English: POS tagging with NLTK

- see [vossanto.py](vossanto.py)

### German: POS tagging with the Stanford tagger

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

## Examples


### 1987

- *New South Wales*, the *Georgian equivalent* of *deep space* (1987/01/25/0007151)
- the *Giants*, the *New York Titans* of the *American Football League* (1987/01/28/0007820)
- Mr. Reagan fares far better, nicknamewise, than some other Presidents in the compendium, including one known as Gloomy Gus, King Richard, the *Bela Lugosi* of *American Politics*, Richard the Chicken-Hearted, the *Nero* of *Our Times*, the Tarnished President, the Godfather, St. Richard the Commie Killer, President Truthful and Trickie Dick. (1987/01/29/0008167)
- *Olivier Award*, the *English equivalent* of the *Tony Award* (1987/02/01/0009058)

### 1988 

- *Mr. Pacepa* is the *Happy Hooker* of the *spy trade* (1988/01/03/0106811)
- *Queen Victoria*, the *Great Satan* of the *time* (1988/02/03/0115425)
- *David Leslie*, the *Evel Knievel* of *performance artists* (1988/02/05/0116272)

### 1990

- the *remarkable enclosed indoor Housewives' Market*, the *Halles* of *soul food*  (1990/01/07/0314867)


### 1991

- *George Foreman*, the *Santa Claus* of *sports* (1991/01/01/0412333)

### 1993

- The *Sig Sauer* is the *Rolex* of *guns* today (1993/01/03/0580645)

### 1995

- *Rush Limbaugh*, the *Babe Ruth* of the *talk-show circuit* (1995/01/05/0735173)
- *Mr. Lovano* is the *General Motors* of *jazz* (1995/01/15/0736903)
- *La Villa*, the *Village Vanguard* of *Paris* (1995/01/15/0736911)

### 1997

- *Thomas Eisner*, the *St. Francis* of *bugs* (1997/01/12/0900997)
- *Shaka*, the *Attila* of *Zululand* (1997/01/18/0902375)
- *Albert Belle*, the *Bad Boy* of *Baseball*, (1997/02/10/0908025)
- *Macco*, the *Calabrian version* of the *dish* (1997/02/14/0908831)

### 1998

- *Lovely Lane Methodist Church*, the *Mother Church* of *American Methodism* (1998/01/09/0986279)

### 1999

- the *Estee Lauder Companies*, the *General Motors* of the *cosmetics world* (1999/01/10/1075990)

### 2000

- *SOFTWARE* is the *DNA* of the *high-technology age* (2000/01/01/1165197)
- *Virginia Gonzalez*  is the *Dorothea Dix* of *Mexico* (har/01/16/1168831)
- *Lorne Michaels*, the *Flo Ziegfeld* of *sketch comedy* (2000/02/06/1174188)
- *Much Music* is the *Canadian version* of *MTV* (2000/02/06/1174454)
- *El Camino Real*, the *Champs-Elysees* of the *new economy* (2000/03/10/1182787)
- *Mr. McMahon* is the *Willie Wonka* of *pro wrestling* (2000/03/17/1184459)
- *Larry*, the *Marvin Miller* of *hoops* (2000/04/02/1188826)
- *James Brown*, the *Godfather* of *Soul* (2000/04/13/1191452)
- *Willis Haviland Carrier*, the *Bill Gates* of the *air conditioner* (2000/05/01/1196085)
- *Miss Loveydear*, the *Mae West* of *dragonflies* (2000/05/12/1198733)
- If *Houston's cozy new Enron Field* is the *Rhode Island* of *ballparks*, then *Comerica Park* is *Alaska* (2000/05/14/1199574)
- *Brighton Beach* is the *Russian bazaar* of *America* (2000/05/21/1201255)
- *Olivier Awards*, the *London equivalent* of the *Tony Awards* (2000/07/05/1212567)
- *Gertrude Jekyll* is the *Elvis* of the *gardening world* (2000/07/23/1217052)
- The *stunt biker Dave Mirra*, the *Michael Jordan* of the *dirt set* (2000/08/13/1222322)
- *Los Angeles* is the *Ellis Island* of the *west* (2000/08/13/1222376)
- *Cafe Riche* is the *Deux Magots* of *Cairo* (2000/08/20/1223752)
- *Cynthia Cooper* is the *Michael Jordan*, the *Larry Bird*, the *Magic Johnson* of *this league* (2000/08/28/1226010)
- *Harris* has been called the *Queen* of *Country Music*, the *Angel* of *This*, the *Sweetheart* of *That* (2000/09/03/1227433)

### 2001

- *Youngman* is the *King* of *One Liners* (2001/01/07/1260710)
- *Palm Springs* is the *Hamptons* of *Los Angeles* (2001/01/14/1262501)
- *Las Vegas* is the *Detroit* of the *New Century* (2001/01/26/1265880)
- *William Woys Weaver* is the *Julia Child* of *long-lost vegetables* (2001/03/15/1277939)
- *Peggy Spina* is the *Brenda Blethyn* of *tap* (2001/03/13/1277631)
- *Celia Cruz*, the *Queen* of *Salsa* (2001/03/16/1278191)
- *Tobias Meyer* is the *James Bond* of the *art market* (2001/05/20/1294977)
- *Orbitz* is the *Standard Oil* of *online travel* (2001/05/27/1296569)
- *cartoon villain Dirty Dee* is the *Pigpen* of *macks* (2001/06/29/1305441)
- *Dr. Alex*, the *Freud* of the *Cocktail Hour* (2001/07/08/1307710)
- *Rebecca Wisocky*, the *Sandra Bernhard* of *dance* (2001/07/17/1309968)

### 2002

- *the North American International Auto Show*, the *Cannes Film Festival* of the *auto industry* (2002/01/06/1357245)
- *today's National Enquirer* is the *Las Vegas* of *journalism* (2002/01/13/1359135)
- *Eldredge* is the *Cadillac* among *Ferraris* (2002/02/12/1367217)
- *J Mascis* is the *Neil Young* of *Generation X* (2002/03/22/1377696)
- *Mr. Bogdanovich*, the *Icarus* of the *New Hollywood* (2002/04/12/1383292)
- *MagLiner*, the *Cadillac* of *hand trucks* (2002/06/09/1399279)
- *Hillary*, the *Cattle Queen* of *commodities trading* (2002/07/10/1407094)
- the *jockey Jim Burns*, the *Jerry Bailey* of *mule racing* (2002/07/11/1407365)

### 2003

- *Eric Bergoust*, the *Babe Ruth* of *freestyle aerials* (2003/01/23/1458686)
- *New Jersey's Vince Lombardi* is the *Yosemite* of *rest stops* (2003/02/02/1461651)
- *Bob Irsay*, the *Caesar* of *sports carpetbaggers* (2003/02/06/1462734)
- *The Emerson Quartet*, the *Fab Four* of the *string world* (2003/02/15/1465110)
- *Mille Lacs* is the *Yankee Stadium* of *ice fishing* (2003/02/21/1466539)
- *Olivier Award*, the *London equivalent* of the *Tony* (2003/03/02/1468848)
- *Las Cruces*, the *Mesilla Valley* of *southern New Mexico* (2003/03/09/1470804)
- *goddess Inanna*, the *Sumerian version* of *Ishtar* (2003/04/13/1480703)
- *Isabella Beeton*, the *Fannie Farmer* of *Britain* (2003/06/11/1495897)

### 2004

- *Arturo Gatti* is the *Oscar De La Hoya* of *New Jersey* (2004/02/22/1560800)
- *Steinway*, the *Mercedes* of *pianos* (2004/02/29/1562589)
- *Azim Premji* is the *Bill Gates* of *India* (2004/03/21/1568087)
- *Yomiuri Giants*, the *Japanese equivalent* of the *Yankees* (2004/03/28/1569955)
- If *Mariano Rivera of the Yankees* is the *Mr. October* of *closers*, *Gagne* is the *Mr. Season*. (2004/05/18/1582589)
- *Lil' John*, the *King* of *Crunk* (2004/05/23/1583885)
- *TechZilla*, the *Lamborghini* of *slow-pitch bats* (2004/05/30/1585628)
- *Dionysos*, the *God of drama* (2004/06/27/1592422)
- *Brenda Bishop*, the *Granny Bandit* of *Macomb County* (2004/07/03/1593896)
