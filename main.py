from nodes.context_profiler import context_profiler
from nodes.bug_analyser import bug_analyzer
from nodes.hypothesis_generator import generate_hypothesis
from nodes.validate_hypothesis import hypothesis_validator
from nodes.investigation_planner import investigation_planner
from nodes.investigation_evaluator import investigation_evaluator
from nodes.investigation_executor import investigation_executor
from nodes.hypothesis_controller import prepare_next_hypothesis

def main():

    state = {
        "code": """
#include <iostream>
#include <vector>

using namespace std;

int main() {
    vector<int> nums = {1, 2, 3};

    int index;
    cin >> index;

    cout << nums[index] << endl;

    return 0;
}
""",

"error": "Segmentation fault",

"stack_trace": """
Segmentation fault
main.cpp:12
main()
""",
"code_profile": None,
    "bug_analysis": None,

    "hypotheses": [],
    "current_hypothesis_index": 0,

    "current_investigation_plan": None,
    "current_observations": [],
    "current_evidence": [],

    "investigation_results": [],

    "human_interactions": [],
    "clarification_count": 0,

    "final_conclusion": None,
    "fix": None
    }

    profile_result = context_profiler(state)
    state.update(profile_result)

    bug_analysis_result = bug_analyzer(state)
    state.update(bug_analysis_result)

    print("CODE PROFILE:\n")
    print(state["code_profile"].model_dump_json(indent=2))
    print("\nBUG REPORT:\n")
    print(state["bug_analysis"].model_dump_json(indent=2))

    hypothesis_result=generate_hypothesis(state)
    state.update(hypothesis_result)

    validation_result = hypothesis_validator(state)
    state.update(validation_result)

    print("\nHYPOTHESES:\n")

    for index, hypothesis in enumerate(state["hypotheses"], start=1):
        print(f"\nHypothesis {index}")
        print(hypothesis.model_dump_json(indent=2))

    while True:
        print(f"\nINVESTIGATING HYPOTHESIS : {state["current_hypothesis_index"]+1}")

        plan_result=investigation_planner(state)
        state.update(plan_result)

        print("\nINVESTIGATION PLAN:")
        print(
            state["current_investigation_plan"]
            .model_dump_json(indent=2)
        )

        executor_result = investigation_executor(state)
        state.update(executor_result)

        evaluator_result=investigation_evaluator(state)
        state.update(evaluator_result)

        print("\nINVESTIGATION RESULT:")

        result = state["investigation_results"][-1]

        print(
            result.model_dump_json(
                indent=2
            )
        )

        next_state=prepare_next_hypothesis(state)
        if next_state is None:
            break

        state.update(next_state)

    print("\n\nALL INVESTIGATION RESULTS:")

    for index, result in enumerate(state["investigation_results"],start=1):
        print(f"\n--- Hypothesis {index} ---")

        print(
            result.model_dump_json(indent=2)
        )

if __name__ == "__main__":
    main()