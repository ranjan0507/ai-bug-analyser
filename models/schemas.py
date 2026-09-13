from pydantic import BaseModel,Field
from enum import Enum
from typing import Any

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

class InvestigationMethods(str,Enum):
	TOOL="tool",
	LLM_REASONING="llm_reasoning"

class InvestigationStep(BaseModel):
	step_number:int
	objective:str
	method:InvestigationMethods
	tool_name:str|None = None
	tool_operation:str|None = None
	tool_arguments:dict[str,Any]=Field(default_factory=dict)
	action:str
	expected_evidence:str

class InvestigationPlan(BaseModel):
	steps: list[InvestigationStep]=Field(default_factory=list)
	hypothesis:str

class Evidence(BaseModel):
	description:str
	source:str

class ToolResult(BaseModel):
	tool_name: str
	success: bool
	observations: list[str] = Field(default_factory=list)
	evidence: list[Evidence] = Field(default_factory=list)
	error: str | None = None

class ReasoningStepResult(BaseModel):
    observations: list[str] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)


class Verdict(str,Enum):
	SUPPORTED="supported"
	REJECTED="rejected"
	INCONCLUSIVE="inconclusive"

class InvestigationResult(BaseModel):
	hypothesis:Hypothesis
	plan:InvestigationPlan
	observations:list[str]=Field(default_factory=list)
	evidence:list[Evidence]=Field(default_factory=list)
	verdict:Verdict
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
