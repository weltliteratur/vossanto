statistics
==========

temporal distribution
---------------------

We plot some temporal distributions:

``` {.bash}
echo "year articles cand wd wd+bl found true prec"
for year in $(seq 1987 2007); do
    echo $year \
     $(grep ^$year ../articles.tsv | cut -d' ' -f2) \
     $(zcat ../theof_${year}.tsv.gz | wc -l) \
     $(cat ../theof_${year}_wd.tsv | wc -l) \
     $(cat ../theof_${year}_wda_bl.tsv | wc -l) \
     $(../org.py -y ../README.org | grep ${year} | wc -l) \
         $(../org.py --ignore-source-ids fictional_humans_in_our_data_set.tsv -y -c -b ../README.org | grep ${year} | awk -F'\t' '{if ($2 == "D" || $3 == "True") print;}' | wc -l)
done
```

  year       articles   cand       wd      wd+bl   found   true   prec   
  ---------- ---------- ---------- ------- ------- ------- ------ ------ ------
  1987       106104     641432     5236    131     129     95     73.6   0.90
  1988       104541     637132     5074    143     141     88     62.4   0.84
  1989       102818     625894     4922    151     148     104    70.3   1.01
  1990       98812      614164     4890    142     140     105    75.0   1.06
  1991       85135      512582     4189    154     154     103    66.9   1.21
  1992       82685      493808     4442    152     152     103    67.8   1.25
  1993       79200      480883     4338    167     167     121    72.5   1.53
  1994       74925      464278     4038    164     164     112    68.3   1.49
  1995       85392      500404     4636    162     162     124    76.5   1.45
  1996       79077      497688     4250    186     186     133    71.5   1.68
  1997       85396      515759     4561    173     173     134    77.5   1.57
  1998       89163      571010     5333    243     243     180    74.1   2.02
  1999       91074      585464     5375    189     189     136    72.0   1.49
  2000       94258      602240     4750    231     231     172    74.5   1.82
  2001       96282      587644     4512    210     209     163    78.0   1.69
  2002       97258      597289     4992    231     229     177    77.3   1.82
  2003       94235      590890     4749    219     216     165    76.4   1.75
  2004       91362      571894     4702    192     191     153    80.1   1.67
  2005       90004      562027     4680    208     207     162    78.3   1.80
  2006       87052      561203     4786    221     221     169    76.5   1.94
  2007       39953      260778     2276    101     101     76     75.2   1.90
  **sum**    1854726    11474463   96731   3770    3753    2775   73.9   1.50
  **mean**   88320      546403     4606    180     179     132    73.7   1.49

  : The temporal distribution of the number of candidate phrases (cand),
  after matching against Wikidata (wd) and a blacklist (wd+bl), and
  after manual inspection (true). The last column shows the precision.

``` {.gnuplot .rundoc-block rundoc-language="gnuplot" rundoc-var="data=temporal-distribution" rundoc-file="nyt_vossantos_over_time.svg" rundoc-results="silent"}
reset
set datafile separator "\t"

set xlabel "year"
set ylabel "frequency"
set grid linetype 1 linecolor 0
set yrange [0:*]
set y2range [0:100]
set y2label 'precision'
set y2tics
set key top left
set style fill solid 1

set term svg enhanced size 800,600 dynamic fname "Palatino Linotype, Book Antiqua, Palatino, FreeSerif, serif" fsize 16
#set out "nyt_vossantos_over_time.svg"
plot data using 1:6 with linespoints pt 6 ps 7 lc "black" title 'candidates',\
     data using 1:7 with linespoints pt 7 ps 7 lc "black"  title 'Vossantos',\
     data using 1:8 with lines lc "black" title 'precision' axes x1y2

# data using 1:2 with linespoints pt 7 axes x1y2 title 'cand',\
#     data using 1:3 with linespoints pt 7 axes x1y2 title 'wd',\

set term png enhanced size 2835,2126 font "Arial,40" lw 4
# set term png enhanced size 800,600 font "Arial,16" lw  2
set out "nyt_vossantos_over_time.png"
replot

# adapted for arxiv paper
set key bottom right
set term pdf enhanced lw 2
set out "nyt_vossantos_over_time.pdf"
plot data using 1:6 with linespoints pt 6 ps 1 title 'candidates',\
     data using 1:7 with linespoints pt 7 ps 1 title 'Vossantos',\
     data using 1:8 with lines title 'precision' axes x1y2


# ---- relative values

set key top left
set term svg enhanced size 800,600 dynamic fname "Palatino Linotype, Book Antiqua, Palatino, FreeSerif, serif" fsize 16
set out "nyt_vossantos_over_time_rel.svg"
set ylabel "frequency (per mille)"
set format y "%2.1f"

plot data using 1:($6/$2*1000) with linespoints pt 6 ps 7 lc "black" title 'candidates',\
     data using 1:($7/$2*1000) with linespoints pt 7 ps 7 lc "black"  title 'Vossantos',\
     data using 1:8 with lines lc "black" title 'precision' axes x1y2


set term png enhanced size 2835,2126 font "Arial,40" lw 4
# set term png enhanced size 800,600 font "Arial,16" lw  2
set out "nyt_vossantos_over_time_rel.png"
replot

# adapted for arxiv paper
set key bottom right
set term pdf enhanced lw 2
set out "nyt_vossantos_over_time_rel.pdf"
plot data using 1:($6/$2*1000) with linespoints pt 6 ps 1 title 'candidates',\
     data using 1:($7/$2*1000) with linespoints pt 7 ps 1 title 'Vossantos',\
     data using 1:8 with lines title 'precision' axes x1y2

```

Absolute frequency: *nyt\_vossantos\_over\_time.png*

Relative frequency: *nyt\_vossantos\_over\_time\_rel.png*

sources
-------

``` {.bash}
../org.py --ignore-source-ids fictional_humans_in_our_data_set.tsv -w -T ../README.org | sort | uniq -c | sort -nr | head -n40
```

  count   source
  ------- ---------------------------------------------------------------
  68      [Michael Jordan](https://www.wikidata.org/wiki/Q41421)
  58      [Rodney Dangerfield](https://www.wikidata.org/wiki/Q436386)
  36      [Babe Ruth](https://www.wikidata.org/wiki/Q213812)
  32      [Elvis Presley](https://www.wikidata.org/wiki/Q303)
  31      [Johnny Appleseed](https://www.wikidata.org/wiki/Q369675)
  23      [Bill Gates](https://www.wikidata.org/wiki/Q5284)
  21      [Pablo Picasso](https://www.wikidata.org/wiki/Q5593)
  21      [Michelangelo](https://www.wikidata.org/wiki/Q5592)
  21      [Donald Trump](https://www.wikidata.org/wiki/Q22686)
  21      [Jackie Robinson](https://www.wikidata.org/wiki/Q221048)
  21      [Madonna](https://www.wikidata.org/wiki/Q1744)
  20      [P. T. Barnum](https://www.wikidata.org/wiki/Q223766)
  20      [Tiger Woods](https://www.wikidata.org/wiki/Q10993)
  18      [Martha Stewart](https://www.wikidata.org/wiki/Q234606)
  16      [Henry Ford](https://www.wikidata.org/wiki/Q8768)
  16      [William Shakespeare](https://www.wikidata.org/wiki/Q692)
  16      [Wolfgang Amadeus Mozart](https://www.wikidata.org/wiki/Q254)
  15      [Adolf Hitler](https://www.wikidata.org/wiki/Q352)
  14      [Greta Garbo](https://www.wikidata.org/wiki/Q5443)
  14      [John Wayne](https://www.wikidata.org/wiki/Q40531)
  14      [Mother Teresa](https://www.wikidata.org/wiki/Q30547)
  13      [Napoleon](https://www.wikidata.org/wiki/Q517)
  13      [Ralph Nader](https://www.wikidata.org/wiki/Q193156)
  12      [Leonardo da Vinci](https://www.wikidata.org/wiki/Q762)
  12      [Cal Ripken](https://www.wikidata.org/wiki/Q731168)
  12      [Leo Tolstoy](https://www.wikidata.org/wiki/Q7243)
  12      [Oprah Winfrey](https://www.wikidata.org/wiki/Q55800)
  12      [Rosa Parks](https://www.wikidata.org/wiki/Q41921)
  12      [Susan Lucci](https://www.wikidata.org/wiki/Q242936)
  11      [Walt Disney](https://www.wikidata.org/wiki/Q8704)
  11      [Willie Horton](https://www.wikidata.org/wiki/Q8021572)
  11      [Rembrandt](https://www.wikidata.org/wiki/Q5598)
  10      [Albert Einstein](https://www.wikidata.org/wiki/Q937)
  10      [Thomas Edison](https://www.wikidata.org/wiki/Q8743)
  10      [Mike Tyson](https://www.wikidata.org/wiki/Q79031)
  10      [Julia Child](https://www.wikidata.org/wiki/Q214477)
  9       [Ross Perot](https://www.wikidata.org/wiki/Q313697)
  9       [Dennis Rodman](https://www.wikidata.org/wiki/Q201608)
  8       [James Dean](https://www.wikidata.org/wiki/Q83359)
  8       [Mikhail Gorbachev](https://www.wikidata.org/wiki/Q30487)

categories
----------

### online

Extract the categories for the articles:

``` {.bash .rundoc-block rundoc-language="sh" rundoc-results="silent"}
export PYTHONIOENCODING=utf-8
for year in $(seq 1987 2007); do
    ./nyt.py --category ../nyt_corpus_${year}.tar.gz \
        | sed -e "s/^nyt_corpus_//" -e "s/\.har\//\//" -e "s/\.xml\t/\t/" \
        | sort >> nyt_categories.tsv
done
```

Compute frequency distribution over all articles:

``` {.bash .rundoc-block rundoc-language="sh" rundoc-results="silent"}
cut -d$'\t' -f2 nyt_categories.tsv | sort -S1G | uniq -c \
   | sed -e "s/^ *//" -e "s/ /\t/" | awk -F'\t' '{print $2"\t"$1}' \
                                          > nyt_categories_distrib.tsv
```

Check the number of and the top categories:

``` {.bash}
echo articles $(wc -l < nyt_categories.tsv)
echo categories $(wc -l < nyt_categories_distrib.tsv)
echo ""
sort -nrk2 nyt_categories_distrib.tsv | head
```

  ------------ ---------
  articles     1854726
  categories   1580
  Business     291982
  Sports       160888
  Opinion      134428
  U.S.         89389
  Arts         88460
  World        79786
  Style        65071
  Obituaries   19430
  Magazine     11464
  Travel       10440
  ------------ ---------

Collect the categories of the articles

``` {.bash}
echo "vossantos" $(../org.py --ignore-source-ids fictional_humans_in_our_data_set.tsv -T ../README.org | wc -l) articles $(wc -l < ../nyt_categories.tsv)
../org.py --ignore-source-ids fictional_humans_in_our_data_set.tsv -T -f ../README.org | join ../nyt_categories.tsv - | sed "s/ /\t/" | awk -F'\t' '{print $2}' \
    | sort | uniq -c \
    | sed -e "s/^ *//" -e "s/ /\t/" | awk -F'\t' '{print $2"\t"$1}' \
    | join -t$'\t' -o1.2,1.1,2.2 - ../nyt_categories_distrib.tsv \
    | sort -nr | head -n20
```

  vossantos   2646    category                 articles   1854726
  ----------- ------- ------------------------ ---------- ---------
  336         12.7%   Sports                   160888     8.7%
  334         12.6%   Arts                     88460      4.8%
  290         11.0%   New York and Region      221897     12.0%
  237         9.0%    Arts; Books              35475      1.9%
  158         6.0%    Movies; Arts             27759      1.5%
  109         4.1%    Business                 291982     15.7%
  102         3.9%    Opinion                  134428     7.2%
  96          3.6%    U.S.                     89389      4.8%
  95          3.6%    Magazine                 11464      0.6%
  62          2.3%    Style                    65071      3.5%
  61          2.3%    Arts; Theater            13283      0.7%
  46          1.7%    World                    79786      4.3%
  39          1.5%    Home and Garden; Style   13978      0.8%
  32          1.2%    Travel                   10440      0.6%
  31          1.2%    Technology; Business     23283      1.3%
  27          1.0%                             42157      2.3%
  25          0.9%    Week in Review           17107      0.9%
  25          0.9%    Home and Garden          5546       0.3%
  17          0.6%    World; Washington        24817      1.3%
  17          0.6%    Style; Magazine          1519       0.1%

### desks

Extract the desks for the articles:

``` {.bash .rundoc-block rundoc-language="sh" rundoc-results="silent"}
export PYTHONIOENCODING=utf-8
for year in $(seq 1987 2007); do
    ./nyt.py --desk ../nyt_corpus_${year}.tar.gz \
        | sed -e "s/^nyt_corpus_//" -e "s/\.har\//\//" -e "s/\.xml\t/\t/" \
        | sort >> nyt_desks.tsv
done
```

Compute frequency distribution over all articles:

``` {.bash .rundoc-block rundoc-language="sh" rundoc-results="silent"}
cut -d$'\t' -f2 nyt_desks.tsv | sort -S1G | uniq -c \
   | sed -e "s/^ *//" -e "s/ /\t/" | awk -F'\t' '{print $2"\t"$1}' \
                                          > nyt_desks_distrib.tsv
```

Check the number of and the top categories:

``` {.bash}
echo articles $(wc -l < nyt_desks.tsv)
echo categories $(wc -l < nyt_desks_distrib.tsv)
echo ""
sort -t$'\t' -nrk2 nyt_desks_distrib.tsv | head
```

  ------------------------- ---------
  articles                  1854727
  categories                398
  Metropolitan Desk         237896
  Financial Desk            206958
  Sports Desk               174823
  National Desk             143489
  Editorial Desk            131762
  Foreign Desk              129732
  Classified                129660
  Business/Financial Desk   112951
  Society Desk              44032
  Cultural Desk             40342
  ------------------------- ---------

Collect the desks of the articles

``` {.bash}
echo "vossantos" $(./org.py -T README.org | wc -l) articles $(wc -l < nyt_desks.tsv)
./org.py -T -f README.org | join nyt_desks.tsv - | sed "s/ /\t/" | awk -F'\t' '{print $2}' \
    | sort | uniq -c \
    | sed -e "s/^ *//" -e "s/ /\t/" | awk -F'\t' '{print $2"\t"$1}' \
    | join -t$'\t' -o1.2,1.1,2.2 - nyt_desks_distrib.tsv \
    | sort -nr | head -n20
```

  vossantos   2764   desk                      articles   1854727
  ----------- ------ ------------------------- ---------- ---------
  133         4.8%   Sports Desk               174823     9.4%
  77          2.8%   Cultural Desk             40342      2.2%
  68          2.5%   Book Review Desk          32737      1.8%
  61          2.2%   National Desk             143489     7.7%
  54          2.0%   Financial Desk            206958     11.2%
  51          1.8%   Metropolitan Desk         237896     12.8%
  46          1.7%   Weekend Desk              18814      1.0%
  38          1.4%   Arts & Leisure Desk       6742       0.4%
  35          1.3%   Editorial Desk            131762     7.1%
  31          1.1%   Foreign Desk              129732     7.0%
  31          1.1%   Arts and Leisure Desk     27765      1.5%
  25          0.9%   Magazine Desk             25433      1.4%
  25          0.9%   Long Island Weekly Desk   20453      1.1%
  22          0.8%   Living Desk               6843       0.4%
  19          0.7%   Home Desk                 8391       0.5%
  15          0.5%   Week in Review Desk       21897      1.2%
  14          0.5%   Style Desk                21569      1.2%
  13          0.5%   Styles of The Times       2794       0.2%
  12          0.4%                             6288       0.3%
  9           0.3%   Travel Desk               23277      1.3%

Note: there are many errors in the specification of the desks ... so
this table should be digested with care.

authors
-------

Extract the authors for the articles:

``` {.bash .rundoc-block rundoc-language="sh" rundoc-results="silent"}
export PYTHONIOENCODING=utf-8
for year in $(seq 1987 2007); do
    ./nyt.py --author ../nyt_corpus_${year}.tar.gz \
        | sed -e "s/^nyt_corpus_//" -e "s/\.har\//\//" -e "s/\.xml\t/\t/" \
        | sort >> nyt_authors.tsv
done
```

Compute frequency distribution over all articles:

``` {.bash .rundoc-block rundoc-language="sh" rundoc-results="silent"}
cut -d$'\t' -f2 nyt_authors.tsv | sort -S1G | uniq -c \
   | sed -e "s/^ *//" -e "s/ /\t/" | awk -F'\t' '{print $2"\t"$1}' \
                                          > nyt_authors_distrib.tsv
```

Check the number of and the top authors:

``` {.bash}
echo articles $(wc -l < nyt_authors.tsv)
echo categories $(wc -l < nyt_authors_distrib.tsv)
echo ""
sort -t$'\t' -nrk2 nyt_authors_distrib.tsv | head 
```

  --------------------- ---------
  articles              1854726
  categories            30691
                        961052
  Elliott, Stuart       6296
  Holden, Stephen       5098
  Chass, Murray         4544
  Pareles, Jon          4090
  Brozan, Nadine        3741
  Fabricant, Florence   3659
  Kozinn, Allan         3654
  Curry, Jack           3654
  Truscott, Alan        3646
  --------------------- ---------

**requires cleansing!**

Collect the authors of the articles

``` {.bash}
echo "vossantos" $(../org.py --ignore-source-ids fictional_humans_in_our_data_set.tsv -T ../README.org | wc -l) articles $(wc -l < ../nyt_authors.tsv)
../org.py --ignore-source-ids fictional_humans_in_our_data_set.tsv -T -f ../README.org | join ../nyt_authors.tsv - | sed "s/ /\t/" | awk -F'\t' '{print $2}' \
    | sort | uniq -c \
    | sed -e "s/^ *//" -e "s/ /\t/" | awk -F'\t' '{print $2"\t"$1}' \
    | join -t$'\t' -o1.2,1.1,2.2 - ../nyt_authors_distrib.tsv \
    | sort -nr | head -n20
```

  vossantos   2646    author                  articles   1854726
  ----------- ------- ----------------------- ---------- ---------
  411         15.5%                           961052     51.8%
  30          1.1%    Holden, Stephen         5098       0.3%
  29          1.1%    Maslin, Janet           2874       0.2%
  26          1.0%    Vecsey, George          2739       0.1%
  23          0.9%    Sandomir, Richard       3140       0.2%
  22          0.8%    Ketcham, Diane          717        0.0%
  20          0.8%    Kisselgoff, Anna        2661       0.1%
  19          0.7%    Dowd, Maureen           1647       0.1%
  19          0.7%    Berkow, Ira             1704       0.1%
  18          0.7%    Kimmelman, Michael      1515       0.1%
  17          0.6%    Brown, Patricia Leigh   568        0.0%
  16          0.6%    Pareles, Jon            4090       0.2%
  16          0.6%    Chass, Murray           4544       0.2%
  15          0.6%    Smith, Roberta          2497       0.1%
  15          0.6%    Lipsyte, Robert         817        0.0%
  15          0.6%    Grimes, William         1368       0.1%
  15          0.6%    Barron, James           2188       0.1%
  15          0.6%    Anderson, Dave          2735       0.1%
  14          0.5%    Stanley, Alessandra     1437       0.1%
  14          0.5%    Haberman, Clyde         2492       0.1%

### Vossantos of the top author

``` {.bash .rundoc-block rundoc-language="sh" rundoc-results="raw"}
# extract list of articles
for article in $(./org.py -T -f README.org | join nyt_authors.tsv - | grep "Maslin, Janet" | cut -d' ' -f1 ); do
  grep "$article" README.org
done
```

-   [Bob
    Hope](https://www.wikidata.org/wiki/Q94081) (1993/04/23/0604282) is
    loaded with rap-related cameos that work only if you recognize the
    players (Fab 5 Freddy, Kid Capri, Naughty by Nature and **the Bob
    Hope of** rap cinema, Ice-T), and have little intrinsic humor of
    their own.
-   [Sandy
    Dennis](https://www.wikidata.org/wiki/Q239691) (1993/09/03/0632371)
    (Ms. Lewis, who has many similar mannerisms, may be fast becoming
    **the Sandy Dennis of** her generation.)
-   [Dorian
    Gray](https://www.wikidata.org/wiki/Q465417) (1993/12/10/0654992)
    Also on hand is Aerosmith, **the Dorian Gray of** rock bands, to
    serve the same purpose Alice Cooper did in the first film.
-   [Adolf
    Hitler](https://www.wikidata.org/wiki/Q352) (1994/02/04/0666537) The
    terrors of the code, as overseen by Joseph Breen (who was nicknamed
    "**the Hitler of** Hollywood" in some quarters), went beyond the
    letter of the document and brought about a more generalized
    moral purge.
-   [Cinderella](https://www.wikidata.org/wiki/Q13685096) (1994/09/11/0711230)
    Kevin Smith, **the Cinderella of** this year's Sundance festival,
    shot this black-and-white movie in the New Jersey store where he
    himself worked.
-   [Hulk
    Hogan](https://www.wikidata.org/wiki/Q44176) (1994/10/25/0720551)
    Libby's cousin Andrew, an art director who's "so incredibly creative
    that, as my mother says, no one's holding their breath for
    grandchildren," opines that "David Mamet is **the Hulk Hogan of**
    the American theater and that his word processor should be tested
    for steroids."
-   [Andrew Dice
    Clay](https://www.wikidata.org/wiki/Q504455) (1995/09/22/0790066)
    Mr. Ezsterhas, **the Andrew Dice Clay of** screenwriting, bludgeons
    the audience with such tirelessly crude thoughts that when a group
    of chimps get loose in the showgirls' dressing room and all they do
    is defecate, the film enjoys a rare moment of good taste.
-   [Thomas
    Jefferson](https://www.wikidata.org/wiki/Q11812) (1996/01/24/0825044)
    Last year's overnight sensation, Edward Burns of "The Brothers
    McMullen," came out of nowhere and now has Jennifer Aniston acting
    in his new film and Robert Redford, **the Thomas Jefferson of**
    Sundance, helping as a creative consultant.
-   [Elliott
    Gould](https://www.wikidata.org/wiki/Q314805) (1996/03/08/0835139)
    All coy grins and daffy mugging, Mr. Stiller plays the role as if
    aspiring to become **the Elliott Gould of** his generation.
-   [Charlie
    Parker](https://www.wikidata.org/wiki/Q103767) (1996/08/09/0870295)
    But for all its admiration, ''Basquiat'' winds up no closer to that
    assessment than to the critic Robert Hughes's more jaundiced one:
    ''Far from being **the Charlie Parker of** SoHo (as his promoters
    claimed), he became its Jessica Savitch.''
-   [Aesop](https://www.wikidata.org/wiki/Q43423) (1996/08/09/0870300)
    Janet Maslin reviews movie Rendezvous in Paris, written and directed
    by Eric Rohmer; photo (M) Eric Rohmer's ''Rendezvous in Paris'' is
    an oasis of contemplative intelligence in the summer movie season,
    presenting three graceful and elegant parables with the moral
    agility that distinguishes Mr. Rohmer as **the Aesop of** amour.
-   [Diana
    Vreeland](https://www.wikidata.org/wiki/Q450619) (1997/06/06/0934955)
    The complex aural and visual style of ''The Pillow Book'' involves
    rectangular insets that flash back to Sei Shonagon (a kind of
    Windows 995) and illustrate the imperious little lists that made her
    sound like **the Diana Vreeland of** 10th-century tastes.
-   [Peter
    Pan](https://www.wikidata.org/wiki/Q107190) (1997/08/08/0949060) Mr.
    Gibson, delivering one of the hearty, dynamic star turns that have
    made him **the Peter Pan of** the blockbuster set, makes Jerry much
    more boyishly likable than he deserves to be.
-   [Thomas
    Edison](https://www.wikidata.org/wiki/Q8743) (1997/09/19/0958685)
    Danny DeVito embodies this as a gleeful Sid Hudgens (a character
    whom Mr. Hanson has called ''**the Thomas Edison of** tabloid
    journalism''), who is the unscrupulous editor of a publication
    called Hush-Hush and winds up linked to many of the other
    characters' nastiest transgressions.
-   [John
    Wayne](https://www.wikidata.org/wiki/Q40531) (1997/09/26/0960422)
    Mr. Hopkins, whose creative collaboration with Bart goes back to
    ''Legends of the Fall,'' has called him ''**the John Wayne of**
    bears.''
-   [Annie
    Oakley](https://www.wikidata.org/wiki/Q230935) (1997/12/24/0982708)
    Running nearly as long as ''Pulp Fiction'' even though its ambitions
    are more familiar and small, ''Jackie Brown'' has the makings of
    another, chattier ''Get Shorty'' with an added homage to Pam Grier,
    **the Annie Oakley of** 1970's blaxploitation.
-   [Robin
    Hood](https://www.wikidata.org/wiki/Q122634) (1998/04/10/1008616)
    ''Do not threaten to call the police or have him thrown out,'' went
    a memorandum issued by another company, when **the Robin Hood of**
    corporate America went on the road to promote his book
    abou downsizing.
-   [Buster
    Keaton](https://www.wikidata.org/wiki/Q103949) (1998/09/18/1047276)
    Fortunately, being **the Buster Keaton of** martial arts, he makes a
    doleful expression and comedic physical grace take the place of
    small talk.
-   [Michelangelo](https://www.wikidata.org/wiki/Q5592) (1998/09/25/1049076)
    She goes to a plastic surgeon (Michael Lerner) who's been dubbed
    ''**the Michelangelo of** Manhattan'' by Newsweek.
-   [Brian
    Wilson](https://www.wikidata.org/wiki/Q313013) (1998/12/31/1073562)
    The enrapturing beauty and peculiar naivete of ''The Thin Red Line''
    heightened the impression of Terrence Malick as **the Brian Wilson
    of** the film world.
-   [Dante
    Alighieri](https://www.wikidata.org/wiki/Q1067) (1999/10/22/1147181)
    Though his latest film explores one more urban inferno and
    colorfully reaffirms Mr. Scorsese's role as **the Dante of** the
    Cinema, creating its air of nocturnal torment took some doing.
-   [Albert
    Einstein](https://www.wikidata.org/wiki/Q937) (2000/12/07/1253134)
    In this much coarser and more violent, action-heavy story, Mr.
    Deaver presents the villainous Dr. Aaron Matthews, whom a newspaper
    once called ''**the Einstein of** therapists'' in the days before
    Hannibal Lecter became his main career influence.
-   [Émile
    Zola](https://www.wikidata.org/wiki/Q504) (2001/03/09/1276449)
    'Right as Rain' George P. Pelecanos arrives with the best possible
    recommendations from other crime writers (e.g., Elmore Leonard likes
    him), and with jacket copy praising him as ''**the Zola of**
    Washington, D.C.'' But what he really displays here, in great
    abundance and to entertaining effect, is a Tarantino touch.
-   [Leonard
    Cohen](https://www.wikidata.org/wiki/Q1276) (2002/08/22/1417676) The
    wry, sexy melancholy of his observations would be seductive enough
    in its own right -- he is **the Leonard Cohen of** the spy genre --
    even without the sharp political acuity that accompanies it.
-   [Kato
    Kaelin](https://www.wikidata.org/wiki/Q6377737) (2003/04/07/1478881)
    Then he has settled in -- as ''a permanent house guest, **the Kato
    Kaelin of** the wine country,'' in the case of Alan Deutschman --
    and tried to figure out what it all means.
-   [Hulk
    Hogan](https://www.wikidata.org/wiki/Q44176) (2003/04/14/1480850)
    Meanwhile, at 5 feet 10 tall and 115 pounds, Andy is **the Hulk
    Hogan of** this food-phobic crowd.
-   [Nora
    Roberts](https://www.wikidata.org/wiki/Q231356) (2003/04/17/1481531)
    For those who write like clockwork (i.e., Stuart Woods, **the Nora
    Roberts of** mystery best-sellerdom), a new book every few months is
    no surprise.
-   [Henny
    Youngman](https://www.wikidata.org/wiki/Q2586583) (2004/03/05/1563840)
    Together Mr. Yetnikoff and Mr. Ritz devise a kind of sitcom
    snappiness that turns Mr. Yetnikoff into **the Henny Youngman
    of** CBS.
-   [Frank
    Stallone](https://www.wikidata.org/wiki/Q959153) (2004/09/20/1612886)
    He can read the biblical story of Aaron and imagine ''**the Frank
    Stallone of** ancient Judaism.''
-   [Marlon
    Brando](https://www.wikidata.org/wiki/Q34012) (2005/11/08/1715899)
    He named his daughter Tuesday, after the actress Tuesday Weld, whom
    Sam Shepard once called ''**the Marlon Brando of** women.''
-   [Jesse
    James](https://www.wikidata.org/wiki/Q213626) (2005/12/09/1723424)
    How else to explain ''Comma Sense,'' which has a blurb from Ms.
    Truss and claims that the apostrophe is **the Jesse James of**
    punctuation marks?
-   [Elton
    John](https://www.wikidata.org/wiki/Q2808) (2006/12/11/1811150)
    Though Foujita had a fashion sense that made him look like **the
    Elton John of** Montparnasse (he favored earrings, bangs and
    show-stopping homemade costumes), and though he is seen here hand in
    hand with a male Japanese friend during their shared tunic-wearing
    phase, he is viewed by Ms. Birnbaum strictly as a lady-killer.
-   [Ernest
    Hemingway](https://www.wikidata.org/wiki/Q23434) (2007/04/30/1844006)
    Mr. Browne also points out that when he introduced Mr. Zevon to an
    audience as ''**the Ernest Hemingway of** the twelve-string
    guitar,'' Mr. Zevon said he was more like Charles Bronson.

modifiers
---------

``` {.bash}
../org.py --ignore-source-ids fictional_humans_in_our_data_set.tsv -o -T ../README.org | sort | uniq -c | sort -nr | head -n30
```

  count   modifier
  ------- ------------------
  55      his day
  33      his time
  29      Japan
  16      tennis
  16      his generation
  16      baseball
  15      China
  13      her time
  13      her day
  12      our time
  11      the 1990's
  10      the Zulus
  10      the 90's
  10      politics
  10      hockey
  10      Brazil
  10      basketball
  10      ballet
  9       jazz
  9       fashion
  8       today
  8       Israel
  8       his era
  8       hip-hop
  8       golf
  8       dance
  7       the art world
  7       the 19th century
  7       Long Island
  7       Iran

### today

#### "today"

Who are the sources for the modifier "today"?

``` {.bash}
./org.py -w -T -t -c README.org | grep "of\* today" | awk -F'\t' '{print $2}' | sort | uniq -c | sort -nr
```

  count   source
  ------- -----------------------------------------------------------------
  1       [Shoeless Joe Jackson](https://www.wikidata.org/wiki/Q955322)
  1       [David Merrick](https://www.wikidata.org/wiki/Q5237521)
  1       [Buck Rogers](https://www.wikidata.org/wiki/Q4982930)
  1       [Bill McGowan](https://www.wikidata.org/wiki/Q4910116)
  1       [William F. Buckley Jr.](https://www.wikidata.org/wiki/Q378098)
  1       [Ralph Fiennes](https://www.wikidata.org/wiki/Q28493)
  1       [Julie London](https://www.wikidata.org/wiki/Q231255)
  1       [Jimmy Osmond](https://www.wikidata.org/wiki/Q1689414)
  1       [Harry Cohn](https://www.wikidata.org/wiki/Q1586470)

#### "his day" or "his time"

Who are the sources for the modifiers "his day", "his time", and "his
generation"?

``` {.bash}
./org.py -w -T -t -c README.org | grep "of\* his \(day\|time\|generation\)" | awk -F'\t' '{print $2}' | sort | uniq -c  | sort -nr  | head
```

  count   source
  ------- --------------------------------------------------------------
  3       [Michael Jordan](https://www.wikidata.org/wiki/Q41421)
  2       [Mike Tyson](https://www.wikidata.org/wiki/Q79031)
  2       [Billy Martin](https://www.wikidata.org/wiki/Q508574)
  2       [Dan Quayle](https://www.wikidata.org/wiki/Q49214)
  2       [Arnold Schwarzenegger](https://www.wikidata.org/wiki/Q2685)
  2       [Martha Stewart](https://www.wikidata.org/wiki/Q234606)
  2       [Donald Trump](https://www.wikidata.org/wiki/Q22686)
  2       [L. Ron Hubbard](https://www.wikidata.org/wiki/Q216896)
  2       [Tiger Woods](https://www.wikidata.org/wiki/Q10993)
  1       [Lawrence Taylor](https://www.wikidata.org/wiki/Q963129)

#### "her day"

Who are the sources for the modifier "her day"?

``` {.bash}
./org.py -w -T -t -c README.org | grep "of\* her day" | awk -F'\t' '{print $2}' | sort | uniq -c | sort -nr
```

  count   source
  ------- ----------------------------------------------------------
  1       [Hilary Swank](https://www.wikidata.org/wiki/Q93187)
  1       [Hillary Clinton](https://www.wikidata.org/wiki/Q6294)
  1       [Marilyn Monroe](https://www.wikidata.org/wiki/Q4616)
  1       [Judith Krantz](https://www.wikidata.org/wiki/Q452206)
  1       [Lucia Pamela](https://www.wikidata.org/wiki/Q3838473)
  1       [Elizabeth Taylor](https://www.wikidata.org/wiki/Q34851)
  1       [Imelda Marcos](https://www.wikidata.org/wiki/Q285536)
  1       [Laurie Anderson](https://www.wikidata.org/wiki/Q235066)
  1       [Nell Gwyn](https://www.wikidata.org/wiki/Q234163)
  1       [Annie Leibovitz](https://www.wikidata.org/wiki/Q225283)
  1       [Tara Reid](https://www.wikidata.org/wiki/Q211082)
  1       [Madonna](https://www.wikidata.org/wiki/Q1744)
  1       [Maria Callas](https://www.wikidata.org/wiki/Q128297)

### country

``` {.bash}
../org.py --ignore-source-ids fictional_humans_in_our_data_set.tsv -o -T ../README.org \
    | sort | uniq -c | sort -nr | grep "Japan\|China\|Brazil\|Iran\|Israel\|Mexico\|India\|South Africa\|Spain\|South Korea\|Russia\|Poland\|Pakistan" | head -n13
```

  count   country
  ------- --------------
  29      Japan
  15      China
  10      Brazil
  8       Israel
  7       Iran
  7       India
  4       South Africa
  4       Mexico
  3       Spain
  3       South Korea
  3       Russia
  3       Poland
  3       Pakistan

What are the sources for the modifier ... ?

#### "Japan"

``` {.bash}
./org.py -w -T -t -c README.org | grep "of\* Japan" | awk -F'\t' '{print $2}' | sort | uniq -c | sort -nr
```

  count   source
  ------- -----------------------------------------------------------
  5       [Walt Disney](https://www.wikidata.org/wiki/Q8704)
  4       [Bill Gates](https://www.wikidata.org/wiki/Q5284)
  2       [Nolan Ryan](https://www.wikidata.org/wiki/Q721948)
  2       [Frank Sinatra](https://www.wikidata.org/wiki/Q40912)
  1       [Richard Perle](https://www.wikidata.org/wiki/Q966859)
  1       [Thomas Edison](https://www.wikidata.org/wiki/Q8743)
  1       [Mike Tyson](https://www.wikidata.org/wiki/Q79031)
  1       [Leonardo da Vinci](https://www.wikidata.org/wiki/Q762)
  1       [Cal Ripken](https://www.wikidata.org/wiki/Q731168)
  1       [Walter Johnson](https://www.wikidata.org/wiki/Q722059)
  1       [Andy Warhol](https://www.wikidata.org/wiki/Q5603)
  1       [Pablo Picasso](https://www.wikidata.org/wiki/Q5593)
  1       [William Wyler](https://www.wikidata.org/wiki/Q51495)
  1       [Katharine Graham](https://www.wikidata.org/wiki/Q435203)
  1       [Rosa Parks](https://www.wikidata.org/wiki/Q41921)
  1       [Stephen King](https://www.wikidata.org/wiki/Q39829)
  1       [Walker Evans](https://www.wikidata.org/wiki/Q363308)
  1       [Brad Pitt](https://www.wikidata.org/wiki/Q35332)
  1       [Galileo Galilei](https://www.wikidata.org/wiki/Q307)
  1       [Richard Avedon](https://www.wikidata.org/wiki/Q305497)
  1       [P. D. James](https://www.wikidata.org/wiki/Q270648)
  1       [Rem Koolhaas](https://www.wikidata.org/wiki/Q232364)
  1       [Babe Ruth](https://www.wikidata.org/wiki/Q213812)
  1       [Steve Jobs](https://www.wikidata.org/wiki/Q19837)
  1       [Ralph Nader](https://www.wikidata.org/wiki/Q193156)
  1       [Madonna](https://www.wikidata.org/wiki/Q1744)
  1       [Jack Kerouac](https://www.wikidata.org/wiki/Q160534)

#### "China"

``` {.bash}
./org.py -w -T -t -c README.org | grep "of\* China" | awk -F'\t' '{print $2}' | sort | uniq -c | sort -nr
```

  count   source
  ------- -----------------------------------------------------------------
  4       [Barbara Walters](https://www.wikidata.org/wiki/Q231417)
  2       [Jack Welch](https://www.wikidata.org/wiki/Q355314)
  1       [Louis XIV of France](https://www.wikidata.org/wiki/Q7742)
  1       [Oskar Schindler](https://www.wikidata.org/wiki/Q60029)
  1       [Napoleon](https://www.wikidata.org/wiki/Q517)
  1       [Keith Haring](https://www.wikidata.org/wiki/Q485635)
  1       [Rosa Parks](https://www.wikidata.org/wiki/Q41921)
  1       [Mikhail Gorbachev](https://www.wikidata.org/wiki/Q30487)
  1       [Donald Trump](https://www.wikidata.org/wiki/Q22686)
  1       [Larry King](https://www.wikidata.org/wiki/Q213430)
  1       [Ted Turner](https://www.wikidata.org/wiki/Q193368)
  1       [Madonna](https://www.wikidata.org/wiki/Q1744)
  1       [The Scarlet Pimpernel](https://www.wikidata.org/wiki/Q1126679)

#### "Brazil"

``` {.bash}
./org.py -w -T -t -c README.org | grep "of\* Brazil" | awk -F'\t' '{print $2}' | sort | uniq -c | sort -nr
```

  count   source
  ------- --------------------------------------------------------
  1       [Giuseppe Verdi](https://www.wikidata.org/wiki/Q7317)
  1       [Jil Sander](https://www.wikidata.org/wiki/Q69066)
  1       [Walter Reed](https://www.wikidata.org/wiki/Q613136)
  1       [Lech Wałęsa](https://www.wikidata.org/wiki/Q444)
  1       [Jim Morrison](https://www.wikidata.org/wiki/Q44301)
  1       [Michael Jordan](https://www.wikidata.org/wiki/Q41421)
  1       [Bob Dylan](https://www.wikidata.org/wiki/Q392)
  1       [Elvis Presley](https://www.wikidata.org/wiki/Q303)
  1       [Scott Joplin](https://www.wikidata.org/wiki/Q191499)
  1       [Larry Bird](https://www.wikidata.org/wiki/Q190152)
  1       [Pablo Escobar](https://www.wikidata.org/wiki/Q187447)
  1       [Tristan Tzara](https://www.wikidata.org/wiki/Q16409)
  1       [Pelé](https://www.wikidata.org/wiki/Q12897)

### sports

``` {.bash}
./org.py -T -t README.org \
    | perl -pe "s/.*of\* (.*?[a-zA-Z0-9\.]{2}.*?)['.,?\!:;].*/\1/" | sed -e "s/^['\"]*//" -e "s/['\"]*$//" \
    | sort | uniq -c | sort -nr | grep "baseball\|basketball\|tennis\|golf\|football\|racing\|soccer\|sailing" | head -n8
```

  count   sports
  ------- ------------
  15      baseball
  12      tennis
  9       basketball
  7       football
  6       racing
  6       golf
  3       soccer
  3       sailing

Who are the sources for the modifier ... ?

#### baseball

``` {.bash}
./org.py -w -T -t -c README.org | grep "of\* baseball" | awk -F'\t' '{print $2}' | sort | uniq -c | sort -nr
```

  count   source
  ------- -------------------------------------------------------------
  3       [P. T. Barnum](https://www.wikidata.org/wiki/Q223766)
  2       [Babe Ruth](https://www.wikidata.org/wiki/Q213812)
  2       [Larry Bird](https://www.wikidata.org/wiki/Q190152)
  1       [Paul Brown](https://www.wikidata.org/wiki/Q968798)
  1       [Clifford Irving](https://www.wikidata.org/wiki/Q960612)
  1       [Mike Tyson](https://www.wikidata.org/wiki/Q79031)
  1       [Thomas Dooley](https://www.wikidata.org/wiki/Q695751)
  1       [Marco Polo](https://www.wikidata.org/wiki/Q6101)
  1       [Pablo Picasso](https://www.wikidata.org/wiki/Q5593)
  1       [Horatio Alger](https://www.wikidata.org/wiki/Q453251)
  1       [Rodney Dangerfield](https://www.wikidata.org/wiki/Q436386)
  1       [Michael Jordan](https://www.wikidata.org/wiki/Q41421)
  1       [Alan Alda](https://www.wikidata.org/wiki/Q310394)
  1       [Brandon Tartikoff](https://www.wikidata.org/wiki/Q2923786)
  1       [Howard Hughes](https://www.wikidata.org/wiki/Q189081)
  1       [Elisha Cook, Jr.](https://www.wikidata.org/wiki/Q1330714)
  1       [Thomas Jefferson](https://www.wikidata.org/wiki/Q11812)

#### tennis

``` {.bash}
./org.py -w -T -t -c README.org | grep "of\* tennis" | awk -F'\t' '{print $2}' | sort | uniq -c | sort -nr
```

  count   source
  ------- ----------------------------------------------------------
  2       [George Foreman](https://www.wikidata.org/wiki/Q213919)
  1       [Tim McCarver](https://www.wikidata.org/wiki/Q7803927)
  1       [Pete Rose](https://www.wikidata.org/wiki/Q739866)
  1       [Nolan Ryan](https://www.wikidata.org/wiki/Q721948)
  1       [Crash Davis](https://www.wikidata.org/wiki/Q5182352)
  1       [Spike Lee](https://www.wikidata.org/wiki/Q51566)
  1       [John Madden](https://www.wikidata.org/wiki/Q51516)
  1       [Michael Jordan](https://www.wikidata.org/wiki/Q41421)
  1       [John Wayne](https://www.wikidata.org/wiki/Q40531)
  1       [George Hamilton](https://www.wikidata.org/wiki/Q359416)
  1       [Michael Dukakis](https://www.wikidata.org/wiki/Q319099)
  1       [Jackie Robinson](https://www.wikidata.org/wiki/Q221048)
  1       [Babe Ruth](https://www.wikidata.org/wiki/Q213812)
  1       [Dennis Rodman](https://www.wikidata.org/wiki/Q201608)
  1       [Madonna](https://www.wikidata.org/wiki/Q1744)

#### basketball

``` {.bash}
./org.py -w -T -t -c README.org | grep "of\* basketball" | awk -F'\t' '{print $2}' | sort | uniq -c | sort -nr
```

  count   source
  ------- ----------------------------------------------------------------
  2       [Babe Ruth](https://www.wikidata.org/wiki/Q213812)
  1       [Joseph Stalin](https://www.wikidata.org/wiki/Q855)
  1       [Martin Luther King, Jr.](https://www.wikidata.org/wiki/Q8027)
  1       [John Madden](https://www.wikidata.org/wiki/Q51516)
  1       [Bill Stern](https://www.wikidata.org/wiki/Q4911006)
  1       [Pol Pot](https://www.wikidata.org/wiki/Q39464)
  1       [Johnny Appleseed](https://www.wikidata.org/wiki/Q369675)
  1       [Adolf Hitler](https://www.wikidata.org/wiki/Q352)
  1       [Bugsy Siegel](https://www.wikidata.org/wiki/Q315487)
  1       [Elvis Presley](https://www.wikidata.org/wiki/Q303)
  1       [Chuck Yeager](https://www.wikidata.org/wiki/Q271939)
  1       [Norm Crosby](https://www.wikidata.org/wiki/Q1999216)

#### football

``` {.bash}
./org.py -w -T -t -c README.org | grep "of\* football" | awk -F'\t' '{print $2}' | sort | uniq -c | sort -nr
```

  count   source
  ------- ----------------------------------------------------------
  1       [Pliny the Elder](https://www.wikidata.org/wiki/Q82778)
  1       [Michael Myers](https://www.wikidata.org/wiki/Q535502)
  1       [Ann Calvello](https://www.wikidata.org/wiki/Q4766303)
  1       [Bobby Fischer](https://www.wikidata.org/wiki/Q41314)
  1       [Mark Cuban](https://www.wikidata.org/wiki/Q318503)
  1       [Patrick Henry](https://www.wikidata.org/wiki/Q311885)
  1       [Susan Lucci](https://www.wikidata.org/wiki/Q242936)
  1       [Jackie Robinson](https://www.wikidata.org/wiki/Q221048)
  1       [Babe Ruth](https://www.wikidata.org/wiki/Q213812)
  1       [Rich Little](https://www.wikidata.org/wiki/Q1341644)

#### racing

``` {.bash}
./org.py -w -T -t -c README.org | grep "of\* racing" | awk -F'\t' '{print $2}' | sort | uniq -c | sort -nr
```

  count   source
  ------- -------------------------------------------------------------
  2       [Rodney Dangerfield](https://www.wikidata.org/wiki/Q436386)
  1       [John Madden](https://www.wikidata.org/wiki/Q51516)
  1       [Bobo Holloman](https://www.wikidata.org/wiki/Q4935855)
  1       [Lou Gehrig](https://www.wikidata.org/wiki/Q357444)
  1       [Wayne Gretzky](https://www.wikidata.org/wiki/Q209518)

#### golf

``` {.bash}
./org.py -w -T -t -c README.org | grep "of\* golf" | awk -F'\t' '{print $2}' | sort | uniq -c | sort -nr
```

  count   source
  ------- ----------------------------------------------------------
  2       [Michael Jordan](https://www.wikidata.org/wiki/Q41421)
  2       [Jackie Robinson](https://www.wikidata.org/wiki/Q221048)
  1       [J. D. Salinger](https://www.wikidata.org/wiki/Q79904)
  1       [James Brown](https://www.wikidata.org/wiki/Q5950)
  1       [Marlon Brando](https://www.wikidata.org/wiki/Q34012)
  1       [Babe Ruth](https://www.wikidata.org/wiki/Q213812)
  1       [Simon Cowell](https://www.wikidata.org/wiki/Q162629)

### culture

``` {.bash}
./org.py -T -t README.org \
    | perl -pe "s/.*of\* (.*?[a-zA-Z0-9\.]{2}.*?)['.,?\!:;].*/\1/" | sed -e "s/^['\"]*//" -e "s/['\"]*$//" \
    | sort | uniq -c | sort -nr | grep "dance\|hip-hop\|jazz\|fashion\|weaving\|ballet\|the art world\|wine\|salsa"   | head -n9
```

  count   modifier
  ------- -------------------
  8       jazz
  8       hip-hop
  8       fashion
  8       dance
  7       the art world
  6       ballet
  4       wine
  4       salsa
  2       the fashion world

### Michael Jordan

``` {.bash .rundoc-block rundoc-language="sh" rundoc-results="raw"}
./org.py -T -l -t README.org | awk -F'\t' '{if ($1 == "Michael Jordan") print $2}' \
    | perl -pe "s/.*of\* (.*?[a-zA-Z0-9\.]{2}.*?)['.,?\!:;)\"].*/\1/" | sed -e "s/^['\"]*//" -e "s/['\"]*$//" -e "s/^/- /" \
    | sort -u
```

the Michael Jordan of

-   12th men
-   actresses
-   Afghanistan
-   Australia
-   baseball home where he was raised in Cincinnati
-   BMX racing
-   boxing
-   Brazilian basketball for the past 20 years
-   college coaches
-   computer games
-   cricket
-   cyberspace to log a few minutes on a real basketball court
-   dance
-   diving
-   dressage horses
-   fast food
-   figure skating
-   foosball
-   game shows
-   geopolitics
-   geopolitics -- the overwhelmingly dominant system
-   golf
-   Harlem
-   hers
-   his day
-   his sport
-   his team
-   his time
-   hockey
-   hockey by a former Lightning owner
-   horse racing
-   hunting and fishing
-   Indiana
-   integrating insurance and health care
-   julienne
-   jumpers
-   language
-   Laser sailing
-   late-night TV
-   management in Digital
-   Meet **the Michael Jordan of** …
-   Mexico
-   motocross racing in the 1980
-   orange juice
-   recording
-   Sauternes
-   snowboarding -- in every interview and article on him
-   soccer and Bebeto is the Magic Johnson of soccer
-   television puppets
-   tennis
-   the Buffalo team
-   the dirt set
-   the Eagles
-   the game
-   the Hudson
-   the National Football League
-   the South Korean penal system
-   the sport
-   the White Sox
-   this sport
-   women

favourites
----------

Robert:

-   [Marquis de
    Sade](https://www.wikidata.org/wiki/Q123867) (1993/09/26/0636952)
    When we introduced Word in October 1983, in its first incarnation it
    was dubbed **the Marquis de Sade of** word processors, which was not
    altogether unfair.
-   [Groucho
    Marx](https://www.wikidata.org/wiki/Q103846) (1987/09/27/0077726)
    But the tide eventually shifted, partly because the supreme
    materialist of physics, Richard Feynman of the California Institute
    of Technology, a man once described as **the Groucho Marx of**
    physics, turned the quest for nuclear substructure into a
    cause celebre.

list of vossantos
=================

``` {.bash}
../org.py --ignore-source-ids fictional_humans_in_our_data_set.tsv -g -H -T ../README.org \
      | pandoc -f org -t markdown -o vossantos.md
```
