import React, { useState } from 'react';
import "./ContributeModal.css";

function ContributeModal({ isOpen, closeModal }) {
  const [contributeOption, setContributeOption] = useState('');
  const [isAlertVisible, setAlertVisible] = useState(false);

  const handleSubmit = () => {
    // Hide the alert after 5 seconds
    setAlertVisible(true);
    setTimeout(() => {
        setAlertVisible(false);
        closeModal();
    }, 5000);

    // Close the modal
    
  };
  
  return (
        <div id="contributeModal" className={`modal ${isOpen ? 'is-open' : ''}`}>
            <div id="contributeModalContent">
                <span className="close" onClick={closeModal}>&times;</span>
                <h3>Would you like to suggest a new domain to add on BLIP?</h3>
                <label htmlFor="contribute-option">Please leave the new domain that you think is important to add:</label>
                <input type="text" id="contribute-option" name="contribute-option" value={contributeOption} onChange={(e) => setContributeOption(e.target.value)} placeholder="Enter new domain..." />
                <div className="contribute options">
                <label>A few options: </label>
                {['Ride-sharing apps', 'Language models', 'Live-streaming', 'Augmented reality'].map((option) => (
                    <button type="button" className="option-button" data-option={option} onClick={() => setContributeOption(option)} key={option}>
                    {option}
                    </button>
                ))}
                </div>
                <button id="submit-button" className="submit-button" onClick={handleSubmit}>Submit</button>
            </div>
            <div id="alert" className={`alert alert-success alert-dismissible fade show ${isAlertVisible ? '' : 'd-none'}`} role="alert">
                Your suggestion has been submitted and received by us. We will evaluate it and push new changes to BLIP soon depending on term popularity.
            </div>
        </div>
  );
}

export default ContributeModal;