import React, { useState, useEffect, useRef } from 'react';
import { chatAPI, solutionsAPI, workflowsAPI } from '../services/api';
import { 
  FaPaperPlane, FaProjectDiagram, FaExchangeAlt, FaSync,
  FaCog, FaNetworkWired, FaCheckCircle, FaCircle
} from 'react-icons/fa';

function SolutionChat({ solutionId, onClose }) {
  const [session, setSession] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [solution, setSolution] = useState(null);
  const [solutionContext, setSolutionContext] = useState(null);
  const [showWorkflowSelector, setShowWorkflowSelector] = useState(false);
  const [blueprint, setBlueprint] = useState(null);
  const [showBlueprint, setShowBlueprint] = useState(true);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    initializeSession();
  }, [solutionId]);

  useEffect(() => {
    if (session) {
      loadSolutionContext();
      loadBlueprint();
    }
  }, [session]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const initializeSession = async () => {
    try {
      setLoading(true);
      
      // Load solution
      const solutionResponse = await solutionsAPI.getById(solutionId);
      setSolution(solutionResponse.data);

      // Create chat session
      const response = await chatAPI.createSession({
        solution_id: solutionId,
        workflow_id: solutionResponse.data.workflows[0] || null,
        metadata: {
          solution_name: solutionResponse.data.name
        }
      });

      setSession(response.data);
      setMessages(response.data.messages || []);
    } catch (err) {
      console.error('Error initializing session:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadSolutionContext = async () => {
    if (!session) return;
    
    try {
      const response = await chatAPI.getSolutionContext(session.session_id);
      setSolutionContext(response.data);
    } catch (err) {
      console.error('Error loading solution context:', err);
    }
  };

  const loadBlueprint = async () => {
    if (!session) return;
    
    try {
      const response = await chatAPI.getBlueprint(session.session_id);
      setBlueprint(response.data);
    } catch (err) {
      console.error('Error loading blueprint:', err);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim() || !session) return;

    const userMessage = input.trim();
    setInput('');
    setLoading(true);

    try {
      const response = await chatAPI.sendMessage(session.session_id, userMessage);
      setSession(response.data);
      setMessages(response.data.messages || []);
      
      // Reload blueprint after message
      await loadBlueprint();
    } catch (err) {
      console.error('Error sending message:', err);
      // Add error message to chat
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your message.',
        timestamp: new Date().toISOString()
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleSwitchWorkflow = async (newWorkflowId) => {
    if (!session) return;

    try {
      setLoading(true);
      const response = await chatAPI.switchWorkflow(session.session_id, {
        new_workflow_id: newWorkflowId,
        transfer_memory: true,
        reason: 'User switched workflows'
      });
      
      setSession(response.data);
      setMessages(response.data.messages || []);
      setShowWorkflowSelector(false);
      
      // Reload context and blueprint
      await loadSolutionContext();
      await loadBlueprint();
    } catch (err) {
      console.error('Error switching workflow:', err);
    } finally {
      setLoading(false);
    }
  };

  const getCurrentWorkflowName = () => {
    if (!solutionContext || !session) return 'Loading...';
    const current = solutionContext.available_workflows?.find(
      w => w.id === session.workflow_id
    );
    return current?.name || session.workflow_id;
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-2xl w-full max-w-7xl h-[90vh] flex flex-col">
        {/* Header */}
        <div className="p-4 border-b border-gray-200 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-t-lg">
          <div className="flex justify-between items-center">
            <div>
              <h2 className="text-2xl font-bold flex items-center gap-2">
                <FaProjectDiagram />
                {solution?.name || 'Solution Chat'}
              </h2>
              <p className="text-sm text-blue-100 mt-1">
                Current Workflow: {getCurrentWorkflowName()}
              </p>
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => setShowBlueprint(!showBlueprint)}
                className="px-3 py-2 bg-white bg-opacity-20 hover:bg-opacity-30 rounded-lg flex items-center gap-2"
                title="Toggle Blueprint"
              >
                <FaNetworkWired /> {showBlueprint ? 'Hide' : 'Show'} Blueprint
              </button>
              <button
                onClick={onClose}
                className="px-3 py-2 bg-white bg-opacity-20 hover:bg-opacity-30 rounded-lg"
              >
                Close
              </button>
            </div>
          </div>
        </div>

        <div className="flex-1 flex overflow-hidden">
          {/* Chat Area */}
          <div className={`flex-1 flex flex-col ${showBlueprint ? 'w-1/2' : 'w-full'}`}>
            {/* Workflow Switcher */}
            {solutionContext?.has_solution && (
              <div className="p-3 bg-gray-50 border-b border-gray-200">
                <div className="flex items-center justify-between">
                  <div className="text-sm text-gray-700">
                    <span className="font-semibold">Available Workflows:</span> {solutionContext.available_workflows?.length || 0}
                  </div>
                  <button
                    onClick={() => setShowWorkflowSelector(!showWorkflowSelector)}
                    className="px-3 py-1 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center gap-2 text-sm"
                  >
                    <FaExchangeAlt /> Switch Workflow
                  </button>
                </div>

                {/* Workflow Selector Dropdown */}
                {showWorkflowSelector && (
                  <div className="mt-3 grid grid-cols-2 gap-2">
                    {solutionContext.available_workflows?.map(workflow => (
                      <button
                        key={workflow.id}
                        onClick={() => handleSwitchWorkflow(workflow.id)}
                        disabled={workflow.is_current}
                        className={`p-3 rounded-lg border-2 text-left transition-all ${
                          workflow.is_current
                            ? 'border-blue-600 bg-blue-50 cursor-default'
                            : 'border-gray-300 hover:border-blue-400 hover:bg-blue-50'
                        }`}
                      >
                        <div className="flex items-center justify-between">
                          <div className="flex-1">
                            <div className="font-semibold text-sm">{workflow.name}</div>
                            <div className="text-xs text-gray-500">{workflow.description}</div>
                          </div>
                          {workflow.is_current && (
                            <FaCheckCircle className="text-blue-600" />
                          )}
                        </div>
                      </button>
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {messages.length === 0 ? (
                <div className="text-center text-gray-500 mt-8">
                  <FaProjectDiagram className="mx-auto mb-3" size={48} />
                  <p>Start a conversation with your solution</p>
                  <p className="text-sm mt-1">Messages will maintain context when switching workflows</p>
                </div>
              ) : (
                messages.map((msg, idx) => (
                  <div
                    key={idx}
                    className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-[70%] rounded-lg p-3 ${
                        msg.role === 'user'
                          ? 'bg-blue-600 text-white'
                          : msg.metadata?.system_event
                          ? 'bg-yellow-100 text-yellow-800 border border-yellow-300'
                          : 'bg-gray-200 text-gray-800'
                      }`}
                    >
                      {msg.metadata?.system_event === 'workflow_switch' && (
                        <div className="flex items-center gap-2 mb-1">
                          <FaExchangeAlt />
                          <span className="text-xs font-semibold">Workflow Switched</span>
                        </div>
                      )}
                      <p className="whitespace-pre-wrap">{msg.content}</p>
                      <p className="text-xs opacity-70 mt-1">
                        {new Date(msg.timestamp).toLocaleTimeString()}
                      </p>
                    </div>
                  </div>
                ))
              )}
              <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div className="p-4 border-t border-gray-200">
              <form onSubmit={handleSendMessage} className="flex gap-2">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Type your message..."
                  disabled={loading}
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                />
                <button
                  type="submit"
                  disabled={loading || !input.trim()}
                  className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 flex items-center gap-2"
                >
                  {loading ? <FaSync className="animate-spin" /> : <FaPaperPlane />}
                  Send
                </button>
              </form>
            </div>
          </div>

          {/* Blueprint Area */}
          {showBlueprint && (
            <div className="w-1/2 border-l border-gray-200 bg-gray-50 overflow-y-auto">
              <div className="p-4">
                <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                  <FaNetworkWired /> Workflow Blueprint
                </h3>

                {blueprint ? (
                  <div className="space-y-6">
                    {/* Current Workflow Info */}
                    <div className="bg-white rounded-lg p-4 shadow">
                      <h4 className="font-semibold mb-2">Current Workflow</h4>
                      <div className="text-sm space-y-1">
                        <p><span className="font-medium">Name:</span> {blueprint.workflow?.name}</p>
                        <p><span className="font-medium">Type:</span> {blueprint.workflow?.type}</p>
                        <p><span className="font-medium">Nodes:</span> {blueprint.workflow?.nodes?.length || 0}</p>
                      </div>
                    </div>

                    {/* Workflow Nodes */}
                    {blueprint.workflow?.nodes && blueprint.workflow.nodes.length > 0 && (
                      <div className="bg-white rounded-lg p-4 shadow">
                        <h4 className="font-semibold mb-3">Workflow Structure</h4>
                        <div className="space-y-2">
                          {blueprint.workflow.nodes.map((node, idx) => (
                            <div key={node.id} className="border-l-4 border-blue-500 pl-3 py-2">
                              <div className="font-medium text-sm">{node.id}</div>
                              {node.agent_ref && (
                                <div className="text-xs text-gray-600">Agent: {node.agent_ref}</div>
                              )}
                              {node.task && (
                                <div className="text-xs text-gray-600 mt-1">{node.task}</div>
                              )}
                              {node.sends_to && node.sends_to.length > 0 && (
                                <div className="text-xs text-gray-500 mt-1">
                                  → Sends to: {node.sends_to.join(', ')}
                                </div>
                              )}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Session State */}
                    {blueprint.session_state && (
                      <div className="bg-white rounded-lg p-4 shadow">
                        <h4 className="font-semibold mb-2">Session State</h4>
                        <div className="text-sm space-y-1">
                          <p><span className="font-medium">Messages:</span> {blueprint.session_state.message_count}</p>
                          {blueprint.session_state.agents_used && blueprint.session_state.agents_used.length > 0 && (
                            <p><span className="font-medium">Agents Used:</span> {blueprint.session_state.agents_used.join(', ')}</p>
                          )}
                          {blueprint.session_state.current_step && (
                            <p><span className="font-medium">Current Step:</span> {blueprint.session_state.current_step}</p>
                          )}
                        </div>
                      </div>
                    )}

                    {/* Solution Context */}
                    {blueprint.solution_context && (
                      <div className="bg-white rounded-lg p-4 shadow">
                        <h4 className="font-semibold mb-3">Solution Communications</h4>
                        <div className="text-sm space-y-2">
                          <p><span className="font-medium">Total Messages:</span> {blueprint.solution_context.total_messages || 0}</p>
                          <p><span className="font-medium">Active Workflows:</span> {blueprint.solution_context.active_workflows?.length || 0}</p>
                          
                          {blueprint.solution_context.workflows && blueprint.solution_context.workflows.length > 0 && (
                            <div className="mt-3">
                              <p className="font-medium mb-2">Workflow Stats:</p>
                              {blueprint.solution_context.workflows.map(wf => (
                                <div key={wf.id} className="text-xs bg-gray-50 p-2 rounded mb-1">
                                  <span className="font-medium">{wf.id}:</span> {wf.sent_messages} sent, {wf.received_messages} received
                                </div>
                              ))}
                            </div>
                          )}
                        </div>
                      </div>
                    )}
                  </div>
                ) : (
                  <div className="text-center text-gray-500 py-8">
                    <FaNetworkWired className="mx-auto mb-3" size={48} />
                    <p>Loading blueprint...</p>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default SolutionChat;
