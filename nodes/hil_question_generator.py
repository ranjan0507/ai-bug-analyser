from models.state import BugState
from models.schemas import HumanInteraction

from utils.llm import get_llm

def hil_question_generator(state:BugState):
	results=state["investigation_results"]
	llm=get_llm()
	llm_with_structure=llm.with_structured_output(HumanInteraction)

	results_text="\n\n".join(
		[
			f"""
HYPOTHESIS {index}:
{result.model_dump_json(indent=2)}
"""	
	for index,result in enumerate(
		results,start=1
	)
		]
	)

	prompt=f"""
You are requesting clarification from a user during a debugging
investigation.

The investigation results are ambiguous, conflicting, or insufficient
to confidently determine the root cause.

Generate ONE specific question that would provide useful information
for resolving the uncertainty.

Rules:

- Ask only one question.
- The question must be specific and directly relevant.
- Do not ask vague questions such as "Can you provide more details?"
- Do not generate a diagnosis.
- Do not generate a fix.
- Do not introduce new hypotheses.
- Explain why the question is necessary.
- related_hypotheses must contain the 1-based indices of hypotheses
  that the question is intended to clarify.
- Set answer to null.

INVESTIGATION RESULTS:

{results_text}
"""
	interaction=llm_with_structure.invoke(prompt)
	interaction.answer=None

	return{
		"human_interactions":[
			*state["human_interactions"],
			interaction
		]
	}