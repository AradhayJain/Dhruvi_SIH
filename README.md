# AI-Based Dynamic Mental Health Monitoring & Distress Prediction System

## Overview

Victims and complainants of atrocities often experience prolonged psychological distress due to threats, intimidation, repeated court appearances, delays, social isolation, financial hardship, and rehabilitation challenges. Existing support mechanisms primarily focus on legal and financial assistance, with limited continuous monitoring of victim well-being.

Our solution is an **AI-powered, longitudinal victim well-being monitoring platform** that detects early signs of psychological distress, predicts escalation, and helps authorities and counsellors provide timely support.

The system follows a continuous loop:

> **Interact → Assess → Track → Predict → Alert → Intervene → Reassess**

## Key Features

### 🧠 Multimodal Distress Analysis

The system analyses multiple sources of interaction:

* Chatbot and text responses
* Voice/IVRS interactions
* Sentiment and emotion indicators
* Behavioural and engagement patterns
* Case-related risk factors
* Historical distress trends

### 📊 Dynamic Distress Score

Instead of performing a one-time assessment, the system maintains a **Dynamic Distress Risk Score** that changes over time based on the victim's interactions and behavioural patterns.

It tracks:

* Current distress level
* Historical trends
* Sudden changes in well-being
* Engagement deterioration
* Case-related stressors

### 🔮 Predictive Risk Modelling

The system predicts whether a victim's distress is likely to escalate in the near future.

Risk levels:

```text
LOW → MODERATE → HIGH → CRITICAL
```

This enables intervention **before a potential crisis emerges**.

### 🚨 Real-Time Risk Alerts

When predefined risk thresholds are crossed, the system can alert:

* Counsellors
* District authorities
* Designated officials

The system prioritises cases requiring human attention.

### 💡 Explainable AI

Every high-risk prediction is accompanied by understandable reasons, such as:

```text
Risk Score: 82/100

↑ Distress increased significantly
↑ Reported safety concerns
↑ Reduced engagement
↑ Negative sentiment trend
↑ Repeated court-related distress
```

This ensures that authorities can understand **why** a case was flagged rather than relying on a black-box prediction.

### 🤝 Intervention Recommendation

Based on detected risk factors, the system recommends appropriate support such as:

* Counselling
* Medical/clinical assessment
* Witness protection review
* Legal aid
* Relocation support
* Financial assistance
* Rehabilitation services

Final decisions remain with authorised human officials.

### 🌐 Multilingual Conversational AI

The platform is designed for multilingual interactions, allowing victims to communicate through supported Indian languages via:

* Chatbot
* Mobile application
* Web portal
* SMS
* IVRS/voice calls

## System Architecture

```text
Victim / Complainant
        ↓
Chatbot / IVRS / SMS / Mobile / Web
        ↓
Multimodal AI Processing
 ┌────────┼───────────┐
 ↓        ↓           ↓
NLP    Voice AI   Behavioural Analysis
 └────────┼───────────┘
          ↓
Dynamic Distress Engine
          ↓
Longitudinal Risk Prediction
          ↓
Explainable Risk Assessment
          ↓
 ┌────────┼────────────┐
 ↓        ↓            ↓
Alerts  Dashboard   Intervention
 └────────┼────────────┘
          ↓
      Human Review
          ↓
      Reassessment
          ↓
   Continuous Monitoring
```

## Core Innovation

The key innovation is the shift from **reactive, event-based victim support to proactive, continuous monitoring**.

Rather than assessing psychological distress only when a victim requests help, the system builds a longitudinal profile of the victim's well-being and identifies changes in distress over time.

This allows authorities to answer:

> **Who is at risk, why are they at risk, how is their condition changing, and what intervention should happen next?**

## Privacy & Safety

Because the platform handles highly sensitive victim information, it incorporates:

* Role-based access control
* Encryption
* Consent management
* Audit logs
* Data minimisation
* De-identified aggregate dashboards
* Human-in-the-loop decision making
* Explainable predictions

The system is designed as an **early-warning and decision-support system, not a replacement for professional mental-health diagnosis or human judgement**.

## Expected Impact

* Early detection of psychological distress
* Prevention of potential mental-health crises
* Faster counselling and support
* Better identification of vulnerable victims
* Improved coordination between authorities and support agencies
* Evidence-based policy and resource allocation
* Greater victim confidence in the justice and rehabilitation process

## Prototype Focus

The SIH prototype will demonstrate:

1. Multilingual victim chatbot
2. Text sentiment/emotion analysis
3. Voice-based distress indicators
4. Dynamic distress scoring
5. Longitudinal distress visualization
6. Predictive risk modelling
7. Explainable risk factors
8. Automated alerts
9. Intervention recommendations
10. District-level monitoring dashboard

> **Our goal is to transform victim support from a reactive process into a proactive, AI-assisted, continuous care and early-warning ecosystem.**
