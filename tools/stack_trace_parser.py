import re
from models.schemas import ToolResult, Evidence

TOOL_NAME = "stack_trace_parser"

TOOL_DESCRIPTION = """
Purpose:
Extract structured, verifiable information from an error message
or stack trace.

Capabilities:
- Identify file references
- Identify line references
- Identify function references
- Preserve raw stack trace entries as evidence

Use when:
You need to locate where a failure occurred or extract
structured information from a stack trace.

Limitations:
- Does not diagnose the underlying bug
- Does not determine the root cause
"""

class StackTraceParser:
	def __init__(self,stack_trace:str|None):
		self.stack_trace=stack_trace

	def parse(self)->ToolResult:
		if not self.stack_trace:
			return ToolResult(
				tool_name="stack_trace_parser",
				success=True,
				observations=[
					"No stack trace was provided."
				]
			)
		lines=[
			line.strip()
			for line in self.stack_trace.splitlines()
			if line.strip()
		]
		file_references=[]
		line_references=[]
		function_references=[]

		for line in lines:
			matches=re.findall(
				 r'([^\s:]+\.[a-zA-Z0-9]+):(\d+)',
				 line
			)
			for file_name, line_number in matches:
				if file_name not in file_references:
					file_references.append(file_name)
				line_number = int(line_number)
				if line_number not in line_references:	
					line_references.append(line_number)

			function_matches = re.findall(
                r'([a-zA-Z_]\w*)\s*\(',
                line
            )
			for function in function_matches:
				if function not in function_references:
					function_references.append(function)

		observations = [
            f"Parsed {len(lines)} stack trace entries.",
            f"Found {len(file_references)} file reference(s).",
            f"Found {len(line_references)} line reference(s).",
            f"Found {len(function_references)} function reference(s)."
        ]

		evidence = [
            Evidence(
                description=line,
                source="stack_trace"
            )
            for line in lines
        ]

		return ToolResult(
            tool_name="stack_trace_parser",
            success=True,
            observations=observations,
            evidence=evidence
        )
		