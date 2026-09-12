from models.state import BugState
from models.schemas import CodeProfile
from utils.llm import get_llm

def context_profiler(state: BugState):
	llm=get_llm()
	llm_with_structure=llm.with_structured_output(CodeProfile)

	prompt = f"""
You are a code profiling system.

Your job is to understand the submitted code WITHOUT diagnosing
or attempting to fix the bug.

Analyze the code and identify:

1. Programming language
2. Libraries or dependencies used
3. Overall code structure
4. Important components such as functions, classes, loops,
   API calls, data structures, or important operations

Do not explain what caused the reported error.
Do not investigate the bug.
Only profile the technical context of the code.

CODE:
{state["code"]}

ERROR MESSAGE:
{state["error"]}

STACK TRACE:
{state.get("stack_trace")}
"""
	profile = llm_with_structure.invoke(prompt)
	return {
		'code_profile':profile
	}