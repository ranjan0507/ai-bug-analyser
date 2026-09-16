from models.state import BugState
from models.schemas import InvestigationDecision
from models.schemas import InvestigationDecision, Verdict
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

	supported_results=[
		result
		for result in results
		if result.verdict==Verdict.SUPPORTED
	]

	inconclusive_results=[
		result
		for result in results
		if result.verdict==Verdict.INCONCLUSIVE
	]

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

An inconclusive investigation result must not be treated
as confirmation of a root cause.

If all plausible explanations remain inconclusive and the
missing information can reasonably be provided by the user,
request human clarification.

Do not conclude merely because the code contains unsafe,
incorrect, or potentially problematic patterns.

Do NOT generate the final conclusion.
Do NOT generate a fix.
Do NOT create new hypotheses.
Do NOT reinterpret or invent evidence.

Decision rules:

- If one or more hypotheses are supported with sufficient evidence
  explaining the reported failure, you may conclude.

- If hypotheses remain inconclusive because runtime information,
  user input, environment details, or execution behavior is missing,
  ask the human.

- If all hypotheses are inconclusive, do NOT claim the root cause
  is confirmed.

- Distinguish between a confirmed code defect and a confirmed cause
  of the reported failure.

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
	if not supported_results and inconclusive_results:
		return {
			"investigation_decision":InvestigationDecision(
				should_ask_human=True,
				should_conclude=False,
				reason=(
					"The investiggation decision did not confirm any hypothesis, "
					"and one or more plausible hypothesis remain inconclusive"
				)
			)
		}
	
	decision=llm_with_structure.invoke(prompt)
	return {
		"investigation_decision":decision
	}