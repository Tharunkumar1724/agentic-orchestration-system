# Contributing to Agentic Orchestration System

Thank you for your interest in contributing! We welcome contributions from the community.

## 🤝 How to Contribute

### Reporting Issues
- **Bug Reports**: Use GitHub Issues with the `bug` label
- **Feature Requests**: Use GitHub Issues with the `enhancement` label
- **Questions**: Use GitHub Discussions

### Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/Tharunkumar1724/agentic-orchestration-system.git
   cd agentic-orchestration-system
   ```

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add tests for new features
   - Update documentation as needed

4. **Test your changes**
   ```powershell
   # Run backend tests
   python -m pytest tests/
   
   # Test specific features
   python test_metrics_complete.py
   python test_dynamic_tools.py
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: Add your feature description"
   # or
   git commit -m "fix: Fix bug description"
   ```

   **Commit Message Format:**
   - `feat:` New feature
   - `fix:` Bug fix
   - `docs:` Documentation changes
   - `style:` Code style changes (formatting, etc.)
   - `refactor:` Code refactoring
   - `test:` Adding or updating tests
   - `chore:` Maintenance tasks

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Go to GitHub and create a PR from your fork
   - Fill in the PR template
   - Link any related issues

## 📋 Development Guidelines

### Code Style

**Python (Backend)**
- Follow PEP 8 style guide
- Use type hints where possible
- Document functions with docstrings
- Keep functions focused and small

**JavaScript/React (Frontend)**
- Use ES6+ features
- Follow React best practices
- Use functional components with hooks
- Keep components small and reusable

### Testing

**Backend Tests**
```python
# Add tests in tests/ directory
def test_your_feature():
    # Arrange
    client = AgenticToolClient()
    
    # Act
    result = client.your_method()
    
    # Assert
    assert result is not None
```

**Frontend Tests**
```javascript
// Add tests alongside components
import { render, screen } from '@testing-library/react';

test('renders component', () => {
  render(<YourComponent />);
  expect(screen.getByText(/text/i)).toBeInTheDocument();
});
```

### Documentation

- Update README.md if you add major features
- Add inline comments for complex logic
- Update API documentation for new endpoints
- Create guide documents for new features (see existing guides)

## 🎯 Areas for Contribution

### High Priority
- [ ] Additional tool templates (15+ goal)
- [ ] Enhanced metrics visualization
- [ ] Docker/Kubernetes deployment templates
- [ ] RAG integration for KAG service
- [ ] Multi-LLM parallel execution

### Medium Priority
- [ ] More comprehensive test coverage
- [ ] Performance optimizations
- [ ] Additional LLM provider integrations
- [ ] Workflow template library
- [ ] Enhanced error handling

### Documentation
- [ ] Video tutorials
- [ ] More code examples
- [ ] Translation to other languages
- [ ] Interactive documentation

## 🐛 Bug Reports

When reporting bugs, include:

1. **Description**: Clear description of the bug
2. **Steps to Reproduce**: Detailed steps to reproduce
3. **Expected Behavior**: What should happen
4. **Actual Behavior**: What actually happens
5. **Environment**:
   - OS (Windows/Linux/Mac)
   - Python version
   - Node.js version (if frontend)
   - LLM provider being used
6. **Logs**: Relevant error messages or logs

## 💡 Feature Requests

When requesting features, include:

1. **Use Case**: Why is this feature needed?
2. **Description**: Detailed description of the feature
3. **Proposed Solution**: How you think it should work
4. **Alternatives**: Other solutions you've considered
5. **Additional Context**: Any other relevant information

## ✅ Code Review Process

1. All PRs require at least one review
2. CI/CD checks must pass
3. Code must follow style guidelines
4. Tests must be included for new features
5. Documentation must be updated

## 📝 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be recognized in:
- README.md acknowledgments
- Release notes
- GitHub contributors page

## 📞 Getting Help

- **Questions**: Use GitHub Discussions
- **Issues**: Create a GitHub Issue
- **Real-time Chat**: Coming soon (Discord/Slack)

## 🌟 First-Time Contributors

New to open source? We welcome first-time contributors!

**Good First Issues**: Look for issues labeled `good-first-issue`

**Resources**:
- [How to Contribute to Open Source](https://opensource.guide/how-to-contribute/)
- [First Contributions](https://github.com/firstcontributions/first-contributions)
- [GitHub Flow](https://guides.github.com/introduction/flow/)

---

Thank you for contributing to Agentic Orchestration System! 🚀
