import CHI_LOGO from '../../assets/CHI.png';  
import FUTURISM_LOGO from '../../assets/Futurism.png';  
import MIT_TECH_REVIEW_LOGO from '../../assets/MIT Tech Review.png';
import TechCrunch from '../../assets/TechCrunch.png';
import The_Verge from '../../assets/The Verge.png';
import WIRED from '../../assets/Wired.png';  
import "./Card.css"

import {
  IconCashBanknote, 
} from '@tabler/icons-react';

function Card({ mode, title, text, gpt_summary, url, sector, magazine, label, onAdd, onRemove }) {
  // Function to determine color based on domain/sector
  const getCardHeaderColor = (aspectLabel) => {
    switch(aspectLabel) {
      case 'economy': 
        return "#cfd8dc";
      case 'equality & justice':
        return "#f8bbd0";
      case 'health & wellbeing':
        return "#b3e5fc";
      case 'access to information & discourse':
        return "#e6ee9c";  
      case 'politics':
        return "#ffcc80";
      case 'power dynamics':
        return "#ef9a9a";
      case 'security & privacy':
        return "#fff59d";
        // "";
      case 'social norms & relationship':
        return "#e1bee7";
      case 'user experience':
        return "#d1c4e9";
      case 'environment & sustainability':
        return "#aed581";
      default:
        return 'bg-secondary';  // Default color for unknown domains
    }
  };

  // Function to determine tabler icon logo based on aspects (e.g., economy, politics, etc.)
  // const processAspectLogo = (aspectLabel) => {
  //   switch(aspectLabel) {
  //     case 'economy':
  //       return (<IconCashBanknote size="16px" />);
  //     case 'equality & justice':
  //       return 'IconUsers';
  //     case 'health & wellbeing':
  //       return 'IconHeart';
  //     case 'access to information & discourse':
  //       return 'IconFileText';
  //     case 'politics':
  //       return 'IconFlag';
  //     case 'power dynamics':
  //       return 'IconPower';
  //     case 'security & privacy':
  //       return 'IconLock';
  //     case 'social norms & relationship':
  //       return 'IconUsers';
  //     case 'user experience':
  //       return 'IconUserCheck';
  //     case 'environment & sustainability':
  //       return 'IconGlobe';
  //     default:
  //       return 'IconFileText';  // Default icon for unknown domains
  //   }
  // };


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
    <div className="card mb-3 shadow card-class">
      <div className={`card-header`} style={{backgroundColor: cardHeaderColor}}>
        <h5 className="card-title aspect"><span className='aspect-name'>{boldFirstLetter(label)}</span></h5>
      </div>
      <div className="card-body">
        {/* <a 
          href={url} 
          className="card-link" 
          target="_blank" 
          rel="noopener noreferrer"
          style={{textDecoration: 'none'}}> */}
            <h5 className="news-title">{title}</h5>
        {/* </a> */}
        <p className="card-text">{gpt_summary}</p>
        {/* <p className="card-text"><small className="text-muted">{sector}</small></p> */}
        

        <div className="d-flex justify-content-between">
          <div className="">
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
          <div className="">
            <img src={magazineLogo} alt={`${magazine} logo`} height="15" />
          </div>
        </div>
        {/* <p className="card-text"><small className="text-muted">{magazine + ''}</small></p> */}
      </div>
    </div>
  );
}

export default Card;
