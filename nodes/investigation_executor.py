from models.state import BugState
from models.schemas import InvestigationStep,ToolResult
from utils.llm import get_llm
from tools.stack_trace_parser import StackTraceParser
from tools.code_inspector import CodeInspector

def execute_tool_step(step:InvestigationStep,state:BugState)->ToolResult:
	if step.tool_name=="code_inspector":
		inspector=CodeInspector(state["code"])

		if step.tool_operation=="get_line":
			return inspector.get_line(**step.tool_arguments)
		elif step.tool_operation=="get_lines":
			return inspector.get_lines(**step.tool_arguments)
		elif step.tool_operation=="search":
			return inspector.search(**step.tool_arguments)
		else:
			return ToolResult(
				tool_name="code_inspector",
				success=False,
				error=(
					f"Unsupported operation: {step.tool_operation}"
				)
			)

	if step.tool_name=="stack_trace_parser":
		parser=StackTraceParser(
			state.get("stack_trace")
		)
		if step.tool_operation=="parse":
			return parser.parse()
		else:
			return ToolResult(
				tool_name="stack_trace_parser",
				success=False,
				error=(
					f"Unsupported operation: {step.tool_operation}"
				)
			)
		
	else:
		return ToolResult(
            tool_name=step.tool_name or "unknown",
            success=False,
            error="Unknown tool."
        )


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
			if result.success:
				observations.extend(result.observations)
				evidence.extend(result.evidence)
			else:
				observations.append(
					f"Tool exectuion failed {result.error}"
				)

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

	return {
		"current_observations":observations,
		"current_evidence":evidence
	}