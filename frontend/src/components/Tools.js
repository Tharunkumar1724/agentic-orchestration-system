import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FaTools, FaPlus, FaEdit, FaTrash, FaTimes, FaSave, FaCode, FaLink } from 'react-icons/fa';
import { 
  Globe, 
  Network, 
  Database, 
  FileText, 
  Terminal, 
  Zap, 
  GitBranch,
  Wrench,
  Settings 
} from 'lucide-react';
import { toolsAPI } from '../services/api';

const TOOL_TYPE_CONFIG = {
  websearch: { icon: Globe, color: 'blue', label: 'Web Search', bgColor: 'bg-blue-500' },
  api: { icon: Network, color: 'green', label: 'API Call', bgColor: 'bg-green-500' },
  http: { icon: Zap, color: 'purple', label: 'HTTP Request', bgColor: 'bg-purple-500' },
  graphql: { icon: GitBranch, color: 'pink', label: 'GraphQL', bgColor: 'bg-pink-500' },
  code: { icon: FaCode, color: 'yellow', label: 'Code Execution', bgColor: 'bg-yellow-500' },
  python: { icon: Terminal, color: 'cyan', label: 'Python Script', bgColor: 'bg-cyan-500' },
  shell: { icon: Terminal, color: 'gray', label: 'Shell Command', bgColor: 'bg-gray-500' },
  database: { icon: Database, color: 'indigo', label: 'Database Query', bgColor: 'bg-indigo-500' },
  file: { icon: FileText, color: 'orange', label: 'File Operation', bgColor: 'bg-orange-500' },
  custom: { icon: Wrench, color: 'red', label: 'Custom Tool', bgColor: 'bg-red-500' },
  function: { icon: FaCode, color: 'blue', label: 'Function', bgColor: 'bg-blue-500' }
};

const ToolCard = ({ tool, onEdit, onDelete }) => {
  const typeConfig = TOOL_TYPE_CONFIG[tool.type] || TOOL_TYPE_CONFIG.custom;
  const IconComponent = typeConfig.icon;

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.9 }}
      className="card p-6"
    >
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className={`p-3 rounded-lg ${typeConfig.bgColor}`}>
            {typeof IconComponent === 'function' && IconComponent.prototype ? (
              <IconComponent className="text-2xl text-white" />
            ) : (
              <IconComponent className="w-6 h-6 text-white" />
            )}
          </div>
          <div>
            <h3 className="text-xl font-bold">{tool.name}</h3>
            <p className="text-sm text-gray-400">{tool.id}</p>
            <span className={`inline-block mt-1 px-2 py-1 rounded text-xs font-medium ${typeConfig.bgColor} bg-opacity-20 text-${typeConfig.color}-400`}>
              {typeConfig.label}
            </span>
          </div>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => onEdit(tool)}
            className="p-2 rounded-lg bg-dark-bg hover:bg-tool-primary transition-colors"
          >
            <FaEdit />
          </button>
          <button
            onClick={() => onDelete(tool.id)}
            className="p-2 rounded-lg bg-dark-bg hover:bg-red-500 transition-colors"
          >
            <FaTrash />
          </button>
        </div>
      </div>

      <div className="space-y-2 text-sm">
        {tool.description && (
          <div className="mt-2 pt-2 border-t border-dark-border">
            <p className="text-xs text-gray-400">{tool.description}</p>
          </div>
        )}
        {tool.config && Object.keys(tool.config).length > 0 && (
          <div className="mt-2 pt-2 border-t border-dark-border">
            <div className="flex items-center gap-2 mb-2">
              <Settings className="w-4 h-4 text-gray-400" />
              <span className="text-xs font-medium text-gray-400">Configuration</span>
            </div>
            {tool.type === 'api' && tool.config.url && (
              <div className="text-xs space-y-1">
                <div className="flex justify-between">
                  <span className="text-gray-400">Method:</span>
                  <span className="font-mono text-tool-primary">{tool.config.method || 'GET'}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">URL:</span>
                  <span className="font-mono text-xs truncate max-w-[200px]" title={tool.config.url}>
                    {tool.config.url}
                  </span>
                </div>
              </div>
            )}
            {tool.type === 'websearch' && (
              <div className="text-xs space-y-1">
                <div className="flex justify-between">
                  <span className="text-gray-400">Max Results:</span>
                  <span className="font-mono">{tool.config.max_results || 5}</span>
                </div>
                {tool.config.region && (
                  <div className="flex justify-between">
                    <span className="text-gray-400">Region:</span>
                    <span className="font-mono">{tool.config.region}</span>
                  </div>
                )}
              </div>
            )}
            {tool.type === 'database' && (
              <div className="text-xs space-y-1">
                {tool.config.db_type && (
                  <div className="flex justify-between">
                    <span className="text-gray-400">Database:</span>
                    <span className="font-mono capitalize">{tool.config.db_type}</span>
                  </div>
                )}
              </div>
            )}
            {(tool.type === 'python' || tool.type === 'shell' || tool.type === 'code') && (
              <div className="text-xs">
                <div className="flex justify-between">
                  <span className="text-gray-400">Timeout:</span>
                  <span className="font-mono">{tool.config.timeout || 30}s</span>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </motion.div>
  );
};

const ToolModal = ({ tool, onSave, onClose }) => {
  const [formData, setFormData] = useState(
    tool || {
      id: `tool_${Date.now()}`,
      name: '',
      type: 'function',
      description: '',
      config: {},
      function_code: '',
    }
  );

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Ensure ID is unique and valid
    const finalData = {
      ...formData,
      id: formData.id.trim() || `tool_${Date.now()}`,
    };
    
    onSave(finalData);
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
            <FaTools className="text-tool-primary" />
            {tool ? 'Edit Tool' : 'Create New Tool'}
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
              <label className="block text-sm font-medium mb-2">Tool ID</label>
              <input
                type="text"
                className="input-field"
                value={formData.id}
                onChange={(e) => setFormData({ ...formData, id: e.target.value })}
                placeholder="auto-generated if empty"
                disabled={!!tool}
              />
              {!tool && (
                <p className="text-xs text-gray-400 mt-1">Auto-generated if left empty</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Tool Name</label>
              <input
                type="text"
                className="input-field"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                placeholder="My Tool"
                required
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Tool Type</label>
            <select
              className="select-field"
              value={formData.type}
              onChange={(e) => setFormData({ ...formData, type: e.target.value })}
            >
              <option value="function">Function</option>
              <option value="websearch">Web Search</option>
              <option value="api">API Call</option>
              <option value="http">HTTP Request</option>
              <option value="graphql">GraphQL</option>
              <option value="code">Code Execution</option>
              <option value="python">Python Script</option>
              <option value="shell">Shell Command</option>
              <option value="database">Database Query</option>
              <option value="file">File Operation</option>
              <option value="custom">Custom</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Description</label>
            <textarea
              className="input-field"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              placeholder="What does this tool do?"
              rows="3"
            />
          </div>

          {formData.type === 'api' && (
            <div className="space-y-4 p-4 bg-dark-bg rounded-lg border border-dark-border">
              <h3 className="font-semibold text-tool-primary">API Configuration</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Method</label>
                  <select
                    className="select-field"
                    value={formData.config.method || 'GET'}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        config: { ...formData.config, method: e.target.value },
                      })
                    }
                  >
                    <option value="GET">GET</option>
                    <option value="POST">POST</option>
                    <option value="PUT">PUT</option>
                    <option value="DELETE">DELETE</option>
                    <option value="PATCH">PATCH</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Timeout (seconds)</label>
                  <input
                    type="number"
                    className="input-field"
                    value={formData.config.timeout || 30}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        config: { ...formData.config, timeout: parseInt(e.target.value) },
                      })
                    }
                    min="1"
                    max="300"
                  />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">URL</label>
                <input
                  type="text"
                  className="input-field"
                  value={formData.config.url || ''}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      config: { ...formData.config, url: e.target.value },
                    })
                  }
                  placeholder="https://api.example.com/endpoint"
                />
              </div>
            </div>
          )}

          {formData.type === 'websearch' && (
            <div className="space-y-4 p-4 bg-dark-bg rounded-lg border border-dark-border">
              <h3 className="font-semibold text-tool-primary">Web Search Configuration</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Max Results</label>
                  <input
                    type="number"
                    className="input-field"
                    value={formData.config.max_results || 5}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        config: { ...formData.config, max_results: parseInt(e.target.value) },
                      })
                    }
                    min="1"
                    max="20"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Region</label>
                  <input
                    type="text"
                    className="input-field"
                    value={formData.config.region || 'wt-wt'}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        config: { ...formData.config, region: e.target.value },
                      })
                    }
                    placeholder="wt-wt (worldwide)"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">SafeSearch</label>
                  <select
                    className="select-field"
                    value={formData.config.safesearch || 'moderate'}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        config: { ...formData.config, safesearch: e.target.value },
                      })
                    }
                  >
                    <option value="off">Off</option>
                    <option value="moderate">Moderate</option>
                    <option value="strict">Strict</option>
                  </select>
                </div>
              </div>
            </div>
          )}

          {formData.type === 'database' && (
            <div className="space-y-4 p-4 bg-dark-bg rounded-lg border border-dark-border">
              <h3 className="font-semibold text-tool-primary">Database Configuration</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Database Type</label>
                  <select
                    className="select-field"
                    value={formData.config.db_type || 'postgresql'}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        config: { ...formData.config, db_type: e.target.value },
                      })
                    }
                  >
                    <option value="postgresql">PostgreSQL</option>
                    <option value="mysql">MySQL</option>
                    <option value="sqlite">SQLite</option>
                    <option value="mongodb">MongoDB</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Connection String</label>
                  <input
                    type="text"
                    className="input-field"
                    value={formData.config.connection_string || ''}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        config: { ...formData.config, connection_string: e.target.value },
                      })
                    }
                    placeholder="postgresql://user:pass@host:port/db"
                  />
                </div>
              </div>
            </div>
          )}

          {(formData.type === 'python' || formData.type === 'shell' || formData.type === 'code') && (
            <div className="space-y-4 p-4 bg-dark-bg rounded-lg border border-dark-border">
              <h3 className="font-semibold text-tool-primary">Execution Configuration</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Timeout (seconds)</label>
                  <input
                    type="number"
                    className="input-field"
                    value={formData.config.timeout || 30}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        config: { ...formData.config, timeout: parseInt(e.target.value) },
                      })
                    }
                    min="1"
                    max="300"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Working Directory</label>
                  <input
                    type="text"
                    className="input-field"
                    value={formData.config.working_dir || ''}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        config: { ...formData.config, working_dir: e.target.value },
                      })
                    }
                    placeholder="/path/to/working/directory"
                  />
                </div>
              </div>
            </div>
          )}

          {formData.type === 'http' && (
            <div className="space-y-4 p-4 bg-dark-bg rounded-lg border border-dark-border">
              <h3 className="font-semibold text-tool-primary">HTTP Configuration</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Method</label>
                  <select
                    className="select-field"
                    value={formData.config.method || 'GET'}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        config: { ...formData.config, method: e.target.value },
                      })
                    }
                  >
                    <option value="GET">GET</option>
                    <option value="POST">POST</option>
                    <option value="PUT">PUT</option>
                    <option value="DELETE">DELETE</option>
                    <option value="PATCH">PATCH</option>
                    <option value="HEAD">HEAD</option>
                    <option value="OPTIONS">OPTIONS</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Timeout (seconds)</label>
                  <input
                    type="number"
                    className="input-field"
                    value={formData.config.timeout || 30}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        config: { ...formData.config, timeout: parseInt(e.target.value) },
                      })
                    }
                    min="1"
                    max="300"
                  />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">URL</label>
                <input
                  type="text"
                  className="input-field"
                  value={formData.config.url || ''}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      config: { ...formData.config, url: e.target.value },
                    })
                  }
                  placeholder="https://example.com/endpoint"
                />
              </div>
            </div>
          )}

          {formData.type === 'graphql' && (
            <div className="space-y-4 p-4 bg-dark-bg rounded-lg border border-dark-border">
              <h3 className="font-semibold text-tool-primary">GraphQL Configuration</h3>
              <div>
                <label className="block text-sm font-medium mb-2">Endpoint URL</label>
                <input
                  type="text"
                  className="input-field"
                  value={formData.config.url || ''}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      config: { ...formData.config, url: e.target.value },
                    })
                  }
                  placeholder="https://api.example.com/graphql"
                />
              </div>
            </div>
          )}

          {formData.type === 'file' && (
            <div className="space-y-4 p-4 bg-dark-bg rounded-lg border border-dark-border">
              <h3 className="font-semibold text-tool-primary">File Operation Configuration</h3>
              <div>
                <label className="block text-sm font-medium mb-2">Operation Type</label>
                <select
                  className="select-field"
                  value={formData.config.operation || 'read'}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      config: { ...formData.config, operation: e.target.value },
                    })
                  }
                >
                  <option value="read">Read</option>
                  <option value="write">Write</option>
                  <option value="append">Append</option>
                  <option value="delete">Delete</option>
                  <option value="list">List</option>
                </select>
              </div>
            </div>
          )}

          {formData.type === 'function' && (
            <div>
              <label className="block text-sm font-medium mb-2">Function Code (Python)</label>
              <textarea
                className="input-field font-mono text-sm"
                value={formData.function_code || ''}
                onChange={(e) => setFormData({ ...formData, function_code: e.target.value })}
                placeholder="def my_function(input):\n    # Your code here\n    return result"
                rows="8"
              />
            </div>
          )}

          <div className="flex gap-4 justify-end">
            <button
              type="button"
              onClick={onClose}
              className="px-6 py-3 rounded-lg bg-dark-bg hover:bg-dark-hover transition-colors"
            >
              Cancel
            </button>
            <button type="submit" className="btn-tool flex items-center gap-2">
              <FaSave /> {tool ? 'Update Tool' : 'Create Tool'}
            </button>
          </div>
        </form>
      </motion.div>
    </div>
  );
};

const Tools = () => {
  const [tools, setTools] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [editingTool, setEditingTool] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTools();
  }, []);

  const fetchTools = async () => {
    try {
      const response = await toolsAPI.getAll();
      setTools(response.data);
    } catch (error) {
      console.error('Error fetching tools:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async (toolData) => {
    try {
      if (editingTool) {
        await toolsAPI.update(toolData.id, toolData);
      } else {
        await toolsAPI.create(toolData);
      }
      await fetchTools();
      setShowModal(false);
      setEditingTool(null);
    } catch (error) {
      console.error('Error saving tool:', error);
      alert('Error saving tool: ' + (error.response?.data?.detail || error.message));
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this tool?')) {
      try {
        await toolsAPI.delete(id);
        await fetchTools();
      } catch (error) {
        console.error('Error deleting tool:', error);
        alert('Error deleting tool: ' + (error.response?.data?.detail || error.message));
      }
    }
  };

  const handleEdit = (tool) => {
    setEditingTool(tool);
    setShowModal(true);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-tool-primary"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold mb-2">Tools</h1>
          <p className="text-gray-400">Manage your AI tools and integrations</p>
        </div>
        <button
          onClick={() => {
            setEditingTool(null);
            setShowModal(true);
          }}
          className="btn-tool flex items-center gap-2"
        >
          <FaPlus /> Create Tool
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {tools.map((tool) => (
          <ToolCard
            key={tool.id}
            tool={tool}
            onEdit={handleEdit}
            onDelete={handleDelete}
          />
        ))}
      </div>

      {tools.length === 0 && (
        <div className="card p-12 text-center">
          <FaTools className="text-6xl text-gray-600 mx-auto mb-4" />
          <h3 className="text-xl font-bold mb-2">No tools yet</h3>
          <p className="text-gray-400 mb-4">Create your first tool to get started</p>
          <button
            onClick={() => setShowModal(true)}
            className="btn-tool flex items-center gap-2 mx-auto"
          >
            <FaPlus /> Create First Tool
          </button>
        </div>
      )}

      <AnimatePresence>
        {showModal && (
          <ToolModal
            tool={editingTool}
            onSave={handleSave}
            onClose={() => {
              setShowModal(false);
              setEditingTool(null);
            }}
          />
        )}
      </AnimatePresence>
    </div>
  );
};

export default Tools;
