# Security Policy

## Overview

This document outlines the security measures implemented in the white-paper project to protect against common vulnerabilities and ensure safe operation.

## Security Improvements Implemented

### 1. Code Injection Prevention

**Issue**: The application previously used `exec()` to execute AI-generated code without validation, which could allow arbitrary code execution.

**Solution**: Implemented `validate_and_execute_chart_code()` function that:
- Validates code using AST parsing before execution
- Checks for dangerous operations (eval, __import__, file operations, etc.)
- Limits code length (max 100 lines)
- Restricts imports to safe modules only (pyecharts, pandas, numpy, datetime, math)
- Executes code in a restricted scope with limited builtins

**Location**: `python/src/app.py`

### 2. Input Validation

**File Uploads**:
- Maximum file size: 10 MB
- CSV row limit: 100,000 rows
- Proper error handling for malformed CSV/JSON files
- File type validation

**Location**: `python/src/app.py`

### 3. Path Traversal Prevention

**Issue**: File paths were constructed using string concatenation without validation.

**Solution**:
- Replaced `os.path` with `pathlib.Path`
- Added path validation to ensure files are within expected directories
- Use `.resolve()` to get absolute paths and `.is_relative_to()` for validation

**Location**: `python/src/app.py`

### 4. Command Injection Prevention

**Issue**: Subprocess commands were executed using string-based `execSync()`, which is vulnerable to shell injection.

**Solution**:
- Replaced `execSync(string)` with `spawnSync(array)` syntax
- Commands are now passed as arrays, preventing shell injection

**Location**: `scripts/generate-pdfs.js`

### 5. API Key Security

**Current Measures**:
- API keys stored in `.env` file (not committed to version control)
- Keys masked in UI using `type="password"`
- Environment variables used for sensitive configuration
- Security notice displayed to users

**Location**: `python/src/app.py`

## Best Practices

### For Developers

1. **Never commit secrets**: Always use `.env` files for sensitive data
2. **Validate all inputs**: Check file sizes, formats, and content before processing
3. **Use parameterized queries**: When adding database support, use parameterized queries
4. **Keep dependencies updated**: Regularly update dependencies to patch security vulnerabilities
5. **Type safety**: Use type hints in Python and TypeScript for better code safety

### For Users

1. **Protect your API keys**: Never share your API keys or commit them to version control
2. **File uploads**: Only upload trusted CSV/JSON files
3. **Environment setup**: Follow the security setup in `config/.env.example`

## Reporting Security Issues

If you discover a security vulnerability, please report it by:

1. **Do NOT** open a public issue
2. Contact the repository maintainers directly
3. Provide detailed information about the vulnerability
4. Allow time for the issue to be fixed before public disclosure

## Security Checklist for New Features

When adding new features, ensure:

- [ ] All user inputs are validated
- [ ] File operations use safe path handling
- [ ] No use of `eval()`, `exec()`, or similar dangerous functions without validation
- [ ] Dependencies are from trusted sources
- [ ] Secrets are not hardcoded
- [ ] Error messages don't leak sensitive information
- [ ] Rate limiting is considered for resource-intensive operations

## Dependencies Security

### Python Dependencies

```
streamlit          # Web framework - keep updated
streamlit-echarts  # Chart rendering
pyecharts          # Chart library - added in security improvements
pandas             # Data processing
numpy              # Numerical operations
scipy              # Scientific computing
python-dotenv      # Environment variable management
openai             # AI integration - validate API responses
```

### JavaScript Dependencies

```
playwright         # Browser automation for PDF generation
express            # Web server - keep updated
react              # UI framework
typescript         # Type safety
echarts            # Charting library
recharts           # React charts
vite               # Build tool
```

## Regular Security Tasks

- [ ] Review and update dependencies monthly
- [ ] Scan for known vulnerabilities using GitHub Dependabot
- [ ] Review access controls and permissions
- [ ] Audit logs for suspicious activity (when logging is fully implemented)
- [ ] Test input validation with edge cases

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [Node.js Security Best Practices](https://nodejs.org/en/docs/guides/security/)

## Version History

- **2024-01**: Initial security improvements implemented
  - Code injection prevention
  - Input validation
  - Path traversal prevention
  - Command injection fixes
  - Type hints added
