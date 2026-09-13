from models.state import BugState
from models.schemas import InvestigationResult
from utils.llm import get_llm
from tools.stack_trace_parser import StackTraceParser
from tools.code_inspector import CodeInspector

def execute_tool_step(step,state):
	pass

def execute_reasoning_step(step,state):
	pass

def investigation_executor(state:BugState):
	plan=state['current_investigation_plan']
	current_idx=state['current_hypothesis_index']
	hypothesis=state['hypotheses'][current_idx]

	observations=[]
	evidence=[]

	for step in plan.steps:

		if step.method=="tool":
			result=execute_tool_step(step,state)
			observations.extend(result)
			for item in result.evidence:
				evidence.append(item.description)

		if step.method=="llm_reasoning":
			result = execute_reasoning_step(
                step,
                state,
                hypothesis,
                observations,
                evidence
            )
			observations.extend(
                result["observations"]
            )
			evidence.extend(
                result["evidence"]
			)
	investigation_result=InvestigationResult(
		hypothesis=hypothesis,
		plan=plan
		observations=observations,
		evidence=evidence
	)