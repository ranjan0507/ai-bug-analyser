from models.state import BugState

MAX_CLARIFICATION_ATTEMPTS=2 

def can_request_clarification(state:BugState)->bool:
	return(
		state["clarification_count"] < MAX_CLARIFICATION_ATTEMPTS
	)