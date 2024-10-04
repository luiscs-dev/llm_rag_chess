import os
from dotenv import load_dotenv
from db_utils import init_db
import chess 
import chess.pgn
import io
import chardet
from elasticsearch import Elasticsearch

load_dotenv()

def get_chess_games():
    with open('../data/lichess_db.pgn') as f:
        lines = f.read().strip().split("\n\n")

    games = list()

    i=0
    while (i < len(lines)-1):
        games.append(f'{lines[i]} \n{lines[i+1]}')
        i += 2

    docs = list()
    bads = list()
    # Parse each game
    for game_text in games[:2000]:
        try:
            pgn = chess.pgn.read_game(io.StringIO(game_text))
            headers = pgn.headers
            #moves = [move for move in pgn.mainline_moves()]

            data = {
                "event": headers['Event'],
                "site": headers['Site'],
                "white": headers['White'],
                "black": headers['Black'],
                "result": headers['Result'],
                "utc_date": headers['UTCDate'],
                "utc_time": headers['UTCTime'],
                "white_elo": headers['WhiteElo'],
                "black_elo": headers['BlackElo'],
                "eco": headers['ECO'],
                "opening": headers['Opening'],
                "time_control": headers['TimeControl'],
                "termination": headers['Termination'],
                "moves": str(pgn.mainline_moves()).replace('\n', ' ')
            }
            docs.append(data)
        except:
            bads.append(game_text)

    return docs

def load_docs_in_elasticsearch(docs):
    es_client = Elasticsearch(os.getenv("ELASTIC_URL_LOCAL", "http://localhost:9200"))
    index_name = os.getenv("INDEX_NAME", "chess-rag")
    es_client.options(ignore_status=[400,404]).indices.delete(index=index_name)
    
    index_settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "moves": {"type": "text"},
                "white_player": {"type": "text"},
                "black_player": {"type": "text"},
                "white_elo": {"type": "text"},
                "black_elo": {"type": "text"},
                "event": {"type": "text"},
                "result": {"type": "text"},
                "opening": {"type": "keyword"} 
            }
        }
    }
    es_client.indices.create(index=index_name, body=index_settings)

    for doc in docs:
        new_doc = {
            "moves": doc["moves"],
            "white_player": doc["white"],
            "black_player": doc["black"],
            "white_elo": doc["white_elo"],
            "black_elo": doc["black_elo"],
            "event": doc["event"],
            "result": doc["result"],
            "opening": doc["opening"]
        }
        es_client.index(index=index_name, document=new_doc)

if __name__ == "__main__":
    print("Initializing database...")
    init_db()

    print("Extracting info from data/lichess_db.pgn...")
    load_docs_in_elasticsearch(get_chess_games())
