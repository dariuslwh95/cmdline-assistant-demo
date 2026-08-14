# Skill: Troubleshooting Scenario Development Guide

This document provides the guidelines and best practices for creating and refining troubleshooting scenarios. The goal is to build effective, consistent, and educational demonstrations that showcase the value of the `c` command-line assistant to a user who is learning Linux administration.

**Objective:** To define a standardized framework for scenario development, ensuring each demo is clear, repeatable, and effectively highlights how `c` simplifies complex troubleshooting tasks.

---

## Core Principles of a Good Scenario

A successful scenario is a narrative. It presents a relatable problem, guides the user through the confusion, and uses the `c` assistant as the hero that leads to a resolution.

1.  **Start with a "Why":** The scenario should begin with a common, real-world problem (e.g., "My disk is full but I can't find the files," "My application is slow").
2.  **Empathize with the Novice:** Write from the perspective of someone who doesn't know the answer. Use phrases like "This is confusing," "I don't know what this output means," to set the stage for `c` to provide clarity.
3.  **Show, Don't Just Tell:** The value of `c` is in its ability to interpret cryptic information. A good scenario pipes the raw, confusing output of a command (`lsof`, `dmesg`, `ss`) into `c` and shows how the assistant translates it into a simple, actionable explanation.
4.  **Focus on the Workflow:** The scenario should demonstrate a logical troubleshooting workflow. The `c` assistant should not just give the final answer, but guide the user through the *next step* (e.g., "Okay, you've found the port, now check the process status").

---

## Scenario Structure & Guidelines

Each scenario must be self-contained within its own directory and follow a standardized structure.

### 1. Directory Structure

Every new scenario should be placed in a numbered directory with a descriptive name. All scripts must be separated into their own files.

```
<scenario-number>-<scenario-name>/
├── scenario.md     # The main guide for this scenario.
├── setup.sh        # Main script to prepare the scenario.
├── cleanup.sh      # A script to undo the setup and revert all changes.
├── *.py            # Any helper Python scripts.
└── outputs/        # (Optional) A directory for expected log snippets or other static files.
```

### 2. `scenario.md` Template

Each `scenario.md` file must contain the following sections:

**`# Scenario: [Clear, Descriptive Title]`**
A one-sentence summary of the problem to be solved.

**`## 1. Objective`**
What the user will learn or understand by the end of the demo.

**`## 2. The Scripts`**
This section details the scripts used. Do not embed large scripts in the markdown. Instead, provide the filename and a brief explanation of what the script does. For short, one-line commands, they can be listed directly.

**`## 3. The Demonstration`**
This is the core of the document. It must be a step-by-step walkthrough:

1.  **Setup:** Instruct the user to run the `setup.sh` script.
2.  **The Problem:** Describe the symptoms from the novice's point of view. What do they see? Why is it confusing?
3.  **Troubleshooting with `c`:** This is a guided narrative.
    - Start with a plain-English question to `c`.
    - Show the command whose output will be piped to `c`.
    - Provide the full command, including the pipe to `c` and the question (e.g., `dmesg | c "Can you find any I/O errors in this log?"`).
    - Describe the *expected type* of response from `c` and how it helps move to the next step.
4.  **Resolution:** Explain how the information from `c` leads to the solution.
5.  **Cleanup:** Instruct the user to run the `cleanup.sh` script.
