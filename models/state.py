from models.schemas import BugAnalysis,CodeProfile,Hypothesis,InvestigationPlan,InvestigationResult,HumanInteraction,Evidence,FinalConclusion,Fix
from typing import TypedDict

class BugState(TypedDict):
	code:str
	error:str
	stack_trace:str|None

	code_profile:CodeProfile
	bug_analysis:BugAnalysis

	hypotheses:list[Hypothesis]
	current_hypothesis_index:int

	current_investigation_plan=InvestigationPlan|None
	current_observations:list[str]
	current_evidenc:list[Evidence]

	investigation_results:list[InvestigationResult]

	human_interactions:list[HumanInteraction]
	clarification_count:int

	final_conclusion:FinalConclusion|None
	fix:Fix|None



	




