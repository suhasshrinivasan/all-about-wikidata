from utils import HTTPRequest, log
import re
import pickle

class Qids:
    """
    Class for retrieving, storing and managing QIDs using
    sparql queries. 
    QIDs are unique entity identifiers in the Wikidata knowledge base.
    QIDS of some popular entities:
    1. Cristiano Ronaldo - Q11571
    2. COVID 19 - Q84263196
    3. Germany - Q183
    """
    def __init__(self):
        self.qids = []
        self.entity_count = 0
        self.sparql_query = ''
        self.count_query = ''
        self.log_fname = ''
        self.__sparql_endpoint_url = 'https://query.wikidata.org/sparql' 
        self.__sparql_response = None
        self.__count_response = None
        self.__http_request_sparql = HTTPRequest(self.__sparql_endpoint_url)

    def retrieve_qids(self, sparql_fname, log_fname):
        """
        This method expects a sparql filename that contains a valid sparql query,
        specifying wikidata Entities of Interest.
        The sparql query is then submitted to the Wikidata sparql endpoint
        at https://query.wikidata.org/sparql. 
        The method extracts all returned QIDs from the response, storing them in the list self.qids.
        The sparql endpoint does not always return all Entities of Interest as specified by the sparql
        query, frequently due to timeout exceptions. This method hence also submits an 
        automatically generated count query that counts the total number of Entities of Interest
        and stores the count in self.entity_count.
        """
        with open(sparql_fname, 'r') as f:
            self.sparql_query = f.read()
        self.log_fname = log_fname
        # send http request to sparql endpoint
        self.__sparql_response = self.__http_request_sparql.get(
            url=self.__sparql_endpoint_url,
            params={
                'query': self.sparql_query
            },
            headers={
                'Accept': 'application/sparql-results+json'
            },
            exc_fname=log_fname,    # for logging purposes
            timeout=300,
            raw=True    # to only return raw http response
        )
        # extract all the QIDs from the http response
        self.qids = self.__extract_qids()
        # automatically generate count query from sparql query
        self.count_query = re.sub(r'\?item', '(COUNT(?item) AS ?count)', self.sparql_query, count=1)
        # send count query to sparql endpoint 
        self.__count_response = self.__http_request_sparql.get(
            url=self.__sparql_endpoint_url,
            params={
                'query': self.count_query
            },
            headers={
                'Accept': 'application/sparql-results+json'
            },
            exc_fname=log_fname,
            raw=False
        )
        # extract the count from count query response
        self.entity_count = self.__extract_count()
        return

    def save(self, qids_fname):
        """
        This methods writes the retrieved QIDs to file.
        """
        with open(qids_fname, 'wb') as f:
            pickle.dump(self.qids, f)

    def __extract_qids(self):
        """
        This method extracts QIDs from sparql response.
        """
        try:
            qids = []
            result_list = self.__sparql_response.json()['results']['bindings']
            for result in result_list:
                uri = result['item']['value']
                qid = uri.split('/')[-1]
                qids.append(qid)
        except:
            """
            Timeout exceptions are frequent which garble the response.
            In such cases, QIDs from the response need to be scraped.
            """
            uri_regex = r"http\:\/\/www.wikidata.org\/entity\/Q[0-9]*"
            uris = re.findall(uri_regex, self.__sparql_response.text)
            qids = [uri.split('/')[-1] for uri in uris]
        return qids

    def __extract_count(self):
        """
        This method extracts the count from a count query response.
        """
        try:
            entity_count = int(self.__count_response['results']['bindings'][0]['count']['value'])
        except Exception as e:
            log(e, self.__count_response, self.log_fname)
            entity_count = -1
        return entity_count