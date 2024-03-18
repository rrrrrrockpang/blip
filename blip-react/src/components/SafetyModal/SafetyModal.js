import React from 'react';
import './SafetyModal.css';

function SafetyModal({ onClose }) {
  return (
    <div id="popup-container">
        <div id="popup-message">
          <h4>BLIP</h4>
          <div className="disclaimer">This is a research prototype. Our goal is to get external feedback to improve our system. It is not intended to give advice.</div>
          <div className="disclaimer">BLIP employs large language models, the system may occasionally generate inaccurate summaries or inaccurate categorizations of online articles.</div>
          <div className="disclaimer">Please contact us if you'd like to share your feedback or found any issues.</div>
          
          <button id="popup-close" onClick={onClose}>Close</button>
        </div>
    </div>
  );
}

export default SafetyModal;
