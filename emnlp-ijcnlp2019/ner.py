# takes a file from theof.py and applies stanford ner tagging on each sentence. Checks whether the source is completely tagged as "PERSON" and writes those candidates in a new file

import csv
from sner import Ner

# type your pattern in here
pattern = "thefor"
first_pattern = "the"
second_pattern = "for"

# file from theof.py
cand_file = " "
# output
outputfile = " "
k = 0


with open(cand_file, "r") as input, open(outputfile, "w") as output:
    reader = csv.reader(input, delimiter="\t")
    writer = csv.writer(output, delimiter="\t", quoting=csv.QUOTE_ALL)
    for row in reader:
        articleid = row[0]
        source = row[1]
        sent = row[2]
        # using the server from stanford ner tagger
        tagger = Ner(host="localhost", port=9199)
        # tagging the candidate sentence
        tag = tagger.get_entities(sent)
        # check if all source words are tagged with "PERSON"
        for i in range(len(tag)):
            flag = False
            if tag[i][0] == first_pattern:
                source_person = []
                for j in range(1, min(6, len(tag) - i)):
                    if (
                        tag[i + j][1] != "PERSON"
                        and tag[i + j][0] != second_pattern
                        and tag[i + j][0] != first_pattern
                    ):
                        break
                    elif tag[i + j][0] == first_pattern:
                        source_person = []
                        source_person = []
                    elif (
                        tag[i + j][0] == second_pattern
                        and source_person != []
                        and " ".join(source.split()[1:-1]).find(" ".join(source_person))
                        != -1
                    ):
                        print(
                            articleid,
                            source,
                            " ".join(source_person),
                            sent,
                            tag,
                            sep="\t",
                        )
                        writer.writerow(
                            [articleid, source, " ".join(source_person), sent, tag]
                        )
                        k = k + 1
                        flag = True
                        break
                    elif tag[i + j][1] == "PERSON":
                        source_person.append(tag[i + j][0])

                if flag == True:
                    break
