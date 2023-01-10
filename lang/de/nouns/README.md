# List of German Nouns
## About
This dataset provides a list of German nouns with their nominative singular and plural forms.

The list is derived from the [German Wiktionary](https://de.wiktionary.org/wiki/Wiktionary:Hauptseite) using a triple
store data dump provided by the [Dbnary](http://kaiko.getalp.org/about-dbnary/) project.

## Data files

* [release/de-nouns-dump.txt](release/de-nouns-dump.txt) - list of German nouns.
  
  Format: `<singular>,<plural>`

  Note that a noun might not have a singular or a plural form.
* [release/de-nouns.txt](release/de-nouns.txt) - list of German nouns after removing nouns that are maintained on the
  [input/de-nouns-del.txt](input/de-nouns-del.txt) exclusion list. Background: the list has been created with an
  application in mind that finds a canonical word form (usually the nominative singular form) in the list. 
  This can sometimes not be done easily as the same word form can be the plural form of one singular-plural pair and
  at the same time the singular form of the other. For example, `Feste` can be the plural of `Fest` (_celebration_). But
  it can also be the singular in the singular/plural pair `Feste/Festen`, meaning _fortress_ so that looking up  
  `Feste` in the word list brings up more than one item and makes deciding upon the canonical form difficult. In this 
  specific case, the pair `Feste/Festen` is hardly used in current day German and we this simply remove it from the list
  via putting it on the `de-nouns-del.txt` exclusion list.

### Building the data files
Follow these steps to build the data files yourself:
1) Clone or download this project
2) Download the triple store files `de_dbnary_ontolex.ttl` and `de_dbnary_morphology.ttl` from Dbnary
   [http://kaiko.getalp.org/static/ontolex/latest/](http://kaiko.getalp.org/static/ontolex/latest/) and unzip them into 
   [input/dbnary](input/dbnary).
3) `cd scripts`
4) Install required Python libraries via `pip install -r requirements.txt`
5) Run `python build.py` - This might run for ca. 60 mins. You will find the generated files in the `release` folder.

### Contributing to the exclusion list
Just provide a pull request for file [input/de-nouns-del.txt](input/de-nouns-del.txt). Please make sure you keep the
entries in alphabetical order and also provide an explanation why you want to modify the list.

## License
The List of German Nouns is derived from files provided by the [Dbnary](http://kaiko.getalp.org/about-dbnary/) project,
which in turn are derived from the [German Wiktionary](https://de.wiktionary.org/wiki/Wiktionary:Hauptseite). The List
of German Nouns dataset is made available by the maintainers of the Querqy Datasets project under the Creative Commons
Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0) -
see [https://creativecommons.org/licenses/by-sa/4.0/](https://creativecommons.org/licenses/by-sa/4.0/).

The tools for creating and maintaining this dataset are made available by the maintainers of the Querqy Datasets project
under the Apache License, Version 2
(see [https://www.apache.org/licenses/LICENSE-2.0](https://www.apache.org/licenses/LICENSE-2.0))


