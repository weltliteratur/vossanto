# author: ms
# takes a filtered version and removes all candidates where source+ following words are an entity in wikidata

import csv
import re
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Find entries matching humans.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("phrases", type=str, help="output from theof.py")
    parser.add_argument("entities", type=str, help="Wikidata entities")
    parser.add_argument(
        "-o", "--output", type=str, help="output tsv file", default=None
    )

    args = parser.parse_args()
    with open(args.phrases, "r") as candidate_file, open(
        args.entities, "r"
    ) as entity_file, open(args.output, "w") as output_file:
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
            first_pattern = source.split()[0]
            second_pattern = source.split()[len(source.split()) - 1]
            pattern = first_pattern + "_" + second_pattern
            # creates a list with all entities from wikidata where the source appears
            entity_list = [
                line[1].strip().lower()
                for line in entity_reader_list
                if len(line) >= 2 and source in line[1].strip().lower()
            ]
            # no match
            if entity_list == []:
                writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5]])
                count_cand += 1
            else:
                i = 0
                # checks if the entity candidate is fully appearing in the sentence.
                for ent in entity_list:

                    i += 1
                    the_source_of = source
                    source_of = " ".join(source.split()[1:])
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
