import React from "react";
import { createRoot } from "react-dom/client";
import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib";
import KpiCard from "./KpiCard";

class StreamlitKpiCard extends StreamlitComponentBase {
  render() {
    const {
      name,
      value,
      valueBefore,
      delta,
      deltaPercent,
      relativeChange,
      timeSeriesData,
      format,
      backgroundColor,
      border,
      shadow,
      borderRadius,
      lineColor,
      height,
      showAverage,
      averageValue,
      infoText,
      isInverse,
      chartType,
    } = this.props.args;

    return (
      <KpiCard
        name={name}
        value={value}
        valueBefore={valueBefore}
        delta={delta}
        deltaPercent={deltaPercent}
        relativeChange={relativeChange}
        timeSeriesData={timeSeriesData}
        format={format}
        backgroundColor={backgroundColor}
        border={border}
        shadow={shadow}
        borderRadius={borderRadius}
        lineColor={lineColor}
        height={height}
        showAverage={showAverage}
        averageValue={averageValue}
        infoText={infoText}
        isInverse={isInverse}
        chartType={chartType}
      />
    );
  }

  componentDidMount() {
    Streamlit.setFrameHeight();
  }

  componentDidUpdate() {
    Streamlit.setFrameHeight();
  }
}

const StreamlitKpiCardWrapped = withStreamlitConnection(StreamlitKpiCard);

const container = document.getElementById("root");
if (container) {
  const root = createRoot(container);
  root.render(
    <React.StrictMode>
      <StreamlitKpiCardWrapped />
    </React.StrictMode>
  );
}
