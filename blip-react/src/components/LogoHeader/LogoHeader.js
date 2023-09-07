import logo from '../../assets/blip.png';  // assuming you've moved blip.png to the src/images folder
import './LogoHeader.css';

const LogoHeader = ({openArticleModal, openContributeModal}) => {
    return (
        <header id="homepage-logo-header">
            <div></div>
            
            <div className="logo-container">
                <img src={logo} alt="Blip Logo" className="logo-image"/>
                <div className="logo-text">
                    Explore a catalog of unintended, undesirable consequences of technology to gain awareness!
                </div>
            </div>

            <div className="buttons">
                <button className="contribute-button" alt="Import your own article from an URL" onClick={openArticleModal}>
                    Import an Article
                </button>
                <button className="contribute-button" alt="Contribute a domain that you think is missing!" onClick={openContributeModal}>
                    Suggest a New Domain
                </button>
            </div>
        </header>
    );
};

export default LogoHeader;
