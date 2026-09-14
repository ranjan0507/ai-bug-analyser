from models.state import BugState

def hil_response_handler(
		state:BugState,
		answer:str
):
	interactions=[
		*state["human_interactions"]
	]

	if not interactions:
		raise ValueError(
			"No human interaction exists to attach an asnswer to."
		)

	interactions[-1].answer=answer

	return {
		"human_interactions":interactions,
		"clarification_count": state["clarification_count"]+1
	}