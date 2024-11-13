from langchain_core.prompts import PromptTemplate

from utils.logger import logger


def generation_prompt_template(prompt_template: str, prompt_params: dict) -> PromptTemplate:
    logger.info(f"model-match/services/components/prompts/generate_prompts.py generation_prompt_template prompt_template: {prompt_template}, prompt_params: {prompt_params}")

    prompt = PromptTemplate.from_template(
        prompt_template
    )

    invoke = prompt.invoke(prompt_params)
    logger.info(f"model-match/services/components/prompts/generate_prompts.py generation_prompt_template invoke: {invoke}")

    return prompt
