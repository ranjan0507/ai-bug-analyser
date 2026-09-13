from nodes.context_profiler import context_profiler
from nodes.bug_analyser import bug_analyzer
from nodes.hypothesis_generator import generate_hypothesis
from nodes.validate_hypothesis import hypothesis_validator
from nodes.investigation_planner import investigation_planner
from nodes.investigation_executor import execute_tool_step

def main():

    state = {
        "code": """
#include <iostream>
#include <vector>

using namespace std;

int main() {
    vector<int> nums = {1, 2, 3};

    for (int i = 0; i <= nums.size(); i++) {
        cout << nums[i];
    }

    return 0;
}
""",
        "error": "Segmentation fault",
        "stack_trace" : """
Segmentation fault
main.cpp:10
main()
"""
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

    plan_result=investigation_planner(state)
    state.update(plan_result)
    print("\nINVESTIGATION PLAN:")

    print(
        state["current_investigation_plan"]
        .model_dump_json(indent=2)
    )

    plan=state["current_investigation_plan"]
    for step in plan.steps:

        if step.method == "tool":

            result = execute_tool_step(
                step,
                state
            )

            print("\nTOOL EXECUTION RESULT:")

            print(
                result.model_dump_json(
                    indent=2
                )
            )

        break
if __name__ == "__main__":
    main()