
# Attic

Some notes that should not be thrown away, yet.

## German: POS tagging with the Stanford tagger

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
