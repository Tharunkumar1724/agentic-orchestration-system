import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import ReactFlow, { Background, Controls, MarkerType, Position, Handle } from 'reactflow';
import 'reactflow/dist/style.css';
import { FaLightbulb, FaTimes, FaCheckCircle, FaExclamationCircle, FaClock, FaChevronDown, FaChevronUp, FaRobot, FaPlay, FaProjectDiagram, FaComments } from 'react-icons/fa';
import { solutionsAPI, workflowsAPI, agentsAPI } from '../services/api';
import WorkflowBlueprint from './WorkflowBlueprint';
import WorkflowChat from './WorkflowChat';
import InteractiveSolutionChat from './InteractiveSolutionChat';

// Animated Node for workflow visualization
const AnimatedWorkflowNode = ({ data }) => {
  const isActive = data.isActive;
  const isCompleted = data.isCompleted;
  
  return (
    <motion.div
      initial={{ scale: 0.8, opacity: 0 }}
      animate={{ 
        scale: isActive ? 1.1 : 1, 
        opacity: 1,
      }}
      className={`px-4 py-3 shadow-2xl rounded-xl bg-gradient-to-br min-w-[180px] border-2 ${
        isActive ? 'from-agent-primary to-agent-secondary border-white shadow-agent-primary' :
        isCompleted ? 'from-green-600 to-green-700 border-green-400' :
        'from-dark-card to-dark-bg border-gray-600'
      }`}
    >
      <Handle
        type="target"
        position={Position.Top}
        className="w-3 h-3 !bg-white border-2 border-agent-primary"
      />
      <div className="flex items-center gap-2 mb-2">
        <div className={`p-2 rounded-lg ${isActive ? 'animate-pulse' : ''}`}>
          <FaRobot className="text-white text-sm" />
        </div>
        <div className="font-bold text-sm text-white">{data.label}</div>
      </div>
      {data.status && (
        <div className="text-xs text-gray-200 mt-1">
          {isActive && '⚡ Processing...'}
          {isCompleted && '✓ Completed'}
          {!isActive && !isCompleted && '⏳ Pending'}
        </div>
      )}
      <Handle
        type="source"
        position={Position.Bottom}
        className="w-3 h-3 !bg-white border-2 border-agent-secondary"
      />
    </motion.div>
  );
};

const nodeTypes = {
  animated: AnimatedWorkflowNode,
};

const MessageFlow = ({ steps }) => {
  return (
    <div className="space-y-4">
      {steps && steps.map((step, index) => (
        <motion.div
          key={index}
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: index * 0.1 }}
          className="relative"
        >
          {/* Connection line */}
          {index < steps.length - 1 && (
            <div className="absolute left-6 top-12 w-0.5 h-12 bg-gradient-to-b from-solution-primary to-transparent"></div>
          )}
          
          <div className="flex items-start gap-4">
            <div className="p-3 rounded-full bg-gradient-to-br from-solution-primary to-solution-secondary shadow-lg flex-shrink-0">
              <span className="text-sm font-bold">{index + 1}</span>
            </div>
            <div className="flex-1 card p-4">
              <div className="flex items-center justify-between mb-2">
                <h4 className="font-bold text-solution-primary">{step.agent || step.node_id}</h4>
                <span className="text-xs text-gray-400">{step.timestamp || 'N/A'}</span>
              </div>
              {step.task && (
                <p className="text-sm text-gray-400 mb-2">{step.task}</p>
              )}
              {step.output && (
                <div className="mt-2 p-3 bg-dark-bg rounded-lg">
                  <p className="text-sm font-mono text-gray-300 whitespace-pre-wrap">{step.output}</p>
                </div>
              )}
              {step.tool_calls && step.tool_calls.length > 0 && (
                <div className="mt-2 flex flex-wrap gap-2">
                  {step.tool_calls.map((tool, i) => (
                    <span key={i} className="px-2 py-1 text-xs rounded-full bg-tool-primary bg-opacity-20 text-tool-primary">
                      {tool}
                    </span>
                  ))}
                </div>
              )}
            </div>
          </div>
        </motion.div>
      ))}
    </div>
  );
};

const SolutionModal = ({ solution, onClose }) => {
  const [expanded, setExpanded] = useState(true);
  const [showVisualization, setShowVisualization] = useState(false);
  const [animationStep, setAnimationStep] = useState(0);
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);

  useEffect(() => {
    if (showVisualization && solution.steps) {
      // Build nodes and edges from workflow steps
      const workflowNodes = solution.steps.map((step, index) => ({
        id: step.node_id || `node-${index}`,
        type: 'animated',
        position: { x: 150 + (index % 3) * 300, y: 100 + Math.floor(index / 3) * 200 },
        data: {
          label: step.agent || `Agent ${index + 1}`,
          isActive: index === animationStep,
          isCompleted: index < animationStep,
          status: step.status,
        },
      }));

      const workflowEdges = [];
      for (let i = 0; i < solution.steps.length - 1; i++) {
        const sourceId = solution.steps[i].node_id || `node-${i}`;
        const targetId = solution.steps[i + 1].node_id || `node-${i + 1}`;
        workflowEdges.push({
          id: `e${i}`,
          source: sourceId,
          target: targetId,
          animated: i === animationStep - 1,
          style: { 
            stroke: i < animationStep ? '#10b981' : '#6b7280', 
            strokeWidth: i === animationStep - 1 ? 4 : 2 
          },
          markerEnd: { 
            type: MarkerType.ArrowClosed, 
            color: i < animationStep ? '#10b981' : '#6b7280',
            width: 20,
            height: 20,
          },
          type: 'smoothstep',
        });
      }

      setNodes(workflowNodes);
      setEdges(workflowEdges);
    }
  }, [showVisualization, animationStep, solution.steps]);

  const startAnimation = () => {
    setShowVisualization(true);
    setAnimationStep(0);
    
    // Animate through each step
    const stepCount = solution.steps?.length || 0;
    let currentStep = 0;
    
    const interval = setInterval(() => {
      currentStep++;
      if (currentStep > stepCount) {
        clearInterval(interval);
      } else {
        setAnimationStep(currentStep);
      }
    }, 1500); // 1.5 seconds per step

    return () => clearInterval(interval);
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="modal-content max-w-6xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <FaLightbulb className="text-3xl text-solution-primary" />
            <div>
              <h2 className="text-2xl font-bold">Workflow Execution</h2>
              <p className="text-sm text-gray-400">{solution.workflow_id || solution.run_id}</p>
            </div>
          </div>
          <div className="flex gap-2">
            {solution.steps && solution.steps.length > 0 && (
              <button
                onClick={startAnimation}
                className="px-4 py-2 rounded-lg bg-gradient-to-r from-solution-primary to-solution-secondary hover:shadow-lg transition-all flex items-center gap-2"
              >
                <FaPlay /> {showVisualization ? 'Replay' : 'Visualize Flow'}
              </button>
            )}
            <button
              onClick={onClose}
              className="p-2 rounded-lg hover:bg-dark-hover transition-colors"
            >
              <FaTimes className="text-xl" />
            </button>
          </div>
        </div>

        {/* Status Banner */}
        <div className={`p-4 rounded-lg mb-6 flex items-center gap-3 ${
          solution.status === 'completed' ? 'bg-green-500 bg-opacity-20 border border-green-500' :
          solution.status === 'failed' ? 'bg-red-500 bg-opacity-20 border border-red-500' :
          'bg-yellow-500 bg-opacity-20 border border-yellow-500'
        }`}>
          {solution.status === 'completed' ? <FaCheckCircle className="text-green-500 text-2xl" /> :
           solution.status === 'failed' ? <FaExclamationCircle className="text-red-500 text-2xl" /> :
           <FaClock className="text-yellow-500 text-2xl" />}
          <div>
            <h3 className="font-bold capitalize">{solution.status || 'Unknown'}</h3>
            <p className="text-sm text-gray-400">
              {solution.created_at ? new Date(solution.created_at).toLocaleString() : 'N/A'}
            </p>
          </div>
        </div>

        {/* Agent-Tool Mapping Table */}
        {solution.steps && solution.steps.length > 0 && (
          <div className="mb-6 card p-6">
            <h3 className="font-bold text-lg mb-4 flex items-center gap-2">
              <FaProjectDiagram className="text-purple-500" />
              Agent-Tool Mapping & Execution Flow
            </h3>
            
            {/* Interactive Query Input */}
            <div className="mb-4 p-4 bg-dark-bg rounded-lg border-2 border-purple-500/30">
              <label className="block text-sm font-semibold text-gray-300 mb-2">
                Re-run with New Query
              </label>
              <div className="flex gap-2">
                <input
                  type="text"
                  placeholder="Enter your query to re-execute this workflow..."
                  className="flex-1 px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-purple-500 focus:ring-2 focus:ring-purple-500/30 focus:outline-none"
                />
                <button className="px-6 py-2 rounded-lg bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-semibold transition-all flex items-center gap-2 shadow-lg shadow-purple-500/30">
                  <FaPlay /> Execute
                </button>
              </div>
            </div>

            {/* Mapping Table */}
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-dark-border">
                    <th className="text-left py-3 px-4 text-sm font-bold text-purple-400">Step</th>
                    <th className="text-left py-3 px-4 text-sm font-bold text-purple-400">Agent</th>
                    <th className="text-left py-3 px-4 text-sm font-bold text-blue-400">Tools Used</th>
                    <th className="text-left py-3 px-4 text-sm font-bold text-green-400">Tool Results</th>
                    <th className="text-left py-3 px-4 text-sm font-bold text-gray-400">LLM Output</th>
                  </tr>
                </thead>
                <tbody>
                  {solution.steps.map((step, index) => (
                    <motion.tr
                      key={index}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.05 }}
                      className="border-b border-dark-border hover:bg-dark-hover transition-colors"
                    >
                      <td className="py-4 px-4">
                        <div className="flex items-center gap-2">
                          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-purple-600 to-pink-600 flex items-center justify-center text-sm font-bold shadow-lg">
                            {index + 1}
                          </div>
                        </div>
                      </td>
                      <td className="py-4 px-4">
                        <div className="flex items-center gap-2">
                          <FaRobot className="text-purple-500" />
                          <span className="font-semibold text-white">{step.agent || step.node_id || 'Unknown'}</span>
                        </div>
                        {step.task && (
                          <p className="text-xs text-gray-500 mt-1">{step.task}</p>
                        )}
                      </td>
                      <td className="py-4 px-4">
                        {step.tools_used && step.tools_used.length > 0 ? (
                          <div className="flex flex-wrap gap-1">
                            {step.tools_used.map((tool, i) => (
                              <span key={i} className="px-2 py-1 text-xs rounded-full bg-blue-600/20 text-blue-400 border border-blue-500/30 font-mono">
                                {tool}
                              </span>
                            ))}
                          </div>
                        ) : (
                          <span className="text-xs text-gray-600">No tools</span>
                        )}
                      </td>
                      <td className="py-4 px-4">
                        {step.tool_results && Object.keys(step.tool_results).length > 0 ? (
                          <div className="space-y-1 max-w-md">
                            {Object.entries(step.tool_results).map(([toolName, result], i) => (
                              <div key={i} className="text-xs bg-green-900/20 p-2 rounded border border-green-700/30">
                                <span className="font-semibold text-green-400">{toolName}:</span>
                                <p className="text-gray-400 mt-1 line-clamp-2">
                                  {typeof result === 'string' ? result : JSON.stringify(result).substring(0, 100) + '...'}
                                </p>
                              </div>
                            ))}
                          </div>
                        ) : (
                          <span className="text-xs text-gray-600">-</span>
                        )}
                      </td>
                      <td className="py-4 px-4">
                        {step.output ? (
                          <div className="max-w-md">
                            <p className="text-sm text-gray-300 line-clamp-3">{step.output}</p>
                          </div>
                        ) : (
                          <span className="text-xs text-gray-600">-</span>
                        )}
                      </td>
                    </motion.tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Animated Workflow Visualization */}
        {showVisualization && nodes.length > 0 && (
          <div className="mb-6 card p-0 overflow-hidden">
            <div className="p-4 bg-dark-bg border-b border-dark-border flex items-center justify-between">
              <h3 className="font-bold">Live Workflow Execution</h3>
              <div className="text-sm text-gray-400">
                Step {Math.min(animationStep, solution.steps.length)} of {solution.steps.length}
              </div>
            </div>
            <div className="h-[400px] bg-dark-bg">
              <ReactFlow
                nodes={nodes}
                edges={edges}
                nodeTypes={nodeTypes}
                fitView
                nodesDraggable={false}
                nodesConnectable={false}
                elementsSelectable={false}
              >
                <Background color="#252530" gap={20} />
                <Controls className="bg-dark-card border border-dark-border" />
              </ReactFlow>
            </div>
          </div>
        )}

        {/* Execution Flow */}
        <div className="mb-6">
          <button
            onClick={() => setExpanded(!expanded)}
            className="w-full flex items-center justify-between p-4 bg-dark-bg rounded-lg hover:bg-dark-hover transition-colors"
          >
            <h3 className="font-bold text-lg">Execution Details</h3>
            {expanded ? <FaChevronUp /> : <FaChevronDown />}
          </button>
          
          <AnimatePresence>
            {expanded && (
              <motion.div
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: 'auto', opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
                className="mt-4 overflow-hidden"
              >
                <MessageFlow steps={solution.steps || solution.result?.steps || []} />
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* Final Result */}
        {solution.final_output && (
          <div className="card p-6 bg-gradient-to-br from-solution-primary from-opacity-10 to-transparent">
            <h3 className="font-bold text-lg mb-4 flex items-center gap-2">
              <FaLightbulb className="text-solution-primary" />
              Final Output
            </h3>
            <div className="p-4 bg-dark-bg rounded-lg">
              <p className="whitespace-pre-wrap text-gray-300">{solution.final_output}</p>
            </div>
          </div>
        )}

        {/* Metadata */}
        {solution.metadata && (
          <div className="mt-6 p-4 bg-dark-bg rounded-lg">
            <h4 className="font-semibold mb-2 text-sm text-gray-400">Metadata</h4>
            <pre className="text-xs font-mono text-gray-500 overflow-x-auto">
              {JSON.stringify(solution.metadata, null, 2)}
            </pre>
          </div>
        )}
      </motion.div>
    </div>
  );
};

const SolutionCard = ({ solution, onClick }) => {
  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return 'from-green-500 to-green-600';
      case 'failed':
        return 'from-red-500 to-red-600';
      case 'running':
        return 'from-yellow-500 to-yellow-600';
      default:
        return 'from-gray-500 to-gray-600';
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      whileHover={{ scale: 1.02, boxShadow: "0 10px 30px rgba(139, 92, 246, 0.2)" }}
      className="bg-gray-900 border-2 border-gray-800 rounded-xl p-6 cursor-pointer transition-all hover:border-purple-500/50"
      onClick={onClick}
    >
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className="p-3 rounded-lg bg-gradient-to-br from-purple-600 to-pink-600 shadow-lg shadow-purple-500/30">
            <FaLightbulb className="text-2xl text-white" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-white">{solution.workflow_id || 'Workflow'}</h3>
            <p className="text-sm text-gray-500">{solution.run_id}</p>
          </div>
        </div>
        <div className={`px-3 py-1 rounded-full text-xs font-semibold bg-gradient-to-r ${getStatusColor(solution.status)} shadow-md`}>
          {solution.status || 'unknown'}
        </div>
      </div>

      <div className="space-y-2 text-sm">
        <div className="flex justify-between">
          <span className="text-gray-500">Created:</span>
          <span className="font-medium text-gray-300">
            {solution.created_at ? new Date(solution.created_at).toLocaleDateString() : 'N/A'}
          </span>
        </div>
        {solution.steps && (
          <div className="flex justify-between">
            <span className="text-gray-500">Steps:</span>
            <span className="font-medium text-gray-300">{solution.steps.length}</span>
          </div>
        )}
      </div>

      {solution.final_output && (
        <div className="mt-4 pt-4 border-t border-gray-800">
          <p className="text-xs text-gray-500 line-clamp-2">{solution.final_output}</p>
        </div>
      )}
    </motion.div>
  );
};

const Solutions = () => {
  const [solutions, setSolutions] = useState([]);
  const [workflows, setWorkflows] = useState([]);
  const [agents, setAgents] = useState([]);
  const [selectedSolution, setSelectedSolution] = useState(null);
  const [executingWorkflow, setExecutingWorkflow] = useState(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');
  const [error, setError] = useState(null);
  const [showBlueprint, setShowBlueprint] = useState(false);
  const [blueprintWorkflow, setBlueprintWorkflow] = useState(null);
  const [isExecuting, setIsExecuting] = useState(false);
  const [executionState, setExecutionState] = useState({});
  const [chatWorkflow, setChatWorkflow] = useState(null);
  const [showInteractiveChat, setShowInteractiveChat] = useState(false);
  const [interactiveSolutionId, setInteractiveSolutionId] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [solutionsRes, workflowsRes, agentsRes] = await Promise.all([
        solutionsAPI.getAll(),
        workflowsAPI.getAll(),
        agentsAPI.getAll(),
      ]);
      console.log('Solutions response:', solutionsRes.data);
      setSolutions(solutionsRes.data || []);
      setWorkflows(workflowsRes.data || []);
      setAgents(agentsRes.data || []);
      setError(null);
    } catch (error) {
      console.error('Error fetching data:', error);
      setError(error.message);
      setSolutions([]);
    } finally {
      setLoading(false);
    }
  };

  const fetchSolutions = async () => {
    try {
      const response = await solutionsAPI.getAll();
      console.log('Solutions response:', response.data);
      setSolutions(response.data || []);
      setError(null);
    } catch (error) {
      console.error('Error fetching solutions:', error);
      setError(error.message);
      setSolutions([]);
    }
  };

  const handleExecuteWorkflow = async (workflow) => {
    try {
      // Show blueprint visualization
      setBlueprintWorkflow(workflow);
      setShowBlueprint(true);
      setIsExecuting(true);
      setExecutionState({});
      setExecutingWorkflow({ ...workflow, status: 'running' });

      // Execute workflow
      const result = await workflowsAPI.run(workflow.id);
      
      // Simulate step-by-step execution for visualization
      const nodes = workflow.nodes || [];
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
      
      // Show the result
      setTimeout(() => {
        setSelectedSolution({
          ...result.data,
          workflow_id: workflow.id,
          workflow_name: workflow.name,
        });
      }, 500);
      
      // Refresh solutions list
      await fetchSolutions();
      
    } catch (error) {
      console.error('Error executing workflow:', error);
      alert('Error executing workflow: ' + (error.response?.data?.detail || error.message));
    } finally {
      setIsExecuting(false);
      setExecutingWorkflow(null);
    }
  };

  const filteredSolutions = solutions.filter((solution) => {
    if (filter === 'all') return true;
    return solution.status === filter;
  });

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-solution-primary"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold mb-2 text-white">Solutions</h1>
          <p className="text-gray-500">Execute workflows and view results</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => setFilter('all')}
            className={`px-4 py-2 rounded-lg transition-all font-semibold ${
              filter === 'all' 
                ? 'bg-gradient-to-r from-purple-600 to-pink-600 shadow-lg shadow-purple-500/30 text-white' 
                : 'bg-gray-800 hover:bg-gray-700 border border-gray-700 text-gray-300'
            }`}
          >
            All
          </button>
          <button
            onClick={() => setFilter('completed')}
            className={`px-4 py-2 rounded-lg transition-all font-semibold ${
              filter === 'completed' 
                ? 'bg-gradient-to-r from-green-600 to-green-700 shadow-lg shadow-green-500/30 text-white' 
                : 'bg-gray-800 hover:bg-gray-700 border border-gray-700 text-gray-300'
            }`}
          >
            Completed
          </button>
          <button
            onClick={() => setFilter('failed')}
            className={`px-4 py-2 rounded-lg transition-all font-semibold ${
              filter === 'failed' 
                ? 'bg-gradient-to-r from-red-600 to-red-700 shadow-lg shadow-red-500/30 text-white' 
                : 'bg-gray-800 hover:bg-gray-700 border border-gray-700 text-gray-300'
            }`}
          >
            Failed
          </button>
        </div>
      </div>

      {error && (
        <div className="card p-6 bg-red-500 bg-opacity-10 border border-red-500">
          <p className="text-red-400">Error loading solutions: {error}</p>
        </div>
      )}

      {/* Available Workflows Section */}
      {workflows.length > 0 && (
        <div className="bg-gray-900 border-2 border-gray-800 rounded-xl p-6 shadow-xl">
          <h2 className="text-xl font-bold mb-4 flex items-center gap-2 text-white">
            <FaPlay className="text-purple-500" />
            Available Workflows - Execute or Chat
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {workflows.map((workflow) => (
              <motion.div
                key={workflow.id}
                whileHover={{ scale: 1.02, boxShadow: "0 10px 30px rgba(59, 130, 246, 0.3)" }}
                className="p-4 bg-gray-950 border-2 border-blue-600/50 rounded-lg transition-all hover:border-blue-500"
              >
                <div className="flex items-center gap-3 mb-3">
                  <div className="p-2 rounded-lg bg-gradient-to-br from-blue-600 to-blue-700 shadow-lg shadow-blue-500/30">
                    <FaProjectDiagram className="text-white" />
                  </div>
                  <div className="flex-1">
                    <h3 className="font-bold text-white">{workflow.name}</h3>
                    <p className="text-xs text-gray-500">{workflow.nodes?.length || 0} nodes</p>
                  </div>
                </div>
                {workflow.description && (
                  <p className="text-xs text-gray-500 line-clamp-2 mb-3">{workflow.description}</p>
                )}
                
                {/* Action Buttons */}
                <div className="flex gap-2">
                  <button
                    onClick={() => handleExecuteWorkflow(workflow)}
                    className="flex-1 px-3 py-2 rounded-lg bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 transition-all flex items-center justify-center gap-2 text-sm font-semibold text-white shadow-lg shadow-green-500/30"
                  >
                    <FaPlay className="text-xs" />
                    Run
                  </button>
                  <button
                    onClick={() => setChatWorkflow(workflow)}
                    className="flex-1 px-3 py-2 rounded-lg bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 transition-all flex items-center justify-center gap-2 text-sm font-semibold text-white shadow-lg shadow-blue-500/30"
                  >
                    <FaComments className="text-xs" />
                    Chat
                  </button>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      )}

      {/* Executing Workflow Overlay */}
      <AnimatePresence>
        {executingWorkflow && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm z-50 flex items-center justify-center"
          >
            <motion.div
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              className="card p-8 max-w-md text-center"
            >
              <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-solution-primary mx-auto mb-4"></div>
              <h3 className="text-xl font-bold mb-2">Executing Workflow</h3>
              <p className="text-gray-400">{executingWorkflow.name}</p>
              <div className="mt-4 flex items-center justify-center gap-2">
                <div className="w-2 h-2 bg-solution-primary rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                <div className="w-2 h-2 bg-solution-primary rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                <div className="w-2 h-2 bg-solution-primary rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Past Executions Section */}
      <div>
        <h2 className="text-2xl font-bold mb-4">Past Executions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredSolutions.map((solution) => (
            <SolutionCard
              key={solution.run_id || solution.id}
              solution={solution}
              onClick={() => {
                setInteractiveSolutionId(solution.id);
                setShowInteractiveChat(true);
              }}
            />
          ))}
        </div>
      </div>

      {filteredSolutions.length === 0 && !error && (
        <div className="bg-gray-900 border-2 border-gray-800 rounded-xl p-12 text-center shadow-xl">
          <FaLightbulb className="text-6xl text-gray-700 mx-auto mb-4" />
          <h3 className="text-xl font-bold mb-2 text-white">No workflow runs found</h3>
          <p className="text-gray-500 mb-4">Execute a workflow to see results here</p>
          <div className="text-sm text-gray-600 mt-4">
            <p className="text-gray-500">To create a workflow run:</p>
            <ol className="list-decimal list-inside mt-2 space-y-1 text-gray-600">
              <li>Go to Workflows tab</li>
              <li>Create or select a workflow</li>
              <li>Click the Play ▶ button to execute it</li>
              <li>Return here to see the results</li>
            </ol>
          </div>
        </div>
      )}

      <AnimatePresence>
        {showBlueprint && blueprintWorkflow && (
          <WorkflowBlueprint
            workflow={blueprintWorkflow}
            agents={agents}
            onClose={() => {
              setShowBlueprint(false);
              setBlueprintWorkflow(null);
              setExecutionState({});
            }}
            isExecuting={isExecuting}
            executionState={executionState}
          />
        )}
        {chatWorkflow && (
          <WorkflowChat
            workflow={chatWorkflow}
            agents={agents}
            onClose={() => setChatWorkflow(null)}
          />
        )}
        {showInteractiveChat && interactiveSolutionId && (
          <InteractiveSolutionChat
            solutionId={interactiveSolutionId}
            onClose={() => {
              setShowInteractiveChat(false);
              setInteractiveSolutionId(null);
            }}
          />
        )}
      </AnimatePresence>
    </div>
  );
};

export default Solutions;
