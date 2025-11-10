import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import ReactFlow, { Background, Controls, MarkerType, Position, Handle, useNodesState, useEdgesState } from 'reactflow';
import 'reactflow/dist/style.css';
import { 
  FaTimes, 
  FaPaperPlane, 
  FaRobot, 
  FaUser, 
  FaTools,
  FaSpinner,
  FaProjectDiagram 
} from 'react-icons/fa';
import { workflowsAPI } from '../services/api';

// Animated Agent Node for real-time workflow visualization
const LiveAgentNode = ({ data }) => {
  const isActive = data.isActive;
  const isCompleted = data.isCompleted;
  const isPending = !isActive && !isCompleted;
  
  return (
    <motion.div
      initial={{ scale: 0.9, opacity: 0 }}
      animate={{ 
        scale: isActive ? 1.05 : 1,
        opacity: 1,
      }}
      className={`px-6 py-4 rounded-xl shadow-2xl border-2 transition-all min-w-[200px] ${
        isActive ? 'bg-gradient-to-br from-purple-600 to-pink-600 border-white shadow-lg shadow-purple-500/50 animate-pulse' :
        isCompleted ? 'bg-gradient-to-br from-green-600 to-green-700 border-green-400' :
        'bg-gradient-to-br from-gray-800 to-gray-900 border-gray-700'
      }`}
    >
      {/* Connection Handles */}
      <Handle type="target" position={Position.Top} className="w-3 h-3 !bg-purple-500 !border-2 !border-white" />
      <Handle type="target" position={Position.Left} className="w-3 h-3 !bg-purple-500 !border-2 !border-white" />
      
      <div className="flex items-start gap-3">
        <div className={`p-2 rounded-lg ${isActive ? 'bg-white/20' : 'bg-purple-600'}`}>
          <FaRobot className={`text-lg ${isActive ? 'text-white animate-bounce' : 'text-white'}`} />
        </div>
        <div className="flex-1">
          <div className="font-bold text-white text-sm">{data.label}</div>
          <div className="text-xs text-gray-200 mt-1">
            {isActive && '⚡ Processing...'}
            {isCompleted && '✓ Completed'}
            {isPending && '⏳ Pending'}
          </div>
          {data.tools && data.tools.length > 0 && (
            <div className="flex gap-1 mt-2 flex-wrap">
              {data.tools.map((tool, idx) => (
                <span key={idx} className="text-[10px] px-2 py-0.5 rounded-full bg-blue-500/30 text-blue-200 border border-blue-400/30">
                  <FaTools className="inline mr-1" />{tool}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>
      
      <Handle type="source" position={Position.Bottom} className="w-3 h-3 !bg-purple-500 !border-2 !border-white" />
      <Handle type="source" position={Position.Right} className="w-3 h-3 !bg-purple-500 !border-2 !border-white" />
    </motion.div>
  );
};

const nodeTypes = {
  liveAgent: LiveAgentNode,
};

const WorkflowChat = ({ workflow, agents, onClose }) => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isExecuting, setIsExecuting] = useState(false);
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [activeNodeIndex, setActiveNodeIndex] = useState(-1);
  const messagesEndRef = useRef(null);

  // Initialize workflow visualization
  useEffect(() => {
    if (workflow && workflow.nodes) {
      const flowNodes = workflow.nodes.map((node, index) => {
        const agent = agents.find((a) => a.id === node.agent_ref);
        return {
          id: node.id,
          type: 'liveAgent',
          position: { x: 150 + (index % 3) * 300, y: 100 + Math.floor(index / 3) * 250 },
          data: {
            label: agent?.name || node.agent_ref,
            agentId: node.agent_ref,
            task: node.task,
            tools: node.tools || [],
            isActive: false,
            isCompleted: false,
          },
        };
      });

      const flowEdges = [];
      workflow.nodes.forEach((node) => {
        if (node.dependencies && node.dependencies.length > 0) {
          node.dependencies.forEach((depId) => {
            flowEdges.push({
              id: `e${depId}-${node.id}`,
              source: depId,
              target: node.id,
              animated: false,
              style: { stroke: '#6b7280', strokeWidth: 2 },
              markerEnd: { type: MarkerType.ArrowClosed, color: '#6b7280', width: 18, height: 18 },
              type: 'smoothstep',
            });
          });
        }
      });

      setNodes(flowNodes);
      setEdges(flowEdges);
    }
  }, [workflow, agents, setNodes, setEdges]);

  // Auto-scroll to bottom of chat
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Simulate workflow execution with visual updates
  const executeWorkflow = async (userQuery) => {
    if (!userQuery.trim() || isExecuting) return;

    setIsExecuting(true);
    
    // Add user message
    const userMsg = {
      id: Date.now(),
      type: 'user',
      content: userQuery,
      timestamp: new Date().toLocaleTimeString(),
    };
    setMessages(prev => [...prev, userMsg]);
    setInputMessage('');

    try {
      // Add system message
      const systemMsg = {
        id: Date.now() + 1,
        type: 'system',
        content: `🚀 Starting workflow: ${workflow.name}`,
        timestamp: new Date().toLocaleTimeString(),
      };
      setMessages(prev => [...prev, systemMsg]);

      // Execute workflow via API
      const response = await workflowsAPI.run(workflow.id, { query: userQuery });
      
      console.log('Workflow response:', response.data);
      
      const workflowNodes = workflow.nodes || [];
      
      // Check if we have new structured format
      const isStructuredFormat = response.data?.summary && response.data?.results;
      
      if (isStructuredFormat) {
        // NEW STRUCTURED FORMAT
        console.log('Using new structured output format');
        
        // Show summary first
        const summaryMsg = {
          id: Date.now() + 1,
          type: 'system',
          content: `✓ ${response.data.summary}`,
          timestamp: new Date().toLocaleTimeString(),
        };
        setMessages(prev => [...prev, summaryMsg]);
        
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // Process each node's results
        const results = response.data.results || {};
        let nodeIdx = 0;
        
        for (const [nodeId, nodeData] of Object.entries(results)) {
          // Update active node
          setActiveNodeIndex(nodeIdx);
          updateNodeState(nodeIdx, 'active');
          
          await new Promise(resolve => setTimeout(resolve, 800));
          
          // Add agent response
          const agentMsg = {
            id: Date.now() + nodeIdx + 2,
            type: 'agent',
            agent: nodeData.agent || 'Agent',
            content: nodeData.response || 'No response',
            tools: nodeData.tools_executed?.map(t => t.tool) || [],
            toolResults: nodeData.tools_executed?.reduce((acc, tool) => {
              acc[tool.tool] = tool.summary;
              return acc;
            }, {}) || {},
            timestamp: new Date().toLocaleTimeString(),
          };
          setMessages(prev => [...prev, agentMsg]);
          
          // Mark node as completed
          await new Promise(resolve => setTimeout(resolve, 600));
          updateNodeState(nodeIdx, 'completed');
          
          nodeIdx++;
        }
        
      } else {
        // OLD FORMAT - Process communication log
        const communicationLog = response.data?.meta?.communication_log || [];
        
        if (communicationLog.length > 0) {
          // Process each message in the communication log
          for (let i = 0; i < communicationLog.length; i++) {
            const logEntry = communicationLog[i];
            
            // Find which node this corresponds to
            const nodeIndex = workflowNodes.findIndex(n => 
              logEntry.from === n.agent_ref || logEntry.to === n.agent_ref
            );
            
            if (nodeIndex >= 0) {
              // Update active node
              setActiveNodeIndex(nodeIndex);
              updateNodeState(nodeIndex, 'active');
              
              // Update edges to show active connection
              if (nodeIndex > 0) {
                updateEdgeState(nodeIndex - 1, nodeIndex, 'completed');
              }
            }
            
            // Add message to chat
            await new Promise(resolve => setTimeout(resolve, 800));
            
            // Safely extract content and convert to string if needed
            let messageContent = logEntry.content || logEntry.message || logEntry.llm_response || 'Processing...';
            if (typeof messageContent === 'object') {
              messageContent = JSON.stringify(messageContent, null, 2);
            }
            
            const agentMsg = {
              id: Date.now() + i + 2,
              type: 'agent',
              agent: logEntry.from || logEntry.agent_name || workflowNodes[nodeIndex]?.agent_ref || 'Agent',
              content: messageContent,
              tools: logEntry.tools_used || [],
              toolResults: logEntry.tool_results || {},
              timestamp: new Date().toLocaleTimeString(),
            };
            setMessages(prev => [...prev, agentMsg]);
            
            // Mark node as completed
            if (nodeIndex >= 0) {
              await new Promise(resolve => setTimeout(resolve, 600));
              updateNodeState(nodeIndex, 'completed');
            }
          }
        } else {
          // If no communication log, show the result directly
          const resultMsg = {
            id: Date.now() + 2,
            type: 'agent',
            agent: 'Workflow',
            content: JSON.stringify(response.data?.result || response.data, null, 2),
            tools: [],
            toolResults: {},
            timestamp: new Date().toLocaleTimeString(),
          };
          setMessages(prev => [...prev, resultMsg]);
        }
      }

    } catch (error) {
      console.error('Workflow execution error:', error);
      const errorMsg = {
        id: Date.now() + 1000,
        type: 'error',
        content: `Error: ${error.response?.data?.detail || error.message}`,
        timestamp: new Date().toLocaleTimeString(),
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setIsExecuting(false);
      setActiveNodeIndex(-1);
    }
  };

  const updateNodeState = (index, state) => {
    setNodes((nds) =>
      nds.map((node, idx) => {
        if (idx === index) {
          return {
            ...node,
            data: {
              ...node.data,
              isActive: state === 'active',
              isCompleted: state === 'completed',
            },
          };
        }
        return node;
      })
    );
  };

  const updateEdgeState = (fromIndex, toIndex, state) => {
    const sourceId = workflow.nodes[fromIndex]?.id;
    const targetId = workflow.nodes[toIndex]?.id;
    
    setEdges((eds) =>
      eds.map((edge) => {
        if (edge.source === sourceId && edge.target === targetId) {
          return {
            ...edge,
            animated: state === 'active',
            style: {
              stroke: state === 'completed' ? '#10b981' : state === 'active' ? '#a855f7' : '#6b7280',
              strokeWidth: state === 'active' ? 4 : state === 'completed' ? 3 : 2,
              strokeDasharray: state === 'active' ? '10,5' : 'none',
            },
            markerEnd: {
              type: MarkerType.ArrowClosed,
              color: state === 'completed' ? '#10b981' : state === 'active' ? '#a855f7' : '#6b7280',
              width: state === 'active' ? 24 : 18,
              height: state === 'active' ? 24 : 18,
            },
            label: state === 'active' ? '📡 Data Transfer' : undefined,
            labelStyle: state === 'active' ? { 
              fill: '#a855f7', 
              fontWeight: 600,
              fontSize: 10,
              background: 'rgba(168, 85, 247, 0.1)',
              padding: '4px 8px',
              borderRadius: '4px'
            } : undefined,
            labelBgStyle: state === 'active' ? { 
              fill: '#1f2937',
              fillOpacity: 0.8
            } : undefined,
          };
        }
        return edge;
      })
    );
  };

  const handleSendMessage = (e) => {
    e.preventDefault();
    executeWorkflow(inputMessage);
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="bg-gray-950 rounded-2xl w-[95vw] h-[90vh] flex shadow-2xl overflow-hidden border-2 border-gray-800"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Left Side - Workflow Visualization (60%) */}
        <div className="w-[60%] flex flex-col border-r border-gray-800">
          {/* Workflow Header */}
          <div className="p-4 border-b border-gray-800 bg-gray-900">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-gradient-to-br from-purple-600 to-pink-600 shadow-lg shadow-purple-500/30">
                <FaProjectDiagram className="text-white text-base" />
              </div>
              <div>
                <h3 className="text-base font-bold text-white">Workflow Execution</h3>
                <p className="text-xs text-gray-400">{workflow.name}</p>
              </div>
            </div>
          </div>

          {/* Workflow Canvas */}
          <div className="flex-1 bg-gradient-to-br from-gray-950 via-gray-900 to-gray-950 relative">
            <ReactFlow
              nodes={nodes}
              edges={edges}
              onNodesChange={onNodesChange}
              onEdgesChange={onEdgesChange}
              nodeTypes={nodeTypes}
              fitView
              nodesDraggable={false}
              nodesConnectable={false}
              elementsSelectable={false}
              className="bg-transparent"
            >
              <Background color="#1f2937" gap={16} size={1} variant="dots" />
              <Controls className="!bg-gray-800 !border-gray-700 !rounded-lg [&>button]:!bg-gray-700 [&>button]:!border-gray-600 [&>button]:!text-gray-200" />
            </ReactFlow>
            
            {/* Animated data flow particles */}
            {activeNodeIndex >= 0 && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="absolute top-4 right-4 bg-purple-600/20 backdrop-blur-sm rounded-lg p-3 border border-purple-500/30"
              >
                <div className="flex items-center gap-2">
                  <FaSpinner className="animate-spin text-purple-400" />
                  <span className="text-sm text-purple-300">Processing Step {activeNodeIndex + 1}...</span>
                </div>
              </motion.div>
            )}
          </div>
        </div>

        {/* Right Side - Chat Interface (40%) */}
        <div className="w-[40%] flex flex-col bg-gray-900">
          {/* Chat Header */}
          <div className="p-4 border-b border-gray-800 bg-gray-900 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="p-2 rounded-lg bg-gradient-to-br from-blue-600 to-blue-700">
                <FaRobot className="text-white text-sm" />
              </div>
              <div>
                <h3 className="text-sm font-bold text-white">Chat with Workflow</h3>
                <p className="text-xs text-gray-400">Ask questions and see results</p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="p-2 rounded-lg bg-gray-800 hover:bg-gray-700 text-gray-300 transition-colors border border-gray-700"
            >
              <FaTimes className="text-sm" />
            </button>
          </div>

          {/* Messages Area */}
          <div className="flex-1 overflow-y-auto p-3 space-y-2">
            <AnimatePresence>
              {messages.map((msg) => (
                <motion.div
                  key={msg.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0 }}
                  className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  {msg.type === 'user' ? (
                    <div className="flex items-start gap-2 max-w-[85%]">
                      <div className="bg-gradient-to-br from-purple-600 to-pink-600 rounded-lg p-3 shadow-md">
                        <p className="text-white text-xs">{msg.content}</p>
                        <span className="text-[10px] text-purple-200 mt-1 block">{msg.timestamp}</span>
                      </div>
                      <div className="p-1.5 rounded-full bg-purple-600 flex-shrink-0">
                        <FaUser className="text-white text-[10px]" />
                      </div>
                    </div>
                  ) : msg.type === 'agent' ? (
                    <div className="flex items-start gap-2 max-w-[90%]">
                      <div className="p-1.5 rounded-full bg-gradient-to-br from-blue-600 to-blue-700 flex-shrink-0">
                        <FaRobot className="text-white text-[10px]" />
                      </div>
                      <div className="bg-gray-800 rounded-lg p-3 shadow-md border border-gray-700 flex-1">
                        <div className="flex items-center gap-2 mb-1 flex-wrap">
                          <span className="text-[10px] font-bold text-blue-400">{msg.agent}</span>
                          {msg.tools && msg.tools.length > 0 && (
                            <div className="flex gap-1 flex-wrap">
                              {msg.tools.map((tool, idx) => (
                                <span key={idx} className="text-[9px] px-1.5 py-0.5 rounded-full bg-blue-600/20 text-blue-300 border border-blue-500/30">
                                  {tool}
                                </span>
                              ))}
                            </div>
                          )}
                        </div>
                        <p className="text-gray-200 text-xs whitespace-pre-wrap leading-relaxed">
                          {typeof msg.content === 'object' 
                            ? JSON.stringify(msg.content, null, 2) 
                            : msg.content}
                        </p>
                        {msg.toolResults && Object.keys(msg.toolResults).length > 0 && (
                          <div className="mt-2 p-2 bg-gray-900/50 rounded border border-gray-700">
                            <p className="text-[9px] text-gray-400 mb-1">Tool Results:</p>
                            {Object.entries(msg.toolResults).map(([tool, result], idx) => (
                              <div key={idx} className="text-[9px] text-green-400 font-mono truncate">
                                {tool}: {typeof result === 'string' ? result.substring(0, 60) : JSON.stringify(result).substring(0, 60)}...
                              </div>
                            ))}
                          </div>
                        )}
                        <span className="text-[9px] text-gray-500 mt-1 block">{msg.timestamp}</span>
                      </div>
                    </div>
                  ) : msg.type === 'system' ? (
                    <div className="w-full">
                      <div className="bg-gray-800/50 rounded-lg p-2 text-center border border-gray-700">
                        <p className="text-[10px] text-gray-400">{msg.content}</p>
                      </div>
                    </div>
                  ) : msg.type === 'result' ? (
                    <div className="w-full">
                      <div className="bg-gradient-to-br from-green-900/30 to-green-800/20 rounded-lg p-3 border border-green-700/50">
                        <div className="flex items-center gap-2 mb-2">
                          <div className="p-1 rounded bg-green-600">
                            <FaRobot className="text-white text-[9px]" />
                          </div>
                          <span className="text-[10px] font-bold text-green-400">Final Result</span>
                        </div>
                        <p className="text-gray-200 text-xs whitespace-pre-wrap leading-relaxed">
                          {typeof msg.content === 'object' 
                            ? JSON.stringify(msg.content, null, 2) 
                            : msg.content}
                        </p>
                        <span className="text-[9px] text-gray-500 mt-1 block">{msg.timestamp}</span>
                      </div>
                    </div>
                  ) : (
                    <div className="w-full">
                      <div className="bg-red-900/30 rounded-lg p-2 border border-red-700/50">
                        <p className="text-[10px] text-red-400">{msg.content}</p>
                      </div>
                    </div>
                  )}
                </motion.div>
              ))}
            </AnimatePresence>
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="p-3 border-t border-gray-800 bg-gray-900">
            <form onSubmit={handleSendMessage} className="flex gap-2">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                placeholder="Ask the workflow..."
                disabled={isExecuting}
                className="flex-1 px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white text-xs placeholder-gray-500 focus:border-purple-500 focus:ring-2 focus:ring-purple-500/30 focus:outline-none disabled:opacity-50"
              />
              <button
                type="submit"
                disabled={isExecuting || !inputMessage.trim()}
                className="px-4 py-2 rounded-lg bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white text-xs font-semibold transition-all flex items-center gap-1.5 shadow-lg shadow-purple-500/30 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isExecuting ? (
                  <>
                    <FaSpinner className="animate-spin text-xs" />
                    <span className="hidden sm:inline">Running...</span>
                  </>
                ) : (
                  <>
                    <FaPaperPlane className="text-xs" />
                    <span className="hidden sm:inline">Send</span>
                  </>
                )}
              </button>
            </form>
            <p className="text-[9px] text-gray-500 mt-1.5 text-center">
              Watch nodes communicate on the left
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default WorkflowChat;
