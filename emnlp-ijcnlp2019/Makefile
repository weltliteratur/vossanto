

statistics.md: statistics.org
	pandoc --from org --to markdown+pipe_tables-simple_tables-fenced_code_attributes statistics.org --output=statistics.md

vossantos.md: README.org
	../org.py -T -H -f original README.org | pandoc --from org --to markdown --output=vossantos.md
