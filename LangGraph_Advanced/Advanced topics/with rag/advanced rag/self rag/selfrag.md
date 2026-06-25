
## What Self‑RAG (Self‑Reflective Retrieval-Augmented Generation) is and why it exists

-   Self‑RAG is short for "self‑reflective RAG" where the large language model (LLM) actively judges its own retrieval evidence and answers instead of blindly trusting retrieved documents .
    
-   It was created to fix three major problems in traditional RAG: unnecessary retrieval (indiscriminate retrieval), blind trust in retrieved documents, and lack of verification of generated answers (no self‑check) .
>Self-RAG (Self-Reflective Retrieval-Augmented Generation), a powerful technique designed to fix the biggest flaws in traditional RAG systems: unnecessary retrievals, irrelevant documents, and hallucinations
    
-   The core USP (unique selling point) of Self‑RAG is self‑reflection: at multiple steps the model asks itself if the step it just took was correct and then modifies actions accordingly .

## The four self‑reflection questions Self‑RAG answers (the architecture’s checks)

-   Should retrieval be performed for this query? — decide whether the question can be answered reliably from the LLM’s parametric knowledge or needs citation to external docs
    

-   Are the retrieved documents actually relevant to the query? — evaluate each retrieved chunk and keep only those that genuinely help answer the question
    
    .
    
-   Is the generated response grounded in the retrieved documents (i.e., free of hallucination)? — classify the generated answer as Fully Supported, Partially Supported, or No Support using only evidence present in the retrieved documents
    
    .
    
-   Does the final response actually answer the user’s question (usefulness)? — even a non‑hallucinated answer can be irrelevant or non‑justifying, so Self‑RAG tests whether the answer truly satisfies the query and, if not, loops back to retrieve alternative evidence
    
    .
    
-   These four checks implement a reflective control loop that prunes unnecessary retrievals, rejects or revises hallucinated claims, and ensures the answer justifies the user’s query
    
    .
    

## Detailed behavior for each check with examples

-   Retrieval necessity: the system returns True (do retrieval) when the answer requires specific fact citations unlikely to be present in the LLM’s parametric knowledge; it returns False for general explanations, definitions, or reasoning that the LLM can safely supply
    
    .
    
    -   Example: "How many paid leave days do employees at our company get per year?" requires retrieval from company docs → retrieval True .
        
-   Example: "What is paid leave?" is definitional and can be answered without retrieval → retrieval False .
    

Document relevance filtering: every retrieved document is individually asked "are you relevant to the query?" and only those that answer the question are kept; if none remain the flow returns "no answer found" and terminates

.

-   Example: three retrieved docs about public holidays, remote‑work policy, and leave approval — only the doc stating leave entitlement is kept as relevant
    
    .
    

Hallucination (support) check: generated answers are classified as:

-   Fully Supported — all claimed facts are present in the retrieved documents; accept and proceed
    
    .
    
-   Partially Supported — some facts come from documents but some claims were fabricated by the model; send to "revise answer" node to remove fabricated facts and regenerate
    
    .
    
-   No Support — answer facts are not present in documents at all (full hallucination); send to revision or ultimately reject if repair fails
    
    .
    
-   Example: if docs say "Drug X commonly causes dizziness and nausea" and the model adds "fatigue and headaches (especially in older patients)" from parametric memory, that is partial support (fabricated extra claims) and must be revised
    
    .
    

Usefulness check: after hallucination is resolved, the pipeline checks whether the non‑hallucinated answer actually justifies the original question; if it does not, the system rewrites the user’s query (refinement) and re‑runs retrieval and the loop up to a configured maximum tries, otherwise returns the answer

.

To avoid infinite loops, Self‑RAG imposes break conditions (e.g., maximum retries 5–10) so the revise/retrieve/usefulness loop terminates with "no answer found" if useful answers cannot be produced within the limit .

## Conceptual architecture / flow (step‑by‑step)

-   Step 1: User issues a query; a decision node examines it and decides “need retrieval?” (True/False) using a structured schema prompt that forces True only when external, specific fact citations are needed
    
    .
    
-   Step 2A (if no retrieval needed): send the query directly to the LLM with instructions to use only general knowledge and not assume existence of external documents; return the generated answer
    
    .
    
-   Step 2B (if retrieval needed): perform retrieval from the vector store and collect candidate document chunks (d1, d2, d3…) .
    
-   Step 3: Relevance filtering node inspects each retrieved chunk and keeps only those truly relevant to the question; if none remain, return "no answer found"
    
    .
    
-   Step 4: Generate an answer grounded in the kept documents (but do not yet accept it) .
    
-   Step 5: Support/hallucination verifier classifies the generated answer as Fully Supported, Partially Supported, or No Support; Fully Supported answers pass to usefulness check, others go to revise node
    
    .
    
-   Step 6: Revise node instructs the LLM to remove fabricated facts or to rewrite the answer strictly using the retrieved evidence; revised answers are looped back to the support checker, repeating until Fully Supported or a retry limit is reached
    
    .
    
-   Step 7: Usefulness verifier ensures the supported answer actually answers the user's question; if not, the system rewrites/refines the original query, fetches new documents, and repeats the process until either a useful, supported answer is produced or the retry cap is hit, at which point the system returns "no answer found"
    
    .
    
-   The architecture therefore forms a controlled loop: decide → (maybe) retrieve → filter → generate → verify support → revise until supported → verify usefulness → return or repeat/reject .
    

## Implementation strategy 

-  Implementing Self‑RAG incrementally in LangGraph (a graph‑based orchestration tool) rather than delivering an end‑to‑end monolith by add features step‑by‑step so to  understand each node's role
    
    .
    
-   For the prototype, a hypothetical company "Nexa AI Solutions" and a small document set (company profile, HR policies, product/pricing page) are used as the knowledge base; the documents were synthetically generated with ChatGPT .
    
-   Preprocessing steps  include text splitting with chunk size 600 and overlap 150, embedding all chunks into a vector store, and creating a retriever object — these chunk sizes were chosen experimentally as giving good results for this dataset .
    
-   The prototype keeps a state object that stores the user question, a boolean "need_retrieval" decision, retrieved docs, and final answer; routing logic uses that state to choose graph paths (direct generation vs retrieval) .
    
-   The “should_retrieve” node uses a structured output schema (JSON True/False) and system prompts that instruct the model when to choose True (need specific fact citations) versus False (definitions/general explanations) — guideline: choose True when answer requires specific fact citations or info likely not in model memory; choose False for generic explanations
    
    .
    
-   The direct‑answer node uses a system prompt explicitly preventing assumptions of external docs (so the LLM won’t hallucinate sources) and returns the LLM’s generated answer when retrieval is unnecessary .
    
-   The retrieval node simply invokes the retriever with the user question and returns candidate docs; an additional later improvement filters those docs for per‑document relevance before answering .
    
-   This implementation differs from the original Self‑RAG paper: the paper used a specially fine‑tuned model and different training setups, whereas this use OpenAI LLMs; core conceptual ideas are preserved but implementation details diverge .
    

## Practical decision rules and examples the tutorial uses

-   When deciding retrieval necessity: if answer requires "specific fact citations and info likely not in the model" then retrieval True; if question asks for general explanation/definition or you are unsure, default to True (conservative) — choosing True when clarity is missing .
    
-   Relevance filtering is essential because retrieved sets often include tangential docs (e.g., a doc about remote work policy is not relevant to leave entitlements) — the system eliminates irrelevant chunks before generating answers to reduce noise and hallucination risk
    
    .
    
-   Hallucination handling: three result categories (Fully Supported / Partially Supported / No Support) determine whether to accept, revise, or reject the answer; the revise step must instruct the model to remove claims not present in documents and then re‑check support, repeating until Fully Supported or retry limit reached
    
    .
    
-   Usefulness handling: even a Fully Supported answer can be non‑useful (i.e., does not satisfy the specific question) — in that case rewrite the query and repeat retrieval/generation to find better evidence or terminate with "no answer found" after retries
    
    .
    

## Engineering safeguards and parameters

-   To prevent infinite revision loops there must be a max tries parameter (e.g., 5–10 attempts) after which the system returns "no answer found" .
    

    
-   This uses LangGraph nodes for structured outputs (e.g., schema for should_retrieve) to force deterministic routing decisions and reduce prompt ambiguity
    
    .
    

## Summary of benefits compared to traditional RAG

-   Reduces unnecessary retrieval and compute by skipping retrieval when the model can reliably answer from parametric knowledge (addresses indiscriminate retrieval) .
    
-   Avoids blind reliance on retrieved documents by filtering relevance and checking whether answers are actually grounded in evidence (addresses blind trust)
    
    .
    
-   Detects and mitigates hallucinations through the support classification + revise loop, improving factual reliability (addresses lack of verification)
    
    .
    
-   Adds a usefulness check so accepted answers not only are factually supported but also properly answer the user’s intent .
    

## How this demonstrates these ideas 

-    building  a simplified Self‑RAG flow in LangGraph: a "should_retrieve" decision node, a direct generator node, a retriever node, a per‑document relevance filter, a generator that uses kept docs, a support verifier, a revise node (looping back), and a usefulness verifier — all wired so the state determines routing and retries are bounded
    
    .
    
-   This shows testing both branches: asking "Who is the CEO of Nexa AI?" triggers retrieval and shows the retrieved doc with the CEO name; asking "What is machine learning?" triggers direct generation with no docs fetched
    
    .
    
-   The  documents and example prompts are synthetic (created with ChatGPT)  (no fine‑tuned model used here)
    
    .
    

## Practical tips and caveats for real deployments

-   Implementation differences matter: the original Self‑RAG paper used specialized fine‑tuned models and training; if you use off‑the‑shelf LLMs you must rely on careful prompts, structured outputs, and engineering to approximate the same safeguards .
    
-   Tune chunking, overlap, retriever settings, and retry limits for your corpus to balance performance and cost; the tutorial picked chunk size 600 / overlap 150 by experimentation for its demo corpus but these are not universal defaults .
    
-   Structured schemas (JSON True/False outputs) and strong system prompts make routing decisions more robust and reduce ambiguous model outputs at control nodes (e.g., should_retrieve) .
    
-   Always include per‑document relevance checks and a strict support verifier before accepting any claims as grounded; otherwise the pipeline may still hallucinate or produce answers that misinterpret retrieved content
    
    .
    

## Minimal checklist to implement a usable Self‑RAG prototype 

-   Prepare and embed your document corpus (text splitting, embeddings, vector store) .
    
-   Build a "should_retrieve" decision node with a structured schema and system prompt that outputs True/False
    
    .
    
-   Implement direct generator and retrieval generator branches with explicit system prompts (direct branch: no external doc assumptions; retrieval branch: provide kept docs). Use a retriever to fetch candidate chunks when needed
    
    .
    
-   Add per‑document relevance filtering to discard noisy retrieved chunks
    
    .
    
-   Add a support verifier that classifies generated answers into Fully Supported / Partially Supported / No Support using only retrieved evidence
    
    .
    
-   Add a revise node that instructs the LLM to remove unsupported claims and regenerate; loop back to verification and bound the max retries
    
    .
    
-   Add a usefulness verifier that checks whether the supported answer actually answers the user; if not, refine the query and re‑run retrieval/generation with retry limits
    
    .
    

## Conclusion
-   This emphasizes an incremental build — add features one by one in the graph so to  see how each improvement changes behavior and improves reliability
    
    .


----------

## Self-RAG improvement: filtering retrieved documents for relevance

-    adding a step that evaluates each retrieved document to decide whether it is relevant to the user's question, keeping only documents marked relevant and discarding the rest .
    
-   The retained "relevant_docs" list (a state field holding document objects) is built from the retrieved documents; answers are later generated using only those relevant documents .
    
-   The decision is integrated into the LangGraph workflow: after Decide Retrieval determines whether to retrieve, retrieval runs, then each retrieved document is tested and only relevant ones are stored; that ends the retrieval branch
    
    .
    
-   Implementation details: the code adds an is_relevant boolean field in a small JSON/pydantic schema and a system prompt instructs the LLM to judge document relevance (returning JSON matching the schema) — "true if the document helps answer the question, else false" .
    
-   The workflow loops over retrieved docs, invokes the LLM per document, and appends documents judged true into the relevant_docs list in state .
    
-   If retrieval was needed, the flow proceeds to retrieval; otherwise the graph uses Direct Generation — the branching remains unchanged except for the new relevance-filtering node and state key .
    

> Key behavior example: the query "Who is the CEO of Nexai?" triggers retrieval; four documents are retrieved but only the one that explicitly states the CEO is marked relevant and stored — the other three are ignored as syntactically close but not relevant for answering the question
> 
> .

-   Rationale: this relevance filter reduces noise by restricting later generation to only documents that directly support the question, so future answer generation uses a smaller, grounded context .
    

## Generating answers from merged relevant context

-   The next improvement merges all relevant documents into a single "context" string (state field) and supplies that context plus the question to the LLM to produce the answer .
    
-   If at least one document is relevant, the system generates the answer from that merged context; if zero relevant docs are found, it returns "no information" to the user and ends the workflow .
    
-   The implementation uses a system prompt instructing the LLM to act as a "business RAG assistant" and answer using only the provided context; the code builds the context string by concatenating relevant documents and invokes the LLM with question + context .
    
-   Example: asking "Who is the CEO of Nexai?" yields a relevant doc and the answer "Arav Mehta" generated from the relevant context .
    
-   Example non-answer: asking "What is Nexai's refund policy?" finds no relevant passage in the documents, so the flow goes to the branch that reports "no relevant document found" .
    
-   Extensibility: the video explains a placeholder node "No relevant docs" can be replaced by a web-search node; if no internal doc is relevant, one can run web search, re-evaluate returned pages for relevance, and then generate from any web-sourced relevant docs
    
    .
    

## Self-reflection: detecting hallucination (is_supported check)

-   The architecture adds a Support node that classifies a generated answer as one of three values: "fully_supported", "partially_supported", or "not_supported" based on the merged relevant context and question .
    
-   The code extracts evidence items (a list) from the context; evidence is optional for operation but aids debugging and transparency .
    
-   A structured-output LLM is used: it receives the question, the generated answer, and the merged context and returns the support verdict plus evidence items per a pydantic schema .
    
-   Behavior examples:
    
    -   Fully supported: when the answer's facts are all present in the relevant context, the node returns "fully_supported" and lists the supporting evidence snippets (e.g., "Nexa AI has 85+ employees" appears fully grounded)
        
        .
        
-   Partially supported: when the LLM added facts beyond the context (took "freedom" to include additional claims), the node returns "partially_supported" with evidence showing which parts are grounded and which are not .
    
-   Not supported: when no evidence exists in the relevant docs for the question (e.g., free trial length not present in documents), the node returns "no support" and the system can mark the answer not supported
    
    .
    

## Automated revision loop to eliminate hallucination (revise_answer)

-   If the support verdict is "partially_supported" or "not_supported", the graph enters a Revise Answer node: a strict rewriter prompt instructs the LLM to rewrite the answer so every fact is sourced strictly from the provided context .
    
-   After revision, the new answer is re-evaluated by the support checker; this loop repeats until the answer becomes "fully_supported" or a retry limit is reached to avoid infinite loops .
    
-   The code implements a max_retries counter (e.g., break after 5 attempts) and will return "not_supported" if the loop exhausts retries
    
    .
    
-   Demonstration: a question that initially yielded "partially_supported" was revised in a single retry into a "fully_supported" answer trimmed to evidence-based statements — the system prints that one retry sufficed and shows the revised answer grounded in context
    
    .
    

## Usefulness check and retrieval-query rewriting (is_useful and rewrite_query)

-   After achieving a supported answer, the flow runs an "is_useful" node: the LLM judges whether the generated answer actually satisfies (is useful for) the user's question and returns usefulness plus a reason
    
    .
    
-   Two outcomes:
    
    -   If "useful", the workflow finalizes and returns the answer to the user .
        
-   If "not useful", the workflow triggers a rewrite-and-retry loop: the original user question is rewritten into a "retrieval_query" optimized for vector retrieval over internal PDFs (short, preserving entities, 2–5 high-signal keywords), and the system uses that rewritten query to fetch new documents and repeat the whole pipeline
    
    .
    

Control flow safeguards: rewrite attempts are bounded by a max_tries variable (e.g., 5–10) to prevent infinite loops; if retries exceed the limit, the system exits with "no answer found" and labels the result "not useful" .

Implementation notes: the initial retrieval_query equals the user's question; the query field updates whenever the system rewrites the query after a failed usefulness check; subsequent retrieval uses this optimized retrieval_query rather than the raw question

.

Demonstrated run: for "Describe Nexai company culture", the pipeline showed need_retrieval true, rewrite_try 0, support checks, two relevant docs, support = fully_supported, usefulness = useful with a reason, and a final grounded answer built from evidence .

## Overall Self-RAG architecture and purpose

-   Self-RAG puts multiple LLM-mediated checks in the retrieval-augmented generation loop: (1) per-document relevance filtering, (2) answer generation from merged relevant context, (3) support-checking to detect hallucination, (4) automated revision until fully supported (bounded by retries), and (5) usefulness evaluation with query rewriting and additional retrieval if the answer is not useful
    
    .
    
-   Each node is implemented with small pydantic schemas and structured-output prompts so the LLM returns JSON matching expected fields (relevance booleans, support enum + evidence list, usefulness enum + reason, rewritten query)
    
    .
    
-   The design emphasizes grounding answers in cited context snippets and iterative correction of hallucinations before returning answers to users, while using retry limits and optional web search fallbacks to remain practical and avoid infinite loops
    
    .
    

## Practical recommendations 

-   Keep the per-document relevance judgment strict: only documents that explicitly help answer the question should be retained to reduce noise in final generation .
    
-   Use structured-output prompts and pydantic schemas to ensure reliable machine-readable decisions from the LLM at each node (relevance, support, usefulness, rewritten query)
    
    .
    
-   Implement retry limits (max_retries / max_tries) for both revision and retrieval-query rewrite loops to prevent infinite cycles; return "no answer found" if limits are exhausted
    
    .
    
-   Optionally add a web-search node to the "no relevant docs" branch so the system can fetch external documents when internal corpora lack evidence; self-RAG demo includes code pointers for that possibility but does not enable web search in the provided architecture by default
    
    .
    
-   Suggested tests: try factual questions that exist in corpus (should return fully supported answers), questions without supporting docs (should return "no relevant document found"), and questions where the model may overreach (should be detected as partially/not supported and revised) — the video runs such examples to demonstrate behavior
    
    .
    



## gain by Self-RAG

-   Answers become more grounded because generation uses only filtered, evidence-containing documents and support is explicitly checked and enforced by a revise loop
    
    .
    
-   The pipeline reduces hallucinations and allows automated correction when the model invents unsupported facts; it also provides auditability via evidence snippets returned with verdicts
    
    .
    
-   The architecture is modular: nodes can be swapped (e.g., web search for "no relevant docs") and prompts/schemas adjusted as needed for different domains or corpora
    
    .