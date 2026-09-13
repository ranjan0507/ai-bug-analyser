from models.state import BugState
from models.schemas import InvestigationPlan
from utils.llm import get_llm

from tools.code_inspector import TOOL_NAME as CODE_INSPECTOR_NAME
from tools.code_inspector import TOOL_DESCRIPTION as CODE_INSPECTOR_DESCRIPTION

from tools.stack_trace_parser import TOOL_NAME as STACK_PARSER_NAME
from tools.stack_trace_parser import TOOL_DESCRIPTION as STACK_PARSER_DESCRIPTION


def investigation_planner(state:BugState):
	llm=get_llm()
	current_index=state["current_hypothesis_index"]
	current_hypothesis=state["hypotheses"][current_index]

	llm_with_structure=llm.with_structured_output(InvestigationPlan)

	available_tools=f"""
TOOL: {CODE_INSPECTOR_NAME}

{CODE_INSPECTOR_DESCRIPTION}p/


TOOL: {STACK_PARSER_NAME}

{STACK_PARSER_DESCRIPTION}
"""
	prompt=f"""
You are an evidence-driven debugging investigation planner.

Your task is to create an investigation plan for ONE hypothesis.

You are NOT investigating yet.

You are only deciding:

- What should be checked
- How it should be checked
- Whether LLM reasoning or an available tool should be used
- What evidence each step should attempt to obtain

RULES:

1. Create a logical sequence of investigation steps.

2. Each step must use one of these methods:

- tool
- llm_reasoning

3. If method is "tool", tool_name MUST be one of
the available tools provided below.

4. Do not invent tools.

5. Use a tool when deterministic evidence can be
obtained from it.

6. Use llm_reasoning when interpretation or logical
analysis is required.

7. Do NOT investigate the hypothesis.

8. Do NOT generate observations or evidence.

9. Do NOT decide whether the hypothesis is correct.

10. Do NOT generate a fix.


CURRENT HYPOTHESIS:

{current_hypothesis.model_dump_json(indent=2)}


CODE:

{state["code"]}


ERROR:

{state["error"]}


STACK TRACE:

{state.get("stack_trace")}


BUG ANALYSIS:

{state["bug_analysis"].model_dump_json(indent=2)}


AVAILABLE TOOLS:

{available_tools}
"""
	plan = llm_with_structure.invoke(prompt)

	return {
        "current_investigation_plan": plan
    }