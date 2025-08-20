def build_mutant_prompt(ori_code):
    prompt = """
    You are an AI code editor and generator. Your goal is to analyze the @@Existing Code and generate mutants in it
    You can generate one mutant by introducing a single, subtle alteration to the logic, structure, or syntax of the code.
    The mutation should impact the functionality in a meaningful way without completely changing the intent or purpose of the original code.

    @@Existing Code
    {}

    #Requirement: 
    1. Provide generated mutants directly.
    2. Prohibit generating the exact same mutants.
    3. Do not explain how the mutant was generated, only output the mutated code. 
    4. The output must be in the following format:
    ```python
    # Your codes here
    ```
    """.strip().format(
        ori_code
    )
    return prompt


def build_gpt_prompt(dataset, code, docstring=None, context=None):
    if dataset == 'CoderEval':
        prompt = """
You are a highly skilled and thoughtful programming assistant tasked with guiding a programmer to improve the code. 
Your primary goal is to analyze the @@Existing Code based on the provided @@Docstring and @@Oracle Context to identify 
potential issues and offer suggestions for improvement.
Carefully review the @@Existing Code and understand its structure, logic, and functionality.
Compare the code against the @@Docstring to ensure it adheres to the described purpose, inputs, outputs, and behavior.
Use the @@Oracle Context to ensure the code correctly interacts with external elements, such as types, APIs, variables, 
or constants, and adheres to the dependencies and integration requirements within the broader environment.
#Requirement: 
1. Offer guidance in a clear and understandable manner, explaining the rationale behind each suggestion.
2. Refrain from providing actual code solutions, but instead focus on conceptual modifications or strategies.
3. Please respond in no more than three sentences.
@@Existing Code
{}

@@Docstring
{}

@@Oracle Context
{}
    """.strip().format(
            code, docstring, context
        )
    elif dataset == 'HumanEval':
        prompt = """
You are a highly skilled and thoughtful programming assistant tasked with guiding a programmer to improve the code. 
Your primary goal is to analyze the @@Existing Code to identify potential issues and offer suggestions for improvement.
Carefully review the @@Existing Code and understand its structure, logic, and functionality.

#Requirement: 
1. Offer guidance in a clear and understandable manner, explaining the rationale behind each suggestion.
2. Refrain from providing actual code solutions, but instead focus on conceptual modifications or strategies.
3. Please respond in no more than three sentences.
@@Existing Code
{}
""".strip().format(
            code
        )
    else:
        raise ValueError(f"Invalid dataset: {dataset}")
    return prompt


def build_gpt_gt_prompt(dataset, code, correct_code, docstring=None, context=None):
    if dataset == 'CoderEval':
        prompt = """
You are a highly skilled and thoughtful programming assistant tasked with guiding a programmer to improve the code. 
Your primary goal is to analyze the @@Existing Code based on the provided @@Docstring, @@Oracle Context and 
@@Correct Code to identify potential issues and offer suggestions for improvement.
Carefully review the @@Existing Code and understand its structure, logic, and functionality.
Compare the code against the @@Docstring to ensure it adheres to the described purpose, inputs, outputs, and behavior.
Use the @@Oracle Context to ensure the code correctly interacts with external elements, such as types, APIs, variables, 
or constants, and adheres to the dependencies and integration requirements within the broader environment. Then, compare 
the @@Existing Code against the @@Correct Code to highlight deviations, misunderstandings, or missed optimizations.
#Requirement: 
1. Offer guidance in a clear and understandable manner, explaining the rationale behind each suggestion.
2. Refrain from providing actual code solutions, but instead focus on conceptual modifications or strategies.
3. Please respond in no more than three sentences.
@@Existing Code
{}

@@Docstring
{}

@@Oracle Context
{}

@@Correct Code
{}
    """.strip().format(
            code, docstring, context, correct_code
        )
    elif dataset == 'HumanEval':
        prompt = """
You are a highly skilled and thoughtful programming assistant tasked with guiding a programmer to improve the code. 
Your primary goal is to analyze the @@Existing Code to identify potential issues and offer suggestions for improvement.
Carefully review the @@Existing Code and understand its structure, logic, and functionality. Then, compare 
the @@Existing Code against the @@Correct Code to highlight deviations, misunderstandings, or missed optimizations.

#Requirement: 
1. Offer guidance in a clear and understandable manner, explaining the rationale behind each suggestion.
2. Refrain from providing actual code solutions, but instead focus on conceptual modifications or strategies.
3. Please respond in no more than three sentences.
@@Existing Code
{}

@@Correct Code
{}
""".strip().format(
            code, correct_code
        )
    else:
        raise ValueError(f"Invalid dataset: {dataset}")
    return prompt


def build_repair_prompt(
        solution,
        feedback,
        docstring=None,
        context=None,
        is_persona=True,
        is_cot=False,
        is_few_shot=False,
        is_instructions=True
):
    persona = "You are a professional code repair assistant skilled at fixing code errors based on the @@Feedback."

    header_parts = []
    if is_persona:
        header_parts.append(persona)
    header_parts.append("Your task is to correct the given erroneous code @@Existing Code.")
    header_parts.append(
        "@@Feedback includes error messages, descriptions of logical issues, or deviations from expected functionality.")
    if docstring:
        header_parts.append(
            "@@Docstring provides a description of the function, its purpose, and details of its input and output parameters.")
    if context:
        header_parts.append(
            "@@Oracle Context refers to code elements such as types, APIs, variables, and consts defined outside the function under generation but within the dependent third-party libraries, current class, file, or project.")
    if is_cot:
        header_parts.append(
            "You should follow the reasoning process below to fix the code:\n"
            "1. Carefully read the feedback and understand the essence of the problem.\n"
            "2. Check the parts of the code that might be causing these issues.\n"
            "3. Consider edge cases and special condition handling.\n"
            "4. Apply appropriate fixes while maintaining code style consistency.\n"
            "5. Verify whether the fix addresses all the issues mentioned in the feedback."
        )
    if is_few_shot:
        header_parts.append(
            """For example:
Erroneous Code:
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)

Feedback:
Consider adding error handling to manage potential issues, such as division by zero when the input list is empty. 
Additionally, using built-in functions like `sum()` can simplify the code and improve readability, making it more pythonic. 
Finally, ensure that the function can handle non-numeric inputs to prevent runtime errors.

Fixed Code:
def calculate_average(numbers):
    if not numbers:
        raise ValueError("Input list is empty. Cannot calculate average.")
    return sum(numbers) / len(numbers)
"""
        )
    header = "\n".join(header_parts)

    prompt_sections: list[str] = []
    prompt_sections = [header, "\n@@Existing Code\n{}".format(solution)]
    if docstring:
        prompt_sections.append("\n@@Docstring\n{}".format(docstring))
    if context:
        prompt_sections.append("\n@@Oracle Context\n{}".format(context))
    prompt_sections.append("\n@@Feedback\n{}".format(feedback))

    if is_instructions:
        instruction_text = (
            "Based on the provided information, fix the erroneous code and ensure the following:\n"
            "Resolve all errors to make the code functional.\n"
            "Address the improvement points mentioned in the feedback.\n"
            "Only need to fix the code; do not modify the function signature.\n"
        )
        if docstring:
            instruction_text += "Adhere to the functionality requirements described in the docstring.\n"
        if context:
            instruction_text += "Utilize the external context (Oracle Context) information for proper API usage, variable references, and any related dependencies.\n"

        prompt_sections.append("\n" + instruction_text)

    prompt_sections.append(
        "\nPlease return the corrected code in the following format:\n```python\n# Your codes here\n```")

    prompt = "\n".join(prompt_sections)
    return prompt
