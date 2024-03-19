import React, { useState, useEffect } from 'react';
import ResultCard from './ResultCard';
import './ArticleModal.css';

function ArticleModal({ isOpen, closeModal }) {
  const [url, setUrl] = useState("");
  const [domain, setDomain] = useState("social media");
  const [isLoading, setIsLoading] = useState(false);
  const [response, setResponse] = useState(null);

  const samples = [
    { url: "https://techcrunch.com/2023/05/24/the-surgeon-generals-advisory-on-risks-of-youth-social-media-use-could-shift-the-conversation/", domain: "social_media", label: "Social Media" },
    { url: "https://www.theguardian.com/world/2015/feb/09/south-korean-womans-hair-eaten-by-robot-vacuum-cleaner-as-she-slept", domain: "robotics", label: "Robotics" },
    { url: "https://medium.com/@sranciato1/ethical-challenges-in-ar-vr-918f259d0b59", domain: "augmented/virtual_reality", label: "Augmented/Virtual Reality" }
  ];

  const submitArticle = async () => {
    if (!/^(ftp|http|https):\/\/[^ "]+$/.test(url)) {
      alert("Invalid URL format");
      return;
    }

    setIsLoading(true);

    try {
      const response = await fetch(
        "https://blip.labinthewild.org/api/request",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ url, domain }),
        }
      );

      if (response.ok) {
        const res = await response.json();
        setResponse(res);
      } else {
        alert("An error occurred. Please try again.");
      }
    } catch (error) {
      alert("An error occurred. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    setResponse(null);
  }, [isOpen]);

  const loadSample = (sample) => {
    setUrl(sample.url);
    setDomain(sample.domain);
  };

  return (
    <div id="articleModal" className={`modal ${isOpen ? 'is-open' : ''}`}>
      <div id="articleModalContent">
        <span className="close" onClick={closeModal}>&times;</span>
        <h3>Analyze Your Own Article</h3>
        <p>You can input a URL of an online article and select one of the domains. You'll be able to see the results run by our pipeline.</p>
        <div>
          {samples.map((sample, index) => (
            <button className="btn btn-outline-success" key={index} onClick={() => loadSample(sample)}>
              Try {sample.label} Sample
            </button>
          ))}
        </div>

        <label htmlFor="url">Article URL:</label>
        <input type="text" id="url" name="url" value={url} onChange={(e) => setUrl(e.target.value)} />
        <br />
        <label htmlFor="domain">Domain:</label>
        <select id="domain" name="domain" value={domain} onChange={(e) => setDomain(e.target.value)}>
          {
            ['Social Media', 'Voice Assistant', 'Augmented/Virtual Reality', "Computer Vision", "Robotics", "Mobile Technology", "AI Decision-Making", "Neuroscience", "Computational Biology", "Ubiquitous Computing"]
              .map((option, index) => (
                <option key={index} value={option.toLowerCase().replace(/ /g, "_")}>{option}</option>
              ))
          }
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
