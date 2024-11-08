from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import CodeInterpreterTool

@CrewBase
class TalkersCrew():
	"""Talkers crew"""

	@agent
	def coder(self) -> Agent:
		return Agent(
			config=self.agents_config['coder'],
			verbose=True,
		)
	
	@agent
	def code_executer(self) -> Agent:
		return Agent(
			config=self.agents_config['code_executer'],
			tools=[CodeInterpreterTool()],
			allow_code_execution=True,
			verbose=True,
		)

	@task
	def code_task(self) -> Task:
		return Task(
			config=self.tasks_config['code_task'],
			output_file='code.py'
		)

	@task
	def code_execution_task(self) -> Task:
		return Task(
			config=self.tasks_config['code_execution_task'],
			output_file='tree.txt'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Talkers crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)