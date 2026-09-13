from models.state import BugState

def prepare_next_hypothesis(state:BugState):
	next_idx=state["current_hypothesis_index"]+1
	if next_idx>=len(state["hypotheses"]):
		return None

	return {
		"current_hypothesis_index":next_idx,
		"current_investigation_plan":None,
		"current_observations":[],
		"current_evidence":[]
	}