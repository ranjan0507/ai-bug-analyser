from models.state import BugState
from models.schemas import HypothesisValidation
from utils.llm import get_llm


def hypothesis_validator(state: BugState):
    llm = get_llm()

    structured_llm = llm.with_structured_output(
        HypothesisValidation
    )

    hypotheses_text = "\n\n".join(
        f"Hypothesis {i + 1}:\n"
        f"{hypothesis.model_dump_json(indent=2)}"
        for i, hypothesis in enumerate(state["hypotheses"])
    )

    prompt = f"""
You are a debugging hypothesis quality validator.

Review the generated hypotheses.

Your job is NOT to generate new hypotheses.
Your job is to filter weak, redundant, or invalid hypotheses.

Check:

1. Does each hypothesis describe a possible ROOT CAUSE?
2. Are any hypotheses merely consequences of another hypothesis?
3. Are any hypotheses just reworded versions of each other?
4. Is each hypothesis independently testable?
5. Is each hypothesis plausible based on the available information?

Remove hypotheses that are:

- Consequences rather than root causes
- Redundant
- Weak or invented
- Not independently testable

Keep only distinct, meaningful hypotheses.

A single strong hypothesis is better than multiple
redundant hypotheses.

BUG ANALYSIS:

{state["bug_analysis"].model_dump_json(indent=2)}

GENERATED HYPOTHESES:

{hypotheses_text}
"""

    result = structured_llm.invoke(prompt)

    return {
        "hypotheses": result.filtered_hypotheses
    }