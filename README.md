# Wikidata Toolkit

Welcome to my Wikidata toolkit repository. This project contains a bunch of high-level classes and methods written in Python that help programmers deal with querying, storing and manipulating data from the Wikidata knowledge base (and also Wikipedia). 

## Usage

Simply clone the repository to get started.

### Retrieving QIDs of entities in Wikidata using SPARQL

Each entity (called item) in Wikidata has a persistent, unique identifier called a QID. For example, QID of Cristiano Ronaldo is ```Q11571```. Read more about QIDs and in general about data access in Wikidata [here](https://www.wikidata.org/wiki/Wikidata:Data_access#Per-item_access_to_data). Data in RDF knowledge bases are queried using a query language like SPARQL. Explore querying Wikidata by SPARQL using the Wikidata Query Service [here](https://query.wikidata.org/). 

Given a valid SPARQL query that retrieves QIDs, ```wikidata-toolkit/qids.py``` provides the class Qid that can retrieve, store and manage QIDs specified by the SPARQL query. As an example, let us use the Qid class to retrieve QIDs of all Cats in Wikidata:
```python
from qids import Qids

# first create a Qids object
cats = Qids()

# we can use the retrieve_qids method in Qids to retrieve QIDs.
# it expects us to provide two arguments - 
# sparql_fname - location of file that contains a valid SPARQL query (in our case - cats.sparql)
# log_fname - a file to use for logging in case of exceptions.
sparql_fname = 'cats.sparql'
log_fname = 'cats_log.txt'

# we can now call the retrieve_qids method.
# note that this method sends an HTTP request to the Wikidata SPARQL endpoint to retrieve QIDs so it may take a while.
cats.retrieve_qids(sparql_fname, log_fname)

# the resulting QIDs are stored in the qids member (a list) of Qid that can be directly accessed
qids_of_cats = cats.qids

# save the qids as a pickle using the save method
qids_fname = 'cats_qids.pickle'
cats.save(qids_fname)
```

Why query QIDs? As mentioned before, QIDs are unique identifiers of entities in Wikidata. You can make a deferenceable URI by appending a QID to the Wikidata concept namespace ```http://www.wikidata.org/entity/``` in order to access data on the entity that the QID represents. As an example, checkout http://www.wikidata.org/entity/Q11571. 

Want to retrieve European premier league football players or actors born in the US? Try them out using ```wikidata-toolkit/premleague.sparql``` and ```wikidata-toolkit/actors.sparql```. You can learn how to write custom SPARQL queries using the [Wikidata SPARQL tutorial](https://www.wikidata.org/wiki/Wikidata:SPARQL_tutorial).

## Project status

This is a WIP!
