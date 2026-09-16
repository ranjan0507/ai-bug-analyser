from langgraph.types import Command
from graph.debugging_graph import build_debugging_graph

def main():

    state = {
"code": """
#include <iostream>
#include <vector>

using namespace std;

int main() {
    vector<int> nums = {10, 20, 30};

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
    "fix": None,

    "investigation_decision":None
    }

    graph=build_debugging_graph()

    config={
        "configurable":{
            "thread_id":"debug-1"
        }
    }

    result=graph.invoke(state,config=config)

    while "__interrupt__" in result:
        interrupt_data=result["__interrupt__"][0].value

        print("\nHUMAN CLARIFICATION")
        print(interrupt_data["question"])
        print(f"\nReason: {interrupt_data['reason']}")
        answer=input("\nYOUR ANSWER: ")

        result = graph.invoke(Command(resume=answer),config=config)

    print("\nFINAL CONCLUSION")

    print(
        result["final_conclusion"].model_dump_json(indent=2)
    )

if __name__ == "__main__":
    main()