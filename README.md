
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

## Ideas for Improvements

- collect values for y and omit matches which contain a frequent y,
  e.g., "Ezer Weizman President Israel"

## Examples


### 1987

- *New South Wales*, the *Georgian equivalent* of *deep space* (1987/01/25/0007151)
- the *Giants*, the *New York Titans* of the *American Football League* (1987/01/28/0007820)
- Mr. Reagan fares far better, nicknamewise, than some other Presidents in the compendium, including one known as Gloomy Gus, King Richard, the *Bela Lugosi* of *American Politics*, Richard the Chicken-Hearted, the *Nero* of *Our Times*, the Tarnished President, the Godfather, St. Richard the Commie Killer, President Truthful and Trickie Dick. (1987/01/29/0008167)
- *Olivier Award*, the *English equivalent* of the *Tony Award* (1987/02/01/0009058)
- *George Romney*, the *Middle America sort* of *guy* (1987/03/15/0021513)
- the *Wireless Service*, the *German equivalent* of the *BBC* (1987/04/05/0027535)
- *Lone Mountain* is the *Club Med* of *dude ranches* (1987/05/24/0043648)
- *Algarve*, the *Riviera* of *Portugal* (1987/06/14/0048773)
- Anne Horner's husband was the great-grandson of *Sir John Horner*, the *Little Jack Horner* of the *nursery rhyme* (1987/06/24/0051512)
- *Hiroshi Itsuki*, the *Frank Sinatra* of *Japan* (1987/06/29/0052991)
- the *Cesars* - the *French equivalent* of *Oscars* (1987/06/29/0052991)
- the *Olivier Award* - the *British equivalent* of a *Tony* (1987/07/10/0055426)
- *Sassy*, the *United States version* of *Dolly* (1987/08/24/0068801)
- *Windsor* is the *Detroit* of *Canada* (1987/09/21/0076414)
- the *Wailers*, the *Beatles* of *reggae* (1987/09/27/0077678)
- *Jeff Reardon*, the *Terminator* of the *Minnesota Twins* (1987/10/17/0083602)
- *Moses Malone* is the *Paul Newman* of *professional basketball* (1987/11/14/0092773)
- *Dana Dane*, the *King* of *Rap*, (1987/11/26/0096606)
- *Laurence Olivier Award*, the *English equivalent* of the *Tony Award* (1987/12/22/0103798)

### 1988 

- *Mr. Pacepa* is the *Happy Hooker* of the *spy trade* (1988/01/03/0106811)
- *Queen Victoria*, the *Great Satan* of the *time* (1988/02/03/0115425)
- *David Leslie*, the *Evel Knievel* of *performance artists* (1988/02/05/0116272)

### 1990

- the *remarkable enclosed indoor Housewives' Market*, the *Halles* of *soul food*  (1990/01/07/0314867)
- *Mr. Gorbachev*, the *Houdini* of *politicians* (1990/02/05/0323616)
- *Clive Barker* is the *Paul McCartney* of *horror fiction* (1990/02/11/0325668)
- *Waterman*, the *Rolls-Royce* of *pens* acquired in 1987, and *Papermate*, the *Chevrolet* of *pens* (1990/02/25/0329728)

### 1991

- *George Foreman*, the *Santa Claus* of *sports* (1991/01/01/0412333)
- *New York* is the *Cadillac* of *welfare states* (1991/01/31/0419226)
- *Gillian Anderson* is the *Pauper* of *professional experience*, *Brenda Blethyn* is the *Princess* (1991/02/20/0424794)
- *Hasselblad*, the *Mercedes-Benz* of *camera makers* (1991/03/10/0428959)
- If the *American Budweiser* is the *King of Beers*, what does that make the *Czech Budweiser*? Why, none other than the *Beer* of *Kings*, if negotiations between the two brewers succeed. (1991/03/10/0429088)

### 1992

-  *Luis Cisneros*, better known to colleagues as *Sandra*, the *Queen* of the *Bois* (1992/01/11/0499353)
- the Islanders, the Boys of Winter nyt_corpus_1992.har/01/24/0502719.xml
- Forget the Yankees of Reggie, the Giants of Taylor, the Mets of Carter and Hernandez, even the Knicks of Reed and DeBusschere. The Islanders won like the old, old New York Yankees and they charmed like the old, old Brooklyn Dodgers (1992/03/04/0511581)
- *Vaz Auto Works*, the *General Motors* of *Russia* (1992/03/08/0512599)

### 1993

- The *Sig Sauer* is the *Rolex* of *guns* today (1993/01/03/0580645)
- *Superintendent Martin Beck*, the *Scandinavian equivalent* of *Sherlock Holmes* (1993/02/21/0591703)
- *Franco Moschino* is the *Weird Al Yankovic* of *fashion* (1993/03/11/0595373)
- *Jack B. Solerwitz* is the *Babe Ruth* of *ripoffs* (1993/03/19/0596753)

### 1994

- *Sweden*, the *Rangers* of *international hockey* (1994/02/12/0668308)
- *Tourte*, the *Stradivarius* of *bows* (1994/02/20/0670039)
- *Phil Liggett*, the *Ben Wright* of the *snow* (1994/02/21/0670187)
- *Ariels*, the *Mexican equivalent* of *Oscars* (1994/03/20/0675424)
- *Canal Plus*, the *HBO* of *France* (1994/03/27/0676813)

### 1995

- *Rush Limbaugh*, the *Babe Ruth* of the *talk-show circuit* (1995/01/05/0735173)
- *Mr. Lovano* is the *General Motors* of *jazz* (1995/01/15/0736903)
- *La Villa*, the *Village Vanguard* of *Paris* (1995/01/15/0736911)

### 1996

- *Ann Landers*, the *Oprah Winfrey* of *newspapers*, (1996/01/17/0823245)
- *Cherry*, the *Rush Limbaugh* of *hockey commentary* (1996/01/21/0824224)
- *Robert Redford*, the *Thomas Jefferson* of *Sundance* (1996/01/24/0825044)
- *Lee Koppelman* is the *Robert Moses* of *Long Island* (1996/02/04/0827620)
- *Peyton* is the *Tanya Harding* of the *plot* (1996/02/10/0828923)
- *Bob Dole* is the *Mozart* of *resentment* (1996/02/11/0829501)
- *Bennett S. LeBow*, the *Niccolo Machiavelli* of the *foxy deal* (1996/03/14/0836529)
- *Julian Luna*, the *Michael Corleone* of *vampires* (1996/04/02/0840971)

### 1997

- *Thomas Eisner*, the *St. Francis* of *bugs* (1997/01/12/0900997)
- *Shaka*, the *Attila* of *Zululand* (1997/01/18/0902375)
- *Albert Belle*, the *Bad Boy* of *Baseball*, (1997/02/10/0908025)
- *Macco*, the *Calabrian version* of the *dish* (1997/02/14/0908831)

### 1998

- *Lovely Lane Methodist Church*, the *Mother Church* of *American Methodism* (1998/01/09/0986279)
- *Benjamin Netanyahu* is the *Ronald Reagan* of *Israel*  (1998/01/20/0989013)
- *Zulu King Shaka*, the *Genghis Khan* of *Africa* (1998/02/05/0993081)
- *Eurosport*, the *European equivalent* of *ESPN* (1998/02/23/0997564)
- The *Palm Pilot* is the *Volkswagen Bug* of the *handheld universe* (1998/02/26/0998073)
- *Parappa* is the *Will Smith* of *video game characters* (1998/03/12/1001407)
- *Beatrice Wood*, the *Mama* of *Dada* (1998/03/14/1001941)
- *Kenneth Starr*, the *Sultan* of the *Subpoena* (1998/03/20/1003494)
- *Adam Graves*, the *Billy Budd* of *hockey* (1998/04/05/1007678)

### 1999

- the *Estee Lauder Companies*, the *General Motors* of the *cosmetics world* (1999/01/10/1075990)
- *Shimano of Japan*, the *Microsoft* of *bicycle-part makers* (1999/03/11/1091448)
- *Tito  Nieves* is called the *Pavarotti of salsa* (1999/03/26/1095206)
- *Special Unit Corps*, the *Yugoslav equivalent* of the *American Special Forces* (1999/04/01/1096836)

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
