from models.state import BugState
from models.schemas import InvestigationResult

from utils.llm import get_llm

def investigation_evaluator(state:BugState):
	current_idx=state["current_hypothesis_index"]
	hypothesis=state["hypotheses"][current_idx]
	plan=state["current_investigation_plan"]
	observations=state["current_observations"]
	evidence=state["current_evidence"]

	llm=get_llm()
	llm_with_structure=llm.with_structured_output(InvestigationResult)

	evidence_text="\n".join(
		[
			f"[{item.source}] {item.description}"
			for item in evidence
		]
	)

	observations_text="\n".join(observations)

	prompt=f"""
You are evaluating the result of ONE debugging hypothesis investigation.

Your task is to determine whether the collected evidence supports,
rejects, or is insufficient to evaluate the hypothesis.

You are NOT determining the final root cause of the entire bug.

You must choose one verdict:

- supported:
  The collected evidence directly supports the hypothesis.

- rejected:
  The collected evidence contradicts the hypothesis.

- inconclusive:
  The available evidence is insufficient to confidently support
  or reject the hypothesis.

Confidence must be between 0.0 and 1.0.

Important rules:

- Base your evaluation only on the provided observations and evidence.
- Do not invent new evidence.
- Do not generate a fix.
- Do not introduce a new hypothesis.
- Do not determine the final root cause.
- Evaluate only the current hypothesis.

CURRENT HYPOTHESIS:

{hypothesis.model_dump_json(indent=2)}

INVESTIGATION PLAN:

{plan.model_dump_json(indent=2)}

OBSERVATIONS:

{observations_text}

EVIDENCE:

{evidence_text}
"""
	evaluation=llm_with_structure.invoke(prompt)

	investigation_result=InvestigationResult(
		hypothesis=hypothesis,
		plan=plan,
		observations=observations,
		evidence=evidence,
		verdict=evaluation.verdict,
		confidence=evaluation.confidence
	)	

	return {
		"investigation_results":[
			*state["investigation_results"],
            investigation_result
		]
	}