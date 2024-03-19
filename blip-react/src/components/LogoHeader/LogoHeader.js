import logo from '../../assets/blip.png';  // assuming you've moved blip.png to the src/images folder
import './LogoHeader.css';

import { Button } from '@mantine/core';
import { useNavigate } from 'react-router-dom';

import { 
    IconPlus,
    IconMicroscope
} from '@tabler/icons-react';

const LogoHeader = ({openArticleModal, openContributeModal}) => {
    const navigate = useNavigate();

    const goBackToHomePage = () => {
        navigate('/'); // Navigates back to the homepage
    };

    return (
        <header className="container-fluid" style={{margin: 0}}>
            <div className="row">
                <div className="col-md-2 col-sm-12">
                    <button 
                        className="btn btn-outline-success pt-10" 
                        onClick={goBackToHomePage}
                        style={{marginTop: 20}}    
                    >Back to Home</button>
                </div>
                
                <div className="col-md-7">
                <div className="logo-container">
                    <img src={logo} alt="Blip Logo" className="logo-image"/>
                    <div className="logo-text mt-3">
                        A catalog of unintended, undesirable consequences of technology.
                    </div>
                </div>
                </div>

                <div className="col-md-3 col-sm-12">
                        <div className="row">
                            <div className="col-12">
                                <Button
                                    variant="filled"
                                    color="green"
                                    size="xs"
                                    radius="sm"
                                    mr={20}
                                    mt={20}
                                    leftIcon={<IconPlus size={15} />}
                                    onClick={openArticleModal}
                                >
                                    Add an Article
                                </Button>
                            </div>
                        </div>

                        <div className="row">
                            <div className="col-12"> 
                                <Button
                                    variant="filled"
                                    color="green"
                                    size="xs"
                                    radius="sm"
                                    mt={10}
                                    mr={20}
                                    leftIcon={<IconMicroscope size={15} />}
                                    onClick={openContributeModal}
                                >
                                    Suggest a New Domain
                                </Button>
                            </div>
                        </div>
                    </div>
            </div>
        </header>
    );
};

export default LogoHeader;
