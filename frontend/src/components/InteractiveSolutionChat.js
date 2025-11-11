import React, { useState, useEffect, useRef } from 'react';
import { FaPaperPlane, FaPlay, FaCheckCircle, FaSpinner, FaBrain, FaNetworkWired, FaPlus, FaArrowRight, FaTimes } from 'react-icons/fa';
import { chatAPI, solutionsAPI, workflowsAPI } from '../services/api';
import ComprehensiveMetricsDisplay from './ComprehensiveMetricsDisplay';

function InteractiveSolutionChat({ solutionId, onClose }) {
  const [solution, setSolution] = useState(null);
  const [availableWorkflows, setAvailableWorkflows] = useState([]);
  const [activeWorkflows, setActiveWorkflows] = useState([]);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [ws, setWs] = useState(null);
  const [executing, setExecuting] = useState(false);
  const [currentWorkflowIndex, setCurrentWorkflowIndex] = useState(-1);
  const [workflowResults, setWorkflowResults] = useState({});
  const messagesEndRef = useRef(null);

  useEffect(() => {
    initializeSolution();
    initializeWebSocket();
    
    return () => {
      if (ws) ws.close();
    };
  }, [solutionId]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const initializeSolution = async () => {
    try {
      const solutionRes = await solutionsAPI.getById(solutionId);
      setSolution(solutionRes.data);
      
      // Load all available workflows
      const workflowsRes = await workflowsAPI.getAll();
      setAvailableWorkflows(workflowsRes.data);
      
      // Initialize with solution's workflows
      setActiveWorkflows(solutionRes.data.workflows || []);
      
      // Welcome message
      addMessage('system', `Welcome! This solution can execute ${solutionRes.data.workflows?.length || 0} workflows with AI-powered context transfer.`);
      addMessage('system', 'Type your query (e.g., "AAPL stock analysis") and I\'ll execute the workflows automatically!');
    } catch (err) {
      console.error('Error loading solution:', err);
      addMessage('error', 'Failed to load solution');
    }
  };

  const initializeWebSocket = () => {
    const websocket = new WebSocket(`ws://localhost:8000/solutions/ws/${solutionId}`);
    
    websocket.onopen = () => {
      console.log('✅ WebSocket connected');
      setWs(websocket);
    };
    
    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      handleWebSocketMessage(data);
    };
    
    websocket.onerror = (error) => {
      console.error('WebSocket error:', error);
      addMessage('error', 'WebSocket connection failed');
    };
    
    websocket.onclose = () => {
      console.log('WebSocket disconnected');
      setWs(null);
    };
  };

  const handleWebSocketMessage = (msg) => {
    console.log('📥 WebSocket message:', msg);
    
    switch (msg.type) {
      case 'execution_started':
        setExecuting(true);
        setCurrentWorkflowIndex(0);
        const strategyEmoji = msg.solution_type === 'research' ? '🔬' : '💡';
        const strategyName = msg.communication_strategy || (msg.solution_type === 'research' ? 'Agentic RAG' : 'KAG+Buffer');
        addMessage('system', `🚀 Starting execution of ${msg.total_workflows} workflows using ${strategyEmoji} ${strategyName}...`);
        break;
        
      case 'workflow_started':
        setCurrentWorkflowIndex(msg.position - 1);
        addMessage('workflow_started', `⚡ Executing: ${msg.workflow_name}`, { workflowId: msg.workflow_id });
        break;
      
      case 'agent_memory_initialized':
        addMessage('system', `🧠 Agent memory initialized for ${msg.agent_node} with RAG context`, { 
          memory: msg.memory,
          workflowId: msg.workflow_id
        });
        break;
        
      case 'workflow_completed':
        setWorkflowResults(prev => ({
          ...prev,
          [msg.workflow_id]: {
            kag: msg.storage_result,
            output: msg.output,
            metrics: msg.metrics,
            agent_memory: msg.agent_memory
          }
        }));
        
        addMessage('workflow_completed', `✅ ${msg.workflow_name} completed!`, {
          workflowId: msg.workflow_id,
          kag: msg.kag_analysis,
          output: msg.output,
          metrics: msg.metrics
        });
        break;
        
      case 'handoff_prepared':
        addMessage('handoff', `🤝 Transferring context: ${msg.from_workflow} → ${msg.to_workflow}`, {
          handoffData: msg.handoff_data
        });
        break;
        
      case 'execution_completed':
        setExecuting(false);
        setCurrentWorkflowIndex(-1);
        
        // Display comprehensive summary with metrics
        addMessage('execution_summary', '🎉 All workflows completed!', {
          summary: msg.summary,
          workflowOutputs: msg.all_workflow_outputs,
          overallMetrics: msg.overall_metrics
        });
        break;
        
      case 'error':
        setExecuting(false);
        addMessage('error', `❌ Error: ${msg.message}`);
        break;
    }
  };

  const addMessage = (type, content, metadata = {}) => {
    setMessages(prev => [...prev, {
      type,
      content,
      metadata,
      timestamp: new Date().toISOString()
    }]);
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim() || !ws) return;

    const userQuery = input.trim();
    setInput('');
    
    // Add user message
    addMessage('user', userQuery);
    
    // Execute solution with user query
    if (ws.readyState === 1) {
      addMessage('system', 'Processing your query through the workflow chain...');
      ws.send(JSON.stringify({ action: 'execute', query: userQuery }));
    } else {
      addMessage('error', 'WebSocket not connected. Please refresh.');
    }
  };

  const addWorkflowToChain = (workflowId) => {
    if (!activeWorkflows.includes(workflowId)) {
      setActiveWorkflows(prev => [...prev, workflowId]);
      const workflow = availableWorkflows.find(w => w.id === workflowId);
      addMessage('system', `➕ Added workflow: ${workflow?.name || workflowId}`);
    }
  };

  const removeWorkflowFromChain = (workflowId) => {
    setActiveWorkflows(prev => prev.filter(id => id !== workflowId));
    const workflow = availableWorkflows.find(w => w.id === workflowId);
    addMessage('system', `➖ Removed workflow: ${workflow?.name || workflowId}`);
  };

  const getWorkflowName = (workflowId) => {
    const workflow = availableWorkflows.find(w => w.id === workflowId);
    return workflow?.name || workflowId;
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-90 flex items-center justify-center z-50">
      <div className="bg-gray-950 rounded-lg shadow-2xl w-full max-w-7xl h-[95vh] flex flex-col border border-purple-500/30">
        
        {/* Header */}
        <div className="p-4 border-b border-gray-800 bg-gradient-to-r from-purple-900/40 to-blue-900/40">
          <div className="flex justify-between items-center">
            <div>
              <div className="flex items-center gap-3">
                <h2 className="text-2xl font-bold text-white flex items-center gap-2">
                  <FaBrain className="text-purple-400" />
                  {solution?.name || 'Solution'}
                </h2>
                <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                  solution?.solution_type === 'research' 
                    ? 'bg-purple-500/20 text-purple-400 border border-purple-500/50' 
                    : 'bg-green-500/20 text-green-400 border border-green-500/50'
                }`}>
                  {solution?.solution_type === 'research' ? '🔬 Research Mode (Agentic RAG)' : '💡 Normal Mode (KAG+Buffer)'}
                </span>
              </div>
              <p className="text-sm text-gray-400 mt-1">
                AI-Powered Workflow Orchestration • {activeWorkflows.length} Active Workflows
              </p>
            </div>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-white text-2xl transition-colors"
            >
              <FaTimes />
            </button>
          </div>
        </div>

        <div className="flex-1 flex overflow-hidden">
          
          {/* Left Side - Chat Interface */}
          <div className="w-1/2 flex flex-col border-r border-gray-800">
            
            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-gray-950">
              {messages.map((msg, idx) => (
                <div key={idx} className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                  
                  {msg.type === 'user' && (
                    <div className="max-w-[80%] bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-lg p-4 shadow-lg">
                      <p>{msg.content}</p>
                      <span className="text-xs text-blue-200 mt-1 block">
                        {new Date(msg.timestamp).toLocaleTimeString()}
                      </span>
                    </div>
                  )}
                  
                  {msg.type === 'system' && (
                    <div className="max-w-[80%] bg-gray-800 border border-gray-700 text-gray-300 rounded-lg p-4">
                      <p className="text-sm">{msg.content}</p>
                    </div>
                  )}
                  
                  {msg.type === 'workflow_started' && (
                    <div className="max-w-[80%] bg-gradient-to-r from-purple-900/50 to-blue-900/50 border border-purple-500/50 text-white rounded-lg p-4 shadow-lg animate-pulse">
                      <p className="font-semibold">{msg.content}</p>
                    </div>
                  )}
                  
                  {msg.type === 'workflow_completed' && (
                    <div className="max-w-[80%] bg-gradient-to-r from-green-900/30 to-green-800/20 border border-green-500/50 text-white rounded-lg p-4">
                      <p className="font-semibold mb-2">{msg.content}</p>
                      
                      {/* AI Summary */}
                      {msg.metadata?.kag && (
                        <div className="mt-3 space-y-2">
                          <div className="bg-black/40 rounded p-3">
                            <p className="text-xs text-gray-400 mb-1">🤖 AI Summary:</p>
                            <p className="text-sm text-green-200">{msg.metadata.kag.summary}</p>
                          </div>
                          {msg.metadata.kag.facts && msg.metadata.kag.facts.length > 0 && (
                            <div className="bg-black/40 rounded p-3">
                              <p className="text-xs text-gray-400 mb-2">📊 Facts Extracted ({msg.metadata.kag.facts.length}):</p>
                              <ul className="space-y-1 max-h-40 overflow-y-auto">
                                {msg.metadata.kag.facts.map((fact, i) => (
                                  <li key={i} className="text-xs text-green-300 flex items-start gap-2">
                                    <span className="text-green-500">•</span>
                                    <span>{fact}</span>
                                  </li>
                                ))}
                              </ul>
                            </div>
                          )}
                        </div>
                      )}
                      
                      {/* Full Workflow Output */}
                      {msg.metadata?.output && (
                        <div className="mt-3 bg-black/40 rounded p-3">
                          <p className="text-xs text-gray-400 mb-2">📄 Full Output:</p>
                          <div className="text-xs text-gray-300 max-h-60 overflow-y-auto whitespace-pre-wrap font-mono">
                            {typeof msg.metadata.output === 'string' ? msg.metadata.output : JSON.stringify(msg.metadata.output, null, 2)}
                          </div>
                        </div>
                      )}
                      
                      {/* Metrics */}
                      {msg.metadata?.metrics && Object.keys(msg.metadata.metrics).length > 0 && (
                        <div className="mt-3 bg-black/40 rounded p-3">
                          <p className="text-xs text-gray-400 mb-2">📈 Comprehensive Metrics:</p>
                          <ComprehensiveMetricsDisplay metrics={msg.metadata.metrics} compact={true} />
                        </div>
                      )}
                    </div>
                  )}
                  
                  {msg.type === 'handoff' && (
                    <div className="max-w-[80%] bg-gradient-to-r from-yellow-900/30 to-orange-900/30 border border-yellow-500/50 text-white rounded-lg p-4">
                      <p className="font-semibold">{msg.content}</p>
                      {msg.metadata?.handoffData?.handoff_data && (
                        <div className="mt-2 bg-black/40 rounded p-2 text-xs text-yellow-200">
                          {String(msg.metadata.handoffData.handoff_data).substring(0, 150)}...
                        </div>
                      )}
                    </div>
                  )}
                  
                  {msg.type === 'error' && (
                    <div className="max-w-[80%] bg-red-900/20 border border-red-500 text-red-300 rounded-lg p-4">
                      <p>{msg.content}</p>
                    </div>
                  )}
                  
                  {msg.type === 'execution_summary' && (
                    <div className="max-w-[95%] bg-gradient-to-r from-purple-900/40 to-blue-900/40 border-2 border-purple-500 text-white rounded-lg p-6">
                      <p className="font-bold text-2xl mb-4">{msg.content}</p>
                      
                      {/* Overall Metrics */}
                      {msg.metadata?.overallMetrics && (
                        <div className="mb-6 bg-black/40 rounded-lg p-4">
                          <p className="text-lg font-semibold mb-3 text-purple-300">📊 Overall Solution Metrics</p>
                          <ComprehensiveMetricsDisplay metrics={msg.metadata.overallMetrics} />
                        </div>
                      )}
                      
                      {/* Combined AI Summary */}
                      {msg.metadata?.summary && (
                        <div className="mb-6 bg-black/40 rounded-lg p-4">
                          <p className="text-lg font-semibold mb-3 text-green-300">🤖 Combined AI Summary</p>
                          <p className="text-gray-200 mb-3">{msg.metadata.summary.final_summary}</p>
                          
                          {msg.metadata.summary.combined_facts && msg.metadata.summary.combined_facts.length > 0 && (
                            <div className="mt-4">
                              <p className="text-sm font-semibold text-green-300 mb-2">
                                📌 All Facts Collected ({msg.metadata.summary.combined_facts.length}):
                              </p>
                              <ul className="space-y-1 max-h-60 overflow-y-auto">
                                {msg.metadata.summary.combined_facts.map((fact, i) => (
                                  <li key={i} className="text-sm text-green-200 flex items-start gap-2">
                                    <span className="text-green-400">•</span>
                                    <span>{fact}</span>
                                  </li>
                                ))}
                              </ul>
                            </div>
                          )}
                        </div>
                      )}
                      
                      {/* All Workflow Outputs */}
                      {msg.metadata?.workflowOutputs && msg.metadata.workflowOutputs.length > 0 && (
                        <div className="bg-black/40 rounded-lg p-4">
                          <p className="text-lg font-semibold mb-3 text-blue-300">📄 Complete Workflow Outputs</p>
                          <div className="space-y-4 max-h-96 overflow-y-auto">
                            {msg.metadata.workflowOutputs.map((wf, i) => (
                              <div key={i} className="bg-gray-900/50 rounded p-4 border border-gray-700">
                                <div className="flex items-center gap-2 mb-2">
                                  <div className="w-6 h-6 rounded-full bg-blue-500 text-white text-xs flex items-center justify-center font-bold">
                                    {i + 1}
                                  </div>
                                  <p className="font-semibold text-blue-200">{wf.workflow_name}</p>
                                </div>
                                
                                {/* Workflow AI Analysis */}
                                {wf.kag_analysis && (
                                  <div className="mb-3 bg-black/40 rounded p-2">
                                    <p className="text-xs text-gray-400 mb-1">AI Analysis:</p>
                                    <p className="text-sm text-gray-300">{wf.kag_analysis.summary}</p>
                                    {wf.kag_analysis.facts && wf.kag_analysis.facts.length > 0 && (
                                      <p className="text-xs text-green-300 mt-1">
                                        {wf.kag_analysis.facts.length} facts extracted
                                      </p>
                                    )}
                                  </div>
                                )}
                                
                                {/* Workflow Output */}
                                <div className="bg-black/60 rounded p-3">
                                  <p className="text-xs text-gray-400 mb-2">Output:</p>
                                  <div className="text-xs text-gray-300 max-h-40 overflow-y-auto whitespace-pre-wrap font-mono">
                                    {typeof wf.output === 'string' ? wf.output : JSON.stringify(wf.output, null, 2)}
                                  </div>
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                  
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div className="p-4 border-t border-gray-800 bg-gray-900">
              <form onSubmit={handleSendMessage} className="flex gap-2">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Type your query (e.g., 'Analyze AAPL stock')..."
                  disabled={executing || !ws}
                  className="flex-1 px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                />
                <button
                  type="submit"
                  disabled={executing || !input.trim() || !ws}
                  className="px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg font-semibold hover:from-purple-700 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                >
                  {executing ? <FaSpinner className="animate-spin" /> : <FaPaperPlane />}
                  {executing ? 'Processing...' : 'Send'}
                </button>
              </form>
            </div>
          </div>

          {/* Right Side - Workflow Visualization */}
          <div className="w-1/2 flex flex-col bg-gray-900">
            
            {/* Active Workflow Chain */}
            <div className="flex-1 overflow-y-auto p-6">
              <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
                <FaNetworkWired className="text-purple-400" />
                Active Workflow Chain
              </h3>
              
              <div className="space-y-4">
                {activeWorkflows.map((workflowId, index) => {
                  const isActive = index === currentWorkflowIndex;
                  const isCompleted = workflowResults[workflowId];
                  const isPending = index > currentWorkflowIndex || !executing;
                  
                  return (
                    <div key={workflowId}>
                      {/* Workflow Card */}
                      <div className={`p-4 rounded-lg border-2 transition-all ${
                        isActive ? 'border-blue-500 bg-gradient-to-r from-blue-900/50 to-purple-900/50 shadow-lg shadow-blue-500/30 scale-105' :
                        isCompleted ? 'border-green-500 bg-gradient-to-r from-green-900/20 to-green-800/10' :
                        'border-gray-700 bg-gray-800'
                      }`}>
                        <div className="flex items-center justify-between mb-2">
                          <div className="flex items-center gap-3">
                            <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold ${
                              isActive ? 'bg-blue-500 text-white animate-pulse' :
                              isCompleted ? 'bg-green-500 text-white' :
                              'bg-gray-700 text-gray-400'
                            }`}>
                              {index + 1}
                            </div>
                            <div>
                              <div className="font-semibold text-white">{getWorkflowName(workflowId)}</div>
                              <div className="text-xs text-gray-400">
                                {isActive && '⚡ Executing...'}
                                {isCompleted && '✅ Completed'}
                                {isPending && '⏳ Pending'}
                              </div>
                            </div>
                          </div>
                          <button
                            onClick={() => removeWorkflowFromChain(workflowId)}
                            disabled={executing}
                            className="text-gray-500 hover:text-red-400 transition-colors disabled:opacity-50"
                          >
                            <FaTimes />
                          </button>
                        </div>
                        
                        {isCompleted && workflowResults[workflowId]?.kag && (
                          <div className="mt-3 space-y-2">
                            <div className="bg-black/40 rounded p-3 text-xs">
                              <p className="text-green-400 font-semibold mb-1">🤖 AI Analysis:</p>
                              <p className="text-gray-300">{workflowResults[workflowId].kag.summary?.substring(0, 100)}...</p>
                              {workflowResults[workflowId].kag.facts && (
                                <p className="text-green-300 mt-2">
                                  📌 {workflowResults[workflowId].kag.facts.length} facts extracted
                                </p>
                              )}
                            </div>
                            
                            {/* Metrics in right panel */}
                            {workflowResults[workflowId]?.metrics && Object.keys(workflowResults[workflowId].metrics).length > 0 && (
                              <div className="bg-black/40 rounded p-3 text-xs">
                                <p className="text-blue-400 font-semibold mb-2">📊 Full Metrics:</p>
                                <ComprehensiveMetricsDisplay metrics={workflowResults[workflowId].metrics} compact={true} />
                              </div>
                            )}
                          </div>
                        )}
                      </div>
                      
                      {/* Arrow between workflows */}
                      {index < activeWorkflows.length - 1 && (
                        <div className="flex justify-center my-2">
                          <FaArrowRight className="text-2xl text-purple-500" />
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Available Workflows to Add */}
            <div className="border-t border-gray-800 p-4 bg-gray-950">
              <h4 className="text-sm font-semibold text-gray-400 mb-3 flex items-center gap-2">
                <FaPlus className="text-purple-400" />
                Add More Workflows
              </h4>
              <div className="flex flex-wrap gap-2">
                {availableWorkflows
                  .filter(w => !activeWorkflows.includes(w.id))
                  .slice(0, 5)
                  .map(workflow => (
                    <button
                      key={workflow.id}
                      onClick={() => addWorkflowToChain(workflow.id)}
                      disabled={executing}
                      className="px-3 py-2 text-xs bg-gray-800 border border-gray-700 text-gray-300 rounded-lg hover:bg-purple-900/30 hover:border-purple-500/50 transition-all disabled:opacity-50"
                    >
                      + {workflow.name}
                    </button>
                  ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default InteractiveSolutionChat;
