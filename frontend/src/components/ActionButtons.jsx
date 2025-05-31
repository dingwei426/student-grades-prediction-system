import React from "react";
import "../assets/styles.css"; // Import styles

function ActionButtons({ onView, onDelete }) {
  return (
    <>
      <button className="view-button" onClick={onView}>
        View
      </button>
      <button className="delete-button" onClick={onDelete}>
        Delete
      </button>
    </>
  );
}

export default ActionButtons;
