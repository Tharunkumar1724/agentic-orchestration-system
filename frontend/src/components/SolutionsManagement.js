import React, { useState, useEffect } from 'react';
import { solutionsAPI, workflowsAPI } from '../services/api';
import { 
  FaPlus, FaEdit, FaTrash, FaProjectDiagram, FaComments, 
  FaCog, FaSave, FaTimes, FaNetworkWired 
} from 'react-icons/fa';
import InteractiveSolutionChat from './InteractiveSolutionChat';

function Solutions() {
  const [solutions, setSolutions] = useState([]);
  const [workflows, setWorkflows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedSolution, setSelectedSolution] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [activeChatSolution, setActiveChatSolution] = useState(null);
  const [formData, setFormData] = useState({
    id: '',
    name: '',
    description: '',
    workflows: [],
    communication_config: {},
    metadata: {}
  });
  const [error, setError] = useState(null);
  const [communications, setCommunications] = useState([]);

  useEffect(() => {
    fetchSolutions();
    fetchWorkflows();
  }, []);

  const fetchSolutions = async () => {
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
  };

  const fetchWorkflows = async () => {
    try {
      const response = await workflowsAPI.getAll();
      setWorkflows(response.data || []);
    } catch (err) {
      console.error('Error fetching workflows:', err);
    }
  };

  const handleCreate = () => {
    setFormData({
      id: '',
      name: '',
      description: '',
      solution_type: 'normal',  // Default to normal
      workflows: [],
      communication_config: {},
      metadata: {}
    });
    setShowForm(true);
    setSelectedSolution(null);
  };

  const handleEdit = (solution) => {
    setFormData({
      id: solution.id,
      name: solution.name,
      description: solution.description || '',
      solution_type: solution.solution_type || 'normal',
      workflows: solution.workflows || [],
      communication_config: solution.communication_config || {},
      metadata: solution.metadata || {}
    });
    setShowForm(true);
    setSelectedSolution(solution);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (selectedSolution) {
        // Update existing solution
        await solutionsAPI.update(selectedSolution.id, {
          name: formData.name,
          description: formData.description,
          solution_type: formData.solution_type,
          workflows: formData.workflows,
          communication_config: formData.communication_config,
          metadata: formData.metadata
        });
      } else {
        // Create new solution
        await solutionsAPI.create(formData);
      }
      
      setShowForm(false);
      fetchSolutions();
      setError(null);
    } catch (err) {
      console.error('Error saving solution:', err);
      setError(err.response?.data?.detail || 'Failed to save solution');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this solution?')) return;
    
    try {
      await solutionsAPI.delete(id);
      fetchSolutions();
      setError(null);
    } catch (err) {
      console.error('Error deleting solution:', err);
      setError('Failed to delete solution');
    }
  };

  const handleAddWorkflow = async (solutionId, workflowId) => {
    try {
      await solutionsAPI.addWorkflow(solutionId, workflowId);
      fetchSolutions();
      setError(null);
    } catch (err) {
      console.error('Error adding workflow:', err);
      setError('Failed to add workflow');
    }
  };

  const handleRemoveWorkflow = async (solutionId, workflowId) => {
    try {
      await solutionsAPI.removeWorkflow(solutionId, workflowId);
      fetchSolutions();
      setError(null);
    } catch (err) {
      console.error('Error removing workflow:', err);
      setError('Failed to remove workflow');
    }
  };

  const loadCommunications = async (solutionId) => {
    try {
      const response = await solutionsAPI.getCommunications(solutionId);
      setCommunications(response.data || []);
    } catch (err) {
      console.error('Error loading communications:', err);
    }
  };

  const toggleWorkflow = (workflowId) => {
    setFormData(prev => ({
      ...prev,
      workflows: prev.workflows.includes(workflowId)
        ? prev.workflows.filter(id => id !== workflowId)
        : [...prev.workflows, workflowId]
    }));
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-purple-500"></div>
      </div>
    );
  }

  return (
    <div className="p-6 min-h-screen">
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
              Manage solutions containing multiple workflows with shared context
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
                  {/* ID (only for new solutions) */}
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

                  {/* Name */}
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

                  {/* Description */}
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

                  {/* Workflows */}
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      Workflows
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

                  {/* Actions */}
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
            <FaProjectDiagram className="mx-auto text-gray-600 mb-4" size={48} />
            <h3 className="text-xl font-semibold text-white mb-2">No Solutions Yet</h3>
            <p className="text-gray-400 mb-4">
              Create your first solution to manage multiple workflows with shared context
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
                      <div className="flex items-center gap-3 mb-1">
                        <h3 className="text-xl font-bold text-white">{solution.name}</h3>
                        <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                          solution.solution_type === 'research' 
                            ? 'bg-purple-500/20 text-purple-400 border border-purple-500/50' 
                            : 'bg-green-500/20 text-green-400 border border-green-500/50'
                        }`}>
                          {solution.solution_type === 'research' ? '🔬 Research (Agentic RAG)' : '💡 Normal (KAG+Buffer)'}
                        </span>
                      </div>
                      <p className="text-sm text-gray-500 mb-2">{solution.id}</p>
                      {solution.description && (
                        <p className="text-gray-400 mb-3">{solution.description}</p>
                      )}
                      <div className="flex gap-4 text-sm text-gray-500">
                        <span className="flex items-center gap-1">
                          <FaNetworkWired />
                          {solution.workflows?.length || 0} workflow(s)
                        </span>
                        {solution.created_at && (
                          <span>
                            Created: {new Date(solution.created_at).toLocaleDateString()}
                          </span>
                        )}
                      </div>
                    </div>
                    <div className="flex gap-2">
                      <button
                        onClick={() => setActiveChatSolution(solution.id)}
                        className="p-2 text-purple-400 hover:bg-purple-900/30 rounded transition-colors"
                        title="Open Chat"
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
                        onClick={() => loadCommunications(solution.id)}
                        className="p-2 text-green-400 hover:bg-green-900/30 rounded transition-colors"
                        title="View Communications"
                      >
                        <FaNetworkWired />
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

                  {/* Workflows */}
                  {solution.workflows && solution.workflows.length > 0 && (
                    <div className="mt-4 pt-4 border-t border-gray-800">
                      <h4 className="text-sm font-semibold text-gray-400 mb-2">Workflows:</h4>
                      <div className="flex flex-wrap gap-2">
                        {solution.workflows.map(workflowId => {
                          const workflow = workflows.find(w => w.id === workflowId);
                          return (
                            <span
                              key={workflowId}
                              className="inline-flex items-center gap-2 px-3 py-1 bg-blue-900/30 text-blue-300 border border-blue-700/50 rounded-full text-sm"
                            >
                              {workflow?.name || workflowId}
                              <button
                                onClick={() => handleRemoveWorkflow(solution.id, workflowId)}
                                className="text-blue-400 hover:text-blue-200 transition-colors"
                                title="Remove from solution"
                              >
                                <FaTimes size={12} />
                              </button>
                            </span>
                          );
                        })}
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

export default Solutions;
