# RAG, Vector Databases, Hallucination, and Temperature

Interview answers with a real-life example: a company HR chatbot that answers questions from the employee handbook.

## Questions

1. [What is meant by RAG?](#what-is-rag)
2. [What is meant by a vector database?](#what-is-a-vector-database)
3. [What problems do you get with RAG and without RAG?](#problems-with-and-without-rag)
4. [What is hallucination, and how do you prevent it?](#what-is-hallucination)
5. [What is temperature in a model, and how does it improve the answer?](#what-is-temperature)

---

<a id="what-is-rag"></a>

## 1. What is meant by RAG?

**RAG** stands for **Retrieval-Augmented Generation**.

A normal LLM (Large Language Model) answers only from what it learned during training. That knowledge is frozen at training time, and the model has no access to your private documents.

RAG adds a lookup step **before** the model writes the answer:

1. The user asks a question.
2. The system **retrieves** the most relevant chunks from your own documents (handbook, wiki, tickets, PDFs).
3. Those chunks are attached to the prompt as context.
4. The LLM **generates** an answer grounded in that retrieved text.

```
User question
    |
    v
Retrieve relevant chunks  <-- your documents, stored as embeddings
    |
    v
Prompt = question + retrieved chunks
    |
    v
LLM generates the answer
```

**Real-life example**

An employee asks: *"How many paid sick days do I get in India?"*

- **Without RAG:** the model guesses from general internet knowledge and may say "10 days" because that is a common number it has seen.
- **With RAG:** the system finds the India leave-policy page, which says "12 paid sick days per year, unused days do not carry forward," and the model answers from that page.

RAG does not retrain the model. It gives the model the right pages to read at answer time, the same way you would hand a colleague the policy PDF before asking them to reply.

---

<a id="what-is-a-vector-database"></a>

## 2. What is meant by a vector database?

A **vector database** stores text (or images, audio) as **embeddings**: lists of numbers that capture meaning.

Two sentences with similar meaning end up as nearby points in that number space, even when they do not share the same words.

| Sentence | Why they match |
| --- | --- |
| "How many sick leaves do I get?" | Same intent |
| "What is the paid medical leave entitlement?" | Different words, same meaning |

A normal SQL database finds rows with `WHERE text LIKE '%sick%'`. It misses the second sentence because the word "sick" is not there.

A vector database finds both, because it searches by **meaning** (nearest neighbors), not by exact keywords.

### Why a vector database instead of a traditional database

Imagine walking into a massive library.

A **traditional database** is like a strict librarian with a rigid card catalog. They only understand exact spelling and literal text. If you ask for a book on "auto repair," they hand you books that contain the exact phrase "auto repair." If a book is titled "Fixing your car engine," they miss it and say they do not have it, because the words do not match.

A **vector database** is like an expert librarian who understands meaning and context. If you ask for "auto repair," they hand you books on fixing car engines, changing tires, and vehicle maintenance, because those ideas mean the same thing even when the words are different.

### Real-world scenario: e-commerce search

You run an online clothing store. A customer types a natural-language query:

> "I need a cozy outfit to keep me warm during a freezing snowstorm."

**How a traditional database (SQL/NoSQL) handles it**

It looks for exact keyword matches in product columns such as title and description. It searches for rows containing "cozy," "outfit," "warm," and "snowstorm."

Result: it can return **0 products**, because the catalog titles are "Heavy fleece wool sweater" and "Thermal winter parka." None of those titles contain the words the customer typed. The customer leaves empty-handed.

**How a vector database handles it**

It matches **semantic similarity** (meaning), not spelling.

1. **Embedding conversion.** The search phrase is turned into a vector: a list of numbers that represents the idea "clothing for extreme cold."
2. **Proximity matching.** Every product description was converted into a vector ahead of time and placed in that same space.
3. **Result.** "Heavy fleece wool sweater" and "Thermal winter parka" sit next to "freezing snowstorm clothing," so both are returned even though the words do not overlap.

### When to use which

| Feature | Traditional database (SQL) | Vector database |
| --- | --- | --- |
| How it thinks | "Do these exact characters match?" | "Do these concepts mean the same thing?" |
| Best used for | User accounts, exact lookups, financial transactions, inventory counts | AI chatbots, RAG context retrieval, semantic search, intelligent recommendations |

Use both together in most products. SQL stores the order, the price, and the stock count. The vector database finds the products or document chunks whose meaning matches the question.

### How a chunk gets stored

1. Split the handbook into chunks (for example, one section or ~500 tokens).
2. Send each chunk through an embedding model. Output is a vector, for example 1536 numbers.
3. Store the vector plus the original text and metadata (document name, page, country, last updated date).
4. At query time, embed the user's question the same way and return the closest chunks.

**HR bot example**

The HR bot stores:

- `leave-policy-india.pdf` → chunk: "Employees in India receive 12 paid sick days..."
- `leave-policy-us.pdf` → chunk: "US employees receive 8 paid sick days..."

The question *"sick leave in Bangalore office"* embeds close to the India chunk, so that chunk is retrieved. The US chunk is farther away and is not used.

Vector databases used in production include Pinecone, Weaviate, Milvus, Qdrant, pgvector (Postgres), and Chroma. The idea is the same: store embeddings and run similarity search.

---

<a id="problems-with-and-without-rag"></a>

## 3. Problems you get without RAG, and problems you still get with RAG

### Without RAG

| Problem | What happens |
| --- | --- |
| Stale knowledge | The model does not know your 2026 policy. It only knows what was in its training data. |
| No private data | It cannot read your handbook, Confluence, or tickets. |
| Hallucination | When it does not know, it still produces a fluent, confident, wrong answer. |
| No source | You cannot point to the page the answer came from. |

**Example:** The India sick-leave policy changed from 10 days to 12 days in January 2026. A model without RAG still says 10, because that is what it memorized, or it invents a number.

### With RAG

RAG fixes "the model has never seen our documents." It does **not** remove every failure.

| Problem | What happens | Real example |
| --- | --- | --- |
| Retrieval miss | The right chunk is not in the top results, so the model answers from the wrong page or from nothing. | The question says "Bangalore" but the chunk only says "India." If metadata filters or the embedding are weak, the US policy is returned instead. |
| Bad chunking | A rule is split across two chunks, and only half is retrieved. | "12 sick days" is in chunk A. "Unused days do not carry forward" is in chunk B. The bot quotes 12 days and wrongly implies they roll over. |
| Outdated index | The PDF was updated, but embeddings were not rebuilt. | HR published 12 days in January. The index still has the 2024 PDF that says 10. RAG faithfully repeats the old document. |
| Conflicting sources | Two documents disagree, and the model blends them. | An old email says 10 days. The current handbook says 12. The bot says "around 10–12 days." |
| Irrelevant context | Extra chunks confuse the model (lost in the middle). | Five unrelated policies are stuffed into the prompt. The model mixes maternity leave rules into the sick-leave answer. |
| The model still ignores context | Even with the right page attached, the LLM sometimes prefers its own prior guess. | The prompt contains "12 days," and the model still answers "typically 10." |
| No answer in the documents | Retrieval returns weak matches, and the model fills the gap. | Nobody wrote a policy for contractors. The bot invents one that sounds official. |

**Short difference**

- **Without RAG:** the model has no company document, so it guesses from training memory.
- **With RAG:** the model is supposed to read your documents first. Wrong answers now usually come from retrieving the wrong or old chunk, or from the model not sticking to the chunk it was given.

---

<a id="what-is-hallucination"></a>

## 4. What is hallucination, and how do you prevent it?

**Hallucination** means the model states something that is not supported by the source of truth, while sounding sure.

It is not a typo. The sentence is grammatical and confident, and the fact is false.

**Example**

> "As per company policy, India employees get 15 paid sick days and unused days carry forward for 2 years."

The real policy says 12 days and they do not carry forward. The model invented 15 and the carry-forward rule.

### Why it happens

- The model is trained to continue text that looks likely, not to say "I don't know" by default.
- Without documents, it fills gaps from similar policies it has seen on the internet.
- With RAG, it still fills gaps when retrieval is empty, weak, or contradictory.

### How to prevent it

1. **Use RAG with a real source of truth.** Answer only from the current handbook, not from model memory.
2. **Force grounded answers.** System prompt: answer only from the provided context. If the context does not contain the answer, say "I could not find this in the policy" and stop.
3. **Return citations.** Every claim should point at document name, section, and page. If a sentence has no citation, drop it.
4. **Retrieve well.**
   - Chunk by section, with a small overlap, so a rule is not cut in half.
   - Store metadata (country, doc version, effective date) and filter before similarity search.
   - Re-index when a document changes.
   - Use hybrid search: keywords plus vectors, so "sick leave" and the policy title both match.
5. **Reject weak retrieval.** If the best chunk is below a similarity threshold, do not call the LLM to invent an answer. Return "not found."
6. **Keep the context small and relevant.** Pass the top few chunks, not the whole handbook.
7. **Check the draft against the chunks.** A second step can verify that each number in the answer appears in the retrieved text. "15 days" would fail that check.
8. **Prefer extractive answers for facts.** For "how many days," quote the sentence from the policy instead of paraphrasing a new number.
9. **Show the user the source.** People can see the PDF line and catch a wrong summary.
10. **Evaluate with a test set.** Keep questions whose correct answer is known ("India sick leave = 12, no carry forward") and run them after every index or prompt change.

### Same example, after the guardrails

User: *"How many paid sick days do I get in India, and do they carry forward?"*

Retrieved chunk (`leave-policy-india.pdf`, effective 2026-01-01):

> Employees in India receive 12 paid sick days per calendar year. Unused sick days do not carry forward.

Answer:

> You get **12 paid sick days** per calendar year. Unused days **do not** carry forward.
> Source: leave-policy-india.pdf, Leave section, effective 1 Jan 2026.

If the handbook has no contractor policy, the bot says it could not find that rule, instead of inventing one.

---

<a id="what-is-temperature"></a>

## 5. What is temperature in a model, and how does it improve the answer?

**Temperature** is a setting (a hyperparameter) that controls how creative, random, or predictable the model's next word is.

It usually ranges from **0.0 to 1.0**, and some APIs allow values above 1.0.

| Setting | Behavior |
| --- | --- |
| Low temperature (closer to 0.0) | Deterministic, safe, and focused. The model almost always picks the most probable next word. The same question tends to get the same answer. |
| High temperature (closer to 1.0) | Creative and varied. The model is willing to pick less obvious words, so answers differ from one run to the next. |

Temperature does not add new facts. It only changes how the model chooses among words it was already considering. A low temperature repeats the safest choice. A high temperature samples further down the list.

### Real-life example: the cocktail bartender

You walk into a bar and order a drink. The bartender's behavior changes with their temperature setting.

**Temperature = 0.0 (the strict recipe bartender)**

This bartender follows the official recipe with absolute precision. A Gin and Tonic is exactly 2 oz of gin and 4 oz of tonic, measured to the drop. Every time you order it, the drink tastes the same: predictable and correct.

Use this in AI for coding, math, legal document analysis, and resume tailoring. You want strict, factual execution, not creativity.

**Temperature = 0.8 (the creative mixologist)**

This bartender sets the recipe book aside. They add a splash of elderflower liqueur, a twist of burnt orange peel, and a pinch of chili salt. You often get a unique, surprising cocktail. Sometimes the experiment goes too far and the drink is undrinkable.

Use this in AI for brainstorming marketing slogans, writing science-fiction, or coming up with gift ideas.

### How temperature improves the answer

The improvement comes from matching the setting to the task. The same model gives a better answer for facts at a low temperature and a better answer for ideas at a high temperature.

| Task | Ideal temperature | Why |
| --- | --- | --- |
| Resume tailoring | 0.0 to 0.2 | Stops the model from inventing jobs, skills, or dates. This cuts one source of hallucination. |
| Writing code | 0.0 to 0.2 | Keeps syntax exact and avoids random or broken logic. |
| Brainstorming / copywriting | 0.7 to 1.0 | Pushes the model toward diverse wording and unexpected ideas. |

**HR bot example**

- "How many paid sick days in India?" should run at **0.0 to 0.2**. The useful answer is the same every time: 12 days, no carry forward. A high temperature might paraphrase that into "about 10 to 15 days."
- "Give me five subject lines for the leave-policy announcement email" should run at **0.7 to 1.0**. A temperature of 0 keeps repeating the same safe line. A higher temperature produces different options you can choose from.
