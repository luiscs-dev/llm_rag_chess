from openai import OpenAI
from elasticsearch import Elasticsearch
import time
import json 

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
    start_time = time.time()
    response = client.chat.completions.create(
        model='phi3',
        messages=[{"role": "user", "content": prompt}]
    )
    
    answer = response.choices[0].message.content
    tokens = {
            'prompt_tokens': response.usage.prompt_tokens,
            'completion_tokens': response.usage.completion_tokens,
            'total_tokens': response.usage.total_tokens
    }
    end_time = time.time()
    response_time = end_time - start_time

    return answer, tokens, response_time

def evaluate_relevance(question, answer):
    prompt_template = """
    You are an expert evaluator for a Retrieval-Augmented Generation (RAG) system.
    Your task is to analyze the relevance of the generated answer to the given question.
    Based on the relevance of the generated answer, you will classify it
    as "NON_RELEVANT", "PARTLY_RELEVANT", or "RELEVANT".

    Here is the data for evaluation:

    Question: {question}
    Generated Answer: {answer}

    Please analyze the content and context of the generated answer in relation to the question
    and provide your evaluation in parsable JSON without using code blocks:

    {{
      "Relevance": "NON_RELEVANT" | "PARTLY_RELEVANT" | "RELEVANT",
      "Explanation": "[Provide a brief explanation for your evaluation]"
    }}
    """.strip()

    prompt = prompt_template.format(question=question, answer=answer)
    evaluation, tokens, _ = llm(prompt)
    
    try:
        json_eval = json.loads(evaluation)
        return json_eval['Relevance'], json_eval['Explanation'], tokens
    except json.JSONDecodeError:
        return "UNKNOWN", "Failed to parse evaluation", tokens


def rag(query):
    results = elastic_search(query)
    prompt = build_prompt(query, results[:5])
    print(prompt)
    print('//////////')
    answer, tokens, response_time = llm(prompt)
    relevance, explanation, eval_tokens = evaluate_relevance(query, answer)

    return {
        'answer': answer,
        'response_time': response_time,
        'relevance': relevance,
        'relevance_explanation': explanation,
        'model_used': "ollama",
        'prompt_tokens': tokens['prompt_tokens'],
        'completion_tokens': tokens['completion_tokens'],
        'total_tokens': tokens['total_tokens'],
        'eval_prompt_tokens': eval_tokens['prompt_tokens'],
        'eval_completion_tokens': eval_tokens['completion_tokens'],
        'eval_total_tokens': eval_tokens['total_tokens']
    }