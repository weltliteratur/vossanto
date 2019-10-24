# takes a file from check_wikidata_part2.py and removes all candidates where source+ following words are an entity in wikidata

import csv
import re

# type your pattern in here
pattern = "theof"
first_pattern = "the"
second_pattern = "of"

# file from check_wikidata_part1.py
candidates = "../signalmedia_theof_cd_wd_wd1.tsv"
# output file
output = "../signalmedia_theof_cd_wd_wd1_wd2.tsv"

# entity file from wikidata with second pattern in it
entities = "../theof_expanded/entities_of.tsv"

with open(candidates, "r") as candidate_file, open(entities, "r") as entity_file, open(
    output, "w"
) as output_file:
    cand_reader = csv.reader(candidate_file, delimiter="\t")
    entity_reader = csv.reader(entity_file, delimiter="\t")
    writer = csv.writer(output_file, delimiter="\t", quoting=csv.QUOTE_ALL)
    entity_reader_list = list(entity_reader)
    count_cand = 0
    count_match = 0
    # reads all VA candidates
    for row in cand_reader:

        entity_list = []

        article = row[0]

        source = row[2].strip().lower()

        sent = row[5].strip().lower()
        # creates a list with all entities from wikidata where the source appears
        for line in entity_reader_list:

            if len(line) >= 2:

                entity = line[1].strip().lower()

                if source in entity:

                    entity_list.append(entity)
        # no match
        if entity_list == []:
            writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5]])
            count_cand += 1
        else:
            i = 0
            # checks if the entity candidate is fully appearing at the beginning of source + several words after source.
            for ent in entity_list:

                i += 1
                the_source_of = first_pattern + " " + source + " " + second_pattern
                source_of = source + " " + second_pattern
                if the_source_of in sent:
                    sent_part = source_of + sent.split(the_source_of)[1]
                    regex = r"^" + re.escape(ent.lower())
                    sent_part = sent_part.lower()
                    the_sent_part = first_pattern + " " + sent_part.lower()
                    if re.match(regex, sent_part) or re.match(regex, the_sent_part):
                        print(ent, row)
                        count_match += 1
                        break
            else:
                writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5]])
                count_cand += 1
