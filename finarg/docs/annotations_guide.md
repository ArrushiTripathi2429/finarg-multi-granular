# FinArg-MTL Annotation Guide

> **A Step-by-Step Guide for Annotating Financial Arguments in Earnings Conference Calls**

---

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Annotation Schema](#annotation-schema)
4. [Step-by-Step Annotation Process](#step-by-step-annotation-process)
5. [Detailed Guidelines with Examples](#detailed-guidelines-with-examples)
6. [Common Pitfalls & Solutions](#common-pitfalls--solutions)
7. [Quality Control](#quality-control)
8. [Frequently Asked Questions](#frequently-asked-questions)
9. [Glossary](#glossary)

---

## 1. Introduction

### Purpose of This Guide

This guide is designed for annotators who will label financial sentences from earnings conference calls. You'll learn how to:

- Identify whether a sentence is a **Claim** or **Premise**
- Determine the **financial target** being discussed
- Assign **target categories**
- Break sentences into **argumentative spans**
- Label each span as **premise_span** or **claim_span**

### What is Financial Argument Mining?

Financial argument mining is the process of identifying and analyzing arguments in financial texts (like earnings calls). In simple terms:

- A **Claim** is the main point, conclusion, or forecast
- A **Premise** is evidence, reason, or support for the claim

**Example:**
> "Because sales increased, we expect higher revenue next quarter."
> - Premise: "Because sales increased" (evidence)
> - Claim: "we expect higher revenue next quarter" (conclusion)

---

## 2. Getting Started

### Prerequisites
- Basic understanding of business/financial terms
- Familiarity with earnings conference calls
- Patience and attention to detail

### Tools You'll Need
- Access to earnings call transcripts
- Annotation platform (e.g., LabelStudio, Doccano, or custom tool)
- This guide (keep it open while annotating!)

### Time Commitment
- **Training**: 2-3 hours reading this guide
- **Practice**: 1-2 hours on sample sentences
- **Full annotation**: ~2-5 minutes per sentence (varies by complexity)

---

## 3. Annotation Schema

### Overview

Each sentence receives **4 types of annotations**:


### 3.1 Sentence Label

| Label | Definition | When to Use |
|-------|------------|-------------|
| **Claim** | Main assertion, conclusion, forecast, or opinion | The sentence makes a new point or prediction |
| **Premise** | Supporting evidence, reason, context, or background | The sentence provides justification or context |

#### Quick Check:
- Does this sentence assert something new? → **Claim**
- Does this sentence provide evidence or context? → **Premise**

### 3.2 Target

The **specific financial variable** or business topic being discussed.

#### Complete Target List:

| Target | Definition | Example |
|--------|------------|---------|
| **revenue** | Total income from sales | "Revenue increased 10%" |
| **revenue growth** | Rate of revenue increase | "Revenue growth accelerated" |
| **gross margin** | Profit after cost of goods sold | "Gross margin improved" |
| **operating margin** | Profit after operating expenses | "Operating margin expanded" |
| **net income** | Final profit after all expenses | "Net income beat estimates" |
| **earnings** | Company profits | "Earnings exceeded guidance" |
| **EPS** | Earnings per share | "EPS grew 15%" |
| **demand** | Customer demand for products | "Demand remains strong" |
| **sales volume** | Number of units sold | "Sales volume increased" |
| **pricing** | Price changes or strategy | "We raised prices 5%" |
| **guidance** | Future predictions | "Guidance for Q4 is positive" |
| **outlook** | Future expectations | "Outlook remains uncertain" |
| **COGS** | Cost of goods sold | "COGS increased due to raw materials" |
| **operating expenses** | Day-to-day costs | "Operating expenses were reduced" |
| **freight costs** | Shipping/delivery costs | "Freight costs remain elevated" |
| **labor costs** | Employee-related costs | "Labor costs increased 8%" |
| **CAPEX** | Capital expenditure | "CAPEX for new equipment" |
| **R&D** | Research and development | "R&D spending increased" |
| **acquisitions** | Company purchases | "Acquisitions contributed to growth" |
| **capital spending** | Investment in assets | "Capital spending on new facilities" |
| **cash flow** | Cash in/out of company | "Cash flow remained strong" |
| **debt** | Money owed | "We reduced debt significantly" |
| **liquidity** | Available cash/access to cash | "Liquidity position is healthy" |
| **working capital** | Operational liquidity | "Working capital improved" |
| **supply chain** | Supplier/distribution network | "Supply chain challenges persist" |
| **inventory** | Goods in stock | "Inventory levels are high" |
| **production** | Manufacturing output | "Production capacity increased" |
| **capacity** | Production ability | "Capacity utilization is high" |
| **market share** | Company's portion of market | "Market share grew 2%" |
| **competition** | Competitive position | "Competition intensified" |
| **competitive position** | Standing vs competitors | "Our competitive position strengthened" |
| **regulatory risk** | Government regulation threat | "Regulatory risk increased" |
| **restructuring** | Organizational changes | "Restructuring will save costs" |
| **business strategy** | Overall company direction | "Strategy focuses on growth" |
| **new initiatives** | New projects/programs | "New initiatives launched" |

### 3.3 Target Category

Broad grouping of related targets:

| Category | Description | Examples |
|----------|-------------|----------|
| **guidance** | Future-oriented predictions | revenue growth, guidance, outlook, EPS guidance |
| **profitability** | Money-making metrics | margins, net income, earnings, gross margin, operating margin |
| **revenue** | Income from sales | revenue, revenue growth, sales volume, pricing, market share |
| **cost structure** | Company's costs | COGS, operating expenses, freight costs, labor costs |
| **liquidity** | Cash/funding position | cash flow, debt, liquidity, working capital |
| **investment** | Company spending | CAPEX, R&D, acquisitions, capital spending |
| **operations** | Day-to-day business | supply chain, inventory, production, capacity |
| **market** | Competitive landscape | market share, competition, competitive position |
| **risk** | Threats/uncertainties | regulatory risk, currency risk, economic risk |
| **strategy** | Company plans | restructuring, business strategy, new initiatives |

### 3.4 Spans

**Break the sentence into logical segments** and label each as:

| Span Label | Definition | Notes |
|------------|------------|-------|
| **premise_span** | Evidence, reason, support, context | Usually starts with because, since, although, despite, due to |
| **claim_span** | Main point, conclusion, assertion | Usually starts with we expect, we believe, we project, we forecast |
| **non_argumentative_span** | Background information | Use sparingly, only for pure context |

#### Important: Span Segmentation Rules

1. **Use discourse markers as guides** (not rigid rules):
   - Concessive: *although, even though, despite, in spite of*
   - Causal: *because, since, due to, as a result of*
   - Result: *therefore, so, thus, consequently, hence*
   - Contrast: *but, however, while, whereas, yet*
   - Conditional: *if, unless, provided that*

2. **Minimal span principle**: Label the smallest unit that makes sense

3. **Avoid arbitrary chunks**: Don't split mid-thought

---

## 4. Step-by-Step Annotation Process

### The 5-Step Pipeline

```mermaid
graph TD
    A[Read the Sentence] --> B{Step 1: Is it a<br>Claim or Premise?}
    B --> C[Step 2: What's the<br>Financial Target?]
    C --> D[Step 3: Identify the<br>Target Category]
    D --> E[Step 4: Split into<br>Argumentative Spans]
    E --> F[Step 5: Label Each Span]
    F --> G[Export to JSON]


