# Vossian Antonomasia

*Frank Fischer, Robert Jäschke, Elena Krotova, Michel Schwab, Jannik Strötgen*

Automatic extraction of Vossian antonomasia (VA) from large newspaper
corpora. Based on an idea by [Frank Fischer](https://twitter.com/umblaetterer)
(see *[Der Umblätterer](http://www.umblaetterer.de/datenzentrum/vossianische-antonomasien.html)*).

**Vossian antonomasia** is a stylistic device which attributes a
certain property to a person by naming another (more well-known, more
popular) person as a reference point. For instance, when <span
style='color:blue;'>Jim Koch</span> is described as "<a
href='https://www.theatlantic.com/magazine/archive/2014/11/the-steve-jobs-of-beer/380790/)'>the
<span style='color:red'>Steve Jobs</span> of <span
style='color:darkgreen'>Beer</span></a>", certain qualities of Steve
Jobs, be it entrepreneurship or persuasiveness, are assigned to Jim
Koch, co-founder and chairman of the Boston Beer Company.  VAs consist
of three parts: a <span style='color:red;'>source</span> (in our
example "Steve Jobs") serves as paragon to elevate the <span
style='color:blue;'>target</span> ("Jim Koch") by applying a <span
style='color:darkgreen;'>modifier</span> ("of Beer") that provides the
corresponding context.  VA is named after [Gerardus
Vossius](https://en.wikipedia.org/wiki/Gerardus_Vossius) (1577– 1649),
the Dutch classical scholar and author of rhetorical textbooks, who
first distinguished and described VA as a separate phenomenon.


## ICNLSP (2022)
Schwab, M., Jäschke, R., Fischer, F.: “Der Frank Sinatra der
Wettervorhersage”: Cross-Lingual Vossian Antonomasia Extraction [Link
tba]

- [Data and Code](https://github.com/weltliteratur/vossanto/tree/master/icnlsp2022)


## Frontiers in Artificial Intelligence (2022)
Schwab, M., Jäschke, R., Fischer, F.: "The Rodney Dangerfield of Stylistic Devices":
End-to-End Detection and Extraction of
Vossian Antonomasia Using Neural Networks.
(DOI:[10.3389/frai.2022.868249](https://doi.org/10.3389/frai.2022.868249),
[PDF](https://www.frontiersin.org/articles/10.3389/frai.2022.868249/abstract),
[BibTeX](https://www.bibsonomy.org/bib/publication/2ec528a4b293f3ddc9582fcdeed6c6f9/jaeschke))

- [Data](https://github.com/weltliteratur/vossanto/tree/master/frontiers)

## EMNLP-IJCNLP 2019 (November, 2019)
Schwab, M., Jäschke, R., Fischer, F., Strötgen, J.: 'A Buster Keaton
of Linguistics': First Automated Approaches for the Extraction of
Vossian Antonomasia. *Proceedings of the 2019 Conference on Empirical
Methods in Natural Language Processing and the 9th International Joint
Conference on Natural Language Processing*. pp. 6239–6244. Association
for Computational
Linguistics 2019. (DOI:[10.18653/v1/D19-1647](https://doi.org/10.18653/v1/D19-1647),
[PDF](https://www.aclweb.org/anthology/D19-1647.pdf),
[BibTeX](https://www.bibsonomy.org/bib/bibtex/25d30fd8911ded13edd4c0f07bd73e624/jaeschke),
[Poster](https://doi.org/10.6084/m9.figshare.10069886))

- [Timeline](timeline) (**recommended**)
- [Data and Code](https://github.com/weltliteratur/vossanto/tree/master/emnlp-ijcnlp2019)
- [Some Statistics](emnlp-ijcnlp2019/statistics.md)
- [All found VA](emnlp-ijcnlp2019/vossantos.md)

## DSH Paper (January, 2019)
Fischer, F., Jäschke, R.: ‘The Michael Jordan of greatness’—Extracting
Vossian antonomasia from two decades of The New York Times,
1987–2007. *Digital Scholarship in the Humanities*. 2019.
(DOI:[10.1093/llc/fqy087](https://doi.org/10.1093/llc/fqy087),
Preprint: [arXiv:1902.06428](https://arxiv.org/abs/1902.06428))

- [Some More Statistics](theof/humans/statistics.md) (**recommended**)
- [Complete List of Extracted VA](theof/humans/vossantos.md) (**recommended**)
- [Twitter thread](https://twitter.com/umblaetterer/status/1097865223564869635)

## TheOf Approach (2017–2019)
- [Poster *Lange Nacht der Wissenschaften*](https://doi.org/10.6084%2fm9.figshare.6531140) (June, 2018)
- [Data and Code](https://github.com/weltliteratur/vossanto/tree/master/theof)

## First Approach (February, 2017)
- [Slides DHd 2017, Bern](https://lehkost.github.io/slides/2017-bern/) (in German)
- [Abstract DHd 2017, Bern](http://www.dhd2017.ch/wp-content/uploads/2017/02/Abstractband_ergaenzt.pdf#page=122) (in German)
- [Data and Code](first)


## Further Ressources

- [a bibliography of related publications](https://www.bibsonomy.org/user/jaeschke/vossanto)
- [a poster about a Vossanto memory game](https://doi.org/10.6084/m9.figshare.6531140) (in German)
- [VA detection model on HuggingFace](https://huggingface.co/mschwab/va_bert_classification)
# va_source_target_graph
