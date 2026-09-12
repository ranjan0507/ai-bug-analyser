from nodes.context_profiler import context_profiler
from nodes.bug_analyser import bug_analyzer

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
        "stack_trace": None,
    }

    profile_result = context_profiler(state)
    state.update(profile_result)

    bug_analysis_result = bug_analyzer(state)
    state.update(bug_analysis_result)

    print("CODE PROFILE:\n")
    print(state["code_profile"].model_dump_json(indent=2))
    print("\nBUG REPORT:\n")
    print(state["bug_analysis"].model_dump_json(indent=2))


if __name__ == "__main__":
    main()