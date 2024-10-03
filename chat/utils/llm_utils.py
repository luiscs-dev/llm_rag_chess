from openai import OpenAI
from elasticsearch import Elasticsearch

index_name = "chess-rag" 
client = None
es_client = None

if es_client == None: 
    #es_client = Elasticsearch('http://localhost:9200')
    es_client = Elasticsearch('http://host.docker.internal:9200')
    #es_client = Elasticsearch('http://elasticsearch:9200')
    
if client == None: 
    client = OpenAI(
        #base_url='http://localhost:11434/v1/',
        base_url='http://ollama:11434/v1/',
        api_key='ollama',
    )

def get_prompt(version='v1'):
    with open(f"utils/prompts/prompt_{version}.txt") as f:
        content_file = f.read().strip()

    return content_file
    
def build_prompt(query, search_results):
    prompt_template = get_prompt(version='v5')
    
    context = ""
    
    for doc in search_results:
        context += f"{{moves: {doc['moves']}\n"
        context += f"opening: {doc['opening']}\n"
        context += f"match result: {doc['result']}\n"
        context += f"white_player: {doc['white_player']}\n"
        context += f"black_player: {doc['black_player']}\n"
        context += f"white_elo: {doc['white_elo']}\n"
        context += f"black_elo: {doc['black_elo']}\n}}\n"
    
    #games = [
    #    f"{i}. Opening {'opening'} Match result: {game['result']} Match moves:{game['moves']}"
    #    for i, game in enumerate(search_results,1)
    #]
    #context = "\n".join(games)

    prompt=prompt_template.format(question=query, context=context).strip()

    return prompt

def elastic_search(query):
    search_query = {
        "size": 5,
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": query,
                        "fields": ["moves^3", "opening"],
                        "type": "best_fields"
                    }
                }
            }
        }
    }

    r = es_client.search(index=index_name, body=search_query)

    results = []
    
    for hit in r['hits']['hits']:
        results.append(hit['_source'])

    return results

def llm(prompt):
    response = client.chat.completions.create(
        model='phi3',
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

def rag(query):
    results = elastic_search(query)
    prompt = build_prompt(query, results[:5])
    print(prompt)
    print('//////////')
    answer = llm(prompt)

    return answer