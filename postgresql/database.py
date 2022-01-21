import psycopg2
import psycopg2.extras

class database:
    '''
    Mediator Design Pattern
    database class functions as mediator to control all execution function for all tables
    database class rely on one connection from psycogn2
    '''


    def __init__(self):
        self.conn = psycopg2.connect("host='129.158.55.161' port='5432' dbname='claim' user='lei' password='nlp'")
        self.cursor = self.conn.cursor()

    def load_data(self):
        '''

        read tsv and qrels data from both train and test

        import tsv and qrels data to database claim
        '''

        # train pair
        train_pairs_grels = open('../data/v3.0/train/tweet-vclaim-pairs.qrels', encoding='utf-8').read()
        train_pairs = train_pairs_grels.splitlines()
        train_pairs = [(pair.split('\t')[0], pair.split('\t')[2]) for pair in train_pairs] # remove redundant format in qrels
        insert_query = 'insert into train_pairs (tweet_id, vclaim_id) values %s'
        psycopg2.extras.execute_values (
            self.cursor, insert_query, train_pairs
        )

        # dev pair
        dev_pairs_grels = open('../data/v3.0/dev/tweet-vclaim-pairs.qrels', encoding='utf-8').read()
        dev_pairs = train_pairs_grels.splitlines()
        dev_pairs = [(pair.split('\t')[0], pair.split('\t')[2]) for pair in dev_pairs] # remove redundant format in qrels
        insert_query = 'insert into dev_pairs (tweet_id, vclaim_id) values %s'
        psycopg2.extras.execute_values (
            self.cursor, insert_query, dev_pairs
        )

        # train tweets
        tweets_tsv = open('../data/v3.0/train/tweets.queries.tsv', encoding='utf-8')
        next(tweets_tsv) # get rid of headers
        self.cursor.copy_from(tweets_tsv, 'tweets')
        tweets_tsv.close()

        # dev tweets
        tweets_tsv = open('../data/v3.0/dev/tweets.queries.tsv', encoding='utf-8')
        next(tweets_tsv) # get rid of headers
        self.cursor.copy_from(tweets_tsv, 'tweets')
        tweets_tsv.close()

        # vclaims
        vclaims_tsv = open('../data/v3.0/verified_claims.docs.tsv', encoding='utf-8')
        next(vclaims_tsv) # get rid of headers
        self.cursor.copy_from(vclaims_tsv, 'claims')
        vclaims_tsv.close()

        self.conn.commit()


if __name__ == '__main__':
    db = database()
    db.load_data()

