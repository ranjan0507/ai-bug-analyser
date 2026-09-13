from models.schemas import ToolResult,Evidence

TOOL_NAME = "code_inspector"

TOOL_DESCRIPTION = """
Purpose:
Inspect source code and return deterministic, verifiable information.

Capabilities:
- Retrieve a specific line of code
- Retrieve a range of lines
- Search the code for a keyword or pattern

Use when:
You need exact code locations or source snippets as evidence
while investigating a hypothesis.

Limitations:
- Does not diagnose bugs
- Does not generate hypotheses
- Does not determine root causes
"""

class CodeInspector:
	def __init__(self,code:str):
		self.code=code
		self.lines=code.splitlines()

	def get_line(self,line_number:int)->ToolResult:
		if line_number<1 or line_number>len(self.lines):
			return ToolResult(
				tool_name="code_inspector",
				success=False,
				error=f"Line {line_number} does not exist."
			)
		line=self.lines[line_number-1]
		return ToolResult(
			tool_name="code_inspector",
			success=True,
			observations=[
				f"Retreived line {line_number}"
			],
			evidence=[
				Evidence(
					description=f"Line {line_number}: {line}",
					source="code_inspection"
				)
			]
		)

	def get_lines(self,start_line:int,end_line:int)->ToolResult:
		if start_line<1 or end_line>len(self.lines):
			return ToolResult(
				tool_name="code_inspector",
				success=False,
				error="Invalid line range."
			)

		selected_lines=self.lines[
			start_line-1:end_line
		]

		formatted_lines="\n".join(
			f"{i}:{line}"
			for i,line in enumerate(
				selected_lines,
				start=start_line
			)
		)
		return ToolResult(
			tool_name="code_inspector",
			success=True,
			observations=[
				f"Retrieved lines {start_line} to {end_line}"
			],
			evidence=[
				Evidence(
					description=formatted_lines,
					source="code_inspection"
				)
			]
		)

	def search(self,query:str)->ToolResult:
		matches=[]
		for index,line in enumerate(self.lines,start=1):
			if query.lower() in line.lower():
				matches.append(
					f"Line {index}: {line}"
				)
		if not matches:
			return ToolResult(
				tool_name="code_inspector",
				success=True,
				observations=[
					f"No matches found for '{query}'"
				]
			)

		return ToolResult(
			tool_name="code_inspector",
			success=True,
			observations=[
				f"Found {len(matches)} matches for '{query}'"
			],
			evidence=[
				Evidence(
					description="\n".join(matches),
					source="code_inspection"
				)
			]
		)