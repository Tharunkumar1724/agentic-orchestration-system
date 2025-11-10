import React, { useState, useEffect } from 'react';
import { 
  FaCheckCircle, FaSpinner, FaClock, FaArrowRight, 
  FaBrain, FaLightbulb, FaExchangeAlt 
} from 'react-icons/fa';

function WorkflowCommunicationVisualizer({ 
  solution, 
  workflows, 
  executionStatus, 
  communications = [] 
}) {
  const [activeWorkflows, setActiveWorkflows] = useState({});
  const [completedWorkflows, setCompletedWorkflows] = useState({});
  const [handoffs, setHandoffs] = useState([]);
  const [kagData, setKagData] = useState({});

  useEffect(() => {
    if (executionStatus) {
      const { type, workflow_id, data } = executionStatus;
      
      switch(type) {
        case 'workflow_start':
          setActiveWorkflows(prev => ({ ...prev, [workflow_id]: true }));
          break;
        
        case 'workflow_complete':
          setActiveWorkflows(prev => {
            const updated = { ...prev };
            delete updated[workflow_id];
            return updated;
          });
          setCompletedWorkflows(prev => ({ ...prev, [workflow_id]: true }));
          break;
        
        case 'workflow_kag':
          setKagData(prev => ({
            ...prev,
            [workflow_id]: {
              summary: data?.summary,
              facts: data?.facts || []
            }
          }));
          break;
        
        case 'workflow_handoff':
          setHandoffs(prev => [...prev, {
            from: data?.from,
            to: data?.to,
            data: data?.data,
            timestamp: Date.now()
          }]);
          break;
      }
    }
  }, [executionStatus]);

  const getWorkflowStatus = (workflowId) => {
    if (activeWorkflows[workflowId]) return 'running';
    if (completedWorkflows[workflowId]) return 'completed';
    return 'pending';
  };

  const getWorkflowById = (workflowId) => {
    return workflows.find(w => w.id === workflowId);
  };

  const renderWorkflowNode = (workflowId, index) => {
    const status = getWorkflowStatus(workflowId);
    const workflow = getWorkflowById(workflowId);
    const kag = kagData[workflowId];
    
    const statusColors = {
      pending: 'border-gray-700 bg-gray-800',
      running: 'border-blue-500 bg-blue-900/30 shadow-lg shadow-blue-500/20',
      completed: 'border-green-500 bg-green-900/30 shadow-lg shadow-green-500/20'
    };
    
    const statusIcons = {
      pending: <FaClock className="text-gray-500" />,
      running: <FaSpinner className="text-blue-400 animate-spin" />,
      completed: <FaCheckCircle className="text-green-400" />
    };

    return (
      <div key={workflowId} className="relative">
        {/* Workflow Card */}
        <div className={`${statusColors[status]} border-2 rounded-xl p-4 transition-all duration-300`}>
          <div className="flex items-start justify-between mb-3">
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-1">
                {statusIcons[status]}
                <h3 className="text-white font-semibold">{workflow?.name || workflowId}</h3>
              </div>
              <p className="text-xs text-gray-400">{workflow?.description || 'No description'}</p>
            </div>
            <div className="text-xs px-2 py-1 rounded bg-gray-700 text-gray-300">
              Step {index + 1}
            </div>
          </div>

          {/* KAG Summary */}
          {kag && (
            <div className="mt-3 pt-3 border-t border-gray-700">
              <div className="flex items-center gap-2 mb-2">
                <FaBrain className="text-purple-400" />
                <span className="text-xs font-semibold text-purple-300">AI Analysis</span>
              </div>
              <p className="text-xs text-gray-300 mb-2">{kag.summary}</p>
              
              {kag.facts && kag.facts.length > 0 && (
                <div className="space-y-1">
                  <div className="flex items-center gap-1 text-xs text-blue-300">
                    <FaLightbulb size={10} />
                    <span className="font-medium">Key Facts:</span>
                  </div>
                  <ul className="text-xs text-gray-400 space-y-1 ml-4">
                    {kag.facts.slice(0, 3).map((fact, i) => (
                      <li key={i} className="list-disc">{fact}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Connection Arrow */}
        {index < solution.workflows.length - 1 && (
          <div className="flex justify-center my-4">
            <div className="flex items-center gap-2 px-3 py-1 bg-gray-800 border border-gray-700 rounded-full">
              <FaArrowRight className="text-blue-400" />
              <span className="text-xs text-gray-400">Next Workflow</span>
            </div>
          </div>
        )}
      </div>
    );
  };

  const renderHandoffAnimation = (handoff, index) => {
    const fromWorkflow = getWorkflowById(handoff.from);
    const toWorkflow = getWorkflowById(handoff.to);

    return (
      <div 
        key={index} 
        className="absolute left-1/2 transform -translate-x-1/2 pointer-events-none animate-pulse"
        style={{ top: `${(index + 1) * 150}px` }}
      >
        <div className="bg-purple-900/40 border border-purple-500 rounded-lg p-3 backdrop-blur-sm">
          <div className="flex items-center gap-2 text-xs text-purple-300">
            <FaExchangeAlt className="animate-bounce" />
            <span>Transferring context: {fromWorkflow?.name} → {toWorkflow?.name}</span>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="relative">
      {/* Workflow Chain Visualization */}
      <div className="space-y-0">
        {solution.workflows.map((workflowId, index) => 
          renderWorkflowNode(workflowId, index)
        )}
      </div>

      {/* Live Handoff Animations */}
      {handoffs.slice(-3).map((handoff, index) => 
        renderHandoffAnimation(handoff, index)
      )}

      {/* Execution Summary */}
      <div className="mt-6 p-4 bg-gray-900/50 border border-gray-800 rounded-lg">
        <div className="grid grid-cols-3 gap-4 text-center">
          <div>
            <div className="text-2xl font-bold text-gray-400">
              {Object.keys(completedWorkflows).length}
            </div>
            <div className="text-xs text-gray-500">Completed</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-blue-400">
              {Object.keys(activeWorkflows).length}
            </div>
            <div className="text-xs text-gray-500">Running</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-gray-400">
              {solution.workflows.length - Object.keys(completedWorkflows).length - Object.keys(activeWorkflows).length}
            </div>
            <div className="text-xs text-gray-500">Pending</div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default WorkflowCommunicationVisualizer;
