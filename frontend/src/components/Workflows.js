import React, { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  addEdge,
  useNodesState,
  useEdgesState,
  MarkerType,
  Handle,
  Position,
} from 'reactflow';
import 'reactflow/dist/style.css';
import {
  FaProjectDiagram,
  FaPlus,
  FaSave,
  FaPlay,
  FaTrash,
  FaEdit,
  FaTimes,
  FaRobot,
  FaTools,
  FaComments,
} from 'react-icons/fa';
import { workflowsAPI, agentsAPI, toolsAPI } from '../services/api';
import WorkflowChat from './WorkflowChat';
import WorkflowBlueprint from './WorkflowBlueprint';

// Agentic AI Agent Node with 4 handles on each side
const AgentNode = ({ data, selected }) => {
  return (
    <div className={`px-6 py-4 rounded-xl bg-gradient-to-br from-gray-800 to-gray-900 shadow-2xl border-2 transition-all ${
      selected ? 'border-purple-500 shadow-purple-500/50 scale-105' : 'border-gray-700'
    } min-w-[200px] relative`}>
      {/* LEFT SIDE - 4 Target Handles */}
      <Handle
        type="target"
        position={Position.Left}
        id="left-1"
        style={{ top: '25%' }}
        className="w-3 h-3 !bg-purple-500 !border-2 !border-gray-900 hover:!bg-purple-400 transition-colors"
      />
      <Handle
        type="target"
        position={Position.Left}
        id="left-2"
        style={{ top: '42%' }}
        className="w-3 h-3 !bg-purple-500 !border-2 !border-gray-900 hover:!bg-purple-400 transition-colors"
      />
      <Handle
        type="target"
        position={Position.Left}
        id="left-3"
        style={{ top: '58%' }}
        className="w-3 h-3 !bg-purple-500 !border-2 !border-gray-900 hover:!bg-purple-400 transition-colors"
      />
      <Handle
        type="target"
        position={Position.Left}
        id="left-4"
        style={{ top: '75%' }}
        className="w-3 h-3 !bg-purple-500 !border-2 !border-gray-900 hover:!bg-purple-400 transition-colors"
      />

      {/* TOP SIDE - 4 Handles */}
      <Handle
        type="target"
        position={Position.Top}
        id="top-1"
        style={{ left: '25%' }}
        className="w-3 h-3 !bg-purple-500 !border-2 !border-gray-900 hover:!bg-purple-400 transition-colors"
      />
      <Handle
        type="target"
        position={Position.Top}
        id="top-2"
        style={{ left: '42%' }}
        className="w-3 h-3 !bg-purple-500 !border-2 !border-gray-900 hover:!bg-purple-400 transition-colors"
      />
      <Handle
        type="target"
        position={Position.Top}
        id="top-3"
        style={{ left: '58%' }}
        className="w-3 h-3 !bg-purple-500 !border-2 !border-gray-900 hover:!bg-purple-400 transition-colors"
      />
      <Handle
        type="target"
        position={Position.Top}
        id="top-4"
        style={{ left: '75%' }}
        className="w-3 h-3 !bg-purple-500 !border-2 !border-gray-900 hover:!bg-purple-400 transition-colors"
      />
      
      {/* Node Icon and Label */}
      <div className="flex items-start gap-3">
        <div className="p-2 rounded-lg bg-purple-600 shadow-lg">
          <FaRobot className="text-white text-lg" />
        </div>
        <div className="flex-1">
          <div className="font-bold text-white text-sm">{data.label}</div>
          <div className="text-xs text-gray-400 mt-1">{data.agentId}</div>
          {data.tools && data.tools.length > 0 && (
            <div className="flex gap-1 mt-2 flex-wrap">
              {data.tools.map((tool, idx) => (
                <span key={idx} className="text-[10px] px-2 py-0.5 rounded-full bg-blue-600/30 text-blue-300 border border-blue-500/30">
                  <FaTools className="inline mr-1" />{tool}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>
      
      {/* RIGHT SIDE - 4 Source Handles */}
      <Handle
        type="source"
        position={Position.Right}
        id="right-1"
        style={{ top: '25%' }}
        className="w-3 h-3 !bg-purple-500 !border-2 !border-gray-900 hover:!bg-purple-400 transition-colors"
      />
      <Handle
        type="source"
        position={Position.Right}
        id="right-2"
        style={{ top: '42%' }}
        className="w-3 h-3 !bg-purple-500 !border-2 !border-gray-900 hover:!bg-purple-400 transition-colors"
      />
      <Handle
        type="source"
        position={Position.Right}
        id="right-3"
        style={{ top: '58%' }}
        className="w-3 h-3 !bg-purple-500 !border-2 !border-gray-900 hover:!bg-purple-400 transition-colors"
      />
      <Handle
        type="source"
        position={Position.Right}
        id="right-4"
        style={{ top: '75%' }}
        className="w-3 h-3 !bg-purple-500 !border-2 !border-gray-900 hover:!bg-purple-400 transition-colors"
      />

      {/* BOTTOM SIDE - 4 Source Handles */}
      <Handle
        type="source"
        position={Position.Bottom}
        id="bottom-1"
        style={{ left: '25%' }}
        className="w-3 h-3 !bg-purple-500 !border-2 !border-gray-900 hover:!bg-purple-400 transition-colors"
      />
      <Handle
        type="source"
        position={Position.Bottom}
        id="bottom-2"
        style={{ left: '42%' }}
        className="w-3 h-3 !bg-purple-500 !border-2 !border-gray-900 hover:!bg-purple-400 transition-colors"
      />
      <Handle
        type="source"
        position={Position.Bottom}
        id="bottom-3"
        style={{ left: '58%' }}
        className="w-3 h-3 !bg-purple-500 !border-2 !border-gray-900 hover:!bg-purple-400 transition-colors"
      />
      <Handle
        type="source"
        position={Position.Bottom}
        id="bottom-4"
        style={{ left: '75%' }}
        className="w-3 h-3 !bg-purple-500 !border-2 !border-gray-900 hover:!bg-purple-400 transition-colors"
      />
    </div>
  );
};

// Dark-themed Agent Drag Card
const AgentDragItem = ({ agent }) => {
  const onDragStart = (event) => {
    event.dataTransfer.effectAllowed = 'copy';
    event.dataTransfer.setData('application/reactflow', JSON.stringify({ type: 'agent', agent }));
  };

  return (
    <div
      draggable
      onDragStart={onDragStart}
      className="p-3 bg-gradient-to-br from-gray-800 to-gray-900 rounded-lg border-2 border-gray-700 hover:border-purple-500 cursor-grab hover:shadow-lg hover:shadow-purple-500/30 transition-all flex items-center gap-3"
    >
      <div className="p-2 rounded-lg bg-purple-600">
        <FaRobot className="text-white text-base" />
      </div>
      <div className="flex-1">
        <div className="text-sm font-semibold text-white">{agent.name}</div>
        <div className="text-xs text-gray-400">{agent.id}</div>
      </div>
    </div>
  );
};

const ToolDragItem = ({ tool }) => {
  const onDragStart = (event) => {
    event.dataTransfer.effectAllowed = 'copy';
    event.dataTransfer.setData('application/reactflow', JSON.stringify({ type: 'tool', tool }));
  };

  return (
    <div
      draggable
      onDragStart={onDragStart}
      className="p-3 bg-gradient-to-br from-gray-800 to-gray-900 rounded-lg border-2 border-gray-700 hover:border-blue-500 cursor-grab hover:shadow-lg hover:shadow-blue-500/30 transition-all flex items-center gap-3"
    >
      <div className="p-2 rounded-lg bg-blue-600">
        <FaTools className="text-white text-base" />
      </div>
      <div className="flex-1">
        <div className="text-sm font-semibold text-white">{tool.name}</div>
        <div className="text-xs text-gray-400">{tool.type}</div>
      </div>
    </div>
  );
};

const nodeTypes = {
  agentNode: AgentNode,
};

const WorkflowCanvas = ({ workflow, agents, tools, onSave, onClose }) => {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [workflowName, setWorkflowName] = useState(workflow?.name || '');
  const [workflowDescription, setWorkflowDescription] = useState(workflow?.description || '');
  const [reactFlowInstance, setReactFlowInstance] = useState(null);

  const onNodeClick = useCallback((event, node) => {
    console.log('Node clicked:', node);
  }, []);

  useEffect(() => {
    if (workflow && workflow.nodes) {
      // Convert workflow nodes to ReactFlow nodes
      const flowNodes = workflow.nodes.map((node, index) => {
        const agent = agents.find((a) => a.id === node.agent_ref);
        return {
          id: node.id,
          type: 'agentNode',
          position: { x: 150 + (index % 3) * 300, y: 100 + Math.floor(index / 3) * 250 },
          data: {
            label: agent?.name || node.agent_ref,
            agentId: node.agent_ref,
            task: node.task,
            tools: node.tools || [],
          },
        };
      });

      // Convert workflow connections to edges based on dependencies
      const flowEdges = [];
      workflow.nodes.forEach((node) => {
        if (node.dependencies && node.dependencies.length > 0) {
          node.dependencies.forEach((depId) => {
            flowEdges.push({
              id: `e${depId}-${node.id}`,
              source: depId,
              target: node.id,
              animated: true,
              style: { stroke: '#a855f7', strokeWidth: 2.5 },
              markerEnd: { type: MarkerType.ArrowClosed, color: '#a855f7', width: 20, height: 20 },
              type: 'smoothstep',
            });
          });
        }
      });

      setNodes(flowNodes);
      setEdges(flowEdges);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [workflow, agents]);

  const onConnect = useCallback(
    (params) =>
      setEdges((eds) =>
        addEdge(
          {
            ...params,
            animated: true,
            style: { stroke: '#a855f7', strokeWidth: 2.5 },
            markerEnd: { type: MarkerType.ArrowClosed, color: '#a855f7', width: 20, height: 20 },
            type: 'smoothstep',
          },
          eds
        )
      ),
    [setEdges]
  );

  const onDragOver = useCallback((event) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'copy';
  }, []);

  const onDrop = useCallback(
    (event) => {
      event.preventDefault();

      if (!reactFlowInstance) return;

      const data = event.dataTransfer.getData('application/reactflow');
      if (!data) return;

      const { type, agent, tool } = JSON.parse(data);
      const position = reactFlowInstance.screenToFlowPosition({
        x: event.clientX,
        y: event.clientY,
      });
      
      if (type === 'agent') {
        // Create a new agent node when dropped
        const newNode = {
          id: `node_${Date.now()}`,
          type: 'agentNode',
          position,
          data: {
            label: agent.name,
            agentId: agent.id,
            task: 'Enter task description...',
            tools: [],
          },
        };
        setNodes((nds) => [...nds, newNode]);
      } else if (type === 'tool') {
        // Find node at drop position and add tool to it
        let droppedOnNode = nodes.find((node) => {
          const nodeElement = document.querySelector(`[data-id="${node.id}"]`);
          if (!nodeElement) return false;
          const rect = nodeElement.getBoundingClientRect();
          return (
            event.clientX >= rect.left &&
            event.clientX <= rect.right &&
            event.clientY >= rect.top &&
            event.clientY <= rect.bottom
          );
        });

        // Fallback: if DOM-based detection fails (React Flow DOM may vary),
        // try flow-coordinate based detection using node positions.
        if (!droppedOnNode && reactFlowInstance) {
          try {
            const flowPos = reactFlowInstance.screenToFlowPosition({ x: event.clientX, y: event.clientY });
            // assume a default node size for hit testing
            const NODE_WIDTH = 220;
            const NODE_HEIGHT = 140;
            droppedOnNode = nodes.find((node) => {
              const nx = node.position?.x || 0;
              const ny = node.position?.y || 0;
              return (
                flowPos.x >= nx && flowPos.x <= nx + NODE_WIDTH &&
                flowPos.y >= ny && flowPos.y <= ny + NODE_HEIGHT
              );
            });
          } catch (err) {
            console.warn('Fallback node detection failed:', err);
          }
        }

        if (droppedOnNode) {
          setNodes((nds) =>
            nds.map((node) => {
              if (node.id === droppedOnNode.id) {
                const currentTools = node.data.tools || [];
                if (!currentTools.includes(tool.id)) {
                  return {
                    ...node,
                    data: {
                      ...node.data,
                      tools: [...currentTools, tool.id],
                    },
                  };
                }
              }
              return node;
            })
          );
        }
      }
    },
    [reactFlowInstance, nodes, setNodes]
  );

  const handleSave = () => {
    if (!workflowName) {
      alert('Please enter a workflow name');
      return;
    }

    // Build dependency map from edges
    const dependencyMap = {};
    edges.forEach((edge) => {
      if (!dependencyMap[edge.target]) {
        dependencyMap[edge.target] = [];
      }
      dependencyMap[edge.target].push(edge.source);
    });

    // Convert ReactFlow nodes back to workflow format
    const workflowNodes = nodes.map((node) => ({
      id: node.id,
      agent_ref: node.data.agentId,
      task: node.data.task,
      tools: node.data.tools || [],
      dependencies: dependencyMap[node.id] || [],
    }));

    // Determine workflow type based on structure
    const workflowType = dependencyMap && Object.keys(dependencyMap).length > 0 ? 'dag' : 'sequence';

    const workflowData = {
      id: workflow?.id || workflowName.toLowerCase().replace(/\s+/g, '_'),
      name: workflowName,
      description: workflowDescription,
      type: workflowType,
      nodes: workflowNodes,
    };

    onSave(workflowData);
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="bg-gray-950 rounded-2xl w-[95vw] h-[90vh] flex shadow-2xl overflow-hidden border-2 border-gray-800"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Dark Sidebar with Agents & Tools */}
        <div className="w-72 bg-gradient-to-b from-gray-900 to-gray-950 flex flex-col border-r border-gray-800">
          <div className="p-4 border-b border-gray-800 bg-gray-900/50">
            <h3 className="font-bold text-white mb-1 flex items-center gap-2">
              <FaProjectDiagram className="text-purple-500" />
              Agentic Components
            </h3>
            <p className="text-xs text-gray-400">Drag & drop to build workflow</p>
          </div>

          <div className="flex-1 overflow-y-auto p-4 space-y-6">
            {/* Agents Section */}
            <div>
              <h4 className="text-xs font-bold text-gray-300 uppercase mb-3 flex items-center gap-2">
                <FaRobot className="text-purple-500" />
                AI Agents
              </h4>
              <div className="space-y-2">
                {agents.map((agent) => (
                  <AgentDragItem key={agent.id} agent={agent} />
                ))}
                {agents.length === 0 && (
                  <p className="text-xs text-gray-500 text-center py-4">No agents available</p>
                )}
              </div>
            </div>

            {/* Tools Section */}
            <div>
              <h4 className="text-xs font-bold text-gray-300 uppercase mb-3 flex items-center gap-2">
                <FaTools className="text-blue-500" />
                Agent Tools
              </h4>
              <div className="space-y-2">
                {tools.map((tool) => (
                  <ToolDragItem key={tool.id} tool={tool} />
                ))}
                {tools.length === 0 && (
                  <p className="text-xs text-gray-500 text-center py-4">No tools available</p>
                )}
              </div>
            </div>
          </div>

          {/* Dark Instructions Footer */}
          <div className="p-4 border-t border-gray-800 bg-gray-900/70 text-xs text-gray-400 space-y-1">
            <p className="font-semibold text-gray-300 mb-2">Workflow Building Guide:</p>
            <p>• Drag agents from sidebar to canvas</p>
            <p>• Drag tools onto agents to equip them</p>
            <p>• Use 4 connection handles on each side to create arrows</p>
            <p>• Workflow execution determined by dependencies</p>
          </div>
        </div>

        {/* Main Canvas Area */}
        <div className="flex-1 flex flex-col">
          {/* Dark Header */}
          <div className="p-4 border-b border-gray-800 bg-gray-900 flex items-center justify-between">
            <div className="flex items-center gap-3 flex-1">
              <div className="p-2.5 rounded-lg bg-gradient-to-br from-purple-600 to-pink-600 shadow-lg shadow-purple-500/30">
                <FaProjectDiagram className="text-white text-lg" />
              </div>
              <div className="flex-1 grid grid-cols-2 gap-3">
                <input
                  type="text"
                  className="px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-purple-500 focus:ring-2 focus:ring-purple-500/30 focus:outline-none text-sm"
                  placeholder="Workflow Name"
                  value={workflowName}
                  onChange={(e) => setWorkflowName(e.target.value)}
                />
                <input
                  type="text"
                  className="px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-purple-500 focus:ring-2 focus:ring-purple-500/30 focus:outline-none text-sm"
                  placeholder="Description"
                  value={workflowDescription}
                  onChange={(e) => setWorkflowDescription(e.target.value)}
                />
              </div>
            </div>
            <div className="flex gap-3">
              <button 
                onClick={handleSave} 
                className="px-5 py-2.5 rounded-lg bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-semibold transition-all flex items-center gap-2 text-sm shadow-lg shadow-purple-500/30"
              >
                <FaSave /> Save Workflow
              </button>
              <button 
                onClick={onClose} 
                className="p-2.5 rounded-lg bg-gray-800 hover:bg-gray-700 text-gray-300 transition-colors border border-gray-700"
              >
                <FaTimes className="text-lg" />
              </button>
            </div>
          </div>

          {/* Dark Canvas with Grid Pattern */}
          <div className="flex-1 relative bg-gradient-to-br from-gray-950 via-gray-900 to-gray-950">
            <ReactFlow
              nodes={nodes}
              edges={edges}
              onNodesChange={onNodesChange}
              onEdgesChange={onEdgesChange}
              onConnect={onConnect}
              onNodeClick={onNodeClick}
              onInit={setReactFlowInstance}
              onDrop={onDrop}
              onDragOver={onDragOver}
              nodeTypes={nodeTypes}
              fitView
              className="bg-transparent"
              connectionLineStyle={{ 
                stroke: '#a855f7', 
                strokeWidth: 2.5,
                strokeDasharray: '5,5'
              }}
              connectionLineType="smoothstep"
              defaultEdgeOptions={{
                animated: true,
                style: { 
                  stroke: '#a855f7', 
                  strokeWidth: 2.5
                },
                markerEnd: { 
                  type: MarkerType.ArrowClosed, 
                  color: '#a855f7', 
                  width: 20, 
                  height: 20 
                },
                type: 'smoothstep',
              }}
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
                nodeColor="#8b5cf6"
                maskColor="rgba(17, 24, 39, 0.8)"
              />
            </ReactFlow>
            
            {/* Empty State */}
            {nodes.length === 0 && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-center pointer-events-none"
              >
                <div className="bg-gray-800/90 backdrop-blur-sm rounded-2xl p-8 shadow-2xl border-2 border-gray-700">
                  <FaProjectDiagram className="text-6xl text-purple-500 mx-auto mb-4" />
                  <h3 className="text-xl font-bold text-white mb-2">Build Your Agentic Workflow</h3>
                  <p className="text-sm text-gray-400">Drag agents from the sidebar to start designing</p>
                </div>
              </motion.div>
            )}
          </div>

          {/* Dark Footer with Stats */}
          <div className="p-3 border-t border-gray-800 bg-gray-900 flex items-center justify-between text-xs">
            <div className="flex items-center gap-6 text-gray-400">
              <span className="flex items-center gap-2">
                <FaRobot className="text-purple-500" />
                <span className="font-semibold text-white">{nodes.length}</span> Agents
              </span>
              <span className="flex items-center gap-2">
                <span className="text-purple-500">→</span>
                <span className="font-semibold text-white">{edges.length}</span> Connections
              </span>
            </div>
            <div className="text-gray-500">
              Workflow executes based on agent dependencies
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

const WorkflowCard = ({ workflow, onEdit, onDelete, onRun, onChat, onView }) => {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      className="card p-6 cursor-pointer"
      onClick={onView}
    >
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className="p-3 rounded-lg bg-gradient-to-br from-workflow-primary to-workflow-secondary">
            <FaProjectDiagram className="text-2xl" />
          </div>
          <div>
            <h3 className="text-xl font-bold">{workflow.name}</h3>
            <p className="text-sm text-gray-400">{workflow.id}</p>
          </div>
        </div>
        <div className="flex gap-2" onClick={(e) => e.stopPropagation()}>
          <button
            onClick={() => onRun(workflow)}
            className="p-2 rounded-lg bg-dark-bg hover:bg-green-500 transition-colors"
            title="Run Workflow (Blueprint View)"
          >
            <FaPlay />
          </button>
          <button
            onClick={() => onChat(workflow)}
            className="p-2 rounded-lg bg-dark-bg hover:bg-blue-500 transition-colors"
            title="Chat with Workflow"
          >
            <FaComments />
          </button>
          <button
            onClick={() => onEdit(workflow)}
            className="p-2 rounded-lg bg-dark-bg hover:bg-workflow-primary transition-colors"
            title="Edit Workflow"
          >
            <FaEdit />
          </button>
          <button
            onClick={() => onDelete(workflow.id)}
            className="p-2 rounded-lg bg-dark-bg hover:bg-red-500 transition-colors"
            title="Delete Workflow"
          >
            <FaTrash />
          </button>
        </div>
      </div>

      <div className="space-y-2 text-sm">
        <div className="flex justify-between">
          <span className="text-gray-400">Type:</span>
          <span className="font-medium capitalize">{workflow.type}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-400">Nodes:</span>
          <span className="font-medium">{workflow.nodes?.length || 0}</span>
        </div>
        {workflow.description && (
          <div className="mt-2 pt-2 border-t border-dark-border">
            <p className="text-xs text-gray-400">{workflow.description}</p>
          </div>
        )}
      </div>
    </motion.div>
  );
};

const Workflows = ({ onViewSolution }) => {
  const [workflows, setWorkflows] = useState([]);
  const [agents, setAgents] = useState([]);
  const [tools, setTools] = useState([]);
  const [showCanvas, setShowCanvas] = useState(false);
  const [editingWorkflow, setEditingWorkflow] = useState(null);
  const [loading, setLoading] = useState(true);
  const [chatWorkflow, setChatWorkflow] = useState(null);
  const [blueprintWorkflow, setBlueprintWorkflow] = useState(null);
  const [isExecuting, setIsExecuting] = useState(false);
  const [executionState, setExecutionState] = useState({});

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [workflowsRes, agentsRes, toolsRes] = await Promise.all([
        workflowsAPI.getAll(),
        agentsAPI.getAll(),
        toolsAPI.getAll(),
      ]);

      // Debugging logs to help diagnose why tools may not appear in the UI
      console.log('fetchData: workflows response:', workflowsRes);
      console.log('fetchData: agents response:', agentsRes);
      console.log('fetchData: tools response:', toolsRes);

      setWorkflows(workflowsRes.data);
      setAgents(agentsRes.data);
      setTools(toolsRes.data);

      console.log('fetchData: set tools count ->', Array.isArray(toolsRes.data) ? toolsRes.data.length : typeof toolsRes.data);
    } catch (error) {
      console.error('Error fetching data:', error);
      // Ensure UI gets cleared so empty-state messages show and debugging is easier
      setWorkflows([]);
      setAgents([]);
      setTools([]);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async (workflowData) => {
    try {
      console.log('Saving workflow:', workflowData);
      if (editingWorkflow) {
        const response = await workflowsAPI.update(workflowData.id, workflowData);
        console.log('Update response:', response);
      } else {
        const response = await workflowsAPI.create(workflowData);
        console.log('Create response:', response);
      }
      await fetchData();
      setShowCanvas(false);
      setEditingWorkflow(null);
      alert('✅ Workflow saved successfully!');
    } catch (error) {
      console.error('Error saving workflow:', error);
      console.error('Error details:', error.response?.data);
      alert('❌ Error saving workflow: ' + (error.response?.data?.detail || error.message));
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this workflow?')) {
      try {
        await workflowsAPI.delete(id);
        await fetchData();
      } catch (error) {
        console.error('Error deleting workflow:', error);
        alert('Error deleting workflow: ' + (error.response?.data?.detail || error.message));
      }
    }
  };

  const handleRun = async (workflow) => {
    // Open blueprint view and execute workflow
    setBlueprintWorkflow(workflow);
    setIsExecuting(true);
    setExecutionState({});

    try {
      // Execute workflow
      const response = await workflowsAPI.run(workflow.id, { query: 'Run workflow' });
      
      // Process execution to update blueprint in real-time
      const communicationLog = response.data?.meta?.communication_log || [];
      const nodes = workflow.nodes || [];
      
      // Simulate step-by-step execution for visualization
      for (let i = 0; i < nodes.length; i++) {
        const node = nodes[i];
        
        // Mark as active
        setExecutionState(prev => ({
          ...prev,
          [node.id]: { isActive: true, isCompleted: false }
        }));
        
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Mark as completed
        setExecutionState(prev => ({
          ...prev,
          [node.id]: { isActive: false, isCompleted: true }
        }));
      }
      
    } catch (error) {
      console.error('Workflow execution error:', error);
      alert('Error running workflow: ' + (error.response?.data?.detail || error.message));
    } finally {
      setIsExecuting(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-workflow-primary"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold mb-2">Workflows</h1>
          <p className="text-gray-400">Design and orchestrate AI workflows</p>
        </div>
        <button
          onClick={() => {
            setEditingWorkflow(null);
            setShowCanvas(true);
          }}
          className="btn-workflow flex items-center gap-2"
        >
          <FaPlus /> Create Workflow
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {workflows.map((workflow) => (
          <WorkflowCard
            key={workflow.id}
            workflow={workflow}
            onEdit={(wf) => {
              setEditingWorkflow(wf);
              setShowCanvas(true);
            }}
            onDelete={handleDelete}
            onRun={handleRun}
            onChat={(wf) => setChatWorkflow(wf)}
            onView={() => onViewSolution && onViewSolution(workflow, null)}
          />
        ))}
      </div>

      {workflows.length === 0 && (
        <div className="card p-12 text-center">
          <FaProjectDiagram className="text-6xl text-gray-600 mx-auto mb-4" />
          <h3 className="text-xl font-bold mb-2">No workflows yet</h3>
          <p className="text-gray-400 mb-4">Create your first workflow to get started</p>
          <button
            onClick={() => setShowCanvas(true)}
            className="btn-workflow flex items-center gap-2 mx-auto"
          >
            <FaPlus /> Create First Workflow
          </button>
        </div>
      )}

      <AnimatePresence>
        {showCanvas && (
          <WorkflowCanvas
            workflow={editingWorkflow}
            agents={agents}
            tools={tools}
            onSave={handleSave}
            onClose={() => {
              setShowCanvas(false);
              setEditingWorkflow(null);
            }}
          />
        )}
        {chatWorkflow && (
          <WorkflowChat
            workflow={chatWorkflow}
            agents={agents}
            onClose={() => setChatWorkflow(null)}
          />
        )}
        {blueprintWorkflow && (
          <WorkflowBlueprint
            workflow={blueprintWorkflow}
            agents={agents}
            onClose={() => {
              setBlueprintWorkflow(null);
              setExecutionState({});
            }}
            isExecuting={isExecuting}
            executionState={executionState}
          />
        )}
      </AnimatePresence>
    </div>
  );
};

export default Workflows;

