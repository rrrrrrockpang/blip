import React from 'react';
import './Toggle.css'; 

const Toggle = ({ activeView, setActiveView }) => {
  return (
    <div className="btn-group" role="group" aria-label="View toggle">
        <button
           type="button"
           className={`btn ${activeView === 'bookmarks' ? 'btn-success' : 'btn-secondary'}`}
           onClick={() => setActiveView('bookmarks')}
        >
          Bookmarks
        </button>
        <button
          type="button"
          className={`btn ${activeView === 'sidebar' ? 'btn-success' : 'btn-secondary'}`}
          onClick={() => setActiveView('sidebar')}
        >
          Share Your Story
        </button>
      </div>
  );
};

export default Toggle;
