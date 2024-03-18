from src.experiments.agent_subclass.multimodal_websurfer import MultimodalWebsurfer
from src.autogen_configuration.autogen_config import GetConfig


from src.tools.analyze_content import analyze_content

from autogen import ConversableAgent, AssistantAgent, UserProxyAgent, Agent, GroupChat, GroupChatManager
from typing_extensions import Annotated

llm_config = GetConfig().config_list

websurfer = MultimodalWebsurfer(
    name="MultimodalWebsurfer",
    llm_config=llm_config
)

user_proxy = UserProxyAgent(
    llm_config=llm_config,
    name="user_proxy",
    human_input_mode="NEVER",
    code_execution_config=False,
    default_auto_reply="",
    is_termination_msg=lambda x: True,
)

planner_system_message = """As the Planner, your role is to devise a strategy for navigating web content effectively. For this example, the task is to visit a specific website using the 'read_url' function. 

General Plan Outline:
1. Identify the target URL, ensuring it is correctly formatted with the necessary protocol (e.g., 'https://'). In this case, the target is 'www.example.com'.
2. Use the 'read_url' function to direct the websurfer to the specified URL. This step is crucial as it establishes the starting point for our web navigation task.
3. After initiating the 'read_url' function, monitor for confirmation that the websurfer has successfully landed on the desired webpage. This might involve checking for specific page elements or a successful page load indicator.
4. If the initial step is successful, plan subsequent actions based on the task objectives, whether it's gathering information, interacting with the webpage, or navigating further.

The websurfer has access to the followuing functions:
- read_url: Visit a webpage at a given URL and return the current URL.
- scroll: Scroll the webpage 500 pixels up or down.
- jump_to_search_engine: Jump to a google engine.
- go_back: Go back to the previous page.
- input_text: Input text into a text field.
- click_element: Click on an element on the page.
"""


planner = AssistantAgent(
    name="Planner",
    llm_config=llm_config,
    system_message=planner_system_message

)

prioritizer_system_message = """
As the Prioritizer, your primary responsibility is to ensure that the websurfer's actions are prioritized effectively, focusing on the most critical tasks and objectives.
Your task is to choose the next task for the websurfer to perform, based on the current state of the web interaction and the overall mission objectives. In the context of our example task, the primary focus is on prioritizing the navigation to a specific website.
"""

prioritizer = AssistantAgent(
    name="Prioritizer",
    llm_config=llm_config,
    system_message=prioritizer_system_message
)


critic_system_message = """The Critic's responsibility is to evaluate the effectiveness and accuracy of actions taken by the websurfer, particularly after the Planner has issued a navigation plan. In the context of our example task, the primary focus is on verifying the successful navigation to a specific website.

Evaluation Process:
1. Ensure that the websurfer's current location matches the intended URL. This verification confirms that the 'read_url' function achieved its purpose.
2. Examine the webpage to ascertain that it has fully loaded, indicating a successful navigation. Look for standard indicators of a complete page load or specific elements that confirm you're on the correct site.
3. Assess any potential issues encountered during the navigation process, such as errors, redirections, or content accessibility problems. Such issues could necessitate a revision of the initial plan or strategy.
4. Provide feedback based on the evaluation, highlighting successes and identifying areas for improvement. This feedback is essential for refining future navigation plans and enhancing the overall efficiency of the web interaction process.

Through this evaluative lens, the Critic contributes to the continuous improvement of the websurfer's navigation strategies, ensuring tasks are completed effectively and accurately."""


critic = AssistantAgent(
    name="Critic",
    llm_config=llm_config,
    system_message="""Critic. Your function is to meticulously review the plans proposed by the Planner and the actions taken by the MultimodalWebsurfer. Assess the feasibility, safety, and potential effectiveness of the plans, ensuring they are realistic and comply with ethical guidelines and best practices for web usage. Provide constructive feedback to the Planner for refining the strategies, highlighting any overlooked aspects, potential risks, or alternative approaches that could enhance outcomes. Additionally, verify the accuracy and relevance of the information collected by the websurfer, suggesting any necessary adjustments or further analysis. Your critical analysis and insights are pivotal in refining the approach and ensuring the integrity and success of the overall mission.
    ALWAYS USE THE PROVIDED analyze_content FUNCTION TO EVALUATE THE CONTENT OF A WEB PAGE."""
)


@user_proxy.register_for_execution()
@critic.register_for_llm(
    name="analyze_content",
    description="Analyze the content of a web page.",
)
def analyze_content_(query: Annotated[str, "The description of the part of the web page to analyze."]) -> str:
    return analyze_content(query)


groupchat = GroupChat(
    agents=[user_proxy, planner, prioritizer,
            websurfer, critic], messages=[], speaker_selection_method="round_robin"
)
manager = GroupChatManager(
    groupchat=groupchat, llm_config=llm_config)

user_proxy.initiate_chat(
    manager,
    message=""" Find infos about the latest iPhone model. """
)
