import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Wrench,
  Globe,
  Code,
  Database,
  FileText,
  Terminal,
  Network,
  Zap,
  Settings,
  Play,
  TrendingUp,
  AlertCircle,
  CheckCircle,
  Clock,
  BarChart3,
  GitBranch,
  RefreshCw,
  Layers
} from 'lucide-react';

const TOOL_TYPES = {
  websearch: { icon: Globe, color: 'blue', label: 'Web Search' },
  api: { icon: Network, color: 'green', label: 'API Call' },
  http: { icon: Zap, color: 'purple', label: 'HTTP Request' },
  graphql: { icon: GitBranch, color: 'pink', label: 'GraphQL' },
  code: { icon: Code, color: 'yellow', label: 'Code Execution' },
  python: { icon: Terminal, color: 'cyan', label: 'Python Script' },
  shell: { icon: Terminal, color: 'gray', label: 'Shell Command' },
  database: { icon: Database, color: 'indigo', label: 'Database Query' },
  file: { icon: FileText, color: 'orange', label: 'File Operation' },
  custom: { icon: Wrench, color: 'red', label: 'Custom Tool' }
};

const EXECUTION_STRATEGIES = [
  {
    id: 'sequential',
    name: 'Sequential',
    description: 'Execute tools one after another, passing results between them',
    icon: Layers,
    color: 'blue'
  },
  {
    id: 'parallel',
    name: 'Parallel',
    description: 'Execute all tools simultaneously for faster execution',
    icon: GitBranch,
    color: 'green'
  },
  {
    id: 'conditional',
    name: 'Conditional',
    description: 'Execute tools based on conditions and previous results',
    icon: AlertCircle,
    color: 'yellow'
  },
  {
    id: 'retry',
    name: 'Retry',
    description: 'Automatically retry failed tools with exponential backoff',
    icon: RefreshCw,
    color: 'orange'
  },
  {
    id: 'fallback',
    name: 'Fallback',
    description: 'Try alternative tools if primary tools fail',
    icon: Layers,
    color: 'purple'
  }
];

const ToolTypeCard = ({ type, config, onSelect, isSelected }) => {
  const typeInfo = TOOL_TYPES[type] || TOOL_TYPES.custom;
  const Icon = typeInfo.icon;

  return (
    <motion.div
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      onClick={onSelect}
      className={`p-4 rounded-lg border-2 cursor-pointer transition-all ${
        isSelected
          ? `border-${typeInfo.color}-500 bg-${typeInfo.color}-50 shadow-lg`
          : 'border-gray-200 bg-white hover:border-gray-300'
      }`}
    >
      <div className="flex items-center space-x-3">
        <div className={`p-2 rounded-lg bg-${typeInfo.color}-100`}>
          <Icon className={`w-5 h-5 text-${typeInfo.color}-600`} />
        </div>
        <div className="flex-1">
          <h4 className="font-semibold text-gray-800">{typeInfo.label}</h4>
          <p className="text-sm text-gray-500">{type}</p>
        </div>
        {isSelected && (
          <CheckCircle className={`w-5 h-5 text-${typeInfo.color}-600`} />
        )}
      </div>
    </motion.div>
  );
};

const ExecutionStrategyCard = ({ strategy, onSelect, isSelected }) => {
  const Icon = strategy.icon;

  return (
    <motion.div
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      onClick={onSelect}
      className={`p-4 rounded-lg border-2 cursor-pointer transition-all ${
        isSelected
          ? `border-${strategy.color}-500 bg-${strategy.color}-50 shadow-lg`
          : 'border-gray-200 bg-white hover:border-gray-300'
      }`}
    >
      <div className="flex items-start space-x-3">
        <div className={`p-2 rounded-lg bg-${strategy.color}-100`}>
          <Icon className={`w-5 h-5 text-${strategy.color}-600`} />
        </div>
        <div className="flex-1">
          <h4 className="font-semibold text-gray-800">{strategy.name}</h4>
          <p className="text-sm text-gray-600 mt-1">{strategy.description}</p>
        </div>
        {isSelected && (
          <CheckCircle className={`w-5 h-5 text-${strategy.color}-600`} />
        )}
      </div>
    </motion.div>
  );
};

const ToolExecutionVisualizer = ({ executionHistory }) => {
  if (!executionHistory || executionHistory.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        No execution history available
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {executionHistory.map((execution, idx) => {
        const typeInfo = TOOL_TYPES[execution.tool_type] || TOOL_TYPES.custom;
        const Icon = typeInfo.icon;
        const isSuccess = execution.success;

        return (
          <motion.div
            key={idx}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: idx * 0.1 }}
            className={`p-4 rounded-lg border-2 ${
              isSuccess
                ? 'border-green-200 bg-green-50'
                : 'border-red-200 bg-red-50'
            }`}
          >
            <div className="flex items-start justify-between">
              <div className="flex items-start space-x-3 flex-1">
                <div className={`p-2 rounded-lg ${isSuccess ? 'bg-green-100' : 'bg-red-100'}`}>
                  <Icon className={`w-5 h-5 ${isSuccess ? 'text-green-600' : 'text-red-600'}`} />
                </div>
                <div className="flex-1">
                  <div className="flex items-center space-x-2">
                    <h5 className="font-semibold text-gray-800">
                      {execution.tool_name || 'Unknown Tool'}
                    </h5>
                    <span className={`px-2 py-0.5 rounded text-xs font-medium ${
                      isSuccess ? 'bg-green-200 text-green-800' : 'bg-red-200 text-red-800'
                    }`}>
                      {isSuccess ? 'Success' : 'Failed'}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 mt-1">
                    Type: {typeInfo.label}
                  </p>
                  {execution.error && (
                    <p className="text-sm text-red-600 mt-2 flex items-center">
                      <AlertCircle className="w-4 h-4 mr-1" />
                      {execution.error}
                    </p>
                  )}
                  {execution.data && (
                    <div className="mt-2 p-2 bg-white rounded text-xs font-mono">
                      <pre className="whitespace-pre-wrap">
                        {JSON.stringify(execution.data, null, 2).substring(0, 200)}
                        {JSON.stringify(execution.data).length > 200 && '...'}
                      </pre>
                    </div>
                  )}
                </div>
              </div>
              <div className="flex flex-col items-end space-y-1">
                <div className="flex items-center text-sm text-gray-500">
                  <Clock className="w-4 h-4 mr-1" />
                  {execution.execution_time?.toFixed(3)}s
                </div>
                {execution.retry_count > 0 && (
                  <div className="flex items-center text-xs text-orange-600">
                    <RefreshCw className="w-3 h-3 mr-1" />
                    Retried {execution.retry_count}x
                  </div>
                )}
              </div>
            </div>
          </motion.div>
        );
      })}
    </div>
  );
};

const ToolStatistics = ({ stats }) => {
  if (!stats) {
    return null;
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
      <div className="bg-blue-50 p-4 rounded-lg border-2 border-blue-200">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-blue-600 font-medium">Total Executions</p>
            <p className="text-2xl font-bold text-blue-800">{stats.total_executions}</p>
          </div>
          <Play className="w-8 h-8 text-blue-400" />
        </div>
      </div>

      <div className="bg-green-50 p-4 rounded-lg border-2 border-green-200">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-green-600 font-medium">Successful</p>
            <p className="text-2xl font-bold text-green-800">{stats.successful_executions}</p>
          </div>
          <CheckCircle className="w-8 h-8 text-green-400" />
        </div>
      </div>

      <div className="bg-red-50 p-4 rounded-lg border-2 border-red-200">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-red-600 font-medium">Failed</p>
            <p className="text-2xl font-bold text-red-800">{stats.failed_executions}</p>
          </div>
          <AlertCircle className="w-8 h-8 text-red-400" />
        </div>
      </div>

      <div className="bg-purple-50 p-4 rounded-lg border-2 border-purple-200">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-purple-600 font-medium">Avg Time</p>
            <p className="text-2xl font-bold text-purple-800">
              {stats.average_execution_time?.toFixed(2)}s
            </p>
          </div>
          <TrendingUp className="w-8 h-8 text-purple-400" />
        </div>
      </div>
    </div>
  );
};

const ToolOrchestration = ({ agentId, onStrategyChange }) => {
  const [selectedStrategy, setSelectedStrategy] = useState('sequential');
  const [executionHistory, setExecutionHistory] = useState([]);
  const [statistics, setStatistics] = useState(null);
  const [activeView, setActiveView] = useState('strategy'); // strategy, history, stats

  const handleStrategySelect = (strategyId) => {
    setSelectedStrategy(strategyId);
    if (onStrategyChange) {
      onStrategyChange(strategyId);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-800 flex items-center">
            <Settings className="w-6 h-6 mr-2" />
            Tool Orchestration
          </h2>
          <p className="text-gray-600 mt-1">
            Configure how tools are executed for this agent
          </p>
        </div>
      </div>

      {/* View Tabs */}
      <div className="flex space-x-2 border-b border-gray-200">
        <button
          onClick={() => setActiveView('strategy')}
          className={`px-4 py-2 font-medium transition-colors ${
            activeView === 'strategy'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          Execution Strategy
        </button>
        <button
          onClick={() => setActiveView('history')}
          className={`px-4 py-2 font-medium transition-colors ${
            activeView === 'history'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          Execution History
        </button>
        <button
          onClick={() => setActiveView('stats')}
          className={`px-4 py-2 font-medium transition-colors ${
            activeView === 'stats'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          Statistics
        </button>
      </div>

      {/* Content */}
      <AnimatePresence mode="wait">
        {activeView === 'strategy' && (
          <motion.div
            key="strategy"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="space-y-4"
          >
            <h3 className="text-lg font-semibold text-gray-800">
              Select Execution Strategy
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {EXECUTION_STRATEGIES.map((strategy) => (
                <ExecutionStrategyCard
                  key={strategy.id}
                  strategy={strategy}
                  isSelected={selectedStrategy === strategy.id}
                  onSelect={() => handleStrategySelect(strategy.id)}
                />
              ))}
            </div>

            {/* Strategy Details */}
            <div className="p-4 bg-gray-50 rounded-lg border border-gray-200">
              <h4 className="font-semibold text-gray-800 mb-2">Selected Strategy Details</h4>
              <div className="text-sm text-gray-600 space-y-2">
                {selectedStrategy === 'sequential' && (
                  <ul className="list-disc list-inside space-y-1">
                    <li>Tools execute one after another in order</li>
                    <li>Each tool receives results from previous tool</li>
                    <li>Best for workflows with dependencies</li>
                    <li>Slower but more controlled</li>
                  </ul>
                )}
                {selectedStrategy === 'parallel' && (
                  <ul className="list-disc list-inside space-y-1">
                    <li>All tools execute simultaneously</li>
                    <li>Significantly faster execution</li>
                    <li>Best for independent tools</li>
                    <li>No cross-tool data dependencies</li>
                  </ul>
                )}
                {selectedStrategy === 'conditional' && (
                  <ul className="list-disc list-inside space-y-1">
                    <li>Tools execute based on conditions</li>
                    <li>Supports if-then-else logic</li>
                    <li>Skip tools that don't meet conditions</li>
                    <li>Dynamic execution path</li>
                  </ul>
                )}
                {selectedStrategy === 'retry' && (
                  <ul className="list-disc list-inside space-y-1">
                    <li>Automatically retries failed tools</li>
                    <li>Exponential backoff between retries</li>
                    <li>Configurable max retry count</li>
                    <li>Improves reliability</li>
                  </ul>
                )}
                {selectedStrategy === 'fallback' && (
                  <ul className="list-disc list-inside space-y-1">
                    <li>Tries alternative tools on failure</li>
                    <li>Fallback chain execution</li>
                    <li>Ensures task completion</li>
                    <li>Maximum resilience</li>
                  </ul>
                )}
              </div>
            </div>
          </motion.div>
        )}

        {activeView === 'history' && (
          <motion.div
            key="history"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
          >
            <h3 className="text-lg font-semibold text-gray-800 mb-4">
              Tool Execution History
            </h3>
            <ToolExecutionVisualizer executionHistory={executionHistory} />
          </motion.div>
        )}

        {activeView === 'stats' && (
          <motion.div
            key="stats"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
          >
            <h3 className="text-lg font-semibold text-gray-800 mb-4">
              Execution Statistics
            </h3>
            <ToolStatistics stats={statistics} />
          </motion.div>
        )}
      </AnimatePresence>

      {/* Supported Tool Types */}
      <div className="mt-8">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">
          Supported Tool Types
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
          {Object.entries(TOOL_TYPES).map(([type, info]) => {
            const Icon = info.icon;
            return (
              <div
                key={type}
                className={`p-3 rounded-lg border-2 border-${info.color}-200 bg-${info.color}-50`}
              >
                <div className="flex flex-col items-center text-center">
                  <div className={`p-2 rounded-lg bg-${info.color}-100 mb-2`}>
                    <Icon className={`w-5 h-5 text-${info.color}-600`} />
                  </div>
                  <p className="text-sm font-semibold text-gray-800">{info.label}</p>
                  <p className="text-xs text-gray-500 mt-1">{type}</p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default ToolOrchestration;
