from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt
from langgraph.checkpoint.memory import MemorySaver

from models.state import BugState

from nodes.context_profiler import context_profiler
from nodes.bug_analyser import bug_analyzer
from nodes.hypothesis_generator import generate_hypothesis
from nodes.validate_hypothesis import hypothesis_validator

from nodes.investigation_planner import investigation_planner
from nodes.investigation_executor import investigation_executor
from nodes.investigation_evaluator import investigation_evaluator
from nodes.hypothesis_controller import prepare_next_hypothesis

from nodes.investigation_decision import investigation_decision
from nodes.final_conclusion import final_conclusion

from nodes.hil_question_generator import hil_question_generator
from nodes.hil_response_handler import hil_response_handler
from nodes.clarification_evaluator import clarification_evaluator
from nodes.hil_controller import can_request_clarification


def advance_hypothesis(state:BugState):
	result=prepare_next_hypothesis(state)
	if result is None:
		return {}
	return result

def route_after_investigation(state:BugState):
	current_idx=state["current_hypothesis_index"]
	total_hypothesis=len(state["hypotheses"])

	if current_idx+1<total_hypothesis:
		return "advance_hypothesis"
	return "investigation_decision"

def hil_response(state:BugState):
	interaction=state["human_interactions"][-1]
	answer=interrupt(
		{
			"type":"human_clarification",
			"question":interaction.question,
			"reason":interaction.reason_question_was_asked
		}
	)
	return hil_response_handler(state,answer)

def route_after_decision(state:BugState):
	decision=state["investigation_decision"]
	if decision.should_conclude:
		return "final_conclusion"
	if (decision.should_ask_human and can_request_clarification(state)):
		return "hil_question_generator"
	return "final_conclusion"

def route_after_clarification(state:BugState):
	decision=state["investigation_decision"]
	if decision.should_conclude:
		return "final_conclusion"
	if(decision.should_ask_human and can_request_clarification(state)):
		return "hil_question_generator"
	return "final_conclusion"


def build_debugging_graph():
	workflow=StateGraph(BugState)

	workflow.add_node("context_profiler",context_profiler)
	workflow.add_node("bug_analyzer",bug_analyzer)
	workflow.add_node("hypothesis_generator",generate_hypothesis)
	workflow.add_node("hypothesis_validator",hypothesis_validator)

	workflow.add_node("investigation_planner",investigation_planner)
	workflow.add_node("investigation_executor",investigation_executor)
	workflow.add_node("investigation_evaluator",investigation_evaluator)
	workflow.add_node("advance_hypothesis",advance_hypothesis)

	workflow.add_node("investigation_decision",investigation_decision)
	workflow.add_node("final_conclusion",final_conclusion)

	workflow.add_node("hil_question_generator",hil_question_generator)
	workflow.add_node("hil_response",hil_response)
	workflow.add_node("clarification_evaluator",clarification_evaluator)

	workflow.add_edge(START,"context_profiler")
	workflow.add_edge("context_profiler","bug_analyzer")
	workflow.add_edge("bug_analyzer","hypothesis_generator")
	workflow.add_edge("hypothesis_generator","hypothesis_validator")

	workflow.add_edge("hypothesis_validator","investigation_planner")
	workflow.add_edge("investigation_planner","investigation_executor")
	workflow.add_edge("investigation_executor","investigation_evaluator")

	workflow.add_conditional_edges(
		"investigation_evaluator",
		route_after_investigation,
		{
			"advance_hypothesis":"advance_hypothesis",
			"investigation_decision":"investigation_decision"
		}
	)

	workflow.add_edge("advance_hypothesis","investigation_planner")

	workflow.add_conditional_edges(
		"investigation_decision",
		route_after_decision,
		{
			"final_conclusion":"final_conclusion",
			"hil_question_generator":"hil_question_generator"
		}
	)

	workflow.add_edge("hil_question_generator","hil_response")
	workflow.add_edge("hil_response","clarification_evaluator")

	workflow.add_conditional_edges(
		"clarification_evaluator",
		route_after_clarification,
		{
			"final_conclusion":"final_conclusion",
			"hil_question_generator":"hil_question_generator"
		}
	)

	workflow.add_edge("final_conclusion",END)

	checkpointer=MemorySaver()

	return workflow.compile(checkpointer=checkpointer)