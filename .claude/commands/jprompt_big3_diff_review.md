Run 'git diff > diff.txt' 

Then use that file as the input to this just-prompt tool call.

prompts_from_file_to_file(
    from_file = diff.txt,
    models = "openai:o3-mini, anthropic:claude-3-7-sonnet-20250219:4k, gemini:gemini-2.0-flash-thinking-exp"
    output_dir = big3_diff_review
)
