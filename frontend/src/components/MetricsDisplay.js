import React from 'react';
import { FaClock, FaCoins, FaCheckCircle, FaBrain, FaTools, FaNetworkWired, FaExclamationTriangle } from 'react-icons/fa';

/**
 * MetricsDisplay Component
 * Displays comprehensive execution metrics in a beautiful, organized format
 * 
 * @param {Object} metrics - The metrics object from API response
 * @param {string} title - Optional title for the metrics section
 * @param {boolean} compact - If true, shows compact view
 */
function MetricsDisplay({ metrics, title = "Execution Metrics", compact = false }) {
  if (!metrics) {
    return null;
  }

  // Helper to format numbers
  const formatNumber = (num) => {
    if (num === undefined || num === null) return '0';
    return num.toLocaleString();
  };

  // Helper to get color class based on percentage
  const getQualityColor = (value) => {
    if (value >= 80) return 'text-green-400';
    if (value >= 60) return 'text-yellow-400';
    return 'text-red-400';
  };

  if (compact) {
    return (
      <div className="bg-gray-900/50 rounded-lg p-3 border border-gray-700">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
          <div className="flex items-center gap-2">
            <FaClock className="text-blue-400" />
            <div>
              <div className="text-gray-400 text-xs">Latency</div>
              <div className="text-white font-semibold">{formatNumber(metrics.latency_ms)}ms</div>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <FaCoins className="text-yellow-400" />
            <div>
              <div className="text-gray-400 text-xs">Tokens</div>
              <div className="text-white font-semibold">{formatNumber(metrics.token_usage_count)}</div>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <FaCheckCircle className={getQualityColor(metrics.accuracy)} />
            <div>
              <div className="text-gray-400 text-xs">Accuracy</div>
              <div className="text-white font-semibold">{metrics.accuracy?.toFixed(1)}%</div>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <FaCheckCircle className={getQualityColor(metrics.task_completion_rate)} />
            <div>
              <div className="text-gray-400 text-xs">Completion</div>
              <div className="text-white font-semibold">{metrics.task_completion_rate?.toFixed(1)}%</div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-gradient-to-br from-gray-900 to-gray-800 rounded-xl p-6 border border-gray-700 shadow-2xl">
      {/* Header */}
      <div className="flex items-center gap-3 mb-6 border-b border-gray-700 pb-4">
        <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center">
          <FaBrain className="text-white text-xl" />
        </div>
        <h3 className="text-2xl font-bold text-white">{title}</h3>
      </div>

      {/* Performance Metrics */}
      <div className="mb-6">
        <h4 className="text-sm font-semibold text-gray-400 uppercase mb-3 flex items-center gap-2">
          <FaClock className="text-blue-400" />
          Performance Metrics
        </h4>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <MetricCard 
            label="Latency" 
            value={`${formatNumber(metrics.latency_ms)} ms`}
            icon={<FaClock />}
            color="blue"
          />
          <MetricCard 
            label="Total Tokens" 
            value={formatNumber(metrics.token_usage_count)}
            icon={<FaCoins />}
            color="yellow"
          />
          <MetricCard 
            label="Input Tokens" 
            value={formatNumber(metrics.token_input_count)}
            icon={<FaCoins />}
            color="cyan"
          />
          <MetricCard 
            label="Output Tokens" 
            value={formatNumber(metrics.token_output_count)}
            icon={<FaCoins />}
            color="orange"
          />
        </div>
      </div>

      {/* Quality Metrics */}
      <div className="mb-6">
        <h4 className="text-sm font-semibold text-gray-400 uppercase mb-3 flex items-center gap-2">
          <FaCheckCircle className="text-green-400" />
          Quality Metrics
        </h4>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          <QualityMetric label="Accuracy" value={metrics.accuracy} />
          <QualityMetric label="Response Quality" value={metrics.response_quality} />
          <QualityMetric label="Task Completion" value={metrics.task_completion_rate} />
          <QualityMetric label="Context Quality" value={metrics.context_relation_quality} />
          <QualityMetric label="Hallucination Rate" value={metrics.hallucination_rate} inverse />
        </div>
      </div>

      {/* Tool & Execution Metrics */}
      <div className="mb-6">
        <h4 className="text-sm font-semibold text-gray-400 uppercase mb-3 flex items-center gap-2">
          <FaTools className="text-purple-400" />
          Tool & Execution Metrics
        </h4>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <MetricCard 
            label="Tools Invoked" 
            value={formatNumber(metrics.tool_invocation_count)}
            icon={<FaTools />}
            color="purple"
          />
          <QualityMetric label="Tool Success" value={metrics.tool_success_rate} />
          <MetricCard 
            label="Retrieval Errors" 
            value={formatNumber(metrics.retrieval_error_count)}
            icon={<FaExclamationTriangle />}
            color="red"
          />
          <MetricCard 
            label="Agents Executed" 
            value={formatNumber(metrics.agent_execution_count)}
            icon={<FaBrain />}
            color="indigo"
          />
        </div>
      </div>

      {/* Decision & Structure Metrics */}
      <div>
        <h4 className="text-sm font-semibold text-gray-400 uppercase mb-3 flex items-center gap-2">
          <FaNetworkWired className="text-teal-400" />
          Decision & Structure Metrics
        </h4>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <MetricCard 
            label="Decision Depth" 
            value={formatNumber(metrics.decision_depth)}
            icon={<FaNetworkWired />}
            color="teal"
          />
          <MetricCard 
            label="Branching Factor" 
            value={metrics.branching_factor?.toFixed(2)}
            icon={<FaNetworkWired />}
            color="teal"
          />
          <MetricCard 
            label="Workflow Steps" 
            value={formatNumber(metrics.workflow_step_count)}
            icon={<FaNetworkWired />}
            color="teal"
          />
          <MetricCard 
            label="Time per Step" 
            value={metrics.workflow_step_count > 0 
              ? `${(metrics.latency_ms / metrics.workflow_step_count).toFixed(0)} ms`
              : 'N/A'
            }
            icon={<FaClock />}
            color="blue"
          />
        </div>
      </div>

      {/* Errors & Warnings */}
      {(metrics.errors?.length > 0 || metrics.warnings?.length > 0) && (
        <div className="mt-6 space-y-2">
          {metrics.errors?.map((error, i) => (
            <div key={`error-${i}`} className="bg-red-900/20 border border-red-500/50 rounded px-3 py-2 text-red-200 text-sm flex items-start gap-2">
              <FaExclamationTriangle className="text-red-400 mt-0.5" />
              <span>{error}</span>
            </div>
          ))}
          {metrics.warnings?.map((warning, i) => (
            <div key={`warning-${i}`} className="bg-yellow-900/20 border border-yellow-500/50 rounded px-3 py-2 text-yellow-200 text-sm flex items-start gap-2">
              <FaExclamationTriangle className="text-yellow-400 mt-0.5" />
              <span>{warning}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// Helper component for metric cards
function MetricCard({ label, value, icon, color = 'gray' }) {
  const colorClasses = {
    blue: 'from-blue-500/20 to-blue-600/10 border-blue-500/30 text-blue-400',
    yellow: 'from-yellow-500/20 to-yellow-600/10 border-yellow-500/30 text-yellow-400',
    cyan: 'from-cyan-500/20 to-cyan-600/10 border-cyan-500/30 text-cyan-400',
    orange: 'from-orange-500/20 to-orange-600/10 border-orange-500/30 text-orange-400',
    purple: 'from-purple-500/20 to-purple-600/10 border-purple-500/30 text-purple-400',
    red: 'from-red-500/20 to-red-600/10 border-red-500/30 text-red-400',
    indigo: 'from-indigo-500/20 to-indigo-600/10 border-indigo-500/30 text-indigo-400',
    teal: 'from-teal-500/20 to-teal-600/10 border-teal-500/30 text-teal-400',
    gray: 'from-gray-500/20 to-gray-600/10 border-gray-500/30 text-gray-400'
  };

  return (
    <div className={`bg-gradient-to-br ${colorClasses[color]} rounded-lg p-4 border`}>
      <div className="flex items-center gap-2 mb-2">
        {React.cloneElement(icon, { className: `text-lg ${colorClasses[color].split(' ')[3]}` })}
        <span className="text-xs text-gray-400 font-medium">{label}</span>
      </div>
      <div className="text-2xl font-bold text-white">{value}</div>
    </div>
  );
}

// Helper component for quality percentage metrics
function QualityMetric({ label, value, inverse = false }) {
  const percentage = value || 0;
  const getColor = () => {
    if (inverse) {
      // For hallucination rate, lower is better
      if (percentage <= 20) return 'green';
      if (percentage <= 40) return 'yellow';
      return 'red';
    } else {
      // For most metrics, higher is better
      if (percentage >= 80) return 'green';
      if (percentage >= 60) return 'yellow';
      return 'red';
    }
  };

  const color = getColor();
  const colorClasses = {
    green: 'from-green-500/20 to-green-600/10 border-green-500/30',
    yellow: 'from-yellow-500/20 to-yellow-600/10 border-yellow-500/30',
    red: 'from-red-500/20 to-red-600/10 border-red-500/30'
  };

  const textColorClasses = {
    green: 'text-green-400',
    yellow: 'text-yellow-400',
    red: 'text-red-400'
  };

  return (
    <div className={`bg-gradient-to-br ${colorClasses[color]} rounded-lg p-4 border relative overflow-hidden`}>
      {/* Progress bar background */}
      <div className="absolute bottom-0 left-0 right-0 h-1 bg-gray-800">
        <div 
          className={`h-full bg-gradient-to-r ${color === 'green' ? 'from-green-500 to-green-400' : color === 'yellow' ? 'from-yellow-500 to-yellow-400' : 'from-red-500 to-red-400'}`}
          style={{ width: `${percentage}%` }}
        ></div>
      </div>
      
      <div className="text-xs text-gray-400 font-medium mb-1">{label}</div>
      <div className={`text-2xl font-bold ${textColorClasses[color]}`}>{percentage?.toFixed(1)}%</div>
    </div>
  );
}

export default MetricsDisplay;
