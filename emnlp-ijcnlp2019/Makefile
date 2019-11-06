

statistics.md: statistics.org
	pandoc --from org --to markdown+pipe_tables-simple_tables-fenced_code_attributes statistics.org --output=statistics.md

vossantos.md: README.org
	../theof/org.py -g -H -T README.org | pandoc --from org --to markdown --output=vossantos.md
