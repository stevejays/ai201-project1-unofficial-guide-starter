# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->
Professor ratings for some progessors in University of chicago taken from Rate my professor
---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Rate My Professors| Rating Professors | /documents/Michael RoloffLand.txt|
| 2 | Rate My Professors| Rating Professors | /documents/Faisal AkkawiLand.txt|
| 3 | Rate My Professors| Rating Professors | /documents/SheeWuLand.txt|
| 4 | Rate My Professors| Rating Professors | /documents/FangPei CaiLand.txt|
| 5 | Rate My Professors| Rating Professors | /documents/Sabri CetinkuntLand.txt|
| 6 | Rate My Professors| Rating Professors | /documents/Peter Ganong.txt|
| 7 | Rate My Professors| Rating Professors | /documents/Victor LimaLand.txt|
| 8 | Rate My Professors| Rating Professors | /documents/Stuart GazesLand.txt|
| 9 | Rate My Professors| Rating Professors | /documents/Kale DaviesLand.txt|
| 10| Rate My Professors| Rating Professors | /documents/Beatrice FineschiLand.txt|

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**
**Chunk size:**
250

**Overlap:**
50

**Reasoning:**
Individual student reviews are typically 50-200 characters long. 
A 250-character chunk keeps each review mostly intact as its own 
semantic unit, avoiding mixing opinions about different aspects 
(grading, teaching style, difficulty) into a single chunk. This 
makes retrieval more precise — a question about grading should 
return chunks about grading, not chunks that mix grading and 
teaching comments together. Overlap of 50 characters preserves 
context at chunk boundaries where a review might split.

**Overlap:**
50 characters

**Why these choices fit your documents:**
there were some additional text which was not cleaned. Also had to make sure each of the reviews were stand alone and did not overlap

**Final chunk count:**
283 
---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**
LLM_MODEL = "llama-3.3-70b-versatile"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

**Production tradeoff reflection:**
**opted not to fully clean the files as it would take too much effort. Also the source of the documet was a web page where there were too many advertisements and lot of hyperlinks and embedded text not relevant to the rating. **
---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

"You are a university guide assistant. Answer the user's question using ONLY "
                "the context provided below. Do not use any outside knowledge. "
                "If the answer is not found in the context, say clearly: "
                "'I don't have enough information on that in the loaded documents.' "
                "Always indicate which professor or source your answer refers to."

**How source attribution is surfaced in the response:**
 context += f"[Source: {chunk['professor']}]\n{chunk['text']}\n\n"

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | How is Faisal Akkawi rated?|Faisal Akkawi is rated well He has a rating of 3.3. He teaches real world situation | Only positive ratings (5.0 quality) | Very Poor| 20% |
| 2 | How is SheeWu rated? |Reviews about SheeWu from loaded documents| "I don't have enough information" — 
even though SheeWu has 26 chunks in the database | Terrible | 0% | 
| 3 | Who is rated more than 3 out of 5 |List of professors with overall rating > 3 | Only Kale Davies and SheeWu (incomplete)| Poor | 50% |
| 4 | Who has the lowest rating|Peter Ganong | The lowest rating is given by the sources reviewing Professor Peter Ganong and Harris, | Poor | 30% | 
| 5 | what are some comments about Peter Ganong?|comments about Peter Ganong | Provided comments for Peter Ganong | Very good | 99% | 


**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**
so I asked the question - who has the lowest rating of all? 

**What the system returned:**
it gave According to the context provided by Kale Davies, the lowest rating is 1.0, which is given by Kale Davies himself. Retrieved from- Beatrice Fineschi  Kale Davies

**Root cause (tied to a specific pipeline stage):**
This requires comparing across all the 7 documents. However RAG probably cant do that. 

**What you would change to fix it:**
This might be a limitation of RAG that it only takes 4 chunks it has and which might not have content across files to be able to answer this.
---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
The flowchart was helpful in going step by step. The decision on chunk size also made me think ahead. 

**One way your implementation diverged from the spec, and why:**
Was thinking of using another llm but would have had to research to find a suitable one
---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
- so I asked the question - who has the lowest rating of all? and it gave According to the context provided by Kale Davies, the lowest rating is 1.0, which is given by Kale Davies himself. Retrieved from- Beatrice Fineschi  Kale Davies
- *What it produced:*
- That's actually a great failure case to document in your evaluation report!
What went wrong:
The question "who has the lowest rating of all?" requires the system to compare across all professors — but RAG can't do that. It only retrieves 4 chunks and asks the LLM to answer from those. So the LLM can only compare within whatever 4 chunks happened to be retrieved, not across all 283 chunks.
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- so I asked --- how is Peter Ganong rated?---- and response is-------According to the context provided by multiple sources, including HARRIS, Peter Ganong is rated as follows: 
- DIFFICULTY: 3.0 (in one review) and 2.0 (in another review)
- QUALITY: 1.0 (in multiple reviews)
Overall, the reviews suggest that Peter Ganong is considered a poor professor, with one reviewer stating to "Avoid him at all costs!!!". (Source: HARRIS and other anonymous reviews about Peter Ganong)-----Retrieved from--• Peter Ganong
• Sabri Cetinkunt
- *What it produced:*
- That's a good result! The system is working. A few observations:
What's working ✅

Correctly identified Peter Ganong's ratings from the chunks
Grounded in retrieved context
Sources are listed programmatically

Things to note ⚠️

"HARRIS" appearing as a source name is noise from the PDF — it's a department label that got mixed into a chunk, and the LLM treated it as a reviewer name
Sabri Cetinkunt appearing in sources means one of the top 4 retrieved chunks was about a different professor — similar to what we saw earlier with semantic search on proper nouns
- *What I changed or overrode:*
