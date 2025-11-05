import React, { useState } from "react";
import { LineChart, Line, BarChart, Bar, AreaChart, Area, ResponsiveContainer, Tooltip, ReferenceLine } from "recharts";

const KpiCard = ({
  name,
  value,
  delta,
  deltaPercent,
  relativeChange,
  timeSeriesData,
  format = { type: "number", decimals: 1, currency: "$" },
  backgroundColor = "#ffffff",
  border = "1px solid #e5e7eb",
  shadow = true,
  borderRadius = "12px",
  lineColor = null,
  height = null,
  showAverage = false,
  averageValue = null,
  infoText = null,
  isInverse = false,
  chartType = "line",
}) => {
  const [showRelative, setShowRelative] = useState(relativeChange);

  const formatType = format?.type || "number";
  const decimals = format?.decimals ?? 1;
  const currency = format?.currency || "$";

  const formatValue = (val) => {
    switch (formatType) {
      case "percentage":
        return `${val.toFixed(decimals)}%`;
      case "currency":
        return `${currency}${val.toLocaleString(undefined, { minimumFractionDigits: decimals, maximumFractionDigits: decimals })}`;
      case "integer":
        return Math.round(val).toLocaleString();
      case "decimal":
        return val.toFixed(decimals);
      default:
        return val.toLocaleString();
    }
  };

  const formatDelta = () => {
    if (showRelative) {
      return `${deltaPercent >= 0 ? "+" : ""}${deltaPercent.toFixed(decimals)}%`;
    } else {
      return `${delta >= 0 ? "+" : ""}${formatValue(Math.abs(delta))}`;
    }
  };

  const toggleDeltaMode = () => {
    setShowRelative(!showRelative);
  };

  const isPositive = delta >= 0;
  // Invert colors if is_inverse is true (lower is better)
  const actuallyGood = isInverse ? !isPositive : isPositive;
  const deltaColor = actuallyGood ? "#10b981" : "#ef4444";
  const chartLineColor = lineColor || (actuallyGood ? "#10b981" : "#ef4444");

  return (
    <div
      style={{
        backgroundColor: backgroundColor,
        borderRadius: borderRadius,
        padding: "12px",
        boxShadow: shadow ? "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)" : "none",
        border: border || "none",
        fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif",
        maxWidth: "100%",
        height: height || "auto",
        display: "flex",
        flexDirection: "column",
        overflow: "hidden",
      }}
    >
      {/* KPI Name with Info Icon */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "4px",
          flexShrink: 0,
        }}
      >
        <div
          style={{
            fontSize: "11px",
            fontWeight: 500,
            color: "#6b7280",
            textTransform: "uppercase",
            letterSpacing: "0.05em",
          }}
        >
          {name}
        </div>
        {infoText && (
          <div
            title={infoText}
            style={{
              cursor: "help",
              color: "#9ca3af",
              display: "flex",
              alignItems: "center",
            }}
          >
            <svg
              width="14"
              height="14"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="16" x2="12" y2="12"></line>
              <line x1="12" y1="8" x2="12.01" y2="8"></line>
            </svg>
          </div>
        )}
      </div>

      {/* Main Value */}
      <div
        style={{
          fontSize: "32px",
          fontWeight: 700,
          color: "#111827",
          marginBottom: "2px",
          lineHeight: 1,
          flexShrink: 0,
        }}
      >
        {formatValue(value)}
      </div>

      {/* Delta */}
      <div
        onClick={toggleDeltaMode}
        style={{
          display: "flex",
          alignItems: "center",
          gap: "4px",
          marginBottom: "0",
          cursor: "pointer",
          userSelect: "none",
          padding: "2px 6px",
          marginLeft: "-6px",
          borderRadius: "4px",
          transition: "background-color 0.2s",
          width: "fit-content",
          flexShrink: 0,
        }}
        onMouseEnter={(e) => e.currentTarget.style.backgroundColor = "rgba(0, 0, 0, 0.05)"}
        onMouseLeave={(e) => e.currentTarget.style.backgroundColor = "transparent"}
        title="Click to toggle between relative and absolute change"
      >
        <span
          style={{
            fontSize: "12px",
            fontWeight: 600,
            color: deltaColor,
          }}
        >
          {formatDelta()}
        </span>
        <span
          style={{
            fontSize: "11px",
            color: "#9ca3af",
          }}
        >
          vs previous
        </span>
      </div>

      {/* Time Series Chart */}
      {timeSeriesData && timeSeriesData.length > 0 && (
        <div style={{
          marginTop: "4px",
          marginBottom: "2px",
          flexGrow: 1,
          minHeight: "40px",
          height: height ? "auto" : "50px"
        }}>
          <ResponsiveContainer width="100%" height="100%">
            {chartType === "bar" ? (
              <BarChart data={timeSeriesData} margin={{ top: 0, right: 0, left: 0, bottom: 0 }}>
                <Tooltip
                  position={{ y: -30 }}
                  cursor={false}
                  separator=""
                  contentStyle={{
                    backgroundColor: "#ffffff",
                    border: "1px solid #e5e7eb",
                    borderRadius: "4px",
                    color: "#111827",
                    fontSize: "11px",
                    padding: "4px 8px",
                    boxShadow: "0 1px 3px 0 rgba(0, 0, 0, 0.1)",
                    zIndex: 10,
                  }}
                  labelStyle={{ color: "#6b7280", fontWeight: 500, marginBottom: "2px", fontSize: "10px" }}
                  itemStyle={{ color: "#111827", fontWeight: 600, padding: "0", listStyle: "none" }}
                  labelFormatter={(label, payload) => {
                    if (payload && payload.length > 0) {
                      return payload[0].payload.index;
                    }
                    return "";
                  }}
                  formatter={(value) => [formatValue(value), ""]}
                />
                {showAverage && averageValue !== null && (
                  <ReferenceLine
                    y={averageValue}
                    stroke="#374151"
                    strokeDasharray="5 5"
                    strokeWidth={1.5}
                  />
                )}
                <Bar
                  dataKey="value"
                  fill={chartLineColor}
                  animationDuration={300}
                />
              </BarChart>
            ) : chartType === "area" ? (
              <AreaChart data={timeSeriesData} margin={{ top: 0, right: 0, left: 0, bottom: 0 }}>
                <Tooltip
                  position={{ y: -30 }}
                  cursor={false}
                  separator=""
                  contentStyle={{
                    backgroundColor: "#ffffff",
                    border: "1px solid #e5e7eb",
                    borderRadius: "4px",
                    color: "#111827",
                    fontSize: "11px",
                    padding: "4px 8px",
                    boxShadow: "0 1px 3px 0 rgba(0, 0, 0, 0.1)",
                    zIndex: 10,
                  }}
                  labelStyle={{ color: "#6b7280", fontWeight: 500, marginBottom: "2px", fontSize: "10px" }}
                  itemStyle={{ color: "#111827", fontWeight: 600, padding: "0", listStyle: "none" }}
                  labelFormatter={(label, payload) => {
                    if (payload && payload.length > 0) {
                      return payload[0].payload.index;
                    }
                    return "";
                  }}
                  formatter={(value) => [formatValue(value), ""]}
                />
                {showAverage && averageValue !== null && (
                  <ReferenceLine
                    y={averageValue}
                    stroke="#374151"
                    strokeDasharray="5 5"
                    strokeWidth={1.5}
                  />
                )}
                <Area
                  type="monotone"
                  dataKey="value"
                  stroke={chartLineColor}
                  fill={chartLineColor}
                  fillOpacity={0.3}
                  strokeWidth={2}
                  animationDuration={300}
                />
              </AreaChart>
            ) : (
              <LineChart data={timeSeriesData} margin={{ top: 0, right: 0, left: 0, bottom: 0 }}>
                <Tooltip
                  position={{ y: -30 }}
                  cursor={false}
                  separator=""
                  contentStyle={{
                    backgroundColor: "#ffffff",
                    border: "1px solid #e5e7eb",
                    borderRadius: "4px",
                    color: "#111827",
                    fontSize: "11px",
                    padding: "4px 8px",
                    boxShadow: "0 1px 3px 0 rgba(0, 0, 0, 0.1)",
                    zIndex: 10,
                  }}
                  labelStyle={{ color: "#6b7280", fontWeight: 500, marginBottom: "2px", fontSize: "10px" }}
                  itemStyle={{ color: "#111827", fontWeight: 600, padding: "0", listStyle: "none" }}
                  labelFormatter={(label, payload) => {
                    if (payload && payload.length > 0) {
                      return payload[0].payload.index;
                    }
                    return "";
                  }}
                  formatter={(value) => [formatValue(value), ""]}
                />
                {showAverage && averageValue !== null && (
                  <ReferenceLine
                    y={averageValue}
                    stroke="#374151"
                    strokeDasharray="5 5"
                    strokeWidth={1.5}
                  />
                )}
                <Line
                  type="monotone"
                  dataKey="value"
                  stroke={chartLineColor}
                  strokeWidth={2}
                  dot={false}
                  animationDuration={300}
                />
              </LineChart>
            )}
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
};

export default KpiCard;
