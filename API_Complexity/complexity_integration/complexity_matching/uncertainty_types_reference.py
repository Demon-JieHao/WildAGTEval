"""
Comprehensive reference of API uncertainty types and their assessment criteria.

This file contains structured definitions of different uncertainty types that can
appear in API functions, along with specific criteria for evaluating the likelihood
of each uncertainty type arising in real-world implementations.
"""

# Dimension 1: Uncertainty in API Definitions

# Local Uncertainty Types
AMBIGUOUS_DOCUMENTATION = {
    "name": "Ambiguous Documentation/Arguments",
    "description": "Uncertainties that occur within individual API specifications, creating ambiguity in implementation.",
    "examples": [
        "A weather API doesn't specify whether temperature is returned in Celsius or Fahrenheit",
        "Missing documentation for certain parameters, forcing developers to infer behavior through trial and error"
    ],
    "criteria": [
        {
            "name": "Unit/Format Ambiguity Likelihood",
            "definition": "The likelihood that the function handles values that could have multiple interpretations without explicit unit or format specification",
            "question": "How likely is this function to handle measurements, dates, times, or other values that could be interpreted in different formats?",
            "scale": [
                "Handles only unambiguous values (boolean flags, simple identifiers, enumerated types)",
                "Handles some values with standard interpretations (ISO standard formats)",
                "Handles multiple values with potentially ambiguous interpretations (temperatures, dates, coordinates)"
            ]
        },
        {
            "name": "Critical Default Behaviors Likelihood",
            "definition": "The likelihood that the function has significant undocumented default behaviors when optional parameters are omitted",
            "question": "How likely is this function to have important default behaviors that would significantly affect outcomes when parameters are omitted?",
            "scale": [
                "No optional parameters or only trivial defaults (like empty strings)",
                "Some default behaviors with moderate impact on function output",
                "Critical default behaviors that substantially change how the function operates"
            ]
        },
        {
            "name": "Parameter Interdependencies Likelihood",
            "definition": "The likelihood that parameters interact with or affect each other's meaning or behavior",
            "question": "How likely is it that some parameters would change the meaning, requirements, or effects of other parameters?",
            "scale": [
                "Each parameter serves a completely independent purpose",
                "Some mild interactions between parameters that follow logical patterns",
                "Complex interdependencies where parameters significantly modify each other's meaning"
            ]
        },
        {
            "name": "Domain Knowledge Requirements Likelihood",
            "definition": "The likelihood that specialized knowledge is needed to correctly interpret and use the function",
            "question": "How likely is it that using this function correctly would require domain-specific knowledge that might not be obvious?",
            "scale": [
                "Requires only general programming knowledge (string manipulation, basic arithmetic)",
                "Requires some domain familiarity but with common concepts",
                "Requires specialized expertise (financial calculations, medical terminology)"
            ]
        },
        {
            "name": "Abstract Parameter Semantics Likelihood",
            "definition": "The likelihood that parameter meanings are based on abstract rather than concrete concepts",
            "question": "How likely are the parameters to be based on subjective or conceptual ideas rather than concrete, measurable values?",
            "scale": [
                "All parameters represent concrete, measurable values",
                "Some parameters involve mild abstraction but remain mostly objective",
                "Multiple parameters based on highly abstract or subjective concepts"
            ]
        }
    ]
}

AD_HOC_RULES = {
    "name": "Ad Hoc Rules",
    "description": "Special requirements or constraints that, while technically documented, deviate from intuitive expectations.",
    "examples": [
        "Setting targetValue=-1 to request the 'last' item or using PT15M format to represent 15 minutes",
        "Requiring duration in ISO 8601 format (e.g., PT15M for 15 minutes) without explicit documentation"
    ],
    "criteria": [
        {
            "name": "Special Value Semantics Likelihood",
            "definition": "The likelihood that the function uses specific numeric or string values that carry special meanings beyond their literal value",
            "question": "How likely is this function to use specific values that have special behaviors not obvious from the value itself?",
            "scale": [
                "Values are always interpreted literally with no special cases",
                "Few common special values that follow industry conventions",
                "Multiple special values with non-obvious behaviors or meanings"
            ]
        },
        {
            "name": "Non-Standard Format Requirements Likelihood",
            "definition": "The likelihood that the function requires data in specific formats that deviate from common industry standards",
            "question": "How likely is this function to require inputs in unusual formats or strict variations of standard formats?",
            "scale": [
                "Uses only widely adopted standard formats (e.g., ISO-8601, RFC standards)",
                "Mostly standard formats with minor variations",
                "Requires specialized formats or significant deviations from standards"
            ]
        },
        {
            "name": "Counter-Intuitive Parameter Behavior Likelihood",
            "definition": "The likelihood that parameters behave in ways that contradict what most developers would reasonably expect",
            "question": "How likely would a developer familiar with similar APIs misunderstand how to use this function's parameters?",
            "scale": [
                "Parameters behave exactly as their names and common conventions suggest",
                "Some parameters have subtle behaviors that might not be immediately obvious",
                "Multiple parameters with behaviors that significantly deviate from conventions"
            ]
        },
        {
            "name": "Hidden Constraints Likelihood",
            "definition": "The likelihood that the function has undocumented or obscurely documented restrictions on how it can be used",
            "question": "How likely is this function to have important limitations that aren't immediately obvious from its general description?",
            "scale": [
                "All constraints are straightforward and follow standard patterns",
                "Some unique constraints that might not be immediately apparent",
                "Multiple significant constraints that developers would likely miss"
            ]
        },
        {
            "name": "Legacy Compatibility Issues Likelihood",
            "definition": "The likelihood that the function contains unusual behaviors primarily to maintain compatibility with older systems",
            "question": "How likely is this function to contain quirky behaviors that exist mainly for historical/legacy reasons?",
            "scale": [
                "New functionality designed without legacy compatibility concerns",
                "Some accommodation for backward compatibility, following common patterns",
                "Significant adaptations to maintain compatibility with legacy systems or conventions"
            ]
        }
    ]
}

# Global Uncertainty Types
UNCLEAR_FUNCTIONALITY_BOUNDARIES = {
    "name": "Unclear Functionality Boundaries",
    "description": "Uncertainties that emerge from interactions between multiple APIs within an ecosystem.",
    "examples": [
        "stop() vs. pause() functions with subtle differences in behavior",
        "Multiple search-related functions (search(), find(), lookup()) with context-dependent application criteria"
    ],
    "criteria": [
        # {
        #     "name": "Functional Overlap Likelihood",
        #     "definition": "The likelihood that the function's purpose significantly overlaps with other functions in the same API ecosystem",
        #     "question": "How likely is this function to have capabilities that partially duplicate or overlap with other related functions?",
        #     "scale": [
        #         "Completely distinct functionality with no overlap with other functions",
        #         "Minor overlap in edge cases but generally distinct purpose",
        #         "Substantial overlap where multiple functions could accomplish similar tasks"
        #     ]
        # },
        {
            "name": "Naming Similarity vs. Behavior Difference Likelihood",
            "definition": "The likelihood that the function has a name similar to other functions while having subtly different behavior",
            "question": "How likely is this function to have a name that suggests similar behavior to other functions, but operates differently in practice?",
            "scale": [
                "Unique name that clearly distinguishes it from other functions",
                "Similar name to other functions but with clearly differentiated behavior",
                "Nearly identical name to other functions with subtle but important behavioral differences"
            ]
        },
        # {
        #     "name": "Context-Dependent Behavior Likelihood",
        #     "definition": "The likelihood that the function behaves differently depending on context or environment",
        #     "question": "How likely is this function to change its behavior based on application context, user state, or environment conditions?",
        #     "scale": [
        #         "Behavior remains consistent across all contexts",
        #         "Some minor variations in behavior based on well-defined contexts",
        #         "Significant behavioral changes depending on context that may not be obvious"
        #     ]
        # },
        # {
        #     "name": "Functional Scope Expansion Likelihood",
        #     "definition": "The likelihood that the function's scope has expanded over time to include capabilities beyond its original purpose",
        #     "question": "How likely is this function to have accumulated additional capabilities that extend beyond what its name or primary purpose suggests?",
        #     "scale": [
        #         "Focused function that does exactly what its name implies, no more and no less",
        #         "Slightly expanded scope with some additional capabilities that are logically related",
        #         "Significantly expanded scope that includes capabilities not obviously related to its name"
        #     ]
        # }
    ]
}

COMPLEX_DEPENDENCY_CHAINS = {
    "name": "Complex Dependency Chains",
    "description": "Hidden prerequisites between API calls and cascading dependencies across multiple services.",
    "examples": [
        "resume() requires calling searchHistory() first, which requires calling getDevice()"
    ],
    "criteria": [
        {
            "name": "Hidden Prerequisite Likelihood",
            "definition": "The likelihood that the function requires other API calls to be made beforehand to work correctly",
            "question": "How likely is this function to require prior API calls that aren't immediately obvious from its signature or primary purpose?",
            "scale": [
                "Completely self-contained function with no prerequisites",
                "Some prerequisites that are logically expected and straightforward",
                "Critical prerequisites that aren't obvious from the function's definition"
            ]
        },
        {
            "name": "State Dependency Likelihood",
            "definition": "The likelihood that the function depends on specific system or session states to operate correctly",
            "question": "How likely is this function to rely on particular states that must be established through other operations?",
            "scale": [
                "State-independent function that works the same regardless of system state",
                "Some state dependencies that follow logical patterns",
                "Strong dependencies on specific states that must be precisely established"
            ]
        },
        {
            "name": "Cross-Service Interaction Likelihood",
            "definition": "The likelihood that the function requires interaction with multiple services or systems",
            "question": "How likely is this function to involve coordination across different services, potentially with their own authentication and data models?",
            "scale": [
                "Contained within a single service with no external dependencies",
                "Limited interaction with closely related services",
                "Complex coordination across multiple disparate services"
            ]
        },
        {
            "name": "Sequential Operation Requirement Likelihood",
            "definition": "The likelihood that the function is part of a sequence of operations that must be performed in a specific order",
            "question": "How likely is this function to be just one step in a chain of operations that must follow a specific sequence?",
            "scale": [
                "Standalone function that operates independently",
                "Part of a logical flow but with flexible ordering",
                "Strict sequential requirements with specific operations before and after"
            ]
        }
    ]
}

# Dimension 2: Uncertainty in API Return Values

INFORMATIONAL_NOTICE = {
    "name": "Informational Notice",
    "description": "Non-critical messages providing supplementary information or warnings about future changes.",
    "examples": [
        "Parameter 'hourly_forecast' will be deprecated in future versions",
        "Query response time: 1.2s. Consider using the batch API for multiple requests"
    ],
    "criteria": [
        {
            "name": "Lifecycle Status Communication Likelihood",
            "definition": "The likelihood that the function needs to communicate its own lifecycle status (beta, stable, deprecated)",
            "question": "How likely is this function to need warnings about its future availability, changes, or deprecation?",
            "scale": [
                "Stable function with no foreseeable changes in lifecycle",
                "Function that might undergo minor changes worth notifying about",
                "Function likely to change significantly or be deprecated in future versions"
            ]
        },
        {
            "name": "Performance Insight Likelihood",
            "definition": "The likelihood that the function provides performance-related metrics or recommendations",
            "question": "How likely is this function to offer insights about its execution performance or efficiency suggestions?",
            "scale": [
                "Simple function where performance is consistent and predictable",
                "Function where performance might vary in certain circumstances",
                "Complex function likely to include execution statistics and optimization suggestions"
            ]
        },
        {
            "name": "Alternative Approach Suggestion Likelihood",
            "definition": "The likelihood that the function suggests other approaches or alternative functions",
            "question": "How likely is this function to recommend different methods or alternative APIs for certain use cases?",
            "scale": [
                "Specialized function with no reasonable alternatives",
                "Function with some alternatives in specific situations",
                "Function with many alternatives that might be more suitable depending on context"
            ]
        },
        {
            "name": "Usage Pattern Feedback Likelihood",
            "definition": "The likelihood that the function provides feedback on how it's being used",
            "question": "How likely is this function to comment on the caller's usage patterns or parameter choices?",
            "scale": [
                "Simple function where usage patterns don't significantly matter",
                "Function that might suggest better usage in some circumstances",
                "Complex function likely to provide feedback on usage optimization"
            ]
        }
    ]
}

FEATURE_LIMITATION_ERROR = {
    "name": "Feature Limitation Error",
    "description": "Responses that restrict certain features but offer workarounds or alternative paths to success.",
    "examples": [
        "API rejects 'city' parameters while accepting 'state' parameters (workaround)",
        "Daily forecast limit reached. Try using hourly forecast instead (workaround)"
    ],
    "criteria": [
        # {
        #     "name": "Usage Quota Constraint Likelihood",
        #     "definition": "The likelihood that the function enforces usage quotas or rate limits with suggested alternatives",
        #     "question": "How likely is this function to have usage limits that require users to adopt alternative approaches?",
        #     "scale": [
        #         "No usage limits or quotas",
        #         "Moderate limits with straightforward alternatives",
        #         "Strict limits with complex alternative approaches required"
        #     ]
        # },
        {
            "name": "Parameter Constraint Likelihood",
            "definition": "The likelihood that the function restricts certain parameter values but accepts alternatives",
            "question": "How likely is this function to reject certain parameter values while suggesting alternative parameters?",
            "scale": [
                "Accepts all logical parameter values without constraints",
                "Some parameter constraints with obvious alternatives",
                "Significant parameter restrictions requiring non-obvious alternative approaches"
            ]
        },
        {
            "name": "Data Granularity Limitation Likelihood",
            "definition": "The likelihood that the function limits data detail/granularity but offers alternative data forms",
            "question": "How likely is this function to restrict data granularity while suggesting alternative data formats?",
            "scale": [
                "Provides data at full granularity without limitations",
                "Some granularity limits with clear alternative formats",
                "Significant granularity restrictions requiring substantially different data approaches"
            ]
        },
        # {
        #     "name": "Paid Feature Alternative Likelihood",
        #     "definition": "The likelihood that the function offers limited capabilities in its free version while suggesting workarounds for users who don't have paid access",
        #     "question": "How likely is this function to have premium features with suggested alternatives for free-tier users?",
        #     "scale": [
        #         "All capabilities available to all users regardless of payment status",
        #         "Some premium capabilities with simple workarounds for free users",
        #         "Significant premium capabilities requiring complex workarounds for free users"
        #     ]
        # }
    ]
}

SYSTEM_FAILURE_ERROR = {
    "name": "System Failure Error",
    "description": "Critical responses signaling major functionality disruption with no available workarounds within the current request context.",
    "examples": [
        "Weather service is unavailable due to critical infrastructure failure",
        "Authentication service timeout. Retry after system maintenance window (estimated: 2 hours)"
    ],
    "criteria": [
        {
            "name": "External Service Dependency Likelihood",
            "definition": "The likelihood that the function depends on external services that could experience complete outages",
            "question": "How likely is this function to rely on external services that might become entirely unavailable?",
            "scale": [
                "Self-contained function with no external dependencies",
                "Limited dependencies on generally reliable external services",
                "Critical dependencies on multiple or less reliable external services"
            ]
        },
        {
            "name": "Infrastructure Complexity Likelihood",
            "definition": "The likelihood that the function requires complex infrastructure that could experience catastrophic failures",
            "question": "How complex is the infrastructure needed to support this function's operation?",
            "scale": [
                "Simple infrastructure with minimal points of failure",
                "Moderately complex infrastructure with some redundancy",
                "Highly complex infrastructure with multiple potential failure points"
            ]
        },
        {
            "name": "Resource Intensity Likelihood",
            "definition": "The likelihood that the function requires intensive computational resources that could become exhausted",
            "question": "How resource-intensive is this function under normal or peak usage?",
            "scale": [
                "Minimal resource requirements with negligible failure risk",
                "Moderate resource requirements with occasional strain",
                "High resource demands that could exceed available capacity"
            ]
        },
        {
            "name": "Critical Path Position Likelihood",
            "definition": "The likelihood that the function sits on a critical path where failure affects entire system operation",
            "question": "How central is this function to the overall system's ability to operate?",
            "scale": [
                "Auxiliary function whose failure would have minimal system impact",
                "Important function that affects some but not all operations",
                "Core function whose failure would render the entire system inoperable"
            ]
        },
        {
            "name": "Scheduled Maintenance Requirement Likelihood",
            "definition": "The likelihood that the function requires regular maintenance windows causing scheduled downtime",
            "question": "How likely is this function to need periodic maintenance that results in planned unavailability?",
            "scale": [
                "Requires no maintenance windows or downtime",
                "Occasional brief maintenance requirements",
                "Regular or extended maintenance periods necessary"
            ]
        }
    ]
}

PARTIALLY_IRRELEVANT_INFORMATION = {
    "name": "Partially Irrelevant Information",
    "description": "Responses containing some unrelated information mixed with relevant data.",
    "examples": [
        "API returns requested data mixed with promotional content",
        "Vehicle status API including both critical information (fuel level) and non-critical metadata (lifetime mileage statistics)"
    ],
    "criteria": [
        {
            "name": "Data Aggregation Scope Likelihood",
            "definition": "The likelihood that the function aggregates data from multiple sources or domains",
            "question": "How likely is this function to collect and combine data from different systems or contexts?",
            "scale": [
                "Focused function that retrieves data from a single, well-defined source",
                "Function that combines closely related data from a few sources",
                "Function that pulls diverse data from many different systems or domains"
            ]
        },
        {
            "name": "Metadata Inclusion Likelihood",
            "definition": "The likelihood that the function includes extensive metadata alongside primary data",
            "question": "How likely is this function to return supplementary metadata in addition to the specifically requested information?",
            "scale": [
                "Returns only the explicitly requested data",
                "Returns modest metadata that's closely related to the requested data",
                "Returns extensive metadata that goes well beyond what was specifically requested"
            ]
        },
        {
            "name": "Historical Data Bundling Likelihood",
            "definition": "The likelihood that the function includes historical or trend data alongside current information",
            "question": "How likely is this function to include past data or trends when current data is requested?",
            "scale": [
                "Provides only the current/requested timeframe data",
                "Includes some limited historical context when relevant",
                "Automatically bundles extensive historical data with current information"
            ]
        },
        {
            "name": "Promotional Content Inclusion Likelihood",
            "definition": "The likelihood that the function includes marketing or promotional content in responses",
            "question": "How likely is this function to include advertisements, upgrade offers, or other promotional material?",
            "scale": [
                "Contains only factual data with no promotional elements",
                "Contains subtle promotional elements in specific circumstances",
                "Regularly includes prominent promotional content with functional data"
            ]
        },
        {
            "name": "Related Functionality Suggestion Likelihood",
            "definition": "The likelihood that the function provides information about related features beyond what was requested",
            "question": "How likely is this function to suggest or provide data about other available functionality?",
            "scale": [
                "Focuses solely on the requested functionality",
                "Occasionally includes information about closely related functions",
                "Regularly provides extensive information about additional services or functions"
            ]
        }
    ]
}

COMPLETELY_IRRELEVANT_INFORMATION = {
    "name": "Completely Irrelevant Information",
    "description": "Responses with no useful information for the task.",
    "examples": [
        "System responding with cached or default values unrelated to the query parameters"
    ],
    "criteria": [
        {
            "name": "Default Response Fallback Likelihood",
            "definition": "The likelihood that the function returns default or placeholder data when unable to process the request properly",
            "question": "How likely is this function to return generic default values instead of failing explicitly when it cannot produce relevant results?",
            "scale": [
                "Always fails explicitly rather than returning irrelevant defaults",
                "Occasionally returns defaults in specific edge cases",
                "Frequently falls back to returning default data when processing issues occur"
            ]
        },
        {
            "name": "Outdated Cache Return Likelihood",
            "definition": "The likelihood that the function returns cached data regardless of its relevance to the current query",
            "question": "How likely is this function to serve old cached responses without validating their relevance to the current request?",
            "scale": [
                "No caching or always validates cache relevance",
                "Limited caching with some validation mechanisms",
                "Heavy reliance on caching with minimal relevance validation"
            ]
        },
        {
            "name": "Request Misinterpretation Likelihood",
            "definition": "The likelihood that the function fundamentally misinterprets the request parameters",
            "question": "How likely is this function to completely misunderstand what was requested and return unrelated information?",
            "scale": [
                "Straightforward parameter interpretation with minimal ambiguity",
                "Some potential for parameter misinterpretation in complex cases",
                "High risk of parameter misinterpretation due to complexity or ambiguity"
            ]
        },
        {
            "name": "Error Suppression Likelihood",
            "definition": "The likelihood that the function hides errors by returning nominal but irrelevant responses",
            "question": "How likely is this function to mask errors by returning seemingly valid but completely irrelevant data?",
            "scale": [
                "Transparent error reporting without masking failures",
                "Some error conditions might be masked with partial information",
                "Strong tendency to hide errors behind irrelevant normal-looking responses"
            ]
        }
    ]
}

# Dictionary of all uncertainty types for easy access
UNCERTAINTY_TYPES = {
    "ambiguous_documentation": AMBIGUOUS_DOCUMENTATION,
    "ad_hoc_rules": AD_HOC_RULES,
    "unclear_functionality_boundaries": UNCLEAR_FUNCTIONALITY_BOUNDARIES,
    "complex_dependency_chains": COMPLEX_DEPENDENCY_CHAINS,
    "informational_notice": INFORMATIONAL_NOTICE,
    "feature_limitation_error": FEATURE_LIMITATION_ERROR,
    "system_failure_error": SYSTEM_FAILURE_ERROR,
    "partially_irrelevant_information": PARTIALLY_IRRELEVANT_INFORMATION,
    "completely_irrelevant_information": COMPLETELY_IRRELEVANT_INFORMATION
}

# Helper functions

def get_uncertainty_type(type_name):
    """
    Get uncertainty type details by name.
    
    Args:
        type_name: String key for the uncertainty type
        
    Returns:
        Dictionary containing the uncertainty type details
    """
    return UNCERTAINTY_TYPES.get(type_name)

def get_all_uncertainty_types():
    """
    Get a list of all available uncertainty types.
    
    Returns:
        List of uncertainty type names
    """
    return list(UNCERTAINTY_TYPES.keys())

def format_criteria_for_assessment(uncertainty_type):
    """
    Format an uncertainty type's criteria for inclusion in assessment instructions.
    
    Args:
        uncertainty_type: String key for the uncertainty type or uncertainty type dict
        
    Returns:
        Formatted string with criteria ready for assessment template
    """
    if isinstance(uncertainty_type, str):
        uncertainty_type = get_uncertainty_type(uncertainty_type)
        
    if not uncertainty_type:
        return "Unknown uncertainty type"
        
    result = [uncertainty_type["name"] + "\n"]
    result.append("Criteria:")
    
    for i, criterion in enumerate(uncertainty_type["criteria"], 1):
        result.append(f"{i}. {criterion['name']}")
        result.append(f"   - Definition: {criterion['definition']}")
        result.append(f"   - Assessment Question: {criterion['question']}")
        result.append("   - Rating Scale:")
        result.append(f"     - 0: {criterion['scale'][0]}")
        result.append(f"     - 1: {criterion['scale'][1]}")
        result.append(f"     - 2: {criterion['scale'][2]}")
        result.append("")
        
    return "\n".join(result)
