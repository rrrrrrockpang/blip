import React from 'react';
import { useNavigate } from 'react-router-dom';
import "./Homepage.css"
import logo from "../assets/radar.png"

const HomePage = () => {
    const navigate = useNavigate(); // Using useNavigate hook

    const navigateToApp = () => {
        navigate('/app'); // Navigate to the App interface
    };

    return (
        <div className="homepage">
        <section>
            <h1>
                <img src={logo} alt="Icon" className="titleIcon" />
                <span className="bibtex">Blip</span>: &nbsp; 
                <span className="subtitle">Facilitating the Exploration of Undesirable Consequences of Digital Technologies</span>
                </h1>
            <p>Rock Yuren Pang, Sebastin Santy, René Just, Katharina Reinecke</p>
            <p>Paul G. Allen School of Computer Science and Engineering, University of Washington</p>

            <div className = "container">
                <div className = "row justify-content-center">
                    <div className = "col-auto">
                        <button className="btn btn-outline-success" onClick={navigateToApp}>
                            <i className="fas fa-desktop"></i> &nbsp;
                            Demo
                        </button>
                    </div>
                    <div className = "col-auto">
                        <a href="/">
                            <button className="btn btn-outline-success">
                                <i className="fas fa-file-alt"></i> &nbsp;
                                Full Paper
                            </button>
                        </a>
                    </div>
                    <div className = "col-auto">
                        <a href="https://github.com/rrrrrrockpang/blip/">
                            <button className="btn btn-outline-success">
                                <i className="fab fa-github"></i> &nbsp;
                                Source Code
                            </button>
                        </a>
                    </div>
                </div>
            </div>
        </section>

        <section id="abstract">
            <h2><i className="fas fa-file-alt"></i> Abstract</h2>
            <p class="abstract-text">Digital technologies have positively transformed society, but they
                have also led to undesirable consequences not anticipated at the
                time of design or development. We posit that insights into past
                undesirable consequences can help researchers and practitioners
                gain awareness and anticipate potential adverse effects. To test this
                assumption, we introduce Blip, a system that extracts real-world
                undesirable consequences of technology from online articles, sum-
                marizes and categorizes them, and presents them in an interactive,
                web-based interface. In two user studies with 15 researchers in var-
                ious computer science disciplines, we found that Blip substantially
                increased the number and diversity of undesirable consequences
                they could list in comparison to relying on prior knowledge or
                searching online. Moreover, Blip helped them identify undesirable
                consequences relevant to their ongoing projects, made them aware
                of undesirable consequences they “had never considered,” and in-
                spired them to reflect on their own experiences with technology.</p>
        </section>

        <footer>
            <p class="abstract-text">
                If you have any feedback or questions, please feel free to contact us! 
                If you plan to add more content, we are happy to help!
                We would love to improve and collaborate so that we can build tools to consider social impact of digital technologies together.
            </p>

            <i className="fas fa-envelope"></i> &nbsp; 
            <a href="mailto:ypang2@cs.washington"> 
                <button className='btn btn-outline-success'>
                    Contact Us!
                </button>
            </a>
        </footer>
        </div>
    );
};

export default HomePage;
