import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FaRobot, FaPlus, FaEdit, FaTrash, FaTimes, FaSave } from 'react-icons/fa';
import { agentsAPI, toolsAPI } from '../services/api';

const AgentCard = ({ agent, onEdit, onDelete }) => {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.9 }}
      className="card p-6"
    >
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className="p-3 rounded-lg bg-gradient-to-br from-agent-primary to-agent-secondary">
            <FaRobot className="text-2xl" />
          </div>
          <div>
            <h3 className="text-xl font-bold">{agent.name}</h3>
            <p className="text-sm text-gray-400">{agent.id}</p>
          </div>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => onEdit(agent)}
            className="p-2 rounded-lg bg-dark-bg hover:bg-agent-primary transition-colors"
          >
            <FaEdit />
          </button>
          <button
            onClick={() => onDelete(agent.id)}
            className="p-2 rounded-lg bg-dark-bg hover:bg-red-500 transition-colors"
          >
            <FaTrash />
          </button>
        </div>
      </div>

      <div className="space-y-2 text-sm">
        <div className="flex justify-between">
          <span className="text-gray-400">Type:</span>
          <span className="font-medium">{agent.type}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-400">LLM:</span>
          <span className="font-medium">{agent.llm_config?.model || 'N/A'}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-400">Tools:</span>
          <span className="font-medium">{agent.tools?.length || 0}</span>
        </div>
      </div>

      {agent.tools && agent.tools.length > 0 && (
        <div className="mt-4 pt-4 border-t border-dark-border">
          <p className="text-xs text-gray-400 mb-2">Assigned Tools:</p>
          <div className="flex flex-wrap gap-2">
            {agent.tools.map((tool) => (
              <span
                key={tool}
                className="px-2 py-1 text-xs rounded-full bg-tool-primary bg-opacity-20 text-tool-primary"
              >
                {tool}
              </span>
            ))}
          </div>
        </div>
      )}
    </motion.div>
  );
};

const AgentModal = ({ agent, onSave, onClose, availableTools }) => {
  const [formData, setFormData] = useState(
    agent || {
      id: '',
      name: '',
      type: 'react',
      llm_config: {
        provider: 'groq',
        model: 'llama-3.1-70b-versatile',
        temperature: 0.7,
        max_tokens: 1000,
      },
      tools: [],
    }
  );

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(formData);
  };

  const toggleTool = (toolId) => {
    setFormData((prev) => ({
      ...prev,
      tools: prev.tools.includes(toolId)
        ? prev.tools.filter((t) => t !== toolId)
        : [...prev.tools, toolId],
    }));
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.9 }}
        className="modal-content"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold flex items-center gap-2">
            <FaRobot className="text-agent-primary" />
            {agent ? 'Edit Agent' : 'Create New Agent'}
          </h2>
          <button
            onClick={onClose}
            className="p-2 rounded-lg hover:bg-dark-hover transition-colors"
          >
            <FaTimes />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-2">Agent ID</label>
              <input
                type="text"
                className="input-field"
                value={formData.id}
                onChange={(e) => setFormData({ ...formData, id: e.target.value })}
                placeholder="unique_agent_id"
                required
                disabled={!!agent}
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Agent Name</label>
              <input
                type="text"
                className="input-field"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                placeholder="My AI Agent"
                required
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Agent Type</label>
            <select
              className="select-field"
              value={formData.type}
              onChange={(e) => setFormData({ ...formData, type: e.target.value })}
            >
              <option value="zero_shot">Zero Shot</option>
              <option value="react">ReAct</option>
              <option value="custom">Custom</option>
            </select>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-2">LLM Model</label>
              <select
                className="select-field"
                value={formData.llm_config.model}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    llm_config: { ...formData.llm_config, model: e.target.value },
                  })
                }
              >
                <option value="llama-3.1-70b-versatile">Llama 3.1 70B</option>
                <option value="llama-3.1-8b-instant">Llama 3.1 8B Instant</option>
                <option value="claude-sonnet-4-5">Claude Sonnet 4.5</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Temperature</label>
              <input
                type="number"
                className="input-field"
                value={formData.llm_config.temperature}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    llm_config: { ...formData.llm_config, temperature: parseFloat(e.target.value) },
                  })
                }
                min="0"
                max="1"
                step="0.1"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Assign Tools</label>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-2 max-h-40 overflow-y-auto p-4 bg-dark-bg rounded-lg">
              {availableTools.map((tool) => (
                <label
                  key={tool.id}
                  className="flex items-center gap-2 p-2 rounded hover:bg-dark-hover cursor-pointer transition-colors"
                >
                  <input
                    type="checkbox"
                    checked={formData.tools.includes(tool.id)}
                    onChange={() => toggleTool(tool.id)}
                    className="form-checkbox text-agent-primary"
                  />
                  <span className="text-sm">{tool.name}</span>
                </label>
              ))}
            </div>
          </div>

          <div className="flex gap-4 justify-end">
            <button
              type="button"
              onClick={onClose}
              className="px-6 py-3 rounded-lg bg-dark-bg hover:bg-dark-hover transition-colors"
            >
              Cancel
            </button>
            <button type="submit" className="btn-agent flex items-center gap-2">
              <FaSave /> {agent ? 'Update Agent' : 'Create Agent'}
            </button>
          </div>
        </form>
      </motion.div>
    </div>
  );
};

const Agents = () => {
  const [agents, setAgents] = useState([]);
  const [tools, setTools] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [editingAgent, setEditingAgent] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [agentsRes, toolsRes] = await Promise.all([
        agentsAPI.getAll(),
        toolsAPI.getAll(),
      ]);
      setAgents(agentsRes.data);
      setTools(toolsRes.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async (agentData) => {
    try {
      if (editingAgent) {
        await agentsAPI.update(agentData.id, agentData);
      } else {
        await agentsAPI.create(agentData);
      }
      await fetchData();
      setShowModal(false);
      setEditingAgent(null);
    } catch (error) {
      console.error('Error saving agent:', error);
      alert('Error saving agent: ' + (error.response?.data?.detail || error.message));
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this agent?')) {
      try {
        await agentsAPI.delete(id);
        await fetchData();
      } catch (error) {
        console.error('Error deleting agent:', error);
        alert('Error deleting agent: ' + (error.response?.data?.detail || error.message));
      }
    }
  };

  const handleEdit = (agent) => {
    setEditingAgent(agent);
    setShowModal(true);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-agent-primary"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold mb-2">Agents</h1>
          <p className="text-gray-400">Manage your AI agents</p>
        </div>
        <button
          onClick={() => {
            setEditingAgent(null);
            setShowModal(true);
          }}
          className="btn-agent flex items-center gap-2"
        >
          <FaPlus /> Create Agent
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {agents.map((agent) => (
          <AgentCard
            key={agent.id}
            agent={agent}
            onEdit={handleEdit}
            onDelete={handleDelete}
          />
        ))}
      </div>

      {agents.length === 0 && (
        <div className="card p-12 text-center">
          <FaRobot className="text-6xl text-gray-600 mx-auto mb-4" />
          <h3 className="text-xl font-bold mb-2">No agents yet</h3>
          <p className="text-gray-400 mb-4">Create your first AI agent to get started</p>
          <button
            onClick={() => setShowModal(true)}
            className="btn-agent flex items-center gap-2 mx-auto"
          >
            <FaPlus /> Create First Agent
          </button>
        </div>
      )}

      <AnimatePresence>
        {showModal && (
          <AgentModal
            agent={editingAgent}
            onSave={handleSave}
            onClose={() => {
              setShowModal(false);
              setEditingAgent(null);
            }}
            availableTools={tools}
          />
        )}
      </AnimatePresence>
    </div>
  );
};

export default Agents;
