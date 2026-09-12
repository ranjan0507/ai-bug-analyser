from models.state import BugState
from models.schemas import HypothesisList
from utils.llm import get_llm

def generate_hypothesis(state:BugState):
	llm=get_llm()
	llm_with_structure=llm.with_structured_output(HypothesisList)

	prompt=f"""
You are an evidence-driven debugging investigator.

Generate only hypotheses that are meaningfully plausible.

Do not invent weak or redundant hypotheses merely to reach a
specific number.

Based on the code profile and bug analysis, generate between
1 and 4 competing hypotheses that could explain the reported problem.

Important rules:

- Generate between 1 and 4 genuinely distinct hypotheses.
- Each hypothesis must represent a different possible ROOT CAUSE,
  not a consequence or rewording of another hypothesis.
- Do not generate multiple hypotheses that describe different stages
  of the same causal chain.

For example:

Bad:
1. Array index is out of bounds
2. Out-of-bounds access causes undefined behavior

These describe the same underlying issue.

Good:
1. Incorrect loop boundary
2. Unexpected data structure state
3. Earlier memory corruption affecting the index

- Each hypothesis must be independently testable.
- Explain why the hypothesis is plausible.
- Clearly state what should be checked.
- Describe what evidence would support the hypothesis.
- Do not generate a fix.
- Do not assume any hypothesis is confirmed.

ORIGINAL CODE:
{state["code"]}

REPORTED ERROR:
{state["error"]}

STACK TRACE:
{state.get("stack_trace")}

CODE PROFILE:
{state["code_profile"].model_dump_json(indent=2)}

BUG ANALYSIS:
{state["bug_analysis"].model_dump_json(indent=2)}
"""
	result = llm_with_structure.invoke(prompt)

	return {
        "hypotheses": result.hypotheses,
        "current_hypothesis_index": 0
    }