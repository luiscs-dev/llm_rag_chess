## Grafana queries

Answer relevance from user's perspective:

```sql
SELECT
  SUM(CASE WHEN feedback = 1 THEN 1 ELSE 0 END) as thumbs_up,
  SUM(CASE WHEN feedback = -1 THEN 1 ELSE 0 END) as thumbs_down
FROM feedback
```

Relevance of LLM answers:

```sql
SELECT
  relevance,
  COUNT(*) as count
FROM conversations
GROUP BY relevance
```

Prompt Token Usage:

```sql
SELECT
  timestamp AS time,
  prompt_tokens,
  completion_tokens,
  total_tokens
FROM conversations
ORDER BY timestamp
```

Evaluation Token Usage:

```sql
SELECT
  timestamp AS time,
  eval_prompt_tokens,
  eval_completion_tokens,
  eval_total_tokens
FROM conversations
ORDER BY timestamp
```

RAG response time (sec):

```sql
SELECT
  timestamp AS time,
  response_time
FROM conversations
ORDER BY timestamp
```

Last conversations:

```sql
SELECT
  timestamp AS time,
  question,
  answer,
  relevance
FROM conversations
ORDER BY timestamp DESC
LIMIT 5
```