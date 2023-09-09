import logo from '../../assets/blip.png';  // assuming you've moved blip.png to the src/images folder
import './LogoHeader.css';

import { Button } from '@mantine/core';

import { 
    IconPlus,
    IconMicroscope
} from '@tabler/icons-react';

const LogoHeader = ({openArticleModal, openContributeModal}) => {
    return (
        <header id="homepage-logo-header" class="mt-5 mb-4">
            <div></div>
            
            <div className="logo-container">
                <img src={logo} alt="Blip Logo" className="logo-image"/>
                <div className="logo-text mt-3">
                    A catalog of unintended, undesirable consequences of technology.
                </div>
            </div>

            <div className="buttons">
                <Button
                    variant="filled"
                    color="green"
                    size="xs"
                    radius="sm"
                    mr={20}
                    leftIcon={<IconPlus size={15} />}
                    onClick={openArticleModal}
                >
                    Add an Article
                </Button>

                <Button
                    variant="filled"
                    color="green"
                    size="xs"
                    radius="sm"
                    mt={10}
                    mr={20}
                    leftIcon={<IconMicroscope size={15} />}
                    onClick={openArticleModal}
                >
                    Suggest a New Domain
                </Button>

                {/* <button className="contribute-button" alt="Import your own article from an URL" onClick={openArticleModal}>
                    Import an Article
                </button>
                <button className="contribute-button" alt="Contribute a domain that you think is missing!" onClick={openContributeModal}>
                    Suggest a New Domain
                </button> */}
            </div>
        </header>
    );
};

export default LogoHeader;
