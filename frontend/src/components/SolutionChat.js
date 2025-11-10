import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import ReactFlow, { Background, Controls, MarkerType, Position, Handle, useNodesState, useEdgesState } from 'reactflow';
import 'reactflow/dist/style.css';
import { chatAPI, solutionsAPI, workflowsAPI } from '../services/api';
import { 
  FaPaperPlane, FaProjectDiagram, FaExchangeAlt, FaSync, FaTimes,
  FaCog, FaNetworkWired, FaCheckCircle, FaCircle, FaRobot, FaUser,
  FaSpinner, FaBrain, FaArrowRight, FaPlay, FaStop
} from 'react-icons/fa';

// VERSION MARKER - Check console for this!
const SOLUTION_CHAT_VERSION = '2.0.0-ENHANCED-OUTPUT';
console.log('🔥🔥🔥 SOLUTION CHAT VERSION:', SOLUTION_CHAT_VERSION, '🔥🔥🔥');
console.log('🔥 If you see version 2.0.0-ENHANCED-OUTPUT, new code is loaded!');
console.log('🔥 This version includes: Complete Workflow Output + Metrics sections');

// Animated Workflow Node
const AnimatedWorkflowNode = React.memo(({ data, id }) => {
  console.log('🎨 Rendering node:', id, data);
  
  const isActive = data?.isActive || false;
  const isCompleted = data?.isCompleted || false;
  
  return (
    <div
      className={`px-6 py-4 rounded-xl shadow-2xl border-2 transition-all min-w-[220px] ${
        isActive ? 'bg-gradient-to-br from-purple-600 to-blue-600 border-white shadow-lg shadow-purple-500/50' :
        isCompleted ? 'bg-gradient-to-br from-green-600 to-green-700 border-green-400' :
        'bg-gradient-to-br from-gray-800 to-gray-900 border-gray-700'
      }`}
    >
      <Handle type="target" position={Position.Top} className="w-3 h-3 !bg-purple-500 !border-2 !border-white" />
      
      <div className="flex items-start gap-3">
        <div className={`p-2 rounded-lg ${isActive ? 'bg-white/20' : 'bg-purple-600'}`}>
          <FaNetworkWired className={`text-lg text-white`} />
        </div>
        <div className="flex-1">
          <div className="font-bold text-white text-sm">{data?.label || 'Workflow'}</div>
          <div className="text-xs text-gray-200 mt-1">
            {isActive && '⚡ Executing...'}
            {isCompleted && '✓ Completed'}
            {!isActive && !isCompleted && '⏳ Pending'}
          </div>
          {data?.facts && data.facts.length > 0 && (
            <div className="mt-2 text-xs text-green-300">
              📌 {data.facts.length} facts extracted
            </div>
          )}
        </div>
      </div>
      
      <Handle type="source" position={Position.Bottom} className="w-3 h-3 !bg-purple-500 !border-2 !border-white" />
    </div>
  );
});

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
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [activeWorkflowIndex, setActiveWorkflowIndex] = useState(-1);
  const [workflowStates, setWorkflowStates] = useState({});
  const messagesEndRef = useRef(null);
  
  // Solution execution state
  const [ws, setWs] = useState(null);
  const [executing, setExecuting] = useState(false);
  const [executionMessages, setExecutionMessages] = useState([]);

  const nodeTypes = React.useMemo(() => ({
    workflowNode: AnimatedWorkflowNode,
  }), []);

  useEffect(() => {
    initializeSession();
    initializeWebSocket();
  }, [solutionId]);

  useEffect(() => {
    return () => {
      if (ws) {
        ws.close();
      }
    };
  }, [ws]);

  useEffect(() => {
    if (session) {
      loadSolutionContext();
      loadBlueprint();
    }
  }, [session]);

  useEffect(() => {
    // Initialize visualization when solution is loaded
    if (solution && solution.workflows && solution.workflows.length > 0) {
      console.log('Solution loaded, initializing visualization...');
      initializeWorkflowVisualization();
    }
  }, [solution]);

  useEffect(() => {
    console.log('🎨 Nodes state updated:', nodes.length, 'nodes');
    console.log('🎨 Current nodes:', nodes);
  }, [nodes]);

  useEffect(() => {
    console.log('🔗 Edges state updated:', edges.length, 'edges');
  }, [edges]);

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

  const initializeWorkflowVisualization = async () => {
    if (!solution || !solution.workflows) {
      console.log('No solution or workflows to visualize');
      return;
    }

    console.log('🔍 Initializing workflow visualization for:', solution.workflows);
    console.log('🔍 Solution object:', solution);

    try {
      // Load all workflows
      const workflowPromises = solution.workflows.map(wfId => workflowsAPI.getById(wfId));
      const workflowsData = await Promise.all(workflowPromises);

      console.log('✅ Loaded workflow data:', workflowsData);

      const flowNodes = workflowsData.map((wf, index) => ({
        id: wf.data.id,
        type: 'default', // TEMPORARILY using default type to test ReactFlow
        position: { x: 250, y: 100 + index * 220 },
        data: {
          label: wf.data.name || wf.data.id,
          workflowId: wf.data.id,
          isActive: false,
          isCompleted: false,
          facts: []
        },
        style: {
          background: '#1f2937',
          color: '#fff',
          border: '2px solid #8b5cf6',
          borderRadius: '12px',
          padding: '10px',
          width: 220
        }
      }));

      const flowEdges = [];
      for (let i = 0; i < flowNodes.length - 1; i++) {
        flowEdges.push({
          id: `e${i}-${i+1}`,
          source: flowNodes[i].id,
          target: flowNodes[i+1].id,
          animated: true,
          style: { stroke: '#8b5cf6', strokeWidth: 3 },
          markerEnd: { type: MarkerType.ArrowClosed, color: '#8b5cf6', width: 20, height: 20 },
          type: 'smoothstep',
        });
      }

      console.log('📊 Created nodes:', JSON.stringify(flowNodes, null, 2));
      console.log('🔗 Created edges:', JSON.stringify(flowEdges, null, 2));
      console.log('💾 Setting nodes and edges in state...');

      // Set nodes and edges immediately
      setNodes(flowNodes);
      setEdges(flowEdges);
      
      console.log('✨ Nodes and edges set! Count:', flowNodes.length, 'nodes,', flowEdges.length, 'edges');
    } catch (err) {
      console.error('❌ Error initializing workflow visualization:', err);
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

  // WebSocket for solution execution
  const initializeWebSocket = () => {
    if (!solutionId) {
      console.error('❌ Cannot initialize WebSocket: solutionId is missing!');
      return;
    }
    
    const wsUrl = `ws://localhost:8000/solutions/ws/${solutionId}`;
    console.log('🔌 Connecting to WebSocket for solution:', solutionId);
    console.log('🔌 WebSocket URL:', wsUrl);
    
    const websocket = new WebSocket(wsUrl);
    
    websocket.onopen = () => {
      console.log('✅ Solution WebSocket connected!');
      setWs(websocket);
    };
    
    websocket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log('📨 Received WebSocket message:', data);
        handleWebSocketMessage(data);
      } catch (e) {
        console.error('❌ WebSocket message error:', e);
      }
    };
    
    websocket.onerror = (error) => {
      console.error('❌ WebSocket error:', error);
      console.error('❌ WebSocket URL was:', wsUrl);
      console.error('❌ Solution ID:', solutionId);
      setExecutionMessages(prev => [...prev, { 
        type: 'error', 
        message: `WebSocket connection error. URL: ${wsUrl}` 
      }]);
    };
    
    websocket.onclose = (event) => {
      console.log('🔌 Solution WebSocket disconnected');
      console.log('🔌 Close code:', event.code, 'Reason:', event.reason);
      setWs(null);
    };
  };

  const handleWebSocketMessage = (message) => {
    console.log('📥📥📥 WEBSOCKET MESSAGE RECEIVED! 📥📥📥');
    console.log('📥 Message type:', message.type);
    console.log('📥 Full message:', message);
    
    // Log specific fields for workflow_completed
    if (message.type === 'workflow_completed') {
      console.log('🔍 WORKFLOW COMPLETED DETAILS:');
      console.log('  - Has output?', !!message.output);
      console.log('  - Output length:', message.output?.length || 0);
      console.log('  - Has metrics?', !!message.metrics);
      console.log('  - Metrics:', message.metrics);
      console.log('  - Has KAG?', !!message.kag_analysis);
    }
    
    // Log specific fields for execution_completed
    if (message.type === 'execution_completed') {
      console.log('🎉 EXECUTION COMPLETED DETAILS:');
      console.log('  - Has summary?', !!message.summary);
      console.log('  - Has all_workflow_outputs?', !!message.all_workflow_outputs);
      console.log('  - Workflow outputs count:', message.all_workflow_outputs?.length || 0);
      console.log('  - Has overall_metrics?', !!message.overall_metrics);
      console.log('  - Overall metrics:', message.overall_metrics);
    }
    
    console.log('📥 Current executionMessages count:', executionMessages.length);
    
    // ALWAYS add to execution messages
    setExecutionMessages(prev => {
      const newMessages = [...prev, message];
      console.log('📥 Updated executionMessages, new count:', newMessages.length);
      return newMessages;
    });

    switch (message.type) {
      case 'execution_started':
        console.log('▶️ Execution started!');
        setExecuting(true);
        setWorkflowStates({});
        break;

      case 'workflow_started':
        console.log('🔄 Workflow started:', message.workflow_name);
        // Update node to active
        setNodes(prevNodes => prevNodes.map((node, idx) => {
          if (idx === message.position - 1) {
            return {
              ...node,
              data: { ...node.data, isActive: true, isCompleted: false }
            };
          }
          return node;
        }));
        break;

      case 'workflow_completed':
        console.log('✅ Workflow completed:', message.workflow_id, 'Output:', message.output);
        console.log('✅ FULL MESSAGE:', JSON.stringify(message, null, 2));
        console.log('✅ Output field exists?', 'output' in message);
        console.log('✅ Output value:', message.output);
        console.log('✅ Output length:', message.output?.length);
        // Update node to completed
        setNodes(prevNodes => prevNodes.map((node, idx) => {
          const workflowIndex = solution?.workflows?.indexOf(message.workflow_id);
          if (idx === workflowIndex) {
            return {
              ...node,
              data: { 
                ...node.data, 
                isActive: false, 
                isCompleted: true,
                facts: message.kag_analysis?.facts || [],
                output: message.output  // Store the output
              }
            };
          }
          return node;
        }));
        
        setWorkflowStates(prev => ({
          ...prev,
          [message.workflow_id]: {
            status: 'completed',
            kag: message.kag_analysis,
            output: message.output,
            metrics: message.metrics
          }
        }));
        break;

      case 'execution_completed':
        console.log('🎉 Execution completed!', message);
        console.log('📚 All workflow outputs:', message.all_workflow_outputs);
        console.log('📋 Summary:', message.summary);
        // Message already added at top of function, no need to add again
        setExecuting(false);
        break;

      case 'error':
        console.error('❌ Error:', message.message);
        setExecuting(false);
        break;

      default:
        console.log('❓ Unknown message type:', message.type);
    }
  };

  const startExecution = () => {
    console.log('🚀🚀🚀 EXECUTE BUTTON CLICKED! 🚀🚀🚀');
    console.log('🚀 Starting execution, ws state:', ws?.readyState);
    console.log('🚀 WebSocket object:', ws);
    console.log('🚀 Solution ID:', solutionId);
    
    // Show immediate feedback - APPEND to existing messages, don't replace!
    setExecutionMessages(prev => [...prev, { 
      type: 'info', 
      message: `🚀 Starting new execution...` 
    }]);
    
    // WebSocket.OPEN = 1
    if (ws && ws.readyState === 1) {
      console.log('📤 Sending execute command for solution:', solutionId);
      setExecutionMessages(prev => [...prev, { 
        type: 'info', 
        message: `📤 Sending execute command to backend...` 
      }]);
      ws.send(JSON.stringify({ action: 'execute' }));
    } else {
      const errorMsg = !ws ? 'WebSocket not initialized' : `WebSocket not ready. State: ${ws.readyState} (need 1 for OPEN)`;
      console.error('❌', errorMsg);
      alert(`Cannot execute: ${errorMsg}. Please refresh the page.`);
      setExecutionMessages(prev => [...prev, { type: 'error', message: errorMsg }]);
    }
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
              <p className="text-xs text-blue-200 mt-1 flex items-center gap-2">
                WebSocket: {ws?.readyState === 1 ? (
                  <span className="text-green-300">● Connected</span>
                ) : ws?.readyState === 0 ? (
                  <span className="text-yellow-300">● Connecting...</span>
                ) : (
                  <>
                    <span className="text-red-300">● Disconnected</span>
                    <button
                      onClick={initializeWebSocket}
                      className="ml-2 px-2 py-1 text-xs bg-blue-500 hover:bg-blue-600 rounded"
                    >
                      Reconnect
                    </button>
                  </>
                )}
              </p>
            </div>
            <div className="flex gap-2">
              <button
                onClick={startExecution}
                disabled={executing || !ws}
                className={`px-4 py-2 rounded-lg flex items-center gap-2 font-semibold transition-all ${
                  executing 
                    ? 'bg-yellow-600 text-white cursor-not-allowed' 
                    : 'bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 text-white shadow-lg'
                }`}
              >
                {executing ? (
                  <>
                    <FaSpinner className="animate-spin" />
                    Executing...
                  </>
                ) : (
                  <>
                    <FaPlay />
                    Execute Solution
                  </>
                )}
              </button>
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
              {/* Execution Messages */}
              {executionMessages.length > 0 && (
                <div className="bg-purple-900/20 border-2 border-purple-500/50 rounded-lg p-4 mb-4">
                  <h4 className="text-purple-300 font-bold mb-2 flex items-center gap-2">
                    <FaBrain /> Solution Execution Log ({executionMessages.length} messages)
                  </h4>
                  <div className="space-y-3 max-h-[600px] overflow-y-auto">
                    {executionMessages.map((msg, idx) => (
                      <div key={idx} className="text-sm">
                        {msg.type === 'execution_started' && (
                          <div className="text-green-400">▶️ Execution started - {msg.total_workflows} workflows</div>
                        )}
                        {msg.type === 'workflow_started' && (
                          <div className="text-blue-400">🔄 Workflow {msg.position}/{msg.total}: {msg.workflow_name}</div>
                        )}
                        {msg.type === 'workflow_completed' && (
                          <div className="border-l-4 border-green-500 pl-3 py-2 bg-green-900/10 rounded">
                            <div className="text-green-400 font-semibold mb-3 text-base">
                              ✅ Completed: {msg.workflow_name}
                            </div>
                            
                            {/* Workflow Output/Tool Results - ALWAYS SHOW */}
                            <div className="mt-3 bg-gray-800/50 rounded p-3 border border-gray-700">
                              <div className="text-blue-300 text-sm font-bold mb-2">📊 Complete Workflow Output:</div>
                              {msg.output ? (
                                <pre className="text-gray-300 text-xs whitespace-pre-wrap overflow-x-auto max-h-96 overflow-y-auto bg-black/30 p-3 rounded border border-gray-600">
                                  {typeof msg.output === 'string' ? msg.output : JSON.stringify(msg.output, null, 2)}
                                </pre>
                              ) : (
                                <div className="text-red-400 text-xs bg-red-900/20 p-2 rounded">
                                  ⚠️ No output data received from backend
                                </div>
                              )}
                            </div>
                            
                            {/* Metrics - Show if available */}
                            {msg.metrics && Object.keys(msg.metrics).length > 0 && (
                              <div className="mt-3 bg-blue-900/20 rounded p-3 border border-blue-700/30">
                                <div className="text-blue-300 text-sm font-bold mb-2">� Workflow Metrics:</div>
                                <div className="grid grid-cols-2 gap-2 text-xs">
                                  {msg.metrics.execution_time && (
                                    <div className="text-gray-300 bg-black/20 p-2 rounded">
                                      <span className="font-semibold">⏱️ Execution Time:</span> {msg.metrics.execution_time.toFixed(2)}s
                                    </div>
                                  )}
                                  {msg.metrics.total_tokens && (
                                    <div className="text-gray-300 bg-black/20 p-2 rounded">
                                      <span className="font-semibold">🔢 Tokens Used:</span> {msg.metrics.total_tokens}
                                    </div>
                                  )}
                                  {msg.metrics.cost && (
                                    <div className="text-gray-300 bg-black/20 p-2 rounded">
                                      <span className="font-semibold">💰 Cost:</span> ${msg.metrics.cost.toFixed(4)}
                                    </div>
                                  )}
                                  {msg.metrics.model && (
                                    <div className="text-gray-300 bg-black/20 p-2 rounded">
                                      <span className="font-semibold">🤖 Model:</span> {msg.metrics.model}
                                    </div>
                                  )}
                                </div>
                                {/* Show all metrics as JSON if there are more */}
                                <details className="mt-2">
                                  <summary className="text-xs text-gray-400 cursor-pointer hover:text-gray-300">
                                    View all metrics (JSON)
                                  </summary>
                                  <pre className="text-xs text-gray-400 mt-2 bg-black/30 p-2 rounded overflow-auto max-h-40">
                                    {JSON.stringify(msg.metrics, null, 2)}
                                  </pre>
                                </details>
                              </div>
                            )}
                            
                            {/* KAG Analysis */}
                            {msg.kag_analysis && (
                              <div className="mt-3 space-y-2">
                                {msg.kag_analysis.summary && (
                                  <div className="bg-purple-900/20 rounded p-3 border border-purple-700/30">
                                    <div className="text-purple-300 text-sm font-semibold mb-2">🤖 AI Summary:</div>
                                    <div className="text-gray-300 text-sm">{msg.kag_analysis.summary}</div>
                                  </div>
                                )}
                                
                                {msg.kag_analysis.facts && msg.kag_analysis.facts.length > 0 && (
                                  <div className="bg-green-900/20 rounded p-3 border border-green-700/30">
                                    <div className="text-green-300 text-sm font-semibold mb-2">
                                      📌 Facts Extracted ({msg.kag_analysis.facts.length}):
                                    </div>
                                    <ul className="list-disc list-inside text-gray-300 text-sm space-y-1">
                                      {msg.kag_analysis.facts.map((fact, i) => (
                                        <li key={i}>{fact}</li>
                                      ))}
                                    </ul>
                                  </div>
                                )}
                                
                                {msg.kag_analysis.reasoning && (
                                  <div className="bg-blue-900/20 rounded p-3 border border-blue-700/30">
                                    <div className="text-blue-300 text-sm font-semibold mb-2">💭 AI Reasoning:</div>
                                    <div className="text-gray-300 text-sm italic">{msg.kag_analysis.reasoning}</div>
                                  </div>
                                )}
                              </div>
                            )}
                          </div>
                        )}
                        {msg.type === 'handoff_prepared' && (
                          <div className="text-yellow-400">🤝 Handoff: {msg.from_workflow} → {msg.to_workflow}</div>
                        )}
                        {msg.type === 'execution_completed' && (
                          <div className="border-l-4 border-green-500 pl-3 py-2 bg-green-900/10 rounded">
                            <div className="text-green-400 font-bold text-lg mb-3">
                              🎉 Execution Complete!
                            </div>
                            
                            {/* Debug info */}
                            <div className="text-xs text-gray-500 mb-2">
                              DEBUG: Has summary: {msg.summary ? 'YES' : 'NO'} | 
                              Has all_workflow_outputs: {msg.all_workflow_outputs ? 'YES' : 'NO'} | 
                              Outputs count: {msg.all_workflow_outputs?.length || 0}
                            </div>
                            
                            {/* Overall Summary */}
                            {msg.summary && (
                              <div className="mt-3 bg-gradient-to-r from-purple-900/30 to-blue-900/30 rounded-lg p-4">
                                <div className="text-purple-300 text-lg font-bold mb-3 flex items-center">
                                  📋 Overall Solution Summary
                                </div>
                                <div className="text-gray-200 text-base whitespace-pre-wrap leading-relaxed">
                                  {msg.summary}
                                </div>
                              </div>
                            )}
                            
                            {/* All Workflow Outputs */}
                            {msg.all_workflow_outputs && msg.all_workflow_outputs.length > 0 && (
                              <div className="mt-4 space-y-3">
                                <div className="text-cyan-300 text-lg font-bold mb-2">
                                  📚 Complete Workflow Results ({msg.all_workflow_outputs.length} workflows)
                                </div>
                                {msg.all_workflow_outputs.map((workflow, idx) => (
                                  <div key={idx} className="bg-gray-800/50 rounded-lg p-4 border border-gray-700">
                                    <div className="text-yellow-300 font-semibold mb-2">
                                      {idx + 1}. {workflow.workflow_name}
                                    </div>
                                    
                                    {/* Workflow Output */}
                                    {workflow.output && (
                                      <div className="mt-2 bg-black/30 rounded p-3">
                                        <div className="text-blue-300 text-sm font-semibold mb-1">Tool Results:</div>
                                        <pre className="text-gray-300 text-xs whitespace-pre-wrap overflow-x-auto max-h-64 overflow-y-auto">
                                          {typeof workflow.output === 'string' ? workflow.output : JSON.stringify(workflow.output, null, 2)}
                                        </pre>
                                      </div>
                                    )}
                                    
                                    {/* KAG Analysis for this workflow */}
                                    {workflow.kag_analysis && (
                                      <div className="mt-2 space-y-2">
                                        {workflow.kag_analysis.summary && (
                                          <div className="bg-purple-900/20 rounded p-2">
                                            <div className="text-purple-300 text-xs font-semibold mb-1">KAG Summary:</div>
                                            <div className="text-gray-300 text-xs">{workflow.kag_analysis.summary}</div>
                                          </div>
                                        )}
                                        {workflow.kag_analysis.facts && workflow.kag_analysis.facts.length > 0 && (
                                          <div className="bg-green-900/20 rounded p-2">
                                            <div className="text-green-300 text-xs font-semibold mb-1">
                                              Facts ({workflow.kag_analysis.facts.length}):
                                            </div>
                                            <ul className="list-disc list-inside text-gray-300 text-xs">
                                              {workflow.kag_analysis.facts.map((fact, i) => (
                                                <li key={i}>{fact}</li>
                                              ))}
                                            </ul>
                                          </div>
                                        )}
                                      </div>
                                    )}
                                  </div>
                                ))}
                              </div>
                            )}
                            
                            {/* Overall Metrics */}
                            {msg.overall_metrics && Object.keys(msg.overall_metrics).length > 0 && (
                              <div className="mt-3 bg-gradient-to-r from-blue-900/30 to-cyan-900/30 rounded-lg p-4 border border-blue-500/30">
                                <div className="text-cyan-300 text-base font-bold mb-3">📊 Overall Performance Metrics</div>
                                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                                  {msg.overall_metrics.execution_time !== undefined && (
                                    <div className="bg-black/30 rounded p-3">
                                      <div className="text-gray-400 text-xs mb-1">⏱️ Execution Time</div>
                                      <div className="text-white font-bold text-lg">{msg.overall_metrics.execution_time.toFixed(2)}s</div>
                                    </div>
                                  )}
                                  {msg.overall_metrics.total_tokens !== undefined && (
                                    <div className="bg-black/30 rounded p-3">
                                      <div className="text-gray-400 text-xs mb-1">🔢 Total Tokens</div>
                                      <div className="text-white font-bold text-lg">{msg.overall_metrics.total_tokens}</div>
                                    </div>
                                  )}
                                  {msg.overall_metrics.cost !== undefined && (
                                    <div className="bg-black/30 rounded p-3">
                                      <div className="text-gray-400 text-xs mb-1">💰 Total Cost</div>
                                      <div className="text-white font-bold text-lg">${msg.overall_metrics.cost.toFixed(4)}</div>
                                    </div>
                                  )}
                                  {msg.overall_metrics.task_completed !== undefined && (
                                    <div className="bg-black/30 rounded p-3">
                                      <div className="text-gray-400 text-xs mb-1">✅ Status</div>
                                      <div className="text-white font-bold text-lg">{msg.overall_metrics.task_completed ? 'Success' : 'Failed'}</div>
                                    </div>
                                  )}
                                </div>
                                <details className="mt-3">
                                  <summary className="text-xs text-gray-400 cursor-pointer hover:text-gray-300">
                                    View complete metrics (JSON)
                                  </summary>
                                  <pre className="text-xs text-gray-400 mt-2 bg-black/30 p-3 rounded overflow-auto max-h-48">
                                    {JSON.stringify(msg.overall_metrics, null, 2)}
                                  </pre>
                                </details>
                              </div>
                            )}
                            
                            {/* Fallback: Show raw message if nothing is displaying */}
                            {!msg.summary && !msg.all_workflow_outputs && (
                              <div className="mt-3 bg-red-900/20 rounded p-3">
                                <div className="text-red-300 text-sm font-semibold mb-2">⚠️ Raw Message Data:</div>
                                <pre className="text-gray-300 text-xs whitespace-pre-wrap overflow-x-auto max-h-64 overflow-y-auto">
                                  {JSON.stringify(msg, null, 2)}
                                </pre>
                              </div>
                            )}
                          </div>
                        )}
                        {msg.type === 'error' && (
                          <div className="text-red-400">❌ Error: {msg.message}</div>
                        )}
                        {msg.type === 'info' && (
                          <div className="text-yellow-400 text-xs">{msg.message}</div>
                        )}
                        {!['execution_started', 'workflow_started', 'workflow_completed', 'handoff_prepared', 'execution_completed', 'error', 'info'].includes(msg.type) && (
                          <div className="bg-orange-900/20 rounded p-2">
                            <div className="text-orange-300 text-xs font-semibold">Unknown message type: {msg.type}</div>
                            <pre className="text-gray-300 text-xs mt-1">{JSON.stringify(msg, null, 2)}</pre>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}
              
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

          {/* Animated Workflow Visualization */}
          {showBlueprint && (
            <div className="w-1/2 border-l border-gray-200 bg-red-900 relative h-full">
              {/* GIANT TEST BOX */}
              <div className="absolute inset-0 flex items-center justify-center z-50 pointer-events-none">
                <div className="bg-yellow-500 text-black p-8 rounded-lg text-2xl font-bold">
                  TEST: Can you see this yellow box?
                  <div className="text-lg">Nodes: {nodes.length}</div>
                  <div className="text-lg">showBlueprint: {showBlueprint ? 'true' : 'false'}</div>
                </div>
              </div>

              <div className="absolute top-4 left-4 z-10 bg-black/60 backdrop-blur-sm rounded-lg p-3 border border-purple-500/30">
                <h3 className="text-lg font-bold text-white flex items-center gap-2">
                  <FaNetworkWired className="text-purple-400" /> 
                  Live Workflow Chain
                </h3>
                {solution && (
                  <p className="text-sm text-gray-300 mt-1">
                    {solution.workflows?.length || 0} Sequential Workflows
                  </p>
                )}
                {nodes.length > 0 && (
                  <p className="text-xs text-green-400 mt-1">
                    ✓ {nodes.length} nodes loaded
                  </p>
                )}
              </div>

              {nodes.length === 0 ? (
                <div className="flex items-center justify-center h-full">
                  <div className="text-center text-gray-400">
                    <FaSpinner className="animate-spin text-4xl mx-auto mb-3 text-purple-400" />
                    <p>Loading workflow visualization...</p>
                    <p className="text-sm mt-2">Initializing {solution?.workflows?.length || 0} workflows</p>
                  </div>
                </div>
              ) : (
                <>
                  {/* Debug Info */}
                  <div className="absolute top-20 left-4 z-20 bg-black/80 text-white p-2 rounded text-xs max-w-xs">
                    <div>Nodes: {nodes.length}</div>
                    {nodes.map((node, i) => (
                      <div key={i} className="text-green-400">
                        {i+1}. {node.data.label} @ ({node.position.x}, {node.position.y})
                      </div>
                    ))}
                  </div>

                  {/* TEST: Simple absolute positioned divs */}
                  {nodes.map((node, i) => (
                    <div 
                      key={node.id}
                      style={{
                        position: 'absolute',
                        left: node.position.x,
                        top: node.position.y,
                        zIndex: 5
                      }}
                      className="px-6 py-4 bg-purple-700 border-2 border-purple-400 rounded-xl text-white shadow-lg"
                    >
                      <div className="font-bold">{i+1}. {node.data.label}</div>
                      <div className="text-xs text-gray-300 mt-1">⏳ Pending</div>
                    </div>
                  ))}

                  <div className="h-full w-full" style={{ minHeight: '400px', position: 'relative' }}>
                    <ReactFlow
                      key={`reactflow-${nodes.length}`}
                      nodes={nodes}
                      edges={edges}
                      onNodesChange={onNodesChange}
                      onEdgesChange={onEdgesChange}
                      nodeTypes={nodeTypes}
                      fitView
                      fitViewOptions={{ padding: 0.2, minZoom: 0.5, maxZoom: 1.5 }}
                      className="bg-gray-900"
                      proOptions={{ hideAttribution: true }}
                      defaultViewport={{ x: 0, y: 0, zoom: 1 }}
                      minZoom={0.1}
                      maxZoom={2}
                    >
                      <Background color="#333" gap={16} />
                      <Controls className="bg-gray-800 border-gray-700" />
                    </ReactFlow>
                  </div>
                </>
              )}

              {/* Workflow Status Panel */}
              {Object.keys(workflowStates).length > 0 && (
                <div className="absolute bottom-4 left-4 right-4 bg-black/80 backdrop-blur-sm rounded-lg p-4 border border-purple-500/30 max-h-48 overflow-y-auto">
                  <h4 className="text-white font-semibold mb-2 flex items-center gap-2">
                    <FaBrain className="text-purple-400" />
                    AI Analysis
                  </h4>
                  <div className="space-y-2 text-sm">
                    {Object.entries(workflowStates).map(([wfId, state]) => (
                      <div key={wfId} className="text-gray-300">
                        <span className="text-white font-medium">{state.name}:</span>
                        {state.facts && state.facts.length > 0 && (
                          <span className="text-green-400 ml-2">
                            ✓ {state.facts.length} facts
                          </span>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default SolutionChat;
