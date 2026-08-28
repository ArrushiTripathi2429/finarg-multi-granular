# FinArg-MTL: Multi-Granular Financial Argument Mining

**Technical Documentation** | Version 1.0.0 | 

---

## 1. Problem Statement

Current financial argument mining (FinArg) treats each sentence as a single argument unit with binary labels (Claim/Premise). This misses three critical aspects:
- **What** financial topic is being discussed (revenue, margins, guidance, etc.)
- **How** a sentence can contain multiple argumentative functions (mixed premise + claim)
- **Why** a model made a particular prediction (explainability)

**Our Extension**: Multi-granular framework that jointly models sentence-level function, span-level argument components, and target-specific financial semantics.

---

## 2. Annotation Schema

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `id` | string | Unique identifier | `"finarg_001"` |
| `text` | string | Original sentence | `"Even with strong demand, we expect slowdown in Q4."` |
| `sentence_label` | string | Claim or Premise | `"claim"` |
| `target` | string | Specific financial topic | `"growth forecast"` |
| `target_category` | string | Broad semantic group | `"guidance"` |
| `spans` | array | Argument segments with offsets | `[{"start":0, "end":23, "text":"Even with strong demand", "label":"premise_span"}]` |

### Target Categories (10):
`guidance`, `profitability`, `revenue`, `cost_structure`, `liquidity`, `investment`, `operations`, `market`, `risk`, `strategy`

### Specific Targets (40+):
`revenue`, `margins`, `demand`, `pricing`, `guidance`, `COGS`, `operating expenses`, `CAPEX`, `cash flow`, `market share`, etc.

---

## 3. 5-Step Annotation Pipeline

| Step | Action | Output |
|------|--------|--------|
| **1** | Retain original sentence label | Claim/Premise |
| **2** | Add target & category | Target (specific) + Category (broad) |
| **3** | Logical-syntactic segmentation (discourse markers: because, although, therefore, but) | Segmented clauses |
| **4** | Assign span-level roles | premise_span / claim_span per segment |
| **5** | Export to structured JSON | Machine-readable with character offsets |

**Segmentation Markers**: Concessive (although, despite), Causal (because, since), Resultative (therefore, so), Contrastive (but, however), Conditional (if, unless)

---

## 4. Model Architecture
                         Input sentence (+ context window)
                                      │
                         ┌────────────────────────┐
                         │  Shared Transformer      │
                         │  Encoder (e.g. FinBERT / │
                         │  RoBERTa / domain-tuned  │
                         │  LLM backbone)           │
                         └────────────────────────┘
                                      │
              ┌───────────────────────┼───────────────────────┐
              │                       │                       │
     [CLS] pooled repr        [CLS] pooled repr        Token-level hidden states
              │                       │                       │
   ┌──────────▼─────────┐  ┌──────────▼─────────┐  ┌──────────▼──────────┐
   │ Head 1: Sentence    │  │ Head 2: Target /    │  │ Head 3: Span         │
   │ Classification      │  │ Target-Category     │  │ Tagging (BIO scheme  │
   │ (premise/claim)     │  │ Classification       │  │ over premise/claim/  │
   │ softmax over 2       │  │ (multi-class over    │  │ non-arg spans)        │
   │ classes              │  │ target taxonomy)     │  │ token-level softmax   │
   └──────────┬──────────┘  └──────────┬──────────┘  └──────────┬──────────┘
              │                       │                       │
              └───────────────────────┼───────────────────────┘
                                      │
                         Joint loss (weighted sum, see §5)



### Loss Function:
`L_total = 0.25·L_sentence + 0.25·L_target + 0.20·L_category + 0.30·L_span`

---

## 5. Training Details

| Parameter | Value |
|-----------|-------|
| Base Model | BERT-base-uncased (110M params) |
| Learning Rate | 2e-5 |
| Batch Size | 32 |
| Epochs | 10 (early stopping patience=3) |
| Optimizer | AdamW |
| Warmup Ratio | 0.1 |
| Weight Decay | 0.01 |
| Gradient Clipping | 1.0 |
| Max Sequence Length | 256 |

---

## 6. Evaluation Metrics

| Task | Metrics |
|------|---------|
| **Sentence Classification** | Accuracy, Macro-F1 |
| **Target Classification** | Accuracy, Macro-F1 |
| **Category Classification** | Accuracy, Macro-F1 |
| **Span Extraction** | Token-F1, Span-F1 (Exact & Partial) |
| **Joint Evaluation** | Exact-match accuracy, Composite Score |

### Expected Performance Gains:
- Sentence F1: 0.88 → **0.91** (+3%)
- Target F1: 0.73 → **0.80** (+7%)
- Span F1: 0.72 → **0.79** (+7%)

---

## 7. Research Questions

| ID | Question |
|----|----------|
| **RQ1** | How much information is lost with sentence-level only classification? |
| **RQ2** | Can target-aware annotations improve interpretation of claims? |
| **RQ3** | Does span-level supervision improve explainability? |
| **RQ4** | Does MTL outperform separate models? |
| **RQ5** | Do financial targets improve downstream tasks? |

---

## 8. Key Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| Annotation ambiguity | Clear guidelines + inter-annotator agreement (Kappa > 0.85) |
| Target granularity | 10 categories + 40 specific targets (balanced) |
| Overlapping spans | Minimal span principle + discourse markers |
| Domain-specific vocabulary | Finance experts as annotators |
| Mixed-role sentences | Span-level segmentation captures both roles |

---

## 9. Expected Contributions

1. **First multi-granular extension** of FinArg with span-level + target-aware annotations
2. **New benchmark dataset** for financial argument mining
3. **MTL framework** for joint modeling of related financial tasks
4. **Enhanced explainability** through span-level reasoning traces

---

## 10. Repository Structure

finarg-mtl/
├── config/
│   ├── default.yaml
│   ├── training.yaml
│   └── model.yaml
├── data/
│   ├── raw/
│   ├── annotated/
│   └── processed/
├── src/
│   ├── annotation/
│   │   ├── __init__.py
│   │   ├── annotator.py
│   │   ├── segmenter.py
│   │   └── schema.py
│   ├── modeling/
│   │   ├── __init__.py
│   │   ├── encoder.py
│   │   ├── heads.py
│   │   ├── mtl_model.py
│   │   └── losses.py
│   ├── training/
│   │   ├── __init__.py
│   │   ├── trainer.py
│   │   ├── optimizer.py
│   │   └── scheduler.py
│   ├── evaluation/
│   │   ├── __init__.py
│   │   ├── metrics.py
│   │   ├── evaluator.py
│   │   └── analysis.py
│   └── utils/
│       ├── __init__.py
│       ├── data_loader.py
│       ├── preprocessor.py
│       └── visualization.py
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_annotation_analysis.ipynb
│   ├── 03_model_training.ipynb
│   └── 04_results_analysis.ipynb
├── tests/
│   ├── test_annotation.py
│   ├── test_model.py
│   ├── test_training.py
│   └── test_evaluation.py
├── docs/
│   ├── README.md
│   ├── ANNOTATION_GUIDE.md
│   ├── DOCUMENTATION.md
│   └── API_REFERENCE.md
├── requirements.txt
├── setup.py
└── LICENSE