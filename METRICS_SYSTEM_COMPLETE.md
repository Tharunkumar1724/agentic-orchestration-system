# 📊 Comprehensive Metrics System

## Overview

The system now tracks and displays **12 comprehensive metrics** for every workflow, solution, and chat execution. These metrics provide deep insights into performance, quality, and reliability.

---

## 📈 Available Metrics

### 1. **Performance Metrics**

#### Latency (ms)
- **Type**: Float
- **Description**: Total execution time in milliseconds
- **Range**: 0.0 - ∞
- **Lower is better**
- **Example**: `1523.45` (1.5 seconds)

#### Token Usage Count
- **Type**: Integer
- **Description**: Total tokens consumed (input + output)
- **Range**: 0 - ∞
- **Use**: Track API costs and resource usage
- **Example**: `2847`

#### Token Input Count
- **Type**: Integer  
- **Description**: Tokens used for prompts/input
- **Example**: `1500`

#### Token Output Count
- **Type**: Integer
- **Description**: Tokens generated in responses
- **Example**: `1347`

---

### 2. **Quality Metrics**

#### Accuracy
- **Type**: Float (percentage)
- **Description**: Estimated accuracy based on tool success and completion
- **Range**: 0.0 - 100.0
- **Higher is better**
- **Calculation**: Based on tool success rate, agent performance, and error count
- **Example**: `87.5%`

#### Response Quality
- **Type**: Float (percentage)
- **Description**: Overall quality of the response
- **Range**: 0.0 - 100.0
- **Higher is better**
- **Factors**: Task completion, errors, token usage patterns
- **Example**: `92.0%`

#### Hallucination Rate
- **Type**: Float (percentage)
- **Description**: Estimated likelihood of incorrect/fabricated information
- **Range**: 0.0 - 100.0
- **Lower is better**
- **Factors**: Errors, tool failures, context quality
- **Example**: `5.2%`

#### Task Completion Rate
- **Type**: Float (percentage)
- **Description**: Percentage of task successfully completed
- **Range**: 0.0 - 100.0
- **Higher is better**
- **Values**:
  - `100%` = Full success
  - `50-99%` = Partial completion
  - `0%` = Failed
- **Example**: `100.0%`

#### Context Relation Quality
- **Type**: Float (percentage)
- **Description**: How well the response relates to the input context
- **Range**: 0.0 - 100.0
- **Higher is better**
- **Factors**: Tool success, agent performance, error count
- **Example**: `85.5%`

---

### 3. **Tool & Execution Metrics**

#### Tool Invocation Count
- **Type**: Integer
- **Description**: Number of tools/APIs called during execution
- **Range**: 0 - ∞
- **Example**: `5`

#### Tool Success Rate
- **Type**: Float (percentage)
- **Description**: Percentage of tool calls that succeeded
- **Range**: 0.0 - 100.0
- **Higher is better**
- **Calculation**: `(successful_tools / total_tools) * 100`
- **Example**: `80.0%` (4 out of 5 tools succeeded)

#### Retrieval Error Count
- **Type**: Integer
- **Description**: Number of failed tool/API calls
- **Range**: 0 - ∞
- **Lower is better**
- **Example**: `1`

---

### 4. **Decision & Structure Metrics**

#### Decision Depth
- **Type**: Integer
- **Description**: Depth of decision tree traversed
- **Range**: 0 - ∞
- **Use**: Understand execution complexity
- **Example**: `3` (3 decision points)

#### Branching Factor
- **Type**: Float
- **Description**: Average number of branches at each decision point
- **Range**: 1.0 - ∞
- **Values**:
  - `1.0` = Sequential workflow (no branching)
  - `> 1.0` = Parallel or conditional workflows
- **Example**: `2.5` (average of 2-3 branches per decision)

---

### 5. **Additional Tracking**

#### Agent Execution Count
- **Type**: Integer
- **Description**: Number of AI agents executed
- **Example**: `3`

#### Workflow Step Count
- **Type**: Integer
- **Description**: Total workflow steps/nodes executed
- **Example**: `4`

#### Errors
- **Type**: List[String]
- **Description**: List of errors encountered
- **Example**: `["Tool API timeout", "Agent not found"]`

#### Warnings
- **Type**: List[String]
- **Description**: List of warnings
- **Example**: `["High token usage detected"]`

---

## 🔍 Where Metrics Appear

### 1. Workflow Execution (`POST /workflows/{id}/run`)

**Response Structure:**
```json
{
  "workflow_id": "my_workflow",
  "run_id": "abc123",
  "status": "success",
  "results": {...},
  "metrics": {
    "accuracy": 92.5,
    "response_quality": 88.0,
    "hallucination_rate": 3.5,
    "task_completion_rate": 100.0,
    "token_usage_count": 2847,
    "token_input_count": 1500,
    "token_output_count": 1347,
    "latency_ms": 1523.45,
    "tool_invocation_count": 5,
    "tool_success_rate": 80.0,
    "retrieval_error_count": 1,
    "decision_depth": 3,
    "branching_factor": 1.0,
    "context_relation_quality": 85.5,
    "agent_execution_count": 3,
    "workflow_step_count": 4,
    "start_time": "2025-11-09T10:30:00",
    "end_time": "2025-11-09T10:30:01",
    "errors": [],
    "warnings": []
  }
}
```

### 2. Solution Execution (`POST /solutions/{id}/execute`)

**Response Structure:**
```json
{
  "solution_id": "my_solution",
  "solution_name": "Market Analysis",
  "execution_results": [
    {
      "workflow_id": "workflow_1",
      "metrics": {...}  // Individual workflow metrics
    },
    {
      "workflow_id": "workflow_2",
      "metrics": {...}
    }
  ],
  "metrics": {
    // AGGREGATED metrics across all workflows
    "accuracy": 90.0,
    "token_usage_count": 5694,  // Sum of all workflows
    "latency_ms": 3046.90,      // Total time
    "tool_invocation_count": 10,
    // ... all other metrics aggregated
  }
}
```

### 3. Chat Messages (`POST /chat/sessions/{id}/message`)

**Response Structure:**
```json
{
  "session_id": "session_123",
  "workflow_id": "chat_workflow",
  "messages": [
    {
      "role": "user",
      "content": "Hello"
    },
    {
      "role": "assistant",
      "content": "Hi! How can I help?",
      "metadata": {
        "metrics": {
          "latency_ms": 456.78,
          "token_usage_count": 234,
          "accuracy": 95.0,
          // ... all metrics for this message
        }
      }
    }
  ],
  "metadata": {
    "last_message_metrics": {
      // Same metrics as above for quick access
    }
  }
}
```

---

## 📊 Metric Calculation Details

### Accuracy Calculation
```python
# Based on:
1. Tool success rate (0-100%)
2. Agent success rate (0-100%)
3. Error penalty (-10% per error)

accuracy = average(tool_success_rate, agent_success_rate)
accuracy = max(0, accuracy - (error_count * 10))
```

### Response Quality Calculation
```python
# Starting at 70%, bonuses for:
1. Task completed: +20%
2. No errors: +10%
3. High token output: +5%

# Penalties:
1. Each error: -5%

response_quality = min(100, max(0, calculated_value))
```

### Hallucination Rate Calculation
```python
# Starting at 0%, increases from:
1. Errors: +5% per error
2. Tool failures: +(failed/total * 20)%
3. Low context quality: +(70-quality) * 0.3%

hallucination_rate = min(100, calculated_value)
```

### Task Completion Rate
```python
# Binary with partial credit:
- Full success: 100%
- Success with errors: max(50%, 100% - errors*10%)
- Failed: 0%
```

---

## 🧪 Testing Metrics

### Run the Test Suite

```bash
# Make sure backend is running on localhost:8000
python test_metrics_display.py
```

### Expected Output

```
🧪 COMPREHENSIVE METRICS TESTING
================================

TEST 1: Workflow Execution Metrics
✅ Metrics found! Displaying all metrics:

┌─────────────────────────────────┬──────────────────┐
│ Metric Name                     │ Value            │
├─────────────────────────────────┼──────────────────┤
│ accuracy                        │            92.50 │
│ response_quality                │            88.00 │
│ hallucination_rate              │             3.50 │
│ task_completion_rate            │           100.00 │
│ token_usage_count               │             2847 │
│ latency_ms                      │          1523.45 │
│ tool_invocation_count           │                5 │
│ retrieval_error_count           │                1 │
│ decision_depth                  │                3 │
│ branching_factor                │             1.00 │
│ context_relation_quality        │            85.50 │
│ tool_success_rate               │            80.00 │
└─────────────────────────────────┴──────────────────┘

✅ All required metrics are present!
```

---

## 📝 Frontend Integration

### Displaying Metrics in React

```javascript
// After executing workflow/solution/chat
const result = await workflowsAPI.run(workflowId, {query: "test"});

// Access metrics
const metrics = result.data.metrics;

// Display in UI
<div className="metrics-panel">
  <h3>Execution Metrics</h3>
  
  <div className="metric-group">
    <h4>Performance</h4>
    <MetricCard label="Latency" value={`${metrics.latency_ms}ms`} />
    <MetricCard label="Tokens Used" value={metrics.token_usage_count} />
  </div>
  
  <div className="metric-group">
    <h4>Quality</h4>
    <ProgressBar label="Accuracy" value={metrics.accuracy} />
    <ProgressBar label="Response Quality" value={metrics.response_quality} />
    <ProgressBar label="Task Completion" value={metrics.task_completion_rate} />
    <ProgressBar label="Hallucination Rate" value={100 - metrics.hallucination_rate} inverse />
  </div>
  
  <div className="metric-group">
    <h4>Tool Usage</h4>
    <MetricCard label="Tools Invoked" value={metrics.tool_invocation_count} />
    <ProgressBar label="Tool Success" value={metrics.tool_success_rate} />
    <MetricCard label="Errors" value={metrics.retrieval_error_count} error />
  </div>
</div>
```

### Example Component

```javascript
function MetricsDisplay({ metrics }) {
  return (
    <div className="grid grid-cols-3 gap-4">
      {/* Performance Metrics */}
      <MetricCard 
        icon="⚡"
        title="Latency"
        value={`${metrics.latency_ms.toFixed(0)}ms`}
        color="blue"
      />
      <MetricCard 
        icon="🎯"
        title="Accuracy"
        value={`${metrics.accuracy.toFixed(1)}%`}
        color="green"
      />
      <MetricCard 
        icon="✨"
        title="Quality"
        value={`${metrics.response_quality.toFixed(1)}%`}
        color="purple"
      />
      
      {/* Token Usage */}
      <MetricCard 
        icon="💬"
        title="Tokens"
        value={metrics.token_usage_count}
        subtitle={`In: ${metrics.token_input_count} | Out: ${metrics.token_output_count}`}
        color="yellow"
      />
      
      {/* Tool Metrics */}
      <MetricCard 
        icon="🔧"
        title="Tools Used"
        value={metrics.tool_invocation_count}
        subtitle={`${metrics.tool_success_rate.toFixed(0)}% success`}
        color="teal"
      />
      
      {/* Reliability */}
      <MetricCard 
        icon="🎪"
        title="Hallucination"
        value={`${metrics.hallucination_rate.toFixed(1)}%`}
        color={metrics.hallucination_rate < 10 ? "green" : "red"}
      />
    </div>
  );
}
```

---

## 🚀 API Examples

### cURL - Workflow with Metrics

```bash
curl -X POST "http://localhost:8000/workflows/my_workflow/run" \
  -H "Content-Type: application/json" \
  -d '{"query": "Analyze market trends"}' | jq '.metrics'
```

### Python - Solution with Metrics

```python
import requests

response = requests.post(
    "http://localhost:8000/solutions/my_solution/execute",
    params={"query": "Run complete analysis"}
)

metrics = response.json()["metrics"]
print(f"Accuracy: {metrics['accuracy']}%")
print(f"Latency: {metrics['latency_ms']}ms")
print(f"Tokens: {metrics['token_usage_count']}")
```

### JavaScript - Chat with Metrics

```javascript
const response = await fetch(
  `http://localhost:8000/chat/sessions/${sessionId}/message`,
  {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({message: "Hello"})
  }
);

const session = await response.json();
const metrics = session.metadata.last_message_metrics;

console.log('Chat Metrics:', {
  latency: metrics.latency_ms,
  accuracy: metrics.accuracy,
  tokens: metrics.token_usage_count
});
```

---

## 🎯 Best Practices

### 1. **Monitor Key Metrics**
- Track `accuracy` and `response_quality` for AI performance
- Monitor `latency_ms` for user experience
- Watch `token_usage_count` for cost management

### 2. **Set Thresholds**
```python
# Example alert thresholds
if metrics['hallucination_rate'] > 15:
    alert("High hallucination rate detected!")

if metrics['tool_success_rate'] < 70:
    alert("Low tool success rate - check API connections")

if metrics['latency_ms'] > 5000:
    alert("Slow response time - optimize workflow")
```

### 3. **Analyze Trends**
- Store metrics in database for historical analysis
- Create dashboards showing metric trends over time
- Identify patterns in failed executions

### 4. **Optimize Based on Metrics**
- High latency? → Reduce workflow complexity or parallelize
- Low tool success? → Check API endpoints and credentials
- High token usage? → Optimize prompts and reduce context

---

## 📌 Summary

**All 12 metrics are now automatically tracked and displayed for:**
✅ Workflow executions  
✅ Solution executions (aggregated)  
✅ Chat messages  

**No additional configuration needed** - metrics are calculated automatically during execution and included in all API responses.

Run `python test_metrics_display.py` to verify all metrics are working correctly!
