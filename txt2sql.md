[SkyRL-SQL: Matching GPT-4o and o4-mini on Text2SQL with Multi-Turn RL](https://novasky-ai.notion.site/skyrl-sql)

In this post, we share early results on enabling multi-turn reinforcement learning (RL) for Text-to-SQL, where we teach an LLM to iteratively build and refine SQL queries using feedback from databases. We introduce a simple, data-efficient, and scalable multi-turn RL training pipeline for Text-to-SQL task, built on top of VeRL and SearchR1.

[sql_llm_app](https://github.com/jngk07/databaseQueryUsingLangChain/blob/main/sql_llm_app.py)

How to deal with Large databases when doing SQL Q & A Langchain vs MCP Approach

[anyquery](https://github.com/julien040/anyquery)

Anyquery is a SQL query engine that allows you to run SQL queries on pretty much anything. It supports querying files, databases, and apps (e.g. Apple Notes, Notion, Chrome, Todoist, etc.). It's built on top of SQLite and uses plugins to extend its functionality.


[Beyond Text-to-SQL: Semantic Layers for AI Agents Explained](https://aipractitioner.substack.com/p/beyond-text-to-sql-semantic-layers)

<img width="721" height="319" alt="Screenshot 2026-11-28 at 2 56 32 PM" src="https://github.com/user-attachments/assets/4859a9c6-8fca-40fe-99ba-79cae1eb5a97" />

Rather than generating SQL, the agent selects the appropriate metric, dimensions, and filters.

A simplified request could look like this:

```
{
  "metric": "net_revenue_per_order",
  "filters": [
    {
      "dimension": "country",
      "equals": "Germany"
    }
  ],
  "time_range": "last_quarter"
}
```

### Compile the request into SQL.

The semantic layer translates the structured request into SQL using the previously defined business logic.

For example, assuming that net_amount already represents the governed definition of net revenue:

```
-- Calculate net revenue per distinct order.
SELECT
    SUM(o.net_amount) /
    COUNT(DISTINCT o.order_id) AS net_revenue_per_order
FROM orders AS o
WHERE o.country = 'Germany'
    -- Previous calendar quarter as of November 2026.
    AND o.order_date >= DATE '2026-07-01'
    AND o.order_date < DATE '2026-10-01';
```

<img width="742" height="287" alt="Screenshot 2026-11-28 at 3 03 15 PM" src="https://github.com/user-attachments/assets/2f41178f-bbad-44eb-becd-3e793460f970" />


