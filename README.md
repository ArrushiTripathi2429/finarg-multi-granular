# FinArg-MoE: Mixture of Experts for Multi-Granular Financial Argument Mining

> **A Multi-Task, Multi-Expert Framework for Financial Argument Mining in Earnings Conference Calls**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Hugging Face](https://img.shields.io/badge/🤗-Transformers-orange)](https://huggingface.co/)
[![Research](https://img.shields.io/badge/Research-MoE-red)]()

---

##  Table of Contents
1. [Overview](#-overview)
2. [Problem Statement](#-problem-statement)
3. [Key Contributions](#-key-contributions)
4. [Methodology](#-methodology)
5. [Dataset](#-dataset)
6. [Architecture](#-architecture)
7. [Installation](#-installation)
8. [Usage](#-usage)
9. [Training](#-training)
10. [Evaluation](#-evaluation)
11. [Results](#-results)
12. [Project Structure](#-project-structure)
13. [Future Work](#-future-work)
14. [Citation](#-citation)
15. [Contact](#-contact)

---

##  Overview

**FinArg-MoE** is a novel framework for financial argument mining that combines:
- **Multi-Granular Annotations** (Sentence-level + Span-level + Target-aware)
- **Mixture of Experts (MoE)** Architecture
- **Multi-Task Learning** (4 tasks jointly)
- **Domain-Specialized Models**

Traditional financial argument mining treats each sentence as a single argument unit (Claim/Premise). This ignores three critical aspects:

1. **What** financial topic is being discussed (revenue, margins, guidance, etc.)
2. **How** a sentence can contain multiple argumentative functions (mixed premise + claim)
3. **Why** a model made a particular prediction (explainability)

### Our Solution

| Component | Description |
|-----------|-------------|
| **Mixture of Experts** | 3 specialized models (Guidance, Revenue/Profitability, Strategy/Operations) |
| **Router/Gate** | Dynamically routes each sentence to the best expert |
| **Multi-Task Learning** | 4 tasks: Sentence Label, Target, Category, Span Tagging |
| **Explainability** | Span-level reasoning traces for model predictions |

---

##  Problem Statement

### Current Limitation
Input: "Even with strong demand, we expect slowdown in Q4."
Output: "claim"  (Too coarse, no context)


### Our Extended Approach

```json
{
  "text": "Even with strong demand, we expect slowdown in Q4.",
  "sentence_label": "claim",
  "target": "growth forecast",
  "target_category": "guidance",
  "spans": [
    {"text": "Even with strong demand", "label": "premise_span"},
    {"text": "we expect slowdown in Q4", "label": "claim_span"}
  ],
  "expert_used": "guidance_expert",
  "routing_weight": 0.92
}

┌─────────────────────────────────────────────────────────────────┐
│                    5-STEP ANNOTATION PIPELINE                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  STEP 1: Retain Original Sentence Labels                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Input: Raw sentence from FinArg dataset                │  │
│  │  Output: Sentence label (Claim/Premise)                 │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              ▼                                  │
│  STEP 2: Add Target & Target Category Annotations              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Input: Sentence with label                             │  │
│  │  Output: Target (specific) + Target Category (broad)    │  │
│  │  Example: "margins outlook" + "profitability"          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              ▼                                  │
│  STEP 3: Logical-Syntactic Segmentation                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Input: Annotated sentence                              │  │
│  │  Output: Segmented clauses/phrases                      │  │
│  │  Method: Discourse marker-based (because, although, etc.)│  │
│  └──────────────────────────────────────────────────────────┘  │
│                              ▼                                  │
│  STEP 4: Assign Span-Level Argument Roles                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Input: Segmented sentence                              │  │
│  │  Output: premise_span / claim_span labels               │  │
│  │  Method: Argument role classification                   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              ▼                                  │
│  STEP 5: Integrate into Unified Structured JSON               │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Input: All annotations                                 │  │
│  │  Output: Structured JSON with character offsets         │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

 ### 10 Target Categories
text
guidance, profitability, revenue, cost_structure,
liquidity, investment, operations, market, risk, strategy

### 40+ Specific Targets
Category	Examples
guidance :	growth forecast, revenue guidance, margin outlook, EPS guidance
profitability	: margins, net income, earnings, gross margin, operating margin
revenue	: revenue growth, sales volume, pricing, market share
cost_structure :	COGS, operating expenses, freight costs, labor costs
liquidity	: cash flow, debt, liquidity, working capital
investment	: CAPEX, R&D, acquisitions, capital spending
operations :	supply chain, inventory, production, capacity
market :	competition, competitive position, industry trends

 ### Dataset Overview
Feature	Value
Source	Earnings Conference Calls (Facebook, Amazon, Apple, Microsoft)
Total Sentences	7,753
Premises	4,062 (52.4%)
Claims	3,691 (47.6%)
Average Sentence Length	22.4 words
Max Sentence Length	126 words
Source	TheFinAI/finarg-ecc-auc_train

### Architecture 
```
┌─────────────────────────────────────────────────────────────────┐
│                    FINARG-MOE ARCHITECTURE                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Input: "Although freight costs remain elevated..."           │
│                         │                                       │
│                         ▼                                       │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │              Shared BERT Encoder                        │  │
│  │  (ProsusAI/finbert - Domain-specific)                  │  │
│  └─────────────────────────────────────────────────────────┘  │
│                         │                                       │
│                         ▼                                       │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │                   ROUTER / GATE                         │  │
│  │  Takes BERT embedding → Outputs scores for 3 experts   │  │
│  │  Top-2 during training, Top-1 during inference        │  │
│  └─────────────────────────────────────────────────────────┘  │
│                         │                                       │
│         ┌───────────────┼───────────────┐                     │
│         │               │               │                     │
│         ▼               ▼               ▼                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                    │
│  │ EXPERT 1 │  │ EXPERT 2 │  │ EXPERT 3 │                    │
│  │ GUIDANCE │  │ REVENUE/ │  │ STRATEGY/│                    │
│  │          │  │PROFITABIL│  │OPERATION │                    │
│  │ Fine-    │  │ Fine-    │  │ Fine-    │                    │
│  │ tuned on │  │ tuned on │  │ tuned on │                    │
│  │ 2,500    │  │ 3,000    │  │ 2,253    │                    │
│  │ sent.    │  │ sent.    │  │ sent.    │                    │
│  └──────────┘  └──────────┘  └──────────┘                    │
│         │               │               │                     │
│         └───────────────┼───────────────┘                     │
│                         │                                       │
│                         ▼                                       │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  Output: Weighted Combination of Expert Predictions    │  │
│  │  - Sentence Label (Claim/Premise)                      │  │
│  │  - Target (40+ classes)                                │  │
│  │  - Target Category (10 classes)                        │  │
│  │  - Spans (BIO labels per token)                        │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```





