import React from "react";

function LongButton({
  text,
  onClick,
  isClickedColor = "#ccc",
  isHoveredColor = "#779ECB",
  backgroundColor = "#187bcd",
  disabledColor = "#779ECB",
  disabled = false, // Accept disabled prop
}) {
  const [isHovered, setIsHovered] = React.useState(false);
  const [isClicked, setIsClicked] = React.useState(false);

  const handleMouseEnter = () => setIsHovered(true);
  const handleMouseLeave = () => setIsHovered(false);
  const handleMouseDown = () => setIsClicked(true);
  const handleMouseUp = () => setIsClicked(false);

  const buttonStyle = {
    padding: "10px",
    width: "100%",
    backgroundColor: disabled
      ? disabledColor
      : isClicked
      ? isClickedColor
      : isHovered
      ? isHoveredColor
      : backgroundColor,
    color: "#fff",
    border: "none",
    cursor: disabled ? "not-allowed" : "pointer", // Prevent clicking when disabled
    fontSize: "16px",
    boxSizing: "border-box",
    borderRadius: "20px",
    transition: "background-color 0.3s ease",
  };

  return (
    <button
      onClick={!disabled ? onClick : undefined} // Prevent click when disabled
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      onMouseDown={handleMouseDown}
      onMouseUp={handleMouseUp}
      style={buttonStyle}
      disabled={disabled} // Pass disabled attribute
    >
      {text}
    </button>
  );
}

export default LongButton;
