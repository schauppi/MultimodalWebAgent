from src.oai_agent.utils.load_assistant_id import load_assistant_id
from src.autogen_configuration.autogen_config import GetConfig
from src.oai_agent.oai_agent import configure_agent


browsing_agent = configure_agent("BrowsingAgent")
qa_agent = configure_agent("QualityAssuranceAgent")

browsing_agent.name = "BrowsingAgent"

print(browsing_agent.name)
