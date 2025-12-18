def assess_api_uncertainty(api_function_description, uncertainty_type):
    """
    Assess the likelihood that a given API function would naturally develop a specific type of uncertainty 
    in real-world production environments.

    Parameters:
    - api_function_description: The API function's description from its documentation
    - uncertainty_type: Detailed criteria for the uncertainty type being assessed
    
    Assessment focuses on inherent characteristics based on the function's purpose, not its implementation.
    """
    
    # Extract uncertainty type name and criteria if they're provided together
    uncertainty_type_name = uncertainty_type.split('\n')[0] if '\n' in uncertainty_type else uncertainty_type
    uncertainty_type_criteria = '\n'.join(uncertainty_type.split('\n')[1:]) if '\n' in uncertainty_type else ""
    
    # TASK section
    task = """
    Your task is to predict the likelihood that this API function would naturally develop the specified type of
    uncertainty in real-world production environments, based solely on its functional characteristics.
    
    Focus on the inherent nature of what the function aims to accomplish rather than any specific implementation
    details. This assessment helps identify which functions are inherently prone to developing certain types of
    uncertainties regardless of documentation quality or implementation excellence.
    """
    
    # API FUNCTION DESCRIPTION section
    api_description = f"""
    {api_function_description}
    """
    
    # UNCERTAINTY TYPE BEING ASSESSED section
    uncertainty_section = f"""
    {uncertainty_type_name}
    
    {uncertainty_type_criteria}
    """
    
    # INSTRUCTIONS section
    instructions = """
    1. Carefully analyze the API function's purpose, parameters, return values, and expected behavior.
    
    2. Consider how the function's fundamental purpose and domain (not its current implementation) 
       would naturally lead to certain types of uncertainties in real-world usage.
    
    3. Rate the function on each criterion using the provided 0-2 scale, where:
       - 0 = Low likelihood (this characteristic is unlikely given the function's purpose)
       - 1 = Moderate likelihood (this characteristic is somewhat likely given the function's purpose)
       - 2 = High likelihood (this characteristic is very likely given the function's purpose)
    
    4. Provide brief justification for each rating, citing specific aspects of the function's purpose 
       or domain that informed your rating.
    
    5. Calculate the overall uncertainty score using this formula:
       Overall Score = Sum of criterion scores / (Number of criteria × 2)
       This produces a final score between 0 (very unlikely) and 1 (very likely).
    """
    
    # IMPORTANT GUIDELINES section
    guidelines = """
    - Focus on the inherent characteristics of the function's purpose, not how well it might be implemented.
    - Consider the natural tendencies of functions in this domain based on real-world constraints and complexities.
    - Analyze the function's core purpose rather than speculating about its current implementation quality.
    - Base your assessment on practical experiences with similar functions in production environments.
    - Consider industry patterns and common challenges in the function's domain.
    """
    
    # OUTPUT FORMAT section
    output_format = f"""
    Please provide your assessment in the following format:
    
    # Assessment of {uncertainty_type_name} Likelihood
    
    ## Individual Criteria Scores
    
    1. [Criterion Name]: [Score (0-2)]
       - Justification: [Brief explanation referencing the function's characteristics]
    
    2. [Criterion Name]: [Score (0-2)]
       - Justification: [Brief explanation referencing the function's characteristics]
    
    [Continue for all criteria]
    
    ## Overall Assessment
    - Total Score: [Sum of individual scores]
    - Normalized Score: [Total Score / (Number of criteria × 2)]
    - Likelihood: [Low (0-0.33) / Moderate (0.34-0.66) / High (0.67-1.0)]
    - Summary: [2-3 sentences explaining why this function would naturally tend to develop this type of 
      uncertainty in real-world usage]
    """
    
    # Combine all sections into the complete assessment template
    complete_template = f"""# TASK
{task}

# API FUNCTION DESCRIPTION
{api_description}

# UNCERTAINTY TYPE BEING ASSESSED
{uncertainty_section}

# INSTRUCTIONS
{instructions}

# IMPORTANT GUIDELINES
{guidelines}

# OUTPUT FORMAT
{output_format}
"""
    
    return complete_template
