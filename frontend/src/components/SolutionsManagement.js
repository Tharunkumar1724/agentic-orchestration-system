import React, { useState, useEffect } from 'react';
import { solutionsAPI, workflowsAPI } from '../services/api';
import { 
  FaPlus, FaEdit, FaTrash, FaProjectDiagram, FaComments, 
  FaCog, FaSave, FaTimes, FaNetworkWired 
} from 'react-icons/fa';
import SolutionChat from './SolutionChat';

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
        <div className="text-gray-600">Loading solutions...</div>
      </div>
    );
  }

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      {/* Solution Chat Modal */}
      {activeChatSolution && (
        <SolutionChat
          solutionId={activeChatSolution}
          onClose={() => setActiveChatSolution(null)}
        />
      )}

      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-800">Solutions</h1>
            <p className="text-gray-600 mt-1">
              Manage solutions containing multiple workflows with shared context
            </p>
          </div>
          <button
            onClick={handleCreate}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center gap-2"
          >
            <FaPlus /> Create Solution
          </button>
        </div>

        {/* Error Display */}
        {error && (
          <div className="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
            {error}
          </div>
        )}

        {/* Solution Form Modal */}
        {showForm && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-lg shadow-xl max-w-3xl w-full max-h-[90vh] overflow-y-auto">
              <div className="p-6">
                <div className="flex justify-between items-center mb-6">
                  <h2 className="text-2xl font-bold">
                    {selectedSolution ? 'Edit Solution' : 'Create Solution'}
                  </h2>
                  <button
                    onClick={() => setShowForm(false)}
                    className="text-gray-500 hover:text-gray-700"
                  >
                    <FaTimes size={24} />
                  </button>
                </div>

                <form onSubmit={handleSubmit} className="space-y-4">
                  {/* ID (only for new solutions) */}
                  {!selectedSolution && (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        ID (optional - auto-generated if empty)
                      </label>
                      <input
                        type="text"
                        value={formData.id}
                        onChange={(e) => setFormData({ ...formData, id: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                        placeholder="solution_id"
                      />
                    </div>
                  )}

                  {/* Name */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Name *
                    </label>
                    <input
                      type="text"
                      value={formData.name}
                      onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                      required
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                      placeholder="My Solution"
                    />
                  </div>

                  {/* Description */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Description
                    </label>
                    <textarea
                      value={formData.description}
                      onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                      rows="3"
                      placeholder="Solution description..."
                    />
                  </div>

                  {/* Workflows */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Workflows
                    </label>
                    <div className="border border-gray-300 rounded-lg p-4 max-h-60 overflow-y-auto">
                      {workflows.length === 0 ? (
                        <p className="text-gray-500 text-sm">No workflows available</p>
                      ) : (
                        <div className="space-y-2">
                          {workflows.map(workflow => (
                            <label key={workflow.id} className="flex items-center gap-2 cursor-pointer hover:bg-gray-50 p-2 rounded">
                              <input
                                type="checkbox"
                                checked={formData.workflows.includes(workflow.id)}
                                onChange={() => toggleWorkflow(workflow.id)}
                                className="w-4 h-4 text-blue-600"
                              />
                              <div className="flex-1">
                                <div className="font-medium text-sm">{workflow.name}</div>
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
                      className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center justify-center gap-2"
                    >
                      <FaSave /> {selectedSolution ? 'Update' : 'Create'}
                    </button>
                    <button
                      type="button"
                      onClick={() => setShowForm(false)}
                      className="px-4 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400"
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
          <div className="bg-white rounded-lg shadow-md p-12 text-center">
            <FaProjectDiagram className="mx-auto text-gray-400 mb-4" size={48} />
            <h3 className="text-xl font-semibold text-gray-700 mb-2">No Solutions Yet</h3>
            <p className="text-gray-600 mb-4">
              Create your first solution to manage multiple workflows with shared context
            </p>
            <button
              onClick={handleCreate}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              Create Solution
            </button>
          </div>
        ) : (
          <div className="grid gap-6">
            {solutions.map(solution => (
              <div key={solution.id} className="bg-white rounded-lg shadow-md overflow-hidden">
                <div className="p-6">
                  {/* Header */}
                  <div className="flex justify-between items-start mb-4">
                    <div className="flex-1">
                      <h3 className="text-xl font-bold text-gray-800 mb-1">{solution.name}</h3>
                      <p className="text-sm text-gray-600 mb-2">{solution.id}</p>
                      {solution.description && (
                        <p className="text-gray-700 mb-3">{solution.description}</p>
                      )}
                      <div className="flex gap-4 text-sm text-gray-600">
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
                        className="p-2 text-purple-600 hover:bg-purple-50 rounded"
                        title="Open Chat"
                      >
                        <FaComments />
                      </button>
                      <button
                        onClick={() => handleEdit(solution)}
                        className="p-2 text-blue-600 hover:bg-blue-50 rounded"
                        title="Edit"
                      >
                        <FaEdit />
                      </button>
                      <button
                        onClick={() => loadCommunications(solution.id)}
                        className="p-2 text-green-600 hover:bg-green-50 rounded"
                        title="View Communications"
                      >
                        <FaNetworkWired />
                      </button>
                      <button
                        onClick={() => handleDelete(solution.id)}
                        className="p-2 text-red-600 hover:bg-red-50 rounded"
                        title="Delete"
                      >
                        <FaTrash />
                      </button>
                    </div>
                  </div>

                  {/* Workflows */}
                  {solution.workflows && solution.workflows.length > 0 && (
                    <div className="mt-4 pt-4 border-t border-gray-200">
                      <h4 className="text-sm font-semibold text-gray-700 mb-2">Workflows:</h4>
                      <div className="flex flex-wrap gap-2">
                        {solution.workflows.map(workflowId => {
                          const workflow = workflows.find(w => w.id === workflowId);
                          return (
                            <span
                              key={workflowId}
                              className="inline-flex items-center gap-2 px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm"
                            >
                              {workflow?.name || workflowId}
                              <button
                                onClick={() => handleRemoveWorkflow(solution.id, workflowId)}
                                className="text-blue-600 hover:text-blue-800"
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
