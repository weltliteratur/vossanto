
# Vossian Antonomasia

see [Der Umblätterer: Vossianische Antonomasie](http://www.umblaetterer.de/datenzentrum/vossianische-antonomasien.html)

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

source: New York Times corpus 1987-2007

[1987](#1987), [1988](#1988), [1989](#1989), [1990](#1990), [1991](#1991), [1992](#1992), [1993](#1993), [1994](#1994), [1995](#1995), [1996](#1996), [1997](#1997), [1998](#1998), [1999](#1999), [2000](#2000), [2001](#2001), [2002](#2002), [2003](#2003), [2004](#2004), [2005](#2005), [2006](#2006), [2007](#2007)

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
- *Olivier Award*, the *English equivalent* of the *Tony* (1988/02/01/0114868)
- *Queen Victoria*, the *Great Satan* of the *time* (1988/02/03/0115425)
- *David Leslie*, the *Evel Knievel* of *performance artists* (1988/02/05/0116272)
- *Nahlas* - the *Slovak equivalent* of *glasnost* (1988/03/03/0124041)
- the *Young Pioneers* - the *Soviet equivalent* of the *Boy Scouts* (1988/03/21/0129426)
- *Smith*, the *Wizard* of *Ahs* (1988/04/02/0132691)
- If *Mr. Moynihan* is the *Sherlock Holmes* of the *fiscal story*, then *Mr. Stockman* is at once *its Dr. Watson* and *its Moriarty*. (1988/04/17/0136766)
- *Robert Stroud*, the *Birdman* of *Alcatraz* (1988/04/23/0138826)
- *Mr. John*, the *Emperor* of *Fashion* (1988/05/02/0141129)
- *Gypsy Byrne*, the *Beau Brummel* of *Broadway* (1988/05/29/0149355)
- *Morris* has been the *Clark Cable* of the *catnip crowd* (1988/05/29/0149364)
- *Gainsborough* is the *Mozart* of *portraiture* (1988/07/17/0162061)
- *Hughes*, the *Mad Hatter* of *capitalism* (1988/09/11/0178234)
- *Eddie Shore*, the *Babe Ruth* of *hockey* (1988/11/04/0194523)
- *Sax* dressed alongside *Kirk Gibson* and *Mickey Hatcher*, the *Three Musketeers* of *Hyperactivity* (1988/11/27/0201849)
- *Guzman* is regarded as "the *Stalin* of *Patchogue*, the *Idi Amin* of *Long Island*" (1988/12/06/0204254)

### 1989

- *Ace Nelson*, the *Oracle* of *Survay* (1989/01/09/0212675)
- *California* is the *State* of *Champions* (1989/01/24/0217109)
- *EUROPCAR*, the *European counterpart* of *National Car Rental* (1989/03/05/0228921)
- *Late 18th Century*, the *Age* of *Reason* (1989/03/10/0230298)
- *Banter* is the *Ping-Pong* of *debate* (1989/04/30/0245628)
- *Kips Bay* is the *Academy Awards* of *interior design* (1989/05/21/0251994)
- *Barnum* - the *Michelangelo* of *buncombe*, *hokum*, *hoopla* and *ballyhoo* (1989/06/06/0256423)
- *Early Wright*, the *Chaucer* of the *Mississippi Delta* (1989/06/28/0262085)
- *Milton Friedman*, the *American apostle* of *free-market economics* (1989/07/12/0265229)
- *Sturm, Ruger* is the *Benedict Arnold* of the *gun industry* (1989/07/14/0265756)
- the *New Orleans chef Paul Prudhomme*, the *Louis Armstrong* of *jambalaya*, *crawfish pie* and *file gumbo*  (1989/08/17/0276060)
- *Colombia* is the *South Korea* of *flower exporters* (1989/09/20/0284628)
- *Raj Path*, the *Champs-Elysees* of *Delhi* (1989/10/01/0287183)
- *Heiner Goebbels*, the *John Zorn* of *West Germany* (1989/11/10/0299484)
- *Romeo Gigli*, the *Pavarotti* of *embroidery* (1989/11/12/0299980)
- the *Design Museum* is the *Louvre* of *industrial design* (1989/11/19/0302179)
- *Dr. Oswaldo Cruz*, the *Walter Reed* of *Brazil* (1989/11/26/0304421)
- *Clios*, the *Oscars* of *advertising* (1989/11/27/0304652)
- She told on me to Him, *Himself*, the *Bestower* of *All Toys* (1989/12/24/0311534)
- the *House of the Republic*, the *Staircase* of *Honor* (1989/12/31/0313389)

### 1990

- the *remarkable enclosed indoor Housewives' Market*, the *Halles* of *soul food*  (1990/01/07/0314867)
- *Mr. Gorbachev*, the *Houdini* of *politicians* (1990/02/05/0323616)
- *Clive Barker* is the *Paul McCartney* of *horror fiction* (1990/02/11/0325668)
- *Sadaharu Oh*, the *Shogun* of *Swat* (1990/02/19/0328100)
- *Waterman*, the *Rolls-Royce* of *pens* acquired in 1987, and *Papermate*, the *Chevrolet* of *pens* (1990/02/25/0329728)
- *CHARDONNAY* is the *Budweiser* of *white wines* (1990/03/28/0338654)
- *Don Zimmer*, the *Merlin* of the *Chicago Cubs* (1990/04/18/0344773)
- *Robert Tappan Morris* is the *Oliver North* of *computer abuse* (1990/05/08/0351502)
- The *Public Media Center* is the *Ralph Nader* of *agencies* (1990/05/21/0355271)
- *Sam Llewellyn*, the *Dick Francis* of *sailing* (1990/06/10/0360283)
- *Oscar D'Leon*, the *James Brown* of *salsa* (1990/06/29/0364544)
- *Oscar*, the *Larry Bird* of *Brazil* (1990/07/29/0372556)
- *Broadway* is the *Rolls-Royce* of *all theatrical experiences* (1990/08/24/0379112)
- *Olivier Award*, the *British equivalent* of the *Tony* (1990/09/06/0382052)
- *Roscoe Tanner*, the *Nolan Ryan* of *tennis* (1990/09/07/0382279)
- If *Wrigley* is the *Faneuil Hall Marketplace* of *ball parks*, *Comiskey* is *Paddy's Market*. (1990/09/30/0387487)
- *Calvin Trillin* is the *Buster Keaton* of *performance humorists*  (1990/10/15/0392151)
- *Charles Oakley*, the *Charles Atlas* of *forwards* (1990/11/06/0398601)
- the *Grey Cup*, the *Canadian equivalent* of the *Super Bowl* (1990/11/25/0403957)
- "*New York State* is the *Cadillac* of *social services*," Mr. Alfonso said. "*Other states* have *Volkswagens*."  (1990/11/26/0404144)
- If *Toys "R" Us* is the *Gulliver* of *toy sellers*, then *Nintendo* is the *Godzilla of toys*  (1990/12/06/0406527)
- *Delta Pride*, the *General Motors* of *catfish processing factories* (1990/12/10/0407519)
- *Stephanie Wood*, the *Witch* of the *Ruby* (1990/12/16/0409087)
- *Mean Mike*, the *Scourge* of the *Tube* (1990/12/30/0411874)

### 1991

- *George Foreman*, the *Santa Claus* of *sports* (1991/01/01/0412333)
- *New York* is the *Cadillac* of *welfare states* (1991/01/31/0419226)
- *Gillian Anderson* is the *Pauper* of *professional experience*, *Brenda Blethyn* is the *Princess* (1991/02/20/0424794)
- *Hasselblad*, the *Mercedes-Benz* of *camera makers* (1991/03/10/0428959)
- If the *American Budweiser* is the *King of Beers*, what does that make the *Czech Budweiser*? Why, none other than the *Beer* of *Kings*, if negotiations between the two brewers succeed. (1991/03/10/0429088)

### 1992

-  *Luis Cisneros*, better known to colleagues as *Sandra*, the *Queen* of the *Bois* (1992/01/11/0499353)
- the Islanders, the Boys of Winter (1992/01/24/0502719)
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

- *Terry Riley*, the *California Minimalist*; *Astor Piazzolla*, the *Argentine master* of the *nuevo tango*; and *John Zorn*, the *New York bender* of *genres* (2004/01/11/1549709)
- the *Callichoron*, the *Well* of the *Beautiful Dances* (2004/01/15/1550942)
- *Norman Lebrecht* has been the *Cassandra* of *classical music* (2004/02/04/1556102)
- *Hal Schell*, the *Boswell* of the *delta* (2004/02/06/1556601)
- *Ouidad*, the *Queen* of *Curl* (2004/02/15/1559089)
- *Maddux* has been the *Larry Bird* of *baseball* (2004/02/21/1560506)
- *Arturo Gatti* is the *Oscar De La Hoya* of *New Jersey* (2004/02/22/1560800)
- *Steinway*, the *Mercedes* of *pianos* (2004/02/29/1562589)
- *Azim Premji* is the *Bill Gates* of *India* (2004/03/21/1568087)
- *Yomiuri Giants*, the *Japanese equivalent* of the *Yankees* (2004/03/28/1569955)
- If *Mariano Rivera of the Yankees* is the *Mr. October* of *closers*, *Gagne* is the *Mr. Season*. (2004/05/18/1582589)
- *Lil' John*, the *King* of *Crunk* (2004/05/23/1583885)
- *TechZilla*, the *Lamborghini* of *slow-pitch bats* (2004/05/30/1585628)
- *Dionysos*, the *God of drama* (2004/06/27/1592422)
- *Brenda Bishop*, the *Granny Bandit* of *Macomb County* (2004/07/03/1593896)
- *Oden* is the *Japanese equivalent* of *chicken soup* (2004/03/10/1565172)
- A *reforming liberal leader in Russia* is the *Holy Grail* of *Kremlinology* (2004/03/14/1566359)
- *Graham*, the *Keeper* of the *List* (2004/04/04/1571542)
- the *Village Vanguard*, the *Stradivarius* of *jazz clubs* (2004/05/12/1581028)
- *Sirius*, the *Avis* of *satellite radio broadcasters* (2004/06/20/1590789)
- *Daniel Jackling* has been called the *Henry Ford* of *minerals* (2004/07/15/1596782)
- the *Helen Hayes Awards*, the *Tonys* of *Washington* (2004/08/08/1602364)
- *Papa Ge*, the *Demon* of *Death* (2004/08/22/1605641)
- *Arnold Schwarzenegger* is the *John Wayne* of the *current generation* (2004/09/01/1608307)
- *Reggaeton*, the *Puerto Rican amalgam* of *dancehall reggae*, *gangsta rap* and *touches of salsa* (2004/09/03/1608662)
- *Styx Valley*, the *Valley* of the *Giants* (2004/09/12/1610579)
- *Darren Romeo*, the *Voice* of *Magic* (2004/09/19/1612812)
- *Evans* is the *Jerry Lewis* of *modern design* (2004/09/23/1613516)
- the *only alternative* to the *Canyon* of *Heroes* is the *Valley* of *Doom* (2004/09/30/1615408)
- *Dan Flavin*, the *American avatar* of the *fluorescent tube* (2004/10/01/1615466)
- *Nanz Custom Hardware*, the *Barwil* of *cabinet pulls* (2004/10/14/1619047)
- *Mesa Verde National Park* has been called the *Disneyland* of *ancient sites*, but it's also the *Anasazi* *Yosemite* (2004/10/15/1619273)
- *Osama, the *BAAAADest* of the *Bad* (2004/11/02/1624049)
- *Dave Gorman*, the *Picasso* of *procrastination* (2004/11/05/1624728)
- the *southern French city of Grasse*, the *Mecca* of *perfume manufacturers* (2004/11/05/1624748)
- *John Monteleone*, the *Stradivari* of the *six-string world*
- *Ours* is the *Age* of *Recycling* (2004/12/03/1631679)
- *Chip Foose* is the *Vargas* of the *custom-car world* (2004/12/31/1638539)

### 2005

- the *District of Columbia*, the *Camp David* of the *day* (2005/01/09/1640426)
- *Lauren Hutton* is the *Zelig* of *travel* (2005/01/09/1640625)
- *Bill Belichick* is the *Bobby Fischer* of *football* (2005/01/18/1643049)
- *Richard Foreman*, the *Florenz Ziegfeld* of *avant-garde drama* (2005/01/21/1643632)
- *Hocoka*, the *Sioux concept* of *healing* (2005/02/06/1647643)
- *Michael Powell*, the *Savonarola* of the *Federal Communications Commission* (2005/02/06/1647680)
- *Norbert Wiener*, the *Father* of *Cybernetics* (2005/03/01/1653553)
- *Veggie Booty*, the *Cheez Doodles* of the *21st century* (2005/03/06/1654677)
- *Long Island*, the *Galapagos* of *suburban dysfunction* (2005/03/20/1658622)
- *Qwest*, the *Rodney Dangerfield* of the *telephone industry* (2005/04/01/1661389)
- *Mabahith*, the *Egyptian equivalent* of the *F.B.I.* (2005/04/08/1663228)
- *John LaValle* has been the *Gorbachev* of *Brookhaven* (2005/04/10/1663656)
- *Intel*, the *Goliath* of the *chip industry* (2005/04/21/1666553)
- *Mont Ventoux*, the *Giant* of *Provence* (2005/06/05/1678016)
- *Mr. Ruscha*, the *Riddler* of the *art world* (2005/06/12/1679564)
- *Maitreya* is the *Buddha* of the *future* (2005/07/22/1689075)
- *Ravenswood* is the *Death Valley* of *New York City* (2005/07/23/1689358)
- *Frederick Carder* has been called the *Mad Hatter* of *glass* (2005/08/25/1697096)
- *Tony Scott*, the *Ozu* of *action films* (2005/09/11/1701087)
- Known as *First Responders*, the *Paul Reveres* of the *hurricane season* (2005/09/11/1701351)
- *Charles Birnbaum* is the *Johnny Appleseed* of *landscape preservation* (2005/09/15/1702130)
- *Faryab* is the *Wild West* of *Afghanistan* (2005/09/18/1703218)
- *Small* is the *Yankee* of the *hour* (2005/09/30/1706122)
- *Karl Rove* is the *Bill Buckley* of *today* (2005/10/09/1708539)
- *Testaverde* is the *Roger Clemens* of *pro football* (2005/10/10/1708694)
- *SKC*, the *CBGB* of *Belgrade* (2005/10/16/1709847)
- *Clemens*, the *John Wayne* of *pitchers* (2005/10/23/1712004)
- the *younger Redon*, the *Redon* of the *"Noirs"* (2005/10/28/1712946)
- *Puebla* is the *Lyon* of *Mexico* (2005/11/20/1718800)
- "If *bin Laden* is the *Robin Hood* of *jihad*," the authors write, then *Abu Musab al-Zarqawi* "has been its *Horatio Alger*, and *Iraq* his *field of dreams*." (2005/11/20/1719129)
- If the *vast, empty plain of eastern Montana* is the *Saudi Arabia* of *coal*, then *Gov. Brian Schweitzer* may be its *Lawrence*. (2005/11/21/1719391)
- *Cambridge*, the *Athens* of *America* (2005/11/27/1720488)
- *Robinson*, the *Thumbelina* of *rookies* (2005/11/27/1720778)
- *Rijkswaterstaat*, the *Dutch equivalent* of the *Corps of Engineers* (2005/11/29/1721150)
- the *beautiful Hudson*, the *Hudson* of the *imagination* (2005/12/04/1722098)

### 2006

- *Lance Fung*, the *Admiral Perry* of the *art world* (2006/02/02/1736482)
- If *Buenos Aires* is the *Paris* of *South America*, *Quebec City* is the *Paris* of *North America*. (2006/02/19/1740811)
- *Bafta*, the *British equivalent* of the *Academy Awards* (2006/03/06/1744762)
- *Joe Namath* is the *Ann Calvello* of *football* (2006/03/17/1747425)
- *James Brown*, the *Godfather* of *Soul* (2006/03/25/1749390)
- *Sunset Park*, the *Chinatown* of *Brooklyn* (2006/04/09/1753245)
- *Reggie Jackson*, the *Yankees Hall* of *Famer* (2006/04/12/1753998)
- *Everlast* is the *Mercedes-Benz* of *boxing* (2006/04/24/1756853)
- *Treasury Secretary John Snow*, the *Sarah Bernhardt* of the *Bush administration* (2006/05/14/1761468)
- *Moon Mullican*, the *King* of the *Hillbilly Piano* (2006/06/04/1766403)
- *Jeffrey Chodorow* is the *Jerry Bruckheimer* of *restaurants* (2006/06/04/1766638)
- *Mark Hanna*, the *Karl Rove* of *the day* (2006/06/18/1769818)
- *Johnny Miller*, the *Simon Cowell* of *golf criticism* (2006/06/20/1770506)
- *Biz Cool*, the *Japanese equivalent* of *business casual* (2006/06/24/1771315)
- *Liberty*, the *British equivalent* of the *American Civil Liberties Union* (2006/06/25/1771465)
- *Ghana* is the *Brazil* of *Africa* (2006/06/28/1772401)
- *Garberville*, the *Central Valley* of *marijuana* (2006/08/28/1786070)
- the *modern Steinway*, the *Hummer* of *instruments* (2006/08/30/1786358)
- *Elisabeth Hasselbeck*, the *Zeppo Marx* of the *foursome* (2006/09/06/1787907)
- *Jacob Arabo*, the *Harry Winston* of the *bling-bling set* (2006/09/12/1789409)
- the 2006 *Westminster Kennel Club Dog Show*, the *Kentucky Derby* of *canine competitions* (2006/09/24/1792272)
- *Darquier de Pellepoix* is the *Zelig* of this *history* (2006/10/12/1796531)
- *Artaud*, the *Wieland Wagner* of the *present time* (2006/10/22/1799005)
- *Eclipse Awards*, *Oscars* of *horse racing* (2006/10/30/1801003)
- *Chalkhill Estates in London*, the *British equivalent* of a *housing project* (2006/11/01/1801327)
- *Benny Goodman*, the *King* of *Swing* (2006/11/22/1806655)
- *Kyle Avila*, the *Michelangelo* of the *bunch* (2006/12/17/1812547)
- *Vegas*, the *Renaissance Florence* of the *art* (2006/12/22/1813538)
- *Anna Netrebko*, the *Julia Roberts* of *opera* (2006/12/22/1813555)
- the *AVN Awards*, the *Oscars* of the *skin trade* (2006/12/31/1815543)

### 2007

- *Jon Jerde*, the *California master* of *mall design* (2007/01/04/1816247)
- *Richard Feynman*, the *Neal Cassady* of *physics* (2007/01/07/1816844)
- *Mariano*, the *Mariano* of the *present* (2007/02/15/1826443)
- *Mary Magdalene* is the *Ringo* of *this inquiry* (2007/03/03/1830035)
- *New York* is the *Mecca* of *basketball* (2007/04/05/1838196)
- *Talaa Kebira*, the *Broadway* of *Fez* (2007/04/08/1839030)
- *Mr. Gunn* is the *Michelangelo* of *the form* (2007/04/12/1839640)
- *Superman*, the *Man* of *Steel* (2007/04/25/1842867)
- *Clomid* is the *Alfred Hitchcock* of *drugs* (2007/05/02/1844502)
- *Jack Reacher*, the *Paul Bunyan* of the *thriller world* (2007/05/14/1847325)
- *James Brown*, the *Godfather* of *Soul* (2007/05/27/1850236)
- *Alberto Gonzales* is the *Michael Brown* of the *Justice Department* (2007/06/11/1853778)
- *Fred Sandback*, the *American master* of *ethereal string geometries* (2007/06/15/1854531)
