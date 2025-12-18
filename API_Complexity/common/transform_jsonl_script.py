#!/usr/bin/env python3
"""Script to transform API sequences in a JSONL file using a mapping file.

The script matches the order of mappings in the mapping file to the order of
API calls in the JSONL file on a one-to-one basis and applies parameter-level
transformations.
"""

import json
import argparse
import re
import ast
from pathlib import Path


def load_mapping_file(mapping_file):
    """Load the mapping file and return the transform information."""
    with open(mapping_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_jsonl_lines(jsonl_file):
    """Load a JSONL file and return a list of JSON objects per line."""
    lines = []
    with open(jsonl_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                lines.append(json.loads(line))
    return lines


def save_jsonl_lines(jsonl_file, lines):
    """Save a list of JSON objects to a JSONL file."""
    with open(jsonl_file, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(json.dumps(line, ensure_ascii=False) + '\n')


def flatten_api_calls(jsonl_lines):
    """Flatten all API calls across JSONL lines in sequence order."""
    flat_apis = []
    for line_idx, line in enumerate(jsonl_lines):
        api_sequence = line.get("api_sequence", [])
        for api_idx, api_call in enumerate(api_sequence):
            flat_apis.append({
                "line_idx": line_idx,
                "api_idx": api_idx,
                "api_call": api_call.copy()
            })
    return flat_apis


def parse_invoke_tool_with_ast(code_str):
    """Parse an invoke_tool call using AST and extract API name & params."""
    try:
        # Parse an expression of the form: invoke_tool("api", ...)
        tree = ast.parse(code_str, mode='eval')
        call_node = tree.body
        
        if not isinstance(call_node, ast.Call):
            return None
        
        # Check function name
        if (
            isinstance(call_node.func, ast.Name)
            and call_node.func.id == 'invoke_tool'
        ):
            # First argument = API name
            api_name = ast.literal_eval(call_node.args[0]) if call_node.args else None
            if not api_name:
                return None
            
            # Keyword arguments = parameters
            params = {}
            for keyword in call_node.keywords:
                if keyword.arg:  # Ensure keyword.arg is not None
                    params[keyword.arg] = ast.literal_eval(keyword.value)
            
            return {"api": api_name, "params": params}
    except Exception as e:
        print(f"   AST parse failed: {e}")
        return None


def extract_param_changes_from_mapping_ast(mapping):
    """Detect parameter changes using AST-based parsing of invoke_tool calls."""
    before = mapping.get("before", "")
    after = mapping.get("after", "")
    
    if before == after:
        return None
    
    # Parse with AST
    before_parsed = parse_invoke_tool_with_ast(before)
    after_parsed = parse_invoke_tool_with_ast(after)
    
    if not (before_parsed and after_parsed):
        return None
    
    if before_parsed["api"] != after_parsed["api"]:
        return None
    
    # Find parameter-level changes
    param_changes = {}
    before_params = before_parsed["params"]
    after_params = after_parsed["params"]
    
    for param_name in before_params:
        if (
            param_name in after_params
            and before_params[param_name] != after_params[param_name]
        ):
            param_changes[param_name] = {
                "before": before_params[param_name],
                "after": after_params[param_name]
            }
    
    return {
        "api": before_parsed["api"],
        "param_changes": param_changes
    } if param_changes else None


def extract_param_changes_from_mapping_regex(mapping):
    """Detect parameter changes using regex parsing of invoke_tool calls (fallback)."""
    before = mapping.get("before", "")
    after = mapping.get("after", "")
    
    if before == after:
        return None
    
    # Example:
    # invoke_tool("track_order", order_id='ORDER0046')
    #   → invoke_tool("track_order", order_id='OnTrac-DER0046')
    
    # Extract API name and parameter string via regex
    before_match = re.search(r'invoke_tool\([\'\"]([^\'\"]+)[\'\"](?:,\s*(.+))?\)', before)
    after_match = re.search(r'invoke_tool\([\'\"]([^\'\"]+)[\'\"](?:,\s*(.+))?\)', after)
    
    if not before_match or not after_match:
        return None
    
    api_name = before_match.group(1)
    before_params = before_match.group(2) if before_match.group(2) else ""
    after_params = after_match.group(2) if after_match.group(2) else ""
    
    if before_params == after_params:
        return None
    
    # Parse parameter changes into a dictionary
    param_changes = {}
    
    # Simple parsing: key=value style
    before_param_dict = parse_params(before_params)
    after_param_dict = parse_params(after_params)
    
    # Extract only changed parameters
    for key in before_param_dict:
        if key in after_param_dict and before_param_dict[key] != after_param_dict[key]:
            param_changes[key] = {
                "before": before_param_dict[key],
                "after": after_param_dict[key]
            }
    
    return {
        "api": api_name,
        "param_changes": param_changes
    } if param_changes else None


def extract_param_changes_from_mapping(mapping):
    """Extract parameter-level changes from a mapping (AST first, regex as fallback)."""
    # Try AST-based method first
    result = extract_param_changes_from_mapping_ast(mapping)
    if result:
        print("   AST-based parse succeeded")
        return result
    
    # If AST parsing fails, use the legacy regex-based method
    print("   AST-based parse failed, falling back to regex-based method")
    return extract_param_changes_from_mapping_regex(mapping)


def parse_params(param_str):
    """Parse a parameter string into a dictionary."""
    if not param_str:
        return {}
    
    params = {}
    # Simple parsing of key='value' or key=value style
    param_matches = re.findall(r'(\w+)=([\'\"]?)([^\'\"]+)\2', param_str)
    
    for match in param_matches:
        key = match[0]
        value = match[2]
        params[key] = value
    
    return params


def apply_transformation_to_api_call(api_call, param_changes):
    """Apply parameter changes only to the `params` section of an API call."""
    if not param_changes:
        return api_call
    
    api_name = param_changes.get("api")
    changes = param_changes.get("param_changes", {})
    
    # Ensure the API name matches
    if api_call.get("api") != api_name:
        return api_call
    
    # Apply parameter changes to the `params` dict only
    params = api_call.get("params", {})
    for param_name, change in changes.items():
        if param_name in params and params[param_name] == change["before"]:
            params[param_name] = change["after"]
    
    # Do not modify description
    # Do not modify context or other fields
    
    return api_call


def transform_jsonl_with_mapping(mapping_file, input_jsonl, output_jsonl):
    """Transform a JSONL file using the provided mapping file."""
    print(f"📖 Reading mapping file: {mapping_file}")
    mapping_data = load_mapping_file(mapping_file)
    mappings = mapping_data.get("mappings", [])
    
    print(f"📖 Reading JSONL file: {input_jsonl}")
    jsonl_lines = load_jsonl_lines(input_jsonl)
    
    print("🔄 Flattening API calls")
    flat_apis = flatten_api_calls(jsonl_lines)
    
    print("📊 Mapping statistics:")
    print(f"   Total mappings: {len(mappings)}")
    print(f"   Total API calls: {len(flat_apis)}")
    
    if len(mappings) != len(flat_apis):
        print(f"⚠️  Warning: Number of mappings ({len(mappings)}) does not match number of API calls ({len(flat_apis)})!")
    
    # Apply mappings in order
    transform_count = 0
    for i, (flat_api, mapping) in enumerate(zip(flat_apis, mappings)):
        print(f"🔄 Processing ({i+1}/{len(flat_apis)}): {flat_api['api_call'].get('api', 'unknown')}")
        
        # Extract parameter changes from mapping
        param_changes = extract_param_changes_from_mapping(mapping)
        
        if param_changes:
            print(f"   Applying transform: {param_changes}")
            # Apply transform to the API call
            flat_api["api_call"] = apply_transformation_to_api_call(flat_api["api_call"], param_changes)
            flat_api["param_changes"] = param_changes  # For potential future context updates
            transform_count += 1
        else:
            print("   No transform applied")
            flat_api["param_changes"] = None
    
    print(f"✅ Finished applying transforms to {transform_count} API call(s)")
    
    # Reconstruct the JSONL structure with transformed API calls
    print("🔄 Reconstructing JSONL structure")
    for flat_api in flat_apis:
        line_idx = flat_api["line_idx"]
        api_idx = flat_api["api_idx"]
        jsonl_lines[line_idx]["api_sequence"][api_idx] = flat_api["api_call"]
        
        # Do not modify context or other fields (only params in api_sequence)
    
    print(f"💾 Saving transformed JSONL file: {output_jsonl}")
    # Ensure the output directory exists
    output_path = Path(output_jsonl)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    save_jsonl_lines(output_jsonl, jsonl_lines)
    
    print("✅ Transformation complete!")
    print(f"   Input: {input_jsonl}")
    print(f"   Output: {output_jsonl}")
    print(f"   Total lines: {len(jsonl_lines)}")
    print(f"   Total API calls: {len(flat_apis)}")
    print(f"   Transforms applied: {transform_count}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Transform JSONL API sequences using a mapping file')
    parser.add_argument('--mapping', required=True, help='Mapping JSON file path')
    parser.add_argument('--input', required=True, help='Input JSONL file path')
    parser.add_argument('--output', required=True, help='Output JSONL file path')
    
    args = parser.parse_args()
    
    try:
        transform_jsonl_with_mapping(args.mapping, args.input, args.output)
        print("🎉 Job complete!")
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
