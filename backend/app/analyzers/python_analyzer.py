import ast
import re
from typing import List, Dict, Any

def analyze_python_code(code: str) -> Dict[str, Any]:
    """Analyze Python code for clean code practices."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return {
            "overall_score": 0,
            "breakdown": {
                "naming": 0,
                "modularity": 0,
                "comments": 0,
                "formatting": 0,
                "reusability": 0,
                "best_practices": 0
            },
            "recommendations": ["Syntax error in the code. Please fix before analysis."]
        }

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
    naming_issues = check_python_naming(tree)
    if naming_issues:
        scores["naming"] = max(0, scores["naming"] - len(naming_issues) * 2)
        recommendations.extend(naming_issues)
    
    # Check function length and modularity
    modularity_issues = check_function_length(tree)
    if modularity_issues:
        scores["modularity"] = max(0, scores["modularity"] - len(modularity_issues) * 3)
        recommendations.extend(modularity_issues)
    
    # Check comments and docstrings
    comment_issues = check_comments_and_docstrings(tree)
    if comment_issues:
        scores["comments"] = max(0, scores["comments"] - len(comment_issues) * 4)
        recommendations.extend(comment_issues)
    
    # Check formatting
    formatting_issues = check_formatting(code)
    if formatting_issues:
        scores["formatting"] = max(0, scores["formatting"] - len(formatting_issues) * 3)
        recommendations.extend(formatting_issues)
    
    # Check reusability and DRY
    reusability_issues = check_reusability(tree)
    if reusability_issues:
        scores["reusability"] = max(0, scores["reusability"] - len(reusability_issues) * 3)
        recommendations.extend(reusability_issues)
    
    # Check best practices
    best_practice_issues = check_python_best_practices(tree, code)
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

def check_python_naming(tree) -> List[str]:
    """Check for Python naming convention violations."""
    issues = []
    reserved_words = {'sum', 'list', 'dict', 'str', 'int', 'file', 'id', 'type'}
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Check function names (should be snake_case)
            if not re.fullmatch(r'[a-z_][a-z0-9_]*', node.name):
                issues.append(f"Function '{node.name}' should use snake_case naming convention.")
            
            # Check arguments (should be snake_case)
            for arg in node.args.args:
                if not re.fullmatch(r'[a-z_][a-z0-9_]*', arg.arg):
                    issues.append(f"Argument '{arg.arg}' should use snake_case naming convention.")
        
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            # Check variable names (should be snake_case)
            if not re.fullmatch(r'[a-z_][a-z0-9_]*', node.id):
                issues.append(f"Variable '{node.id}' should use snake_case naming convention.")
            
            # Check for reserved words
            if node.id in reserved_words:
                issues.append(f"Avoid using '{node.id}' as a variable name—it's a Python built-in.")
    
    return issues

def check_function_length(tree) -> List[str]:
    """Check for overly long functions."""
    issues = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Count lines in function body
            lines = len(node.body)
            if lines > 20:
                issues.append(f"Function '{node.name}' is too long ({lines} lines). Consider refactoring into smaller functions.")
            elif lines > 15:
                issues.append(f"Function '{node.name}' is somewhat long ({lines} lines). Consider if it can be broken down.")
    
    return issues

def check_comments_and_docstrings(tree) -> List[str]:
    """Check for missing docstrings and comments."""
    issues = []
    
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
            # Check for docstring
            docstring = ast.get_docstring(node)
            if not docstring:
                if isinstance(node, ast.FunctionDef):
                    issues.append(f"Add a docstring to function '{node.name}' to explain its purpose.")
                elif isinstance(node, ast.ClassDef):
                    issues.append(f"Add a docstring to class '{node.name}' to explain its purpose.")
    
    # Check for commented code (bad practice)
    # This would require the raw code, so handled in check_formatting
    
    return issues

def check_formatting(code: str) -> List[str]:
    """Check basic formatting issues."""
    issues = []
    lines = code.split('\n')
    
    # Check for inconsistent indentation
    for i, line in enumerate(lines, 1):
        if line.strip() and not line.startswith((' ', '\t')) and not line.startswith(('def ', 'class ', 'import ', 'from ')):
            issues.append(f"Line {i}: Inconsistent indentation detected.")
    
    # Check for trailing whitespace
    for i, line in enumerate(lines, 1):
        if line.rstrip() != line:
            issues.append(f"Line {i}: Trailing whitespace detected.")
    
    # Check for commented code
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith('#') and len(stripped) > 1 and not stripped[1].isspace():
            # This is a simple check that might have false positives
            issues.append(f"Line {i}: Avoid commented-out code. Remove or explain with proper comments.")
    
    return issues

def check_reusability(tree) -> List[str]:
    """Check for code duplication and reusability issues."""
    issues = []
    functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    
    # Simple check for duplicate code (would need more sophisticated analysis in a real tool)
    function_bodies = {}
    for func in functions:
        body_str = ast.dump(func.body)
        if body_str in function_bodies:
            issues.append(f"Function '{func.name}' has similar code to '{function_bodies[body_str]}'. Consider refactoring to avoid duplication.")
        else:
            function_bodies[body_str] = func.name
    
    return issues

def check_python_best_practices(tree, code: str) -> List[str]:
    """Check for Python best practice violations."""
    issues = []
    
    # Check for use of bare except
    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler) and node.type is None:
            issues.append("Avoid bare 'except:' clauses. Specify the exception type.")
    
    # Check for mutable default arguments
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for default in node.args.defaults:
                if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                    issues.append(f"Function '{node.name}' uses mutable default argument. This can lead to unexpected behavior.")
    
    # Check for use of == None (should use is None)
    for node in ast.walk(tree):
        if isinstance(node, ast.Compare):
            for op in node.ops:
                if isinstance(op, ast.Eq):
                    if isinstance(node.comparators[0], ast.Constant) and node.comparators[0].value is None:
                        issues.append("Use 'is None' instead of '== None' for None comparisons.")
    
    return issues