from qids import Qids
cats = Qids()

sparql_fname = 'cats.sparql'
log_fname = 'cats_qids_log.txt'
cats.retrieve_qids(sparql_fname, log_fname)

print(len(cats.qids))
print(cats.entity_count)

cats.save('cats_qids.pickle')

