#
# SPDX-License-Identifier: Apache-2.0
#
from io import StringIO
from rdflib import Graph
import pandas as pd
from datetime import datetime

DUMP_FILE = '../release/de-nouns-dump.txt'
DATASET_FILE = '../release/de-nouns.txt'
DELETIONS_FILE = '../input/de-nouns-del.txt'

# License for released artefacts:

LICENSE = """# This file is provided by the Querqy Datasets project (https://github.com/querqy/datasets) under the
#
#     Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0)
#     (https://creativecommons.org/licenses/by-sa/4.0/).
#     
# SPDX-License-Identifier: CC-BY-4.0
# 
# It is derived from a dataset provided by Dbnary (http://kaiko.getalp.org/about-dbnary/),
# which in turn was derived from Wiktionary (https://www.wiktionary.org).
#
"""


def create_graph(lex_entry_file: str = '../input/dbnary/de_dbnary_ontolex.ttl',
                 morphology_file: str = '../input/dbnary/de_dbnary_morphology.ttl') -> Graph:

    print('Importing triple store - this might take ca. 60 minutes.', datetime.now())
    g = Graph(store="Oxigraph")
    print('  Importing lexical entries')
    g.parse(lex_entry_file)
    print('  Done. Importing morpology')
    g.parse(morphology_file)
    print('Done.', datetime.now())

    g.commit()

    return g


QUERY = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX ontolex: <http://www.w3.org/ns/lemon/ontolex#>
    PREFIX olia: <http://purl.org/olia/olia.owl#>
    PREFIX lexinfo:  <http://www.lexinfo.net/ontology/2.0/lexinfo#>

    SELECT ?nom_sg ?nom_pl
    WHERE {
        ?word 
            a lexinfo:Noun ;
            ontolex:otherForm ?f_nom_pl ;
            ontolex:otherForm ?f_nom_sg .
            
        ?f_nom_pl rdf:type ontolex:Form ;
            olia:hasCase olia:Nominative ;
            olia:hasNumber      olia:Plural ;
            ontolex:writtenRep ?nom_pl .
           
        
        ?f_nom_sg rdf:type ontolex:Form ;
            olia:hasCase olia:Nominative ;
            olia:hasNumber      olia:Singular ;
            ontolex:writtenRep ?nom_sg .
       
    } 
    GROUP BY ?nom_sg ?nom_pl
    
"""


def extract_sg_pl(graph: Graph) -> pd.DataFrame:
    df = pd.DataFrame([row for row in graph.query(QUERY)], columns =['sg', 'pl'])
    # remove det and lowercase
    df['sg'] = df.sg.apply(lambda x: None if ((x is None) or (x[:4] not in ['der ', 'die ', 'das ']))
                                                else x[4:].lower())
    df['pl'] = df.pl.apply(lambda x: None if ((x is None) or (x[:4] not in ['der ', 'die ', 'das ']))
                                                else x[4:].lower())
    # remove all None entries
    df = df[-(df['sg'].isna() & df['pl'].isna())]
    # remove all where there still is a space in the word
    df = df[df['sg'].apply(lambda x: (x is None) or (' ' not in x)) & df['pl']
                                                                        .apply(lambda x: (x is None) or (' ' not in x))]

    # deduplicate, make it nice and stable
    return df.sort_values(by=['sg', 'pl']).copy().drop_duplicates(subset=['sg', 'pl'])


def preprocess_dump():
    g = create_graph()
    df_dump = extract_sg_pl(g)
    with open(DUMP_FILE, 'w') as f:
        f.write(LICENSE)
        df_dump.to_csv(f, index=False, header=False)
    g.close()


def strip_line(line):
    pos = line.find('#')
    if pos > -1:
        line = line[:pos].strip()

    return line.strip()


def read_pairs_to_remove():
    # post-process
    with open(DELETIONS_FILE, 'r') as f:
        for line in [line.lower() for line in [strip_line(line) for line in f.readlines()] if len(line) > 0]:
            sep = line.find(',')
            sg, pl = line[:sep].strip(), line[sep + 1:].strip()
            yield None if len(sg) == 0 else sg, None if len(pl) == 0 else pl


def remove_unwanted_pairs(df_all: pd.DataFrame, df_del: pd.DataFrame):

    df_tmp = df_all.merge(df_del, on=['sg', 'pl'], how='left', indicator=True)
    return df_tmp[df_tmp['_merge'] != 'both'][['sg', 'pl']].copy().sort_values(by=['sg','pl'])


def post_process():
    df_del = pd.DataFrame([pair for pair in read_pairs_to_remove()], columns=['sg', 'pl']).drop_duplicates()
    with open(DUMP_FILE, 'r') as f:
        lines = [line for line in f.readlines() if not line.startswith('#')]
        df_dump = pd.read_csv(StringIO("\n".join(lines)), header=None, names=['sg', 'pl'])
        df_dump = df_dump.where(pd.notnull(df_dump), None)

        df_release = remove_unwanted_pairs(df_dump, df_del)
        with open(DATASET_FILE, 'w') as f:
            f.write(LICENSE)
            df_release.to_csv(f, index=False, header=False)


preprocess_dump()
post_process()
