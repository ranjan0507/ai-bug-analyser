from models.state import BugState
from models.schemas import InvestigationDecision

from utils.llm import get_llm

def investigation_decision(state:BugState):
	results=state["investigation_results"]
	llm=get_llm()
	llm_with_structure=llm.with_structured_output(InvestigationDecision)

	results_text="\n\n".join(
		[
			f"""
HYPOTHESIS {index}:

{result.model_dump_json(indent=2)}
"""		for index,result in enumerate(results,start=1)
		]
	)

	prompt=f"""
You are deciding what should happen after all debugging
hypotheses have been investigated.

You are given the investigation results for every hypothesis.

Your task is to decide whether the available evidence is sufficient
to proceed toward a final conclusion or whether additional human
clarification is required.

Your reason must explain only why the investigation results are
sufficient or insufficient.

Do not restate, expand, reinterpret, or introduce details about
the suspected bug or root cause in the reason.

Do NOT generate the final conclusion.
Do NOT generate a fix.
Do NOT create new hypotheses.
Do NOT reinterpret or invent evidence.

Set:

should_conclude = true
when the investigation results provide sufficient evidence to
confidently proceed toward determining the root cause.

should_ask_human = true
when the investigation results are ambiguous, conflicting, or
insufficient and additional information from the user is necessary.

Both values should not be true at the same time.

Provide a concise reason for your decision.

INVESTIGATION RESULTS:

{results_text}
"""
	decision=llm_with_structure.invoke(prompt)
	return {
		"investigation_decision":decision
	}