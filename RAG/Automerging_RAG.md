[Auto-Merging RAG: Hierarchical Retrieval](https://dev.to/rushanksavant/auto-merging-rag-hierarchical-retrieval-4dp1)

Auto-merging retrieval organizes data into a tree structure.
You store small Child Chunks (for high-precision searching) that are linked to larger Parent Chunks (for broad context).

```
import uuid
from typing import List, Dict
from collections import Counter
from langchain.chat_models import init_chat_model
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_core.stores import InMemoryStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_core.callbacks import CallbackManagerForRetrieverRun

from dotenv import load_dotenv
load_dotenv()


# --- STEP 1: ULTRA-REALISTIC MEDICAL DATA ---
medical_manual = """
CARDIOVASCULAR PROTOCOL - VERSION 2026
SECTION 1.1: ACUTE MYOCARDIAL INFARCTION (AMI)
Diagnosis: Patient presents with retrosternal chest pressure, radiation to left arm, and diaphoresis. 
ECG Requirements: 12-lead ECG must be performed within 10 minutes of arrival. Look for ST-segment elevation >1mm.
Immediate Treatment: Oxygen saturation maintenance >94%. Aspirin 325mg (chewed). Nitroglycerin 0.4mg sublingual every 5 mins.
Contraindications: Do not use Nitroglycerin if SBP < 90mmHg or if patient has taken PDE5 inhibitors in 24h.

SECTION 1.2: ADULT CARDIAC ARREST (VF/pVT)
Protocol: Initiate high-quality CPR. Attach defibrillator. Shock at 200J (Biphasic).
Drug Therapy: Epinephrine 1mg IV/IO every 3-5 minutes. Amiodarone 300mg IV/IO bolus after 3rd shock.
Post-Resuscitation: If ROSC is achieved, initiate Targeted Temperature Management (32°C-36°C).
Warning: Excessive ventilation (over 10 breaths/min) decreases cardiac output and survival rates.

SECTION 2.1: HYPERTENSIVE CRISIS
Definition: SBP >180 mmHg or DBP >120 mmHg. 
Hypertensive Urgency: No end-organ damage. Treat with oral Labetalol 200mg.
Hypertensive Emergency: Evidence of end-organ damage (Stroke, Encephalopathy). 
Emergency Treatment: Labetalol IV 20mg bolus or Nicardipine IV infusion 5mg/h. 
Goal: Reduce Mean Arterial Pressure (MAP) by no more than 25% in the first hour to prevent cerebral ischemia.

SECTION 3.1: ANAPHYLAXIS EMERGENCY
Symptoms: Urticaria, angioedema, stridor, wheezing, or hypotension following allergen exposure.
Primary Treatment: Epinephrine 0.3mg (1:1000) IM in the lateral thigh. Repeat every 5-15 mins if no improvement.
Secondary Treatment: Diphenhydramine 25-50mg IV. Methylprednisolone 125mg IV.
Observation: Monitor for biphasic reactions for at least 4-6 hours post-symptom resolution.
"""


# --- STEP 2: HIERARCHICAL SPLITTING ---
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
child_splitter = RecursiveCharacterTextSplitter(chunk_size=150, chunk_overlap=20)

# Create parent and child docs with metadata links
docs = [Document(page_content=medical_manual)]
parent_docs = parent_splitter.split_documents(docs)

all_child_docs = []
docstore_data = {}

for parent in parent_docs: # one-level parent-child tree
    parent_id = str(uuid.uuid4())
    docstore_data[parent_id] = parent

    # Split each parent into children
    children = child_splitter.split_documents([parent])
    for child in children:
        child.metadata["parent_id"] = parent_id
        all_child_docs.append(child)


# --- STEP 3: STORAGE ---
embed_model = HuggingFaceEndpointEmbeddings(
    model="sentence-transformers/all-MiniLM-L6-v2", ## this model returns 384 sized vector
    task="feature-extraction")
vectorstore = Chroma.from_documents(all_child_docs, embed_model)
docstore = InMemoryStore()
docstore.mset(list(docstore_data.items())) ## mset stands for Multiple Set, a high-performance way to save a batch of key-value pairs into storage at once.


# --- STEP 4: THE CUSTOM AUTO-MERGING RETRIEVER ---
class AutoMergingRetriever(BaseRetriever):
    vectorstore: Chroma
    docstore: InMemoryStore
    merge_threshold: int = 3 # If 3+ children found, return Parent

    def _get_relevant_documents(self, query: str, *, 
                                run_manager: CallbackManagerForRetrieverRun) -> List[Document]:
        # 1. Fetch top K small children
        initial_hits = self.vectorstore.similarity_search(query, k=12)

        # 2. Track which parents are represented and how many times
        parent_id_map = [doc.metadata.get("parent_id") for doc in initial_hits]
        counts = Counter(parent_id_map)

        final_results = []
        processed_parents = set()

        for doc in initial_hits:
            p_id = doc.metadata.get("parent_id")

            # 3. MERGE LOGIC: If parent is frequent, "Zoom Out"
            if p_id and counts[p_id] >= self.merge_threshold:
                if p_id not in processed_parents:
                    parent_doc = self.docstore.mget([p_id])[0]
                    if parent_doc:
                        final_results.append(parent_doc)
                        processed_parents.add(p_id)
            # 4. If not frequent enough, keep the precise child snippet
            elif p_id not in processed_parents:
                final_results.append(doc)

        return final_results


# --- STEP 5: TEST RUN ---
retriever = AutoMergingRetriever(vectorstore=vectorstore, docstore=docstore)

# Ask a query that touches multiple parts of one section
query = "What is the IV dosage for Labetalol and what is the target MAP reduction for high blood pressure?"
results = retriever.invoke(query)

print(f"Retrieved {len(results)} merged document(s).\n")
print("-" * 30)
for doc in results:
    print(f"SOURCE: {doc.metadata.get('parent_id', 'Child Node')}")
    print(f"CONTENT: {doc.page_content[:400]}...") # Print snippet
    print("-" * 30)

```
    
