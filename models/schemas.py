from pydantic import BaseModel,Field

class CodeProfile(BaseModel):
	language:str
	structure:str
	libraries:list[str]=Field(default_factory=list)
	components:list[str]=Field(default_factory=list)

class BugAnalysis(BaseModel):
	code_intent:str
	expected_behavior:str
	actual_behavior: str
	failure_context: str
	investigation_focus: list[str]=Field(default_factory=list)

class Hypothesis(BaseModel):
	possible_cause: str
	why_suspected:str
	what_to_check: list[str]=Field(default_factory=list)
	expected_evidence: str

class HypothesisList(BaseModel):
	hypotheses:list[Hypothesis]=Field(
		min_length=1,
		max_length=4
	)

class HypothesisValidation(BaseModel):
	valid:bool
	issues: list[str] = Field(default_factory=list)
	filtered_hypotheses: list[Hypothesis] = Field(default_factory=list)

class InvestigationPlan(BaseModel):
	steps: list[str]=Field(default_factory=list)
	tool_or_methods:list[str]=Field(default_factory=list)

class Evidence(BaseModel):
	description:str
	source:str

class InvestigationResult(BaseModel):
	hypothesis:Hypothesis
	plan:InvestigationPlan
	obvservations:list[str]=Field(default_factory=list)
	evidence:list[str]=Field(default_factory=list)
	verdict:str
	confidence:float

class HumanInteraction(BaseModel):
    question: str
    answer: str | None = None
    reason_question_was_asked: str
    related_hypotheses: list[int] = Field(default_factory=list)


class FinalConclusion(BaseModel):
    primary_cause: str | None = None
    contributing_issues: list[str] = Field(default_factory=list)
    unverified_possibilities: list[str] = Field(default_factory=list)
    overall_confidence: float
    decision: str


class Fix(BaseModel):
    what_was_fixed: str
    fixed_code: str
    explanation: str
    confidence: float
