import React, { useEffect } from 'react';
import { motion } from 'framer-motion';
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  MarkerType,
  Position,
  Handle,
  useNodesState,
  useEdgesState,
} from 'reactflow';
import 'reactflow/dist/style.css';
import {
  FaTimes,
  FaRobot,
  FaTools,
  FaProjectDiagram,
  FaPlay,
  FaSpinner,
  FaCheckCircle,
  FaClock
} from 'react-icons/fa';
import MetricsDisplay from './MetricsDisplay';

// Read-only Blueprint Agent Node - Shows execution status
const BlueprintAgentNode = ({ data }) => {
  const { isActive, isCompleted, isPending } = data;
  
  return (
    <motion.div
      initial={{ scale: 0.9, opacity: 0 }}
      animate={{ 
        scale: isActive ? 1.08 : 1,
        opacity: 1,
      }}
      className={`px-6 py-4 rounded-xl shadow-2xl border-2 transition-all min-w-[220px] relative ${
        isActive ? 'bg-gradient-to-br from-purple-600 to-pink-600 border-white shadow-purple-500/50 animate-pulse' :
        isCompleted ? 'bg-gradient-to-br from-green-600 to-green-700 border-green-400 shadow-green-500/30' :
        'bg-gradient-to-br from-gray-800 to-gray-900 border-gray-700'
      }`}
    >
      {/* Connection Handles */}
      <Handle type="target" position={Position.Top} className="w-3 h-3 !bg-purple-500 !border-2 !border-white" />
      <Handle type="target" position={Position.Left} className="w-3 h-3 !bg-purple-500 !border-2 !border-white" />
      
      {/* Status Icon */}
      <div className="absolute -top-3 -right-3">
        {isActive && (
          <div className="p-2 rounded-full bg-purple-500 shadow-lg">
            <FaSpinner className="text-white text-sm animate-spin" />
          </div>
        )}
        {isCompleted && (
          <div className="p-2 rounded-full bg-green-500 shadow-lg">
            <FaCheckCircle className="text-white text-sm" />
          </div>
        )}
        {isPending && (
          <div className="p-2 rounded-full bg-gray-600 shadow-lg">
            <FaClock className="text-gray-300 text-sm" />
          </div>
        )}
      </div>
      
      <div className="flex items-start gap-3">
        <div className={`p-2 rounded-lg ${isActive ? 'bg-white/20' : isCompleted ? 'bg-green-800' : 'bg-purple-600'}`}>
          <FaRobot className={`text-lg ${isActive ? 'text-white animate-bounce' : 'text-white'}`} />
        </div>
        <div className="flex-1">
          <div className="font-bold text-white text-sm">{data.label}</div>
          <div className="text-xs text-gray-200 mt-1 opacity-80">{data.agentId}</div>
          <div className="text-xs mt-2 text-white/80">
            {isActive && '⚡ Processing...'}
            {isCompleted && '✓ Completed'}
            {isPending && '⏳ Waiting'}
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
  blueprintAgent: BlueprintAgentNode,
};

const WorkflowBlueprint = ({ workflow, agents, onClose, isExecuting, executionState }) => {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  // Initialize workflow visualization
  useEffect(() => {
    if (workflow && workflow.nodes) {
      const flowNodes = workflow.nodes.map((node, index) => {
        const agent = agents.find((a) => a.id === node.agent_ref);
        const executionStatus = executionState?.[node.id] || {};
        
        return {
          id: node.id,
          type: 'blueprintAgent',
          position: { x: 150 + (index % 3) * 300, y: 100 + Math.floor(index / 3) * 250 },
          data: {
            label: agent?.name || node.agent_ref,
            agentId: node.agent_ref,
            task: node.task,
            tools: node.tools || [],
            isActive: executionStatus.isActive || false,
            isCompleted: executionStatus.isCompleted || false,
            isPending: !executionStatus.isActive && !executionStatus.isCompleted,
          },
        };
      });

      const flowEdges = [];
      workflow.nodes.forEach((node) => {
        if (node.dependencies && node.dependencies.length > 0) {
          node.dependencies.forEach((depId) => {
            const sourceStatus = executionState?.[depId] || {};
            const targetStatus = executionState?.[node.id] || {};
            
            const isActiveEdge = sourceStatus.isCompleted && targetStatus.isActive;
            const isCompletedEdge = sourceStatus.isCompleted && targetStatus.isCompleted;
            
            flowEdges.push({
              id: `e${depId}-${node.id}`,
              source: depId,
              target: node.id,
              animated: isActiveEdge,
              style: { 
                stroke: isCompletedEdge ? '#10b981' : isActiveEdge ? '#a855f7' : '#6b7280',
                strokeWidth: isActiveEdge ? 4 : isCompletedEdge ? 3 : 2,
              },
              markerEnd: { 
                type: MarkerType.ArrowClosed, 
                color: isCompletedEdge ? '#10b981' : isActiveEdge ? '#a855f7' : '#6b7280',
                width: 20, 
                height: 20 
              },
              type: 'smoothstep',
              label: isActiveEdge ? '📡 Transferring' : undefined,
              labelStyle: isActiveEdge ? { 
                fill: '#a855f7', 
                fontWeight: 600,
                fontSize: 11,
              } : undefined,
            });
          });
        }
      });

      setNodes(flowNodes);
      setEdges(flowEdges);
    }
  }, [workflow, agents, executionState, setNodes, setEdges]);

  return (
    <div className="modal-overlay" onClick={onClose}>
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="bg-gray-950 rounded-2xl w-[90vw] h-[85vh] flex flex-col shadow-2xl overflow-hidden border-2 border-gray-800"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="p-4 border-b border-gray-800 bg-gray-900 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-lg bg-gradient-to-br from-purple-600 to-pink-600 shadow-lg shadow-purple-500/30">
              <FaProjectDiagram className="text-white text-lg" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-white">Workflow Blueprint</h3>
              <p className="text-sm text-gray-400">{workflow.name}</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            {isExecuting && (
              <div className="flex items-center gap-2 px-4 py-2 bg-purple-600/20 rounded-lg border border-purple-500/30">
                <FaSpinner className="animate-spin text-purple-400" />
                <span className="text-sm text-purple-300 font-semibold">Executing...</span>
              </div>
            )}
            <button 
              onClick={onClose} 
              className="p-2.5 rounded-lg bg-gray-800 hover:bg-gray-700 text-gray-300 transition-colors border border-gray-700"
            >
              <FaTimes className="text-lg" />
            </button>
          </div>
        </div>

        {/* Workflow Info */}
        <div className="px-6 py-3 bg-gray-900/50 border-b border-gray-800">
          <div className="flex items-center gap-6 text-xs">
            <div className="flex items-center gap-2">
              <span className="text-gray-400">Type:</span>
              <span className="px-3 py-1 bg-purple-600/20 text-purple-300 rounded-full font-medium capitalize">
                {workflow.type || 'sequence'}
              </span>
            </div>
            <div className="flex items-center gap-2">
              <FaRobot className="text-purple-400" />
              <span className="text-white font-semibold">{workflow.nodes?.length || 0}</span>
              <span className="text-gray-400">Agents</span>
            </div>
            {workflow.description && (
              <div className="flex items-center gap-2 text-gray-400 flex-1">
                <span>•</span>
                <span className="truncate">{workflow.description}</span>
              </div>
            )}
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
            <Background 
              color="#1f2937" 
              gap={16} 
              size={1}
              variant="dots"
              style={{ backgroundColor: 'transparent' }}
            />
            <Controls className="!bg-gray-800 !border-gray-700 !rounded-lg !shadow-xl [&>button]:!bg-gray-700 [&>button]:!border-gray-600 [&>button]:!text-gray-200 [&>button:hover]:!bg-gray-600" />
            <MiniMap
              className="!bg-gray-800 !border-gray-700 !rounded-lg !shadow-xl"
              nodeColor={(node) => {
                if (node.data.isActive) return '#a855f7';
                if (node.data.isCompleted) return '#10b981';
                return '#6b7280';
              }}
              maskColor="rgba(17, 24, 39, 0.8)"
            />
          </ReactFlow>
        </div>

        {/* Metrics Display - Show after execution completes */}
        {!isExecuting && executionState?._metrics && (
          <div className="px-6 py-4 bg-gray-900 border-t border-gray-800 max-h-96 overflow-y-auto">
            <MetricsDisplay 
              metrics={executionState._metrics} 
              title="Workflow Execution Metrics"
              compact={false}
            />
          </div>
        )}

        {/* Footer - Legend */}
        <div className="p-4 border-t border-gray-800 bg-gray-900 flex items-center justify-between">
          <div className="flex items-center gap-6 text-xs">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-gray-600"></div>
              <span className="text-gray-400">Pending</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-purple-500 animate-pulse"></div>
              <span className="text-gray-400">Processing</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-green-500"></div>
              <span className="text-gray-400">Completed</span>
            </div>
          </div>
          <div className="text-xs text-gray-500">
            Read-only blueprint view • Watch agents execute in real-time
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default WorkflowBlueprint;
