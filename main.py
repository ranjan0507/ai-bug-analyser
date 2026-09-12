from nodes.context_profiler import context_profiler


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

    result = context_profiler(state)

    print(result["code_profile"].model_dump_json(indent=2))


if __name__ == "__main__":
    main()