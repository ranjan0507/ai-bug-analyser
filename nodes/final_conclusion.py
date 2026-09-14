from models.state import BugState
from models.schemas import FinalConclusion

from utils.llm import get_llm

def final_conclusion(state:BugState):
	results=state["investigation_results"]
	llm=get_llm()
	llm_with_structure=llm.with_structured_output(
		FinalConclusion
	)
	results_text="\n\n".join(
		[
			f"""
INVESTIGATION {index}:
{result.model_dump_json(indent=2)}
"""		for index,result in enumerate(results,start=1)
		]
	)

	prompt=f"""
You are determining the final conclusion of a debugging investigation.

You are given completed investigation results for all hypotheses.

Determine the most likely root cause based ONLY on the
investigation results and their collected evidence.

Rules:

- Use only the provided investigation results.
- Do not invent evidence.
- Do not introduce new hypotheses.
- Do not generate a fix or modified code.
- A supported hypothesis may be identified as the primary cause.
- Rejected hypotheses should not be identified as the primary cause.
- Inconclusive hypotheses should be included in unverified possibilities
  when relevant.
- Include contributing issues only when supported by the evidence.
- Set overall_confidence between 0.0 and 1.0.
- The decision should clearly summarize the final determination.

INVESTIGATION RESULTS:

{results_text}
"""	
	conclusion=llm_with_structure.invoke(prompt)
	return {
		"final_conclusion":conclusion
	}