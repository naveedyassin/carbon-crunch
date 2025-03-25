import re
from typing import List, Dict, Any

def analyze_javascript_code(code: str) -> Dict[str, Any]:
    """Analyze JavaScript/JSX code for clean code practices."""
    # Initialize scores
    scores = {
        "naming": 10,
        "modularity": 20,
        "comments": 20,
        "formatting": 15,
        "reusability": 15,
        "best_practices": 20
    }
    
    recommendations = []
    
    # Check naming conventions
    naming_issues = check_js_naming(code)
    if naming_issues:
        scores["naming"] = max(0, scores["naming"] - len(naming_issues) * 2)
        recommendations.extend(naming_issues)
    
    # Check function length and modularity
    modularity_issues = check_js_function_length(code)
    if modularity_issues:
        scores["modularity"] = max(0, scores["modularity"] - len(modularity_issues) * 3)
        recommendations.extend(modularity_issues)
    
    # Check comments and documentation
    comment_issues = check_js_comments(code)
    if comment_issues:
        scores["comments"] = max(0, scores["comments"] - len(comment_issues) * 4)
        recommendations.extend(comment_issues)
    
    # Check formatting
    formatting_issues = check_js_formatting(code)
    if formatting_issues:
        scores["formatting"] = max(0, scores["formatting"] - len(formatting_issues) * 3)
        recommendations.extend(formatting_issues)
    
    # Check reusability and DRY
    reusability_issues = check_js_reusability(code)
    if reusability_issues:
        scores["reusability"] = max(0, scores["reusability"] - len(reusability_issues) * 3)
        recommendations.extend(reusability_issues)
    
    # Check best practices
    best_practice_issues = check_js_best_practices(code)
    if best_practice_issues:
        scores["best_practices"] = max(0, scores["best_practices"] - len(best_practice_issues) * 4)
        recommendations.extend(best_practice_issues)
    
    # Calculate overall score
    overall_score = sum(scores.values())
    
    return {
        "overall_score": overall_score,
        "breakdown": scores,
        "recommendations": recommendations[:5]  # Return top 5 recommendations
    }

def check_js_naming(code: str) -> List[str]:
    """Check JavaScript naming conventions."""
    issues = []
    
    # Function names should be camelCase
    function_pattern = r'function\s+([A-Za-z_][A-Za-z0-9_]*)\s*\('
    for match in re.finditer(function_pattern, code):
        func_name = match.group(1)
        if not re.fullmatch(r'[a-z][a-zA-Z0-9]*', func_name):
            issues.append(f"Function '{func_name}' should use camelCase naming convention.")
    
    # Component names should be PascalCase
    component_pattern = r'const\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*\(?\{\s*\)?\s*=>'
    for match in re.finditer(component_pattern, code):
        component_name = match.group(1)
        if not re.fullmatch(r'[A-Z][a-zA-Z0-9]*', component_name):
            issues.append(f"React component '{component_name}' should use PascalCase naming convention.")
    
    # Variable names should be camelCase
    variable_pattern = r'(?:const|let|var)\s+([A-Za-z_][A-Za-z0-9_]*)'
    for match in re.finditer(variable_pattern, code):
        var_name = match.group(1)
        if var_name != var_name.upper() and not re.fullmatch(r'[a-z][a-zA-Z0-9]*', var_name):
            issues.append(f"Variable '{var_name}' should use camelCase naming convention.")
    
    return issues

def check_js_function_length(code: str) -> List[str]:
    """Check for overly long functions in JavaScript."""
    issues = []
    function_pattern = r'function\s+([A-Za-z_][A-Za-z0-9_]*)\s*\([^)]*\)\s*\{([^}]*)\}'
    
    for match in re.finditer(function_pattern, code, re.DOTALL):
        func_name = match.group(1)
        body = match.group(2)
        lines = body.count('\n') + 1
        if lines > 20:
            issues.append(f"Function '{func_name}' is too long ({lines} lines). Consider refactoring into smaller functions.")
        elif lines > 15:
            issues.append(f"Function '{func_name}' is somewhat long ({lines} lines). Consider if it can be broken down.")
    
    # Check arrow functions
    arrow_pattern = r'const\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*\([^)]*\)\s*=>\s*\{([^}]*)\}'
    for match in re.finditer(arrow_pattern, code, re.DOTALL):
        func_name = match.group(1)
        body = match.group(2)
        lines = body.count('\n') + 1
        if lines > 20:
            issues.append(f"Function '{func_name}' is too long ({lines} lines). Consider refactoring into smaller functions.")
        elif lines > 15:
            issues.append(f"Function '{func_name}' is somewhat long ({lines} lines). Consider if it can be broken down.")
    
    return issues

def check_js_comments(code: str) -> List[str]:
    """Check for comments and documentation in JavaScript."""
    issues = []
    
    # Check for JSDoc comments on functions
    function_pattern = r'function\s+([A-Za-z_][A-Za-z0-9_]*)\s*\('
    for match in re.finditer(function_pattern, code):
        func_name = match.group(1)
        # Look for /** ... */ before the function
        preceding_code = code[:match.start()]
        if not re.search(r'/\*\*.*?\*/', preceding_code, re.DOTALL):
            issues.append(f"Add JSDoc documentation for function '{func_name}'.")
    
    # Check for commented code
    commented_code = re.findall(r'//\s*[^\s]', code)
    if len(commented_code) > 5:  # Arbitrary threshold
        issues.append("Avoid excessive single-line comments. Use them sparingly for important notes.")
    
    return issues

def check_js_formatting(code: str) -> List[str]:
    """Check basic JavaScript formatting issues."""
    issues = []
    lines = code.split('\n')
    
    # Check indentation (simple check)
    for i, line in enumerate(lines, 1):
        if line.strip() and not line.startswith((' ', '\t', '}', ']', ')', '//', '/*', '*')):
            issues.append(f"Line {i}: Possible indentation issue detected.")
    
    # Check semicolons (optional in JS but can be enforced)
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped and not stripped.startswith(('//', '/*', '*', '}', '{')) and not stripped.endswith((';', '{', '}', ':', '(', '[', ',')):
            issues.append(f"Line {i}: Consider adding a semicolon at the end of the statement.")
    
    return issues

def check_js_reusability(code: str) -> List[str]:
    """Check for code duplication in JavaScript."""
    issues = []
    # This is a simplified check - a real implementation would need more sophisticated analysis
    
    # Look for repeated code blocks
    lines = [line.strip() for line in code.split('\n') if line.strip()]
    line_counts = {}
    for line in lines:
        if len(line) > 20:  # Only consider significant lines
            line_counts[line] = line_counts.get(line, 0) + 1
    
    for line, count in line_counts.items():
        if count > 3:
            issues.append(f"Similar code appears {count} times. Consider refactoring into a reusable function.")
    
    return issues

def check_js_best_practices(code: str) -> List[str]:
    """Check for JavaScript best practice violations."""
    issues = []
    
    # Check for == instead of ===
    if ' == ' in code:
        issues.append("Use strict equality (===) instead of loose equality (==) to avoid type coercion.")
    
    # Check for var instead of const/let
    if re.search(r'\bvar\s+', code):
        issues.append("Prefer 'const' or 'let' over 'var' for variable declarations.")
    
    # Check for console.log left in code
    if 'console.log' in code:
        issues.append("Remove or comment out 'console.log' statements before committing.")
    
    # Check for React key prop in lists
    if 'map(' in code and 'key={' not in code:
        issues.append("When rendering lists in React, provide a unique 'key' prop to each child.")
    
    return issues