# Testing the New Workflow Visualization Features

## Quick Start Guide

### Prerequisites
1. Backend server running on port 8000
2. Frontend running on port 3000
3. At least one workflow created with multiple agents

## Test Scenarios

### 1. Test Workflow Blueprint (Run Button)

**Steps:**
1. Navigate to **Workflows** page
2. Find any workflow card
3. Click the **▶ Play/Run** button (green on hover)
4. **Expected Result:**
   - Modal opens showing workflow blueprint
   - All agent nodes visible with gray "Pending" status
   - Connections shown between agents
   - Header shows "Workflow Blueprint" with workflow name

5. Watch the execution:
   - Nodes should pulse purple when processing
   - Status badges show spinner icon
   - Edges animate with purple color when data flows
   - Nodes turn green with checkmark when complete
   - Progress tracked in execution state

6. Check features:
   - Minimap in bottom-right shows full workflow
   - Controls allow zoom in/out
   - Legend at bottom explains colors
   - Can close with X button

**What to Look For:**
- ✅ Smooth animations
- ✅ Clear state transitions
- ✅ Proper timing of node activation
- ✅ Connection animations
- ✅ Status indicators updating

---

### 2. Test Workflow Chat Mode (Chat Button)

**Steps:**
1. Navigate to **Workflows** page
2. Find any workflow card
3. Click the **💬 Comments/Chat** button (blue on hover)
4. **Expected Result:**
   - Split-screen modal opens
   - Left side: Workflow visualization canvas
   - Right side: Chat interface
   - Header shows workflow name

5. Send a message:
   - Type in chat input: "Research artificial intelligence"
   - Click **Send**
   - Watch the workflow execute

6. **Expected Behavior:**
   - Left canvas shows agent nodes lighting up
   - Active agent pulses purple
   - Messages appear in right chat panel
   - Each agent response shows in chat
   - Tool usage indicators appear
   - Message flow visualized in real-time

**What to Look For:**
- ✅ Synchronized visualization and chat
- ✅ Agent responses appear as messages
- ✅ Tool results shown in chat
- ✅ Graph updates match chat messages
- ✅ Final result displayed

---

### 3. Test Chat Page Workflow Mode

**Steps:**
1. Navigate to **Chat** page
2. Create or select a chat session
3. Look for **Workflow Mode** dropdown in left sidebar
4. Select a workflow from dropdown (e.g., "AI Research Workflow")
5. **Expected Result:**
   - Dropdown shows selected workflow
   - Text below says "Messages will execute this workflow"
   - Input placeholder changes to "Send to [Workflow Name]..."
   - Button text changes to "Execute"

6. Send a message:
   - Type: "Analyze the future of AI"
   - Click **Execute**

7. **Expected Behavior:**
   - Right panel appears with workflow graph
   - Chat messages appear on left (60% width)
   - Workflow visualization on right (40% width)
   - Graph shows live agent communication
   - Message counters update per agent
   - "Show/Hide Workflow" toggle button appears in header

8. Test toggle:
   - Click "Hide Workflow" button
   - Graph disappears, chat expands to full width
   - Click "Show Workflow" 
   - Graph reappears

**What to Look For:**
- ✅ Split-screen layout works
- ✅ Both panels scroll independently
- ✅ Workflow graph updates in real-time
- ✅ Toggle button works
- ✅ Message history preserved

---

### 4. Test Normal Chat Mode (No Workflow)

**Steps:**
1. In **Chat** page
2. Select "No workflow (Normal chat)" from dropdown
3. **Expected Result:**
   - Workflow visualization hidden
   - Full-width chat interface
   - Input placeholder: "Type your message..."
   - Button text: "Send"

4. Send a normal chat message
5. **Expected Behavior:**
   - Regular AI response (no workflow)
   - No graph visualization
   - Standard chat interface

---

## Visual Checklist

### WorkflowBlueprint Component
- [ ] Modal opens on Run button click
- [ ] Nodes display with agent names
- [ ] Tools shown as blue chips under agents
- [ ] Pending nodes are gray
- [ ] Active nodes pulse purple
- [ ] Completed nodes are green
- [ ] Edges animate during execution
- [ ] Status badges (⏳, ⚡, ✅) display correctly
- [ ] Minimap shows in bottom-right
- [ ] Controls work (zoom, fit view)
- [ ] Legend displays correctly
- [ ] "Executing..." overlay appears during run
- [ ] Close button works

### WorkflowCommunicationGraph Component
- [ ] Graph renders in chat mode
- [ ] Nodes show agent names
- [ ] Message counters appear and update
- [ ] Tool usage chips display
- [ ] Active nodes have pulse animation
- [ ] Completed nodes are green
- [ ] Pending nodes are gray
- [ ] Connection lines animate
- [ ] "Workflow Executing..." overlay shows
- [ ] Legend displays at bottom
- [ ] Message statistics show in top-right
- [ ] Zoom controls work

### Workflow Cards (Updated)
- [ ] Four buttons visible: Run, Chat, Edit, Delete
- [ ] Tooltips show on hover
- [ ] Run button hover: green
- [ ] Chat button hover: blue
- [ ] Edit button hover: purple
- [ ] Delete button hover: red
- [ ] Icons clear and visible

### Chat Interface (Updated)
- [ ] Workflow Mode dropdown visible
- [ ] Dropdown lists all workflows
- [ ] "No workflow" option present
- [ ] Selected workflow name shows in header
- [ ] Split-screen appears when workflow selected
- [ ] Left panel (chat) scrolls independently
- [ ] Right panel (graph) updates live
- [ ] Toggle button appears when workflow active
- [ ] Execute button changes to Send without workflow

---

## Common Issues & Solutions

### Issue: Graph not rendering
**Solution:** 
- Check browser console for errors
- Ensure ReactFlow CSS is loaded
- Verify workflow has nodes

### Issue: No animations
**Solution:**
- Check if `isExecuting` state is updating
- Verify `executionState` object has node data
- Look for console errors

### Issue: Split-screen not appearing
**Solution:**
- Ensure workflow is selected
- Check if `showWorkflowViz` is true
- Verify `communicationLog` has data

### Issue: Messages not showing
**Solution:**
- Check API response format
- Verify `communication_log` in response
- Check browser network tab

---

## Testing Data

### Sample Workflow Structure
```yaml
id: ai_research
name: AI Research Workflow
type: sequence
nodes:
  - id: node_1
    agent_ref: researcher_agent
    task: Research the topic
    tools: [websearch]
  - id: node_2
    agent_ref: analyzer_agent
    task: Analyze findings
    dependencies: [node_1]
  - id: node_3
    agent_ref: writer_agent
    task: Write summary
    dependencies: [node_2]
```

### Sample Communication Log
```json
{
  "communication_log": [
    {
      "sender": "node_1",
      "agent": "researcher_agent",
      "content": "Found 5 research papers...",
      "type": "agent_result",
      "tools_used": ["websearch"]
    },
    {
      "sender": "node_2", 
      "agent": "analyzer_agent",
      "content": "Key findings: ...",
      "type": "agent_result"
    }
  ]
}
```

---

## Performance Metrics

Monitor these during testing:
- [ ] Page load time < 2s
- [ ] Animation frame rate 60fps
- [ ] No memory leaks during execution
- [ ] Smooth scrolling in both panels
- [ ] Graph renders < 1s with 10 nodes
- [ ] State updates within 100ms

---

## Browser Compatibility

Test on:
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)

---

## Accessibility

Check:
- [ ] Keyboard navigation works
- [ ] Screen reader compatibility
- [ ] Color contrast meets WCAG standards
- [ ] Focus indicators visible
- [ ] Alt text on icons

---

## Next Steps After Testing

1. **If everything works:**
   - Test with complex workflows (10+ nodes)
   - Test parallel workflow execution
   - Test error handling (failed nodes)

2. **If issues found:**
   - Document in console logs
   - Check network requests
   - Verify API response format
   - Review state management

3. **Performance optimization:**
   - Profile React components
   - Optimize re-renders
   - Check bundle size
   - Lazy load components

---

## Success Criteria

✅ **Feature is ready when:**
- All visual elements render correctly
- Animations are smooth and synchronized
- State updates happen in real-time
- No console errors
- Works in all major browsers
- Responsive on different screen sizes
- User can easily understand workflow flow
- Documentation is clear

---

## Feedback Collection

Document:
- User reactions to animations
- Clarity of visual states
- Performance on slower machines
- Any confusion points
- Feature requests
- Bug reports
