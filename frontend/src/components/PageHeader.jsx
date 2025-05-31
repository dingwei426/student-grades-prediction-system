import React from "react";

function PageHeader({
  title,
  subtitle,
  color = "black",
  textAlign = "center",
}) {
  return (
    <header
      style={{
        padding: "10px",
        backgroundColor: "transparent",
        textAlign: textAlign,
        color: color,
      }}
    >
      <h1 style={{ margin: "10px" }}>{title}</h1>
      {subtitle && (
        <p style={{ fontSize: "16px", color: "#666" }}>{subtitle}</p>
      )}
    </header>
  );
}

export default PageHeader;
