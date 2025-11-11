import React, { useState, useEffect } from 'react';
import { solutionsAPI, workflowsAPI } from '../services/api';
import WorkflowCommunicationVisualizer from './WorkflowCommunicationVisualizer';
import InteractiveSolutionChat from './InteractiveSolutionChat';
import SolutionExecutionView from './SolutionExecutionView';
import { 
  FaPlus, FaEdit, FaTrash, FaPlay, FaTimes, FaSave,
  FaNetworkWired, FaBrain, FaSpinner, FaCheckCircle, FaComments 
} from 'react-icons/fa';

// WebSocket Hook - DISABLED (using SolutionExecutionView's WebSocket instead)
// This was causing 403 errors because it was using wrong endpoint
function useWorkflowWebSocket(clientId, onMessage) {
  const [ws, setWs] = useState(null);
  const [connected, setConnected] = useState(false);

  // Disabled - SolutionExecutionView handles its own WebSocket
  // useEffect(() => {
  //   if (!clientId) return;
  //   const websocket = new WebSocket(`ws://localhost:8000/solutions/ws/${clientId}`);
  //   // ... rest of code
  // }, [clientId]);

  return { ws, connected };
}

function SolutionsManagement() {
  const [solutions, setSolutions] = useState([]);
  const [workflows, setWorkflows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [selectedSolution, setSelectedSolution] = useState(null);
  const [executingSolution, setExecutingSolution] = useState(null);
  const [executionStatus, setExecutionStatus] = useState(null);
  const [activeChatSolution, setActiveChatSolution] = useState(null);
  const [showExecutionView, setShowExecutionView] = useState(false);
  const [executionResults, setExecutionResults] = useState({});
  const [solutionSummary, setSolutionSummary] = useState(null);
  const [error, setError] = useState(null);
  const [formData, setFormData] = useState({
    id: '',
    name: '',
    description: '',
    solution_type: 'normal',
    workflows: []
  });

  // Removed: const clientId and useWorkflowWebSocket hook - SolutionExecutionView handles WebSocket

  useEffect(() => {
    fetchSolutions();
    fetchWorkflows();
  }, []);

  // Removed: handleWebSocketMessage - SolutionExecutionView handles its own messages

  async function fetchSolutions() {
    try {
      setLoading(true);
      const response = await solutionsAPI.getAll();
      setSolutions(response.data || []);
      setError(null);
    } catch (err) {
      console.error('Error fetching solutions:', err);
      setError('Failed to load solutions');
    } finally {
      setLoading(false);
    }
  }

  async function fetchWorkflows() {
    try {
      const response = await workflowsAPI.getAll();
      setWorkflows(response.data || []);
    } catch (err) {
      console.error('Error fetching workflows:', err);
    }
  }

  async function handleExecuteSolution(solution) {
    if (!solution.workflows || solution.workflows.length === 0) {
      alert('This solution has no workflows to execute');
      return;
    }

    // Open the real-time execution view
    setExecutingSolution(solution);
    setShowExecutionView(true);
  }

  function handleCreate() {
    setFormData({
      id: '',
      name: '',
      description: '',
      solution_type: 'normal',
      workflows: []
    });
    setShowForm(true);
    setSelectedSolution(null);
  }

  function handleEdit(solution) {
    setFormData({
      id: solution.id,
      name: solution.name,
      description: solution.description || '',
      solution_type: solution.solution_type || 'normal',
      workflows: solution.workflows || []
    });
    setShowForm(true);
    setSelectedSolution(solution);
  }

  async function handleSubmit(e) {
    e.preventDefault();
    try {
      if (selectedSolution) {
        await solutionsAPI.update(selectedSolution.id, {
          name: formData.name,
          description: formData.description,
          solution_type: formData.solution_type,
          workflows: formData.workflows
        });
      } else {
        await solutionsAPI.create(formData);
      }
      
      setShowForm(false);
      fetchSolutions();
      setError(null);
    } catch (err) {
      console.error('Error saving solution:', err);
      setError(err.response?.data?.detail || 'Failed to save solution');
    }
  }

  async function handleDelete(id) {
    if (!window.confirm('Are you sure you want to delete this solution?')) return;
    
    try {
      await solutionsAPI.delete(id);
      await solutionsAPI.clearMemory(id);
      fetchSolutions();
      setError(null);
    } catch (err) {
      console.error('Error deleting solution:', err);
      setError('Failed to delete solution');
    }
  }

  function toggleWorkflow(workflowId) {
    setFormData(prev => ({
      ...prev,
      workflows: prev.workflows.includes(workflowId)
        ? prev.workflows.filter(id => id !== workflowId)
        : [...prev.workflows, workflowId]
    }));
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-purple-500"></div>
      </div>
    );
  }

  return (
    <div className="p-6 min-h-screen bg-gray-950">
      {/* Solution Execution View */}
      {showExecutionView && executingSolution && (
        <SolutionExecutionView
          solution={executingSolution}
          onClose={() => {
            setShowExecutionView(false);
            setExecutingSolution(null);
          }}
        />
      )}

      {/* Interactive Solution Chat */}
      {activeChatSolution && (
        <InteractiveSolutionChat
          solutionId={activeChatSolution}
          onClose={() => setActiveChatSolution(null)}
        />
      )}

      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-6">
          <div>
            <h1 className="text-3xl font-bold text-white">Solutions</h1>
            <p className="text-gray-400 mt-1">
              Execute multiple workflows with AI-powered communication
            </p>
          </div>
          <button
            onClick={handleCreate}
            className="px-4 py-2 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-lg hover:from-blue-700 hover:to-blue-800 flex items-center gap-2 shadow-lg shadow-blue-500/30 font-semibold transition-all"
          >
            <FaPlus /> Create Solution
          </button>
        </div>

        {/* Error Display */}
        {error && (
          <div className="mb-4 p-4 bg-red-900/20 border border-red-500 text-red-400 rounded-lg">
            {error}
          </div>
        )}

        {/* Solution Form Modal */}
        {showForm && (
          <div className="fixed inset-0 bg-black bg-opacity-70 backdrop-blur-sm flex items-center justify-center z-50 p-4">
            <div className="bg-gray-900 border-2 border-gray-800 rounded-xl shadow-2xl max-w-3xl w-full max-h-[90vh] overflow-y-auto">
              <div className="p-6">
                <div className="flex justify-between items-center mb-6">
                  <h2 className="text-2xl font-bold text-white">
                    {selectedSolution ? 'Edit Solution' : 'Create Solution'}
                  </h2>
                  <button
                    onClick={() => setShowForm(false)}
                    className="text-gray-400 hover:text-white transition-colors"
                  >
                    <FaTimes size={24} />
                  </button>
                </div>

                <form onSubmit={handleSubmit} className="space-y-4">
                  {!selectedSolution && (
                    <div>
                      <label className="block text-sm font-medium text-gray-300 mb-1">
                        ID (optional - auto-generated if empty)
                      </label>
                      <input
                        type="text"
                        value={formData.id}
                        onChange={(e) => setFormData({ ...formData, id: e.target.value })}
                        className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        placeholder="solution_id"
                      />
                    </div>
                  )}

                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-1">
                      Name *
                    </label>
                    <input
                      type="text"
                      value={formData.name}
                      onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                      required
                      className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      placeholder="My Solution"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-1">
                      Description
                    </label>
                    <textarea
                      value={formData.description}
                      onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                      className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      rows="3"
                      placeholder="Solution description..."
                    />
                  </div>

                  {/* Solution Type */}
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-1">
                      Solution Type *
                    </label>
                    <div className="grid grid-cols-2 gap-3">
                      <label className={`relative flex items-center p-4 border-2 rounded-lg cursor-pointer transition-all ${
                        formData.solution_type === 'normal' 
                          ? 'border-green-500 bg-green-500/10' 
                          : 'border-gray-700 bg-gray-800 hover:border-gray-600'
                      }`}>
                        <input
                          type="radio"
                          name="solution_type"
                          value="normal"
                          checked={formData.solution_type === 'normal'}
                          onChange={(e) => setFormData({ ...formData, solution_type: e.target.value })}
                          className="sr-only"
                        />
                        <div className="flex-1">
                          <div className="font-semibold text-white mb-1">Normal</div>
                          <div className="text-xs text-gray-400">
                            KAG + Conversational Buffer Memory
                          </div>
                          <div className="text-xs text-gray-500 mt-1">
                            LLM-powered fact extraction with intelligent reasoning
                          </div>
                        </div>
                        {formData.solution_type === 'normal' && (
                          <div className="absolute top-2 right-2 w-5 h-5 bg-green-500 rounded-full flex items-center justify-center">
                            <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd"/>
                            </svg>
                          </div>
                        )}
                      </label>
                      
                      <label className={`relative flex items-center p-4 border-2 rounded-lg cursor-pointer transition-all ${
                        formData.solution_type === 'research' 
                          ? 'border-purple-500 bg-purple-500/10' 
                          : 'border-gray-700 bg-gray-800 hover:border-gray-600'
                      }`}>
                        <input
                          type="radio"
                          name="solution_type"
                          value="research"
                          checked={formData.solution_type === 'research'}
                          onChange={(e) => setFormData({ ...formData, solution_type: e.target.value })}
                          className="sr-only"
                        />
                        <div className="flex-1">
                          <div className="font-semibold text-white mb-1">Research</div>
                          <div className="text-xs text-gray-400">
                            Agentic RAG with Embedding & Chunking
                          </div>
                          <div className="text-xs text-gray-500 mt-1">
                            Full context to agent nodes via intelligent retrieval
                          </div>
                        </div>
                        {formData.solution_type === 'research' && (
                          <div className="absolute top-2 right-2 w-5 h-5 bg-purple-500 rounded-full flex items-center justify-center">
                            <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd"/>
                            </svg>
                          </div>
                        )}
                      </label>
                    </div>
                    <p className="text-xs text-gray-500 mt-2">
                      {formData.solution_type === 'normal' 
                        ? '💡 Normal mode: KAG extracts facts using Gemini LLM and maintains conversational buffer memory across workflows'
                        : '🔬 Research mode: Full information chunked & embedded, delivered to agent nodes at startup via TF-IDF similarity search'
                      }
                    </p>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      Workflows (executed in order)
                    </label>
                    <div className="border border-gray-700 bg-gray-800 rounded-lg p-4 max-h-60 overflow-y-auto">
                      {workflows.length === 0 ? (
                        <p className="text-gray-500 text-sm">No workflows available</p>
                      ) : (
                        <div className="space-y-2">
                          {workflows.map(workflow => (
                            <label key={workflow.id} className="flex items-center gap-2 cursor-pointer hover:bg-gray-700 p-2 rounded transition-colors">
                              <input
                                type="checkbox"
                                checked={formData.workflows.includes(workflow.id)}
                                onChange={() => toggleWorkflow(workflow.id)}
                                className="w-4 h-4 text-blue-600 bg-gray-700 border-gray-600 rounded focus:ring-blue-500"
                              />
                              <div className="flex-1">
                                <div className="font-medium text-sm text-white">{workflow.name}</div>
                                <div className="text-xs text-gray-500">{workflow.id}</div>
                              </div>
                            </label>
                          ))}
                        </div>
                      )}
                    </div>
                    <p className="text-xs text-gray-500 mt-1">
                      Selected: {formData.workflows.length} workflow(s)
                    </p>
                  </div>

                  <div className="flex gap-2 pt-4">
                    <button
                      type="submit"
                      className="flex-1 px-4 py-2 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-lg hover:from-blue-700 hover:to-blue-800 flex items-center justify-center gap-2 font-semibold shadow-lg shadow-blue-500/30 transition-all"
                    >
                      <FaSave /> {selectedSolution ? 'Update' : 'Create'}
                    </button>
                    <button
                      type="button"
                      onClick={() => setShowForm(false)}
                      className="px-4 py-2 bg-gray-700 text-gray-200 rounded-lg hover:bg-gray-600 transition-colors font-semibold"
                    >
                      Cancel
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        )}

        {/* Solutions List */}
        {solutions.length === 0 ? (
          <div className="bg-gray-900 border-2 border-gray-800 rounded-xl shadow-xl p-12 text-center">
            <FaNetworkWired className="mx-auto text-gray-600 mb-4" size={48} />
            <h3 className="text-xl font-semibold text-white mb-2">No Solutions Yet</h3>
            <p className="text-gray-400 mb-4">
              Create your first solution with AI-powered workflow communication
            </p>
            <button
              onClick={handleCreate}
              className="px-4 py-2 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-lg hover:from-blue-700 hover:to-blue-800 shadow-lg shadow-blue-500/30 font-semibold transition-all"
            >
              Create Solution
            </button>
          </div>
        ) : (
          <div className="grid gap-6">
            {solutions.map(solution => (
              <div key={solution.id} className="bg-gray-900 border-2 border-gray-800 rounded-xl shadow-xl overflow-hidden hover:border-purple-500/50 transition-all">
                <div className="p-6">
                  {/* Header */}
                  <div className="flex justify-between items-start mb-4">
                    <div className="flex-1">
                      <h3 className="text-xl font-bold text-white mb-1">{solution.name}</h3>
                      <p className="text-sm text-gray-500 mb-2">{solution.id}</p>
                      {solution.description && (
                        <p className="text-gray-400 mb-3">{solution.description}</p>
                      )}
                      <div className="flex gap-4 text-sm text-gray-500">
                        <span className="flex items-center gap-1">
                          <FaNetworkWired />
                          {solution.workflows?.length || 0} workflow(s)
                        </span>
                      </div>
                    </div>
                    <div className="flex gap-2">
                      <button
                        onClick={() => handleExecuteSolution(solution)}
                        disabled={executingSolution === solution.id}
                        className="px-4 py-2 bg-gradient-to-r from-green-600 to-green-700 text-white rounded-lg hover:from-green-700 hover:to-green-800 flex items-center gap-2 shadow-lg shadow-green-500/30 font-semibold transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        {executingSolution === solution.id ? (
                          <>
                            <FaSpinner className="animate-spin" /> Executing...
                          </>
                        ) : (
                          <>
                            <FaPlay /> Execute
                          </>
                        )}
                      </button>
                      <button
                        onClick={() => setActiveChatSolution(solution.id)}
                        className="p-2 text-purple-400 hover:bg-purple-900/30 rounded transition-colors"
                        title="Chat with Solution"
                      >
                        <FaComments />
                      </button>
                      <button
                        onClick={() => handleEdit(solution)}
                        className="p-2 text-blue-400 hover:bg-blue-900/30 rounded transition-colors"
                        title="Edit"
                      >
                        <FaEdit />
                      </button>
                      <button
                        onClick={() => handleDelete(solution.id)}
                        className="p-2 text-red-400 hover:bg-red-900/30 rounded transition-colors"
                        title="Delete"
                      >
                        <FaTrash />
                      </button>
                    </div>
                  </div>

                  {/* Visualization */}
                  {executingSolution === solution.id && (
                    <div className="mt-6 p-6 bg-gray-950 border border-gray-800 rounded-lg">
                      <div className="flex items-center gap-2 mb-4">
                        <FaBrain className="text-purple-400" />
                        <h4 className="text-lg font-semibold text-white">Live Execution</h4>
                      </div>
                      <WorkflowCommunicationVisualizer
                        solution={solution}
                        workflows={workflows}
                        executionStatus={executionStatus}
                      />
                    </div>
                  )}

                  {/* Summary after execution */}
                  {solutionSummary && executionResults[solution.workflows?.[solution.workflows.length - 1]] && (
                    <div className="mt-6 p-6 bg-green-900/20 border border-green-700 rounded-lg">
                      <div className="flex items-center gap-2 mb-4">
                        <FaCheckCircle className="text-green-400" />
                        <h4 className="text-lg font-semibold text-white">Execution Complete</h4>
                      </div>
                      <p className="text-gray-300 mb-4">{solutionSummary.overall_context}</p>
                      <div className="grid grid-cols-3 gap-4 text-center mt-4">
                        <div>
                          <div className="text-2xl font-bold text-green-400">{solutionSummary.total_workflows}</div>
                          <div className="text-xs text-gray-500">Workflows</div>
                        </div>
                        <div>
                          <div className="text-2xl font-bold text-purple-400">{solutionSummary.combined_facts?.length || 0}</div>
                          <div className="text-xs text-gray-500">Facts Extracted</div>
                        </div>
                        <div>
                          <div className="text-2xl font-bold text-blue-400">{solutionSummary.summaries?.length || 0}</div>
                          <div className="text-xs text-gray-500">Summaries</div>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default SolutionsManagement;
