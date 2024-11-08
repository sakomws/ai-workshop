
# Session Title: Low Latency on LLMs and Agent Workflows

Welcome to the **Low Latency on LLMs and Agent Workflows** session of the DevFest AI Workshop! This session will guide you through agentic workflows using Groq.

---

## Session Overview

**Instructor:** [Jose Menendez](https://www.linkedin.com/in/menendezp/)

**Duration:** 20min.

**Objective:**  
- Get an agentic workflow running with low latency LLMs in minutes.
- Orchestrate another workflow to formulate pytho code and execute it.
  
By the end of this session, you will have a deeper understanding of 
- Groq, LPU, and Low Latency LLMs.
- Agentic workflows.
- How to leverage [crewAI](https://crewai.com/) to build them without the hassle.

---

## Prerequisites

- Basic knowledge of LLM prompting
- Basic knowledge of Python
- Basic understanding of YAML

---

## Agenda

1. **Introduction**  
   - Overview of Groq, LPU, and Low Latency LLMs, open source models.

2. **Hands-on Activity**  
   - Create an out-of-the-box workflow with crewAI.
   - Make small adjustments to implement a coder workflow.

3. **Q&A and Discussion**  
   - Open floor for questions / ideas / discussions.

---

## Instructions

### Step 1: CrewAI quickstart.
It's a true quickstart, so you can just [follow the instructions](https://docs.crewai.com/quickstart).

### Step 2: X-Max tree example.
The examples in this folder are:
- `researchers`: Base workflow out of the box.
- `xmas-tree`: A modified version where a couple of agents generate a X-Max tree ASCII art.


### Step 3: Complete the Hands-on Exercise
Following the docs of CrewAI, use configurations to build a workflows that:

- **Exercise 1:** A workflow that takes a URL to read the content and generate a markdown summary of the content. For this you have to implement the `Scrape Website` tool.
- **Exercise 2:** Take it up a notch. Modify the basic researcher workflow to use web search and scraping in order to do an online investigation. 
- **Exercise 3:** Create a custom tool, that can take an audio file, send it to Groq to transcribe it and then summarize the content.

---

## Additional Resources

- **Documentation:**  
  - [Groq docs](https://console.groq.com/docs/overview)
  
- **Further Reading:**  
  - NA

---

## Solutions

- NA

---

## Contact

If you have questions during the workshop, please reach out to **[Jose Menendez]** or open an issue in the repository with label 6_groq.

Happy coding!
