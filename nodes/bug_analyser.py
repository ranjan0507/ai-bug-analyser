from models.schemas import BugAnalysis
from models.state import BugState
from utils.llm import get_llm

def bug_analyzer(state:BugState):
	llm=get_llm()
	llm_with_structure=llm.with_structured_output(BugAnalysis)

	prompt=f"""
You are a bug understanding system.

Your job is to understand the reported problem before
generating hypotheses or attempting a fix.

Analyze the following:

1. What is the code trying to do?
2. What behavior is expected?
3. What behavior is actually occurring?
4. What is the failure context?
5. Which areas of the code should be investigated further?

Do NOT conclude what caused the bug.

You may identify suspicious areas and describe what
should be investigated, but do not state that any
specific issue is the confirmed cause.

For example:
Good: "The loop boundary and vector indexing should be investigated."
Bad: "The loop causes an out-of-bounds access."

Do NOT suggest a fix.
Do NOT generate hypotheses.

Use the full original code along with the code profile
and reported error.

FULL CODE:
{state["code"]}

ERROR:
{state["error"]}

STACK TRACE:
{state.get("stack_trace")}

CODE PROFILE:
{state["code_profile"].model_dump_json(indent=2)}
"""
	analysis=llm_with_structure.invoke(prompt)
	return {
		"bug_analysis":analysis
	}