from os import read

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import PDFSearchTool, ScrapeWebsiteTool

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


@CrewBase
class AWSCrew:
    """AWSCrew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # If you would lik to add tools to your crew, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def aws_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["aws_researcher"],
            tools=[ScrapeWebsiteTool(), PDFSearchTool()],
        )

    @agent
    def aws_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["aws_writer"],
            tools=[ScrapeWebsiteTool(), PDFSearchTool()],
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def read_url_task(self) -> Task:
        return Task(
            config=self.tasks_config["read_url_task"],
        )

    @task
    def write_article_task(self) -> Task:
        return Task(
            config=self.tasks_config["write_article_task"],
            output_file="aws_arq.html",
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Research Crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
