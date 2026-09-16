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
  The collected evidence directly supports that this hypothesis
  explains the reported failure in this specific case.

- rejected:
  The collected evidence directly contradicts the hypothesis.

- inconclusive:
  The hypothesis is plausible or the code contains a potentially
  problematic pattern, but the available evidence does not establish
  that this hypothesis actually caused the reported failure.

Important distinction:

A risky or incorrect code pattern alone is NOT sufficient to mark
a hypothesis as supported.

For example:

- Evidence that unchecked input handling exists does not prove that
  invalid input occurred during this failure.

- Evidence that an index is not bounds-checked does not prove that
  an out-of-bounds index was used during this failure unless the
  investigation provides evidence connecting it to the reported crash.

Use "inconclusive" whenever the hypothesis is possible but requires
runtime information, user input, or other missing evidence to confirm
that it caused this specific failure.

Confidence must reflect how strongly the collected evidence supports
the verdict.

Important rules:

- Base your evaluation only on the provided observations and evidence.
- Do not invent new evidence.
- Do not generate a fix.
- Do not introduce a new hypothesis.
- Do not determine the final root cause.
- Evaluate only the current hypothesis.
- Do not treat a hypothetical execution path as evidence that it
  actually occurred.
- Distinguish between "this code can fail this way" and
  "this failure was caused this way."

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