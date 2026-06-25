
## Traditional RAG Workflow

**Retrieval-Augmented Generation (RAG)** combines retrieval from a knowledge base with generation by a large language model (**LLM**) to produce accurate, context-grounded responses. This workflow addresses limitations in pure LLMs by pulling external documents, preventing reliance solely on parametric knowledge.

The process unfolds in three core steps, building a chain from query to answer:

1.  **Retrieval**: User query (e.g., "What is machine learning?") is embedded using a deep learning **embedding model** (converts text to numerical vectors). This query vector performs semantic search in a **vector database** (e.g., FAISS) storing chunked private documents as vectors. Top-k relevant chunks (e.g., top-4) are retrieved based on vector similarity.
    
2.  **Augmentation**: Retrieved documents are combined with the original query into a prompt sent to the LLM. The prompt instructs the LLM to answer using only the provided context.
    
3.  **Generation**: The LLM generates a response grounded in the retrieved documents.
    

_This matters because it grounds LLM outputs in verifiable sources, reducing hallucinations from internal knowledge._ 

## Limitations of Traditional RAG

Traditional RAG blindly trusts retrieved documents, assuming relevance—which fails when retrieval pulls irrelevant chunks. If documents do not match the query, the LLM generates incorrect answers, as it is forced to use poor context.

-   **Irrelevant Retrieval Example**: Query "What is an LLM?" on a vector DB of only machine learning books (no LLM content). Retrieval might return Random Forest or XGBoost chunks due to semantic proximity in ML topics, leading to fabricated answers.
    
-   **Business Risks**: An employee querying company leave policy (absent from DB) gets wrong info from unrelated docs, causing real-world errors.
    
-   **Hallucination Risk**: Without relevant docs, LLM falls back to parametric knowledge, potentially hallucinating confidently.
    

This vulnerability arises because chunking (splitting docs into fixed-size pieces, e.g., 900 chars with 150 overlap) ignores semantic boundaries, mixing topics. As a result, RAG fails on out-of-scope queries despite good performance on in-scope ones.

##  Traditional RAG with LangGraph 

Building a baseline RAG using **LangGraph** (a framework for stateful LLM graphs) on three classic ML/DL books: "Hands-On Machine Learning," "Deep Learning," and "Pattern Recognition." This setup indexes ~2000 docs, chunks to >6000 pieces. **Setup Steps**:

-   Load PDFs into document objects and combine.
    
-   **Text Splitting**: RecursiveCharacterTextSplitter (chunk_size=900, overlap=150); handle Unicode errors.
    
-   Embeddings: OpenAI model + FAISS vector store.
    
-   Retriever: Similarity search for top-4 docs.
    
-   LLM: ChatOpenAI. **Graph Structure** (simple two-node):
    
-   **Retrieve Node**: Invoke retriever on question, store docs in state.
    
-   **Generate Node**: Join docs into context string; prompt LLM: "Answer only from context; if not in context, say you don't know." Store answer. **Tests**:
    
-   Good query ("What is bias-variance tradeoff?"): Retrieves relevant chunks; accurate answer.
    
-   Bad query ("What are top AI news from last month?"): Correctly says "I don't know."
    
-   Off-topic query ("What is a transformer in deep learning?"): Retrieves unrelated chunks (MLP, CNN, regularization); LLM hallucinates detailed (parametric) answer despite irrelevance.
    



## Corrective RAG (CRAG): Overview

**Corrective RAG (CRAG)** extends RAG by evaluating retrieved documents _before_ generation, avoiding blind trust. 

Introduced in a 2024 paper, it uses a **retrieval evaluator** (fine-tuned T5-large in paper; ChatOpenAI here) to classify retrieval quality.

CRAG handles three cases post-retrieval, building on traditional RAG:

| Case          | Condition                                          | Action                                                                                                                                      |
|---------------|----------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| **Correct**   | At least one retrieved document is highly relevant | Use the relevant document(s) to refine the model's internal knowledge and generate the answer.                                              |
| **Incorrect** | All retrieved documents are irrelevant             | Ignore retrieved documents, perform external knowledge retrieval (e.g., web search), then generate the answer.                             |
| **Ambiguous** | Some documents are relevant while others are not   | Use useful information from relevant documents, perform web search for missing information, combine both sources, then generate the answer. |
_Why it matters_: CRAG dynamically adapts, ensuring grounded answers even with poor internal retrieval—critical for production where DBs are incomplete. The paper's diagram shows query → retrieve → evaluate → branch to internal/external knowledge.

Implementation iteratively adds features to baseline RAG via LangGraph: (1) Knowledge Refinement, (2) Retrieval Evaluation.

## Knowledge Refinement: Cleaning Relevant Documents

Even relevant chunks contain noise from chunking (mixed topics, split semantics). **Knowledge Refinement** extracts precise info via three steps, applied per document if retrieval is correct.

1.  **Decompose**: Break document into **strips** (sentences or 1-2 sentence groups).
    
2.  **Filter**: LLM (fine-tuned T5 in paper) scores each strip's relevance to query (true/false or confidence). Keep only useful strips.
    
3.  **Recompose**: Merge kept strips into refined context. **Example**:
    

-   Query: "What is gradient descent?"
    
-   Raw chunk: GD definition + unrelated neural nets/CNN text.
    
-   Strips: S1/S2 (GD, relevant); S3/S4 (nets/CNN, irrelevant).
    
-   Refined: Only S1/S2 → cleaner context for generation. **Code in LangGraph (Iteration 1)**:
    
-   State adds: strips, kept_strips, refined_context.
    
-   **Refine Node**:
    

    ```
    def decompose_to_sentences(text):  # Splits into sentence list  
    ```
    
    -   Join docs → decompose → loop: LLM prompt ("Strict relevance filter: return keep=True only if sentence directly helps") → structured output (true/false).
        
-   Collect kept → refined_context = "\n".join(kept).
    

Graph: retrieve → refine → generate.

Result: Shorter, precise context improves generation quality.

_Connection_: Refinement assumes correct retrieval; next iteration adds evaluation. Note: Uses ChatOpenAI (not fine-tuned T5, unavailable).

## Retrieval Evaluation: Classifying Document Quality

Post-retrieval, score each document (0-1 scale; 0=irrelevant, 1=sufficient alone) with reasons. Use thresholds: lower=0.3 (3/10), upper=0.7 (7/10). **Classification Logic** (per paper, adapted):

-   **Correct**: ≥1 doc score > upper → use good docs (>lower) after refinement.
    
-   **Incorrect**: All scores ≤ lower → external search.
    
-   **Ambiguous**: Else (mixed) → refine good + external. **Key Nuance**: For generation, _only_ docs > lower threshold ("good_docs"); discard low even in "correct" case. **Example**:
    
-   Docs scores: 0.8, 0.4, 0.2 → Correct (has >0.7); use first two (>0.3). **Code in LangGraph (Iteration 2)**:
    
-   State adds: good_docs, verdict, reason.
    
-   Thresholds: UPPER=0.7, LOWER=0.3.
    
-   **Evaluator Node**:
    
    -   Pydantic schema: score (float), reason (str).
        
-   LLM chain: Prompt ("Strict evaluator: score 0-1; be conservative with high scores") + structured output.
    
-   Loop over docs: Get scores/reasons; collect good_docs (>LOWER).
    
-   Verdict logic:
    
    -   Any >UPPER → "correct"
        
-   All ≤LOWER → "incorrect" (no good_docs)
    
-   Else → "ambiguous"
    

**Router Node**: verdict → refine/generate ("correct"); fail ("incorrect"); ambiguous node.

Refine modified: Context from good_docs only.

Tests:


| Query                    | Verdict     | Reason                |
|--------------------------|-------------|-----------------------|
| Bias-variance tradeoff   | Correct     | ≥1 chunk > 7          |
| AI news last week        | Incorrect   | No chunk sufficient   |
| Attention mechanisms     | Ambiguous   | Mixed signals         |
This builds a robust system: Evaluation gates refinement/generation, enabling future web integration.

> **💡 Key Insight:** CRAG's evaluator (T5-large fine-tuned in paper) outperforms general LLMs for efficiency/accuracy; thresholds tunable.

----------

----------

## Handling Incorrect Retrieval: Adding Web Search for Robustness

The system now evaluates retrieved documents as **correct**, **incorrect**, or **ambiguous** using the **retrieval evaluator**. If deemed **incorrect**—meaning no documents are capable of answering the query—the process doesn't stop; instead, it fetches external knowledge via web search to ensure users receive a useful response rather than empty output.

This builds robustness because traditional RAG fails when internal documents are insufficient, but web search acts as a fallback, using **Tavily** (a search API introduced previously) to query the internet directly with the original question. **Key mechanism:**

-   Extract title, URL, and content from Tavily results.
    
-   Convert them into document objects and store in the LangGraph **state** as `web_docs`.
    
-   Pass these `web_docs` to the existing **refine** node (which chunks, filters via LLM or T5, and recombines into refined context), then to **generation**. **Code reuse efficiency:** The refine and generation nodes from prior iterations are reused—no new code needed for them—keeping the architecture simple while extending it. The graph now routes: correct → refine(good_docs) → generate; incorrect → web_search → refine(web_docs) → generate. **Example outcome:** For "AI news from the last month," internal docs are incorrect, so web search yields recent events like OpenAI's open-source assistant and CES 2026 AI presence, generating a substantive answer.
    

This iteration makes the system more reliable by never leaving users empty-handed.

----------

## Enhancing Web Search: Query Rewrite for Better Results

User queries sent directly to search engines like Tavily may be vague, underspecified, missing keywords, or lacking time constraints (e.g., "Recent AI news"), yielding suboptimal results. To optimize, insert a **query rewrite** step before web search: an LLM refines the original query into a search-engine-friendly version. **Why it matters:** Rewritten queries are concise, keyword-rich, and explicit (e.g., adding "last 30 days" for recency), improving result relevance as search engines favor structured inputs. Paper authors recommend this as a variant improvement for architectures. **Implementation steps:**

1.  After evaluation, if incorrect, invoke **rewrite_query** node with a pydantic schema for a single output query.
    
2.  System prompt: "You are a web search query composer. Keep it short; add recency constraints like 'last 30 days' if implied; return JSON with a single query."
    
3.  LLM generates rewritten query (e.g., "Recent AI news last 30 days"), store in state as `web_query`.
    
4.  Pass `web_query` to Tavily instead of original query. **Graph update:** Insert rewrite_query before web_search; refine and generate remain unchanged. **Example:** "Recent AI news" rewrites to "Recent AI news last 30 days," fetching richer results despite not being overly transformative in all cases—but faithful to the paper.
    

This small change significantly boosts web search effectiveness.

----------

## Resolving Ambiguous Retrieval: Merging Internal and External Knowledge

**Ambiguous** occurs when no retrieved document scores ≥7 (incapable alone) but all score >3 (not worthless). Discarding them loses partial value, so the strategy retains "good docs" (>3 score) while augmenting with web search for a comprehensive context. **Core idea:** Merge good_docs + web_docs in refinement, creating a hybrid context for generation—using internal knowledge where partially useful and external to fill gaps. **Smart state usage in LangGraph:** Simplify to two paths (eliminate separate ambiguous branch):

-   **Correct** (≥1 doc ≥7): refine(good_docs) → generate.
    
-   **Incorrect or ambiguous**: rewrite_query → web_search → refine(good_docs + web_docs) → generate. **Refine node update (key magic):**
    
-   If verdict == "correct": use good_docs.
    
-   Else (incorrect/ambiguous): if ambiguous, concatenate good_docs + web_docs before chunking/filtering/recombining. **Routing logic:** Correct → refine; else → rewrite_query → web_search → refine(merged) → generate. **Example:** "Batch normalization vs layer normalization"—internal books cover batch but not layer (ambiguous: no ≥7, all >3); merges with web docs for full comparison answer.
    

This handles all cases efficiently with state persistence enabling merges without extra branches.

----------

## Complete CRAG Architecture: Faithful to the Paper

The final graph mirrors the paper: retrieval → evaluation (correct/internal only, ambiguous/internal+external, incorrect/external only) → refine → generate. **Knowledge usage distinctions:**

-   Correct: Internal refined knowledge.
    
-   Ambiguous: Internal good + external refined.
    
-   Incorrect: External refined only.
    

Deviations for practicality: LLM instead of T5 for refinement (T5 availability unclear), but architecture-level fidelity preserved. **Recommendation for mastery:** Review provided codes, implement from scratch to internalize—now CRAG is fully understood as an advancement over traditional RAG.