import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import ReactFlow, {
  Background,
  Controls,
  MarkerType,
  Position,
  Handle,
  useNodesState,
  useEdgesState,
} from 'reactflow';
import 'reactflow/dist/style.css';
import { 
  FaRobot, 
  FaTools,
  FaSpinner,
  FaCheckCircle,
  FaClock,
  FaExchangeAlt,
  FaDatabase,
  FaBrain
} from 'react-icons/fa';

// Communication Graph Agent Node - Shows message flow
const CommunicationAgentNode = ({ data }) => {
  const { isActive, isCompleted, isPending, messageCount, toolsUsed } = data;
  
  return (
    <motion.div
      initial={{ scale: 0.8, opacity: 0 }}
      animate={{ 
        scale: isActive ? 1.1 : 1,
        opacity: 1,
      }}
      transition={{ type: 'spring', stiffness: 300, damping: 20 }}
      className={`px-5 py-3 rounded-xl shadow-2xl border-2 transition-all min-w-[180px] relative ${
        isActive ? 'bg-gradient-to-br from-purple-600 to-pink-600 border-white shadow-purple-500/70' :
        isCompleted ? 'bg-gradient-to-br from-green-600 to-emerald-600 border-green-400 shadow-green-500/40' :
        'bg-gradient-to-br from-gray-700 to-gray-800 border-gray-600'
      }`}
    >
      {/* Animated pulse ring for active nodes */}
      {isActive && (
        <motion.div
          className="absolute inset-0 rounded-xl border-4 border-purple-400"
          animate={{
            scale: [1, 1.15, 1],
            opacity: [0.8, 0.3, 0.8],
          }}
          transition={{
            duration: 1.5,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
        />
      )}
      
      {/* Connection Handles */}
      <Handle type="target" position={Position.Top} className="w-3 h-3 !bg-purple-500 !border-2 !border-white" />
      <Handle type="target" position={Position.Left} className="w-3 h-3 !bg-purple-500 !border-2 !border-white" />
      
      {/* Status Badge */}
      <div className="absolute -top-2 -right-2 z-10">
        {isActive && (
          <motion.div 
            className="p-1.5 rounded-full bg-purple-500 shadow-lg"
            animate={{ rotate: 360 }}
            transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
          >
            <FaSpinner className="text-white text-xs" />
          </motion.div>
        )}
        {isCompleted && (
          <motion.div 
            className="p-1.5 rounded-full bg-green-500 shadow-lg"
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: 'spring', stiffness: 500, damping: 15 }}
          >
            <FaCheckCircle className="text-white text-xs" />
          </motion.div>
        )}
        {isPending && (
          <div className="p-1.5 rounded-full bg-gray-500 shadow-lg">
            <FaClock className="text-gray-200 text-xs" />
          </div>
        )}
      </div>
      
      <div className="flex items-start gap-2">
        <div className={`p-2 rounded-lg ${
          isActive ? 'bg-white/30 animate-pulse' : 
          isCompleted ? 'bg-emerald-700' : 
          'bg-gray-600'
        }`}>
          <FaRobot className={`text-base ${
            isActive ? 'text-white' : 'text-gray-100'
          }`} />
        </div>
        <div className="flex-1 min-w-0">
          <div className="font-bold text-white text-xs truncate">{data.label}</div>
          <div className="text-[10px] text-white/70 mt-0.5 truncate">{data.agentId}</div>
          
          {/* Status Text */}
          <div className="text-[10px] mt-1.5 font-semibold text-white/90">
            {isActive && (
              <motion.span
                className="flex items-center gap-1"
                animate={{ opacity: [1, 0.5, 1] }}
                transition={{ duration: 1, repeat: Infinity }}
              >
                <FaBrain className="inline" /> Processing
              </motion.span>
            )}
            {isCompleted && <span className="flex items-center gap-1"><FaCheckCircle className="inline" /> Done</span>}
            {isPending && <span className="flex items-center gap-1"><FaClock className="inline" /> Queued</span>}
          </div>

          {/* Message Counter */}
          {messageCount > 0 && (
            <div className="mt-1.5 text-[9px] bg-white/20 rounded px-1.5 py-0.5 inline-block">
              <FaExchangeAlt className="inline mr-1" />
              {messageCount} msg{messageCount !== 1 ? 's' : ''}
            </div>
          )}

          {/* Tools Used */}
          {toolsUsed && toolsUsed.length > 0 && (
            <div className="flex gap-1 mt-1.5 flex-wrap">
              {toolsUsed.slice(0, 2).map((tool, idx) => (
                <span key={idx} className="text-[8px] px-1.5 py-0.5 rounded-full bg-blue-500/40 text-blue-100 border border-blue-300/30">
                  <FaTools className="inline mr-0.5" />{tool}
                </span>
              ))}
              {toolsUsed.length > 2 && (
                <span className="text-[8px] px-1.5 py-0.5 rounded-full bg-blue-500/40 text-blue-100">
                  +{toolsUsed.length - 2}
                </span>
              )}
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
  commAgent: CommunicationAgentNode,
};

const WorkflowCommunicationGraph = ({ 
  workflow, 
  agents, 
  communicationLog = [],
  currentStep = null,
  isExecuting = false 
}) => {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [activeNodes, setActiveNodes] = useState(new Set());
  const [completedNodes, setCompletedNodes] = useState(new Set());
  const [nodeMessageCounts, setNodeMessageCounts] = useState({});

  // Initialize workflow visualization
  useEffect(() => {
    if (workflow && workflow.nodes) {
      const flowNodes = workflow.nodes.map((node, index) => {
        const agent = agents.find((a) => a.id === node.agent_ref);
        const messageCount = nodeMessageCounts[node.id] || 0;
        
        return {
          id: node.id,
          type: 'commAgent',
          position: { x: 100 + (index % 4) * 250, y: 80 + Math.floor(index / 4) * 200 },
          data: {
            label: agent?.name || node.agent_ref,
            agentId: node.agent_ref,
            task: node.task,
            tools: node.tools || [],
            isActive: activeNodes.has(node.id),
            isCompleted: completedNodes.has(node.id),
            isPending: !activeNodes.has(node.id) && !completedNodes.has(node.id),
            messageCount: messageCount,
            toolsUsed: node.tools || [],
          },
        };
      });

      const flowEdges = [];
      workflow.nodes.forEach((node) => {
        if (node.dependencies && node.dependencies.length > 0) {
          node.dependencies.forEach((depId) => {
            const isActiveEdge = activeNodes.has(node.id) && completedNodes.has(depId);
            const isCompletedEdge = completedNodes.has(node.id) && completedNodes.has(depId);
            
            flowEdges.push({
              id: `e${depId}-${node.id}`,
              source: depId,
              target: node.id,
              animated: isActiveEdge,
              style: { 
                stroke: isCompletedEdge ? '#10b981' : isActiveEdge ? '#a855f7' : '#4b5563',
                strokeWidth: isActiveEdge ? 5 : isCompletedEdge ? 3.5 : 2,
                strokeDasharray: isActiveEdge ? '10,5' : 'none',
              },
              markerEnd: { 
                type: MarkerType.ArrowClosed, 
                color: isCompletedEdge ? '#10b981' : isActiveEdge ? '#a855f7' : '#4b5563',
                width: isActiveEdge ? 24 : 20, 
                height: isActiveEdge ? 24 : 20 
              },
              type: 'smoothstep',
              label: isActiveEdge ? '📡 Data Flow' : undefined,
              labelStyle: isActiveEdge ? { 
                fill: '#fff', 
                fontWeight: 700,
                fontSize: 10,
                background: 'rgba(168, 85, 247, 0.9)',
                padding: '3px 8px',
                borderRadius: '8px',
              } : undefined,
              labelBgStyle: isActiveEdge ? { 
                fill: '#a855f7',
                fillOpacity: 0.9,
              } : undefined,
            });
          });
        }
      });

      setNodes(flowNodes);
      setEdges(flowEdges);
    }
  }, [workflow, agents, activeNodes, completedNodes, nodeMessageCounts, setNodes, setEdges]);

  // Process communication log to update node states
  useEffect(() => {
    if (communicationLog && communicationLog.length > 0) {
      const newActiveNodes = new Set();
      const newCompletedNodes = new Set();
      const newMessageCounts = {};

      communicationLog.forEach((logEntry, index) => {
        const nodeId = logEntry.sender || logEntry.from || logEntry.agent_id;
        
        // Count messages per node
        if (nodeId) {
          newMessageCounts[nodeId] = (newMessageCounts[nodeId] || 0) + 1;
          
          // Last message sender is active, others are completed
          if (index === communicationLog.length - 1 && isExecuting) {
            newActiveNodes.add(nodeId);
          } else {
            newCompletedNodes.add(nodeId);
          }
        }
      });

      setActiveNodes(newActiveNodes);
      setCompletedNodes(newCompletedNodes);
      setNodeMessageCounts(newMessageCounts);
    }
  }, [communicationLog, isExecuting]);

  // Update based on current step
  useEffect(() => {
    if (currentStep && !isExecuting) {
      setActiveNodes(new Set());
      setCompletedNodes((prev) => new Set([...prev, currentStep]));
    }
  }, [currentStep, isExecuting]);

  return (
    <div className="h-full w-full bg-gradient-to-br from-gray-950 via-gray-900 to-gray-950 relative">
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
        minZoom={0.5}
        maxZoom={1.5}
      >
        <Background 
          color="#374151" 
          gap={20} 
          size={1.5}
          variant="dots"
          style={{ backgroundColor: 'transparent' }}
        />
        <Controls 
          className="!bg-gray-800 !border-gray-700 !rounded-lg !shadow-xl [&>button]:!bg-gray-700 [&>button]:!border-gray-600 [&>button]:!text-gray-200 [&>button:hover]:!bg-gray-600"
          showInteractive={false}
        />
      </ReactFlow>
      
      {/* Status Overlay */}
      <AnimatePresence>
        {isExecuting && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="absolute top-4 left-1/2 transform -translate-x-1/2 bg-purple-600/90 backdrop-blur-sm rounded-lg px-4 py-2 shadow-lg border border-purple-400/50 z-10"
          >
            <div className="flex items-center gap-2">
              <FaSpinner className="animate-spin text-white" />
              <span className="text-sm font-semibold text-white">Workflow Executing...</span>
              <div className="flex gap-1 ml-2">
                <div className="w-1.5 h-1.5 bg-white rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                <div className="w-1.5 h-1.5 bg-white rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                <div className="w-1.5 h-1.5 bg-white rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Legend */}
      <div className="absolute bottom-4 left-4 bg-gray-800/90 backdrop-blur-sm rounded-lg px-4 py-2 shadow-xl border border-gray-700">
        <div className="flex items-center gap-4 text-xs">
          <div className="flex items-center gap-1.5">
            <div className="w-2.5 h-2.5 rounded-full bg-gray-500"></div>
            <span className="text-gray-300">Pending</span>
          </div>
          <div className="flex items-center gap-1.5">
            <div className="w-2.5 h-2.5 rounded-full bg-purple-500 animate-pulse"></div>
            <span className="text-gray-300">Active</span>
          </div>
          <div className="flex items-center gap-1.5">
            <div className="w-2.5 h-2.5 rounded-full bg-green-500"></div>
            <span className="text-gray-300">Completed</span>
          </div>
        </div>
      </div>

      {/* Message Count Summary */}
      {Object.keys(nodeMessageCounts).length > 0 && (
        <div className="absolute top-4 right-4 bg-gray-800/90 backdrop-blur-sm rounded-lg px-4 py-2 shadow-xl border border-gray-700">
          <div className="flex items-center gap-2 text-xs">
            <FaDatabase className="text-blue-400" />
            <span className="text-gray-300">
              {Object.values(nodeMessageCounts).reduce((a, b) => a + b, 0)} messages exchanged
            </span>
          </div>
        </div>
      )}
    </div>
  );
};

export default WorkflowCommunicationGraph;
