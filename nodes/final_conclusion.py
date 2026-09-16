from models.state import BugState
from models.schemas import FinalConclusion

from utils.llm import get_llm

def final_conclusion(state:BugState):
	results=state["investigation_results"]
	llm=get_llm()
	llm_with_structure=llm.with_structured_output(FinalConclusion)
	interactions=state["human_interactions"]
	results_text="\n\n".join(
		[
			f"""
INVESTIGATION {index}:
{result.model_dump_json(indent=2)}
"""		for index,result in enumerate(results,start=1)
		]
	)

	clarification_text = "\n\n".join(
    [
        f"""
QUESTION:
{interaction.question}

ANSWER:
{interaction.answer}

REASON QUESTION WAS ASKED:
{interaction.reason_question_was_asked}

RELATED HYPOTHESES:
{interaction.related_hypotheses}
"""
        for interaction in interactions
        if interaction.answer is not None
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

User clarifications are part of the available evidence.

When a user clarification directly resolves uncertainty relevant
to an existing hypothesis, incorporate that information into the
final conclusion.

Do not list a hypothesis as an unverified possibility if the
provided user clarification establishes the relevant fact needed
to support or reject it.

Confidence should reflect the strength of the combined investigation
results and user-provided evidence.

INVESTIGATION RESULTS:

{results_text}

USER CLARIFICATIONS:

{clarification_text}
"""	
	conclusion=llm_with_structure.invoke(prompt)
	return {
		"final_conclusion":conclusion
	}