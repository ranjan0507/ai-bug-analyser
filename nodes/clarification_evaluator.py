from models.state import BugState
from models.schemas import InvestigationDecision

from utils.llm import get_llm

def clarification_evaluator(state:BugState):
	results=state["investigation_results"]
	interactions=state["human_interactions"]

	llm=get_llm()

	llm_with_structure=llm.with_structured_output(
		InvestigationDecision
	)

	results_text="\n\n".join(
		[
			f"""
HYPOTHESIS {index}:
{result.model_dump_json(indent=2)}
"""
	for index,result in enumerate(results,start=1)
		]
	)

	clarification_text="\n\n".join(
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
You are evaluating whether user clarification has resolved
the uncertainty in a debugging investigation.

You are given:

1. Completed investigation results.
2. User clarification obtained during Human-in-the-Loop interaction.

Your task is ONLY to decide whether the available information is
now sufficient to proceed toward a final conclusion.

You must evaluate the clarification against the existing hypotheses
and investigation results.

IMPORTANT:

The user's answer is new evidence.

Do not ignore, weaken, or treat the user's answer as merely contextual
information.

Determine whether the answer directly supports or rejects any existing
hypothesis.

For example, if a hypothesis concerns an input value and the user
provides that exact input value, use that information when determining
whether the hypothesis is sufficiently resolved.

Do NOT generate a final conclusion.
Do NOT generate a fix.
Do NOT create new hypotheses.
Do NOT invent evidence.

Set:

should_conclude = true
when the investigation results combined with the user clarification
provide sufficient evidence to determine the relevant cause among the
existing hypotheses.

Set:

should_ask_human = true
when important uncertainty still remains and another clarification
would materially help distinguish between the existing hypotheses.

Both values must not be true at the same time.

If the clarification directly resolves the uncertainty relevant to
one of the existing hypotheses, prefer should_conclude = true.

Your reason must explain only why the available information is
sufficient or insufficient.

INVESTIGATION RESULTS:

{results_text}

USER CLARIFICATIONS:

{clarification_text}
"""
	decision=llm_with_structure.invoke(prompt)

	return {
		"investigation_decision":decision
	}