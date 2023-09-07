import CHI_LOGO from '../../assets/CHI.png';  
import FUTURISM_LOGO from '../../assets/Futurism.png';  
import MIT_TECH_REVIEW_LOGO from '../../assets/MIT Tech Review.png';
import TechCrunch from '../../assets/TechCrunch.png';
import The_Verge from '../../assets/The Verge.png';
import WIRED from '../../assets/Wired.png';  
import "./Card.css"

function Card({ mode, title, text, gpt_summary, url, sector, magazine, label, onAdd, onRemove }) {
  // Function to determine color based on domain/sector
  const getCardHeaderColor = (aspectLabel) => {
    switch(aspectLabel) {
      case 'economy': 
        return "rgba(102, 194, 165, 0.4)";
      case 'equality & justice':
        return "rgba(252, 141, 98, 0.4)";
      case 'health & wellbeing':
        return "rgba(141, 160, 203, 0.4)";
      case 'access to information & discourse':
        return "rgba(231, 138, 195, 0.4)";  
      case 'politics':
        return "rgba(166, 216, 84, 0.4)";
      case 'power dynamics':
        return "rgba(255, 217, 47, 0.4)";
      case 'security & privacy':
        return "rgba(229, 196, 148, 0.4)";
      case 'social norms & relationship':
        return "rgba(179, 179, 179, 0.4)";
      case 'user experience':
        return "rgba(76, 175, 80, 0.4)";
      case 'environment & sustainability':
        return "rgba(123, 123, 231, 0.4)";
      default:
        return 'bg-secondary';  // Default color for unknown domains
    }
  };

  const getMagazineLogo = (magazine) => {
    switch(magazine) {
      case 'CHI':
        return CHI_LOGO;
      case 'Futurism':
        return FUTURISM_LOGO;
      case 'MIT Tech Review':
        return MIT_TECH_REVIEW_LOGO;
      case 'TechCrunch':
        return TechCrunch;
      case 'The Verge':
        return The_Verge;
      case 'Wired':
        return WIRED;
      default:
        return 'bg-secondary';  // Default color for unknown domains
    }
  };

  const boldFirstLetter = (text) => {
    return text.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
    // return text.charAt(0).toUpperCase() + text.slice(1);
  };

  const cardHeaderColor = getCardHeaderColor(label);
  const magazineLogo = getMagazineLogo(magazine);

  return (
    <div className="card mb-3">
      <div className={`card-header`} style={{backgroundColor: cardHeaderColor}}>
        <h5 className="card-title">{boldFirstLetter(label)}</h5>
      </div>
      <div className="card-body">
        <a 
          href={url} 
          className="card-link" 
          target="_blank" 
          rel="noopener noreferrer"
          style={{textDecoration: 'none'}}>
            <h5 className="card-title">{title}</h5>
        </a>
        <p className="card-text">{gpt_summary}</p>
        {/* <p className="card-text"><small className="text-muted">{sector}</small></p> */}
        

        <div className="d-flex justify-content-between">
          <div className="p-2">
            {
              mode !== 'accordion' && 
              <button className="bookmark-btn btn btn-sm mr-2" onClick={onAdd}>
                <i className="fas fa-bookmark"></i>
              </button>
            }
            <button className="bookmark-cancel-btn btn btn-sm" onClick={onRemove} style={{color: "#ff9800"}}>
              <i className="fas fa-times-circle"></i>
            </button>
          </div>
          <div className="p-2">
            <img src={magazineLogo} alt={`${magazine} logo`} height="15" />
          </div>
        </div>
        {/* <p className="card-text"><small className="text-muted">{magazine + ''}</small></p> */}
      </div>
    </div>
  );
}

export default Card;
