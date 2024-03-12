import React, { useState, useEffect } from 'react';
import ResultCard from './ResultCard';
import './ArticleModal.css';

function ArticleModal({ isOpen, closeModal }) {
  const [url, setUrl] = useState("");
  const [domain, setDomain] = useState("social media");
  const [isLoading, setIsLoading] = useState(false);
  const [response, setResponse] = useState(null);

  const submitArticle = async () => {
    // Validate the URL
    if (!/^(ftp|http|https):\/\/[^ "]+$/.test(url)) {
      alert("Invalid URL format");
      return;
    }

    setIsLoading(true);

    try {
      const response = await fetch("http://104.197.248.47:80/request", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url, domain }),
      });

      if (response.ok) {
        const res = await response.json();
        setResponse(res);
      } else {
        alert("An error occurred. Please try again.");
      }
    } catch (error) {
      alert("An error occurred. Please try again.");
    }

    setIsLoading(false);
  };

  // Reset results when the modal is closed or opened
  useEffect(() => {
    setResponse(null);
  }, [isOpen]);

  return (
    <div id="articleModal" className={`modal ${isOpen ? 'is-open' : ''}`}>
      <div id="articleModalContent">
        <span className="close" onClick={closeModal}>&times;</span>
        <h3>Analyze Your Own Article</h3>
        <p>You can input a URL of an online article and select one of the domains. You'll be able to see the results run by our pipeline.</p>
        <label htmlFor="url">Article URL:</label>
        <input type="text" id="url" name="url" value={url} onChange={(e) => setUrl(e.target.value)} />
        <br />
        <label htmlFor="domain">Domain:</label>
        <select id="domain" name="domain" value={domain} onChange={(e) => setDomain(e.target.value)}>
          <option value="social media">social media</option>
          <option value="voice assistant">voice assistant</option>
          <option value="virtual reality">virtual reality</option>
        </select>
        <br />
        <button id="submitButton" className="submit-button" onClick={submitArticle}>Submit</button>
        <br />
        <div id="results">
          {isLoading ? <div className="loader"></div> : response && <ResultCard url={url} domain={domain} response={response}></ResultCard>}
        </div>
      </div>
    </div>
  );
}

export default ArticleModal;


// import React, { useState } from 'react';
// import './ContributeModal.css';

// function ArticleModal({ isOpen, closeModal }) {
//   const [url, setUrl] = useState("");
//   const [domain, setDomain] = useState("social media");
//   console.log("Is the modal open?", isOpen);  // Add this line for debugging

//   return (
//     <div id="articleModal" className={`modal ${isOpen ? 'is-open' : ''}`}>
//       <div id="articleModalContent">
//         <span className="close" onClick={closeModal}>&times;</span>
//         <h3>Analyze Your Own Article</h3>
//         <p>You can input an URL of an online article and select one of the domain. You'll be able to see the results run by our pipeline.</p>
//         <label htmlFor="url">Article URL:</label>
//         <input type="text" id="url" name="url" value={url} onChange={(e) => setUrl(e.target.value)} />
//         <br />
//         <label htmlFor="domain">Domain:</label>
//         <select id="domain" name="domain" value={domain} onChange={(e) => setDomain(e.target.value)}>
//           <option value="social media">social media</option>
//           <option value="voice assistant">voice assistant</option>
//           <option value="virtual reality">virtual reality</option>
//         </select>
//         <br />
//         <button id="submitButton" className="submit-button" onClick={() => {/* Submit code here */}}>Submit</button>
//         <br />
//         <div id="results"></div>
//       </div>
//     </div>
//   );
// }

// export default ArticleModal;
