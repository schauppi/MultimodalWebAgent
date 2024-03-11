# MultimodalWebAgent

[![Watch the video](https://img.youtube.com/vi/jQ2Os682Ybs/0.jpg)](https://www.youtube.com/watch?v=jQ2Os682Ybs&t=0s)

## Introduction

This is a multimodal web agent that can understand and generate natural language and visual content implemented using the [AutoGen](https://microsoft.github.io/autogen/) framework and the [Assistants API](https://platform.openai.com/docs/assistants/overview).\
It is based on the Paper [WebVoyager: Building an End-to-End Web Agent with Large Multimodal Models](https://arxiv.org/abs/2401.13919).

## Disclaimer

This project is still in development and not yet ready for use.\
I managed to get the agent to work, but the results are not yet satisfactory.
The prompt has to be carefully crafted to get good results. F.e. the prompt describes every step what the agent has to do in detail like "Go to the website, click on the button using tool X, scroll down using tool Y, click on the next button using tool Z, etc.". With this approach the webagent is working pretty well tbh. So feel free to try it out, give feedback and contribute.

## Installation

1. Rename the file '.env example' to '.env' and fill in your OpenAI API key.
2. Install the required packages using the following command:
   `poetry install`

## Run the agent

1. Craft an precise prompt for the agent. The prompt should describe every step what the agent has to do in detail.
   You find an example prompt in the file `src/oai_agent/utils/prompt`.
2. Run the agent using the following command:
   `poetry run webagent`

## Further steps

- [ ] Test: Improve the agent to work with more general prompts.
- [ ] Test: Implement an `autogen.GroupChat`with an additional Planner and QA agent. To refine and correct the steps on the fly
