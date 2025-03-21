Create a new file called diff.md.

At the top of the file, add the following markdown:

```md
# Code Review
Review the diff, report on issues, bugs, and improvements. 
End with a concise table of any issues, solutions, and a risk assessment for each issue if applicable.
Use emojis to convey the severity of each issue.

## Diff

```

Then run git diff and append the output to the file.

Then use that file as the input to this just-prompt tool call.

prompts_from_file_to_file(
    from_file = diff.md,
    models = "openai:o3-mini, anthropic:claude-3-7-sonnet-20250219:4k, gemini:gemini-2.0-flash-thinking-exp"
)
