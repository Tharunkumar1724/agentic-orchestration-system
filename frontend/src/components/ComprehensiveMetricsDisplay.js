import React from 'react';
import { 
  FaClock, 
  FaChartLine, 
  FaBrain, 
  FaCheckCircle, 
  FaExclamationTriangle,
  FaTools,
  FaLayerGroup,
  FaProjectDiagram,
  FaNetworkWired,
  FaDatabase
} from 'react-icons/fa';

/**
 * Comprehensive Metrics Display Component
 * Shows all 12 key metrics with visual indicators
 */
const ComprehensiveMetricsDisplay = ({ metrics, compact = false }) => {
  if (!metrics) return null;

  // Metric categories for organization
  const performanceMetrics = [
    {
      key: 'latency_ms',
      label: 'Latency',
      icon: FaClock,
      color: 'purple',
      format: (val) => `${val?.toFixed(0) || 0}ms`,
      description: 'Total execution time'
    },
    {
      key: 'token_usage_count',
      label: 'Token Usage',
      icon: FaDatabase,
      color: 'blue',
      format: (val) => val || 0,
      description: 'Total tokens used',
      details: metrics.token_input_count && metrics.token_output_count 
        ? `In: ${metrics.token_input_count} | Out: ${metrics.token_output_count}`
        : null
    }
  ];

  const qualityMetrics = [
    {
      key: 'accuracy',
      label: 'Accuracy',
      icon: FaChartLine,
      color: 'green',
      format: (val) => `${val?.toFixed(1) || 0}%`,
      description: 'Response accuracy score',
      isPercentage: true,
      value: metrics.accuracy
    },
    {
      key: 'response_quality',
      label: 'Quality',
      icon: FaBrain,
      color: 'teal',
      format: (val) => `${val?.toFixed(1) || 0}%`,
      description: 'Overall response quality',
      isPercentage: true,
      value: metrics.response_quality
    },
    {
      key: 'hallucination_rate',
      label: 'Hallucination',
      icon: FaExclamationTriangle,
      color: 'red',
      format: (val) => `${val?.toFixed(1) || 0}%`,
      description: 'Estimated hallucination rate (lower is better)',
      isPercentage: true,
      inverse: true, // Lower is better
      value: metrics.hallucination_rate
    },
    {
      key: 'task_completion_rate',
      label: 'Completion',
      icon: FaCheckCircle,
      color: 'green',
      format: (val) => `${val?.toFixed(1) || 0}%`,
      description: 'Task completion percentage',
      isPercentage: true,
      value: metrics.task_completion_rate
    },
    {
      key: 'context_relation_quality',
      label: 'Context Quality',
      icon: FaNetworkWired,
      color: 'indigo',
      format: (val) => `${val?.toFixed(1) || 0}%`,
      description: 'Context relevance score',
      isPercentage: true,
      value: metrics.context_relation_quality
    }
  ];

  const executionMetrics = [
    {
      key: 'tool_invocation_count',
      label: 'Tool Calls',
      icon: FaTools,
      color: 'yellow',
      format: (val) => val || 0,
      description: 'Number of tools invoked'
    },
    {
      key: 'tool_success_rate',
      label: 'Tool Success',
      icon: FaCheckCircle,
      color: 'emerald',
      format: (val) => `${val?.toFixed(1) || 0}%`,
      description: 'Tool success rate',
      isPercentage: true,
      value: metrics.tool_success_rate
    },
    {
      key: 'retrieval_error_count',
      label: 'Errors',
      icon: FaExclamationTriangle,
      color: 'red',
      format: (val) => val || 0,
      description: 'Retrieval/tool errors',
      inverse: true
    },
    {
      key: 'decision_depth',
      label: 'Decision Depth',
      icon: FaLayerGroup,
      color: 'violet',
      format: (val) => val || 0,
      description: 'Depth of decision tree'
    },
    {
      key: 'branching_factor',
      label: 'Branching',
      icon: FaProjectDiagram,
      color: 'pink',
      format: (val) => val?.toFixed(2) || 0,
      description: 'Average branching factor'
    }
  ];

  // Helper to get progress bar color based on value and if inverse
  const getProgressColor = (value, inverse = false) => {
    const effectiveValue = inverse ? 100 - value : value;
    if (effectiveValue >= 80) return 'bg-green-500';
    if (effectiveValue >= 60) return 'bg-yellow-500';
    if (effectiveValue >= 40) return 'bg-orange-500';
    return 'bg-red-500';
  };

  const getColorClasses = (color) => ({
    bg: `bg-${color}-900/30`,
    border: `border-${color}-500/30`,
    text: `text-${color}-300`,
    icon: `text-${color}-400`
  });

  if (compact) {
    // Compact view - single row with key metrics
    return (
      <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-xs">
        {[...performanceMetrics, ...qualityMetrics.slice(0, 2)].map((metric) => {
          const Icon = metric.icon;
          const value = metrics[metric.key];
          return (
            <div key={metric.key} className="bg-gray-800/50 rounded p-2 border border-gray-700">
              <div className="flex items-center gap-2 mb-1">
                <Icon className={`text-${metric.color}-400 text-xs`} />
                <span className="text-gray-400 text-[10px]">{metric.label}</span>
              </div>
              <div className={`text-${metric.color}-300 font-bold`}>
                {metric.format(value)}
              </div>
            </div>
          );
        })}
      </div>
    );
  }

  // Full metrics display
  return (
    <div className="space-y-4">
      {/* Performance Metrics */}
      <div>
        <h4 className="text-xs font-semibold text-gray-400 mb-2 flex items-center gap-2">
          <FaClock className="text-purple-400" />
          Performance Metrics
        </h4>
        <div className="grid grid-cols-2 gap-2">
          {performanceMetrics.map((metric) => {
            const Icon = metric.icon;
            const value = metrics[metric.key];
            return (
              <div key={metric.key} className={`bg-${metric.color}-900/30 rounded-lg p-3 border border-${metric.color}-500/30`}>
                <div className="flex items-center gap-2 mb-1">
                  <Icon className={`text-${metric.color}-400 text-sm`} />
                  <span className="text-xs text-gray-300">{metric.label}</span>
                </div>
                <div className={`text-xl font-bold text-${metric.color}-200 mb-1`}>
                  {metric.format(value)}
                </div>
                {metric.details && (
                  <div className="text-[10px] text-gray-400">{metric.details}</div>
                )}
                <div className="text-[9px] text-gray-500 mt-1">{metric.description}</div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Quality Metrics */}
      <div>
        <h4 className="text-xs font-semibold text-gray-400 mb-2 flex items-center gap-2">
          <FaBrain className="text-teal-400" />
          Quality Metrics
        </h4>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
          {qualityMetrics.map((metric) => {
            const Icon = metric.icon;
            const value = metrics[metric.key] || 0;
            const progressColor = metric.isPercentage 
              ? getProgressColor(value, metric.inverse) 
              : 'bg-gray-500';
            
            return (
              <div key={metric.key} className={`bg-${metric.color}-900/30 rounded-lg p-3 border border-${metric.color}-500/30`}>
                <div className="flex items-center gap-2 mb-2">
                  <Icon className={`text-${metric.color}-400 text-sm`} />
                  <span className="text-xs text-gray-300">{metric.label}</span>
                </div>
                <div className={`text-lg font-bold text-${metric.color}-200 mb-2`}>
                  {metric.format(value)}
                </div>
                {metric.isPercentage && (
                  <div className="w-full bg-gray-800 rounded-full h-1.5 mb-1">
                    <div 
                      className={`h-1.5 rounded-full ${progressColor} transition-all duration-500`}
                      style={{ width: `${Math.min(100, value)}%` }}
                    />
                  </div>
                )}
                <div className="text-[9px] text-gray-500">{metric.description}</div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Execution Metrics */}
      <div>
        <h4 className="text-xs font-semibold text-gray-400 mb-2 flex items-center gap-2">
          <FaTools className="text-yellow-400" />
          Execution Metrics
        </h4>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
          {executionMetrics.map((metric) => {
            const Icon = metric.icon;
            const value = metrics[metric.key] || 0;
            
            return (
              <div key={metric.key} className={`bg-${metric.color}-900/30 rounded-lg p-3 border border-${metric.color}-500/30`}>
                <div className="flex items-center gap-2 mb-1">
                  <Icon className={`text-${metric.color}-400 text-sm`} />
                  <span className="text-xs text-gray-300">{metric.label}</span>
                </div>
                <div className={`text-lg font-bold text-${metric.color}-200 mb-1`}>
                  {metric.format(value)}
                </div>
                <div className="text-[9px] text-gray-500">{metric.description}</div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Additional Info */}
      {(metrics.errors?.length > 0 || metrics.warnings?.length > 0) && (
        <div className="bg-gray-900/50 rounded-lg p-3 border border-gray-700">
          {metrics.errors?.length > 0 && (
            <div className="mb-2">
              <div className="text-xs font-semibold text-red-400 mb-1">Errors ({metrics.errors.length}):</div>
              <ul className="space-y-1 max-h-20 overflow-y-auto">
                {metrics.errors.map((error, idx) => (
                  <li key={idx} className="text-[10px] text-red-300">• {error}</li>
                ))}
              </ul>
            </div>
          )}
          {metrics.warnings?.length > 0 && (
            <div>
              <div className="text-xs font-semibold text-yellow-400 mb-1">Warnings ({metrics.warnings.length}):</div>
              <ul className="space-y-1 max-h-20 overflow-y-auto">
                {metrics.warnings.map((warning, idx) => (
                  <li key={idx} className="text-[10px] text-yellow-300">• {warning}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ComprehensiveMetricsDisplay;
