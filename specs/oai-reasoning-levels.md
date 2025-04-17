Feature Request: Add low, medium, high reasoning levels to the OpenAI o-series reasoning models
> o3-mini, o4-mini, o3

## Implementation Notes
- Just like how claude-3-7-sonnet has budget tokens in 


## Relevant Files (Context)
README.md
src/just_prompt/molecules/prompt.py
src/just_prompt/atoms/llm_providers/anthropic.py
src/just_prompt/atoms/llm_providers/openai.py
src/just_prompt/tests/atoms/llm_providers/test_openai.py

## Self Validation (Close the loop)
- uv run pytest src/just_prompt/tests/atoms/llm_providers/test_openai.py
- uv run pytest src/just_prompt/tests/molecules/test_prompt.py