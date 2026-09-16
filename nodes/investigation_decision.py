from models.state import BugState
from models.schemas import InvestigationDecision, Verdict

def investigation_decision(state:BugState):
	results=state["investigation_results"]

	supported_results=[
		result
		for result in results
		if result.verdict==Verdict.SUPPORTED
	]

	inconclusive_results=[
		result
		for result in results
		if result.verdict==Verdict.INCONCLUSIVE
	]

	if supported_results :
		return {
			"investigation_decision":InvestigationDecision(
				should_ask_human=False,
				should_conclude=True,
				reason=(
					"Atleast one hypothesis is supported by investigation evidence. "
					"So human clarification is not required. "
				)
			)
		}
	if inconclusive_results:
		return {
			"investigation_decision":InvestigationDecision(
				should_ask_human=True,
				should_conclude=False,
				reason=(
					"No hypothesis was confirmed and one or more plausible hypothesis"
					"remain inconclusive. Additional human clarification is required"
				)
			)
		}
	
	return {
		"investigation_decision":InvestigationDecision(
			should_ask_human=False,
			should_conclude=True,
			reason=(
				"No hypothesis was supported and no inconclusive hypothesis"
				"remains requiring human clarification. "
			)
		)
	}