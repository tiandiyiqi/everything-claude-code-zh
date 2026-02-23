# Interactive Discussion Mode

A systematic skill for conducting in-depth product discussions through structured multiple-choice questions.

## Overview

This skill transforms Claude into a collaborative product discussion partner, using a systematic approach to explore product requirements, technical decisions, and implementation details through interactive multiple-choice questions.

## Key Features

- **10 Discussion Dimensions**: Covers functionality, technology, design, business, UX, performance, security, market competition, user research, and data analysis
- **3-Phase Process**: Requirements understanding → Multi-dimensional analysis → Solution refinement
- **Choice-Based Interaction**: Primarily uses multiple-choice questions to maintain focus and clarity
- **Dynamic Adaptation**: Adjusts follow-up questions based on your responses

## When to Use

- Clarifying product requirements before planning
- Evaluating technical architecture options
- Discussing UX/UI design decisions
- Assessing business viability
- Before executing `/plan` command

## Activation

Trigger this skill by saying:
- "Let's discuss [topic]"
- "I want to have an interactive discussion about [topic]"
- "Enable interactive discussion mode"

## Integration with Other Skills

This skill works best as the first step in the development workflow:

```
Interactive Discussion → Planning → TDD Development → Code Review → Security Review → Verification
```

## Example Usage

```
User: "Let's discuss a new user authentication system"

Claude: [Enters interactive discussion mode]
# Interactive Discussion: User Authentication System

## Phase 1: Requirements Understanding

1. Primary user base?
   A. Enterprise employees
   B. External customers
   C. Mixed user groups
   D. Other (please specify)

2. Core authentication priority?
   A. Username/password
   B. OAuth2 third-party login
   C. Multi-factor authentication
   D. Hybrid approach
```

## Documentation

For detailed documentation in Chinese, see `SKILL.md` in this directory.
