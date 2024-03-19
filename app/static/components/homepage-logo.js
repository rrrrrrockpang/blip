// const buildHomepageLogo = () => {
//     console.log("Building homepage logo");

//     $("#homepage-logo-header").append(`
//     <div class="row flex-nowrap justify-content-between align-items-center">
//         <div class="col-3 pt-1">
//         <!-- <a class="link-secondary" href="#">Subscribe</a> -->
//         </div>
//         <div class="col-6 text-center">
//             <div class="row justify-content-center">
//                 <div class="col-3 align-self-center">
//                     <a href="/"><img src={{ url_for('static', path='/images/blip.png') }} class="img-fluid"></a>
//                 </div>
//             </div>
//         </div>
//         <div class="col-3 d-flex align-items-center">
//         </div>
//     </div>`);
// }

// const buildPlayground = () => {
//     console.log("Building playground");
// };

// const buildHompageNavbar = () => {
//     console.log("Building navbar");
//     $("#homepage-navbar").append(`
//         <div class="col-12">
//             <div class="card mb-5 shadow-sm bg-light">
//                 <div class="card-body d-flex flex-column">
//                     <div class="row display-flex">
//                         <div class="col-3">
//                             <div class="row">
//                                 <div class="input-group mb-3 btn-group dropup">
//                                     <label class="input-group-text" for="domaininput">Domain</label>
//                                     <select class="form-select" id="domaininput">
//                                         <option value="all" selected>All</option>
//                                         <option value="sm">Social Media</option>
//                                         <option value="va">Voice Assistants</option>
//                                         <option value="vr">Virtual Reality</option>
//                                     </select>
//                                 </div>
//                             </div>
//                         </div>
                        
//                         <div class="col-9 align-self-end">
//                             <div class="row">
//                                 <div class="col-6">
//                                     <input id="search" type="text" class="form-control" placeholder="Search terms (≥2 chars)" aria-label="Search terms (≥3 chars)" aria-describedby="basic-addon1">
//                                 </div>
//                                 <div class="col-4 justify-content-end">
//                                     <div class="input-group mb-3">
//                                         <label class="input-group-text" for="aspectinput">Aspect</label>
//                                         <select class="form-select" id="aspectinput"><option value="All" selected=""></option><option value="undefined">undefined</option></select>
//                                     </div>
//                                 </div>
//                                 <div class="col-2 justify-content-end">
//                                     <button id="shuffle-btn" class="btn btn-light btn-block"><i class="fas fa-sync-alt"></i> Shuffle</button>
//                                 </div>
//                             </div>
//                         </div>
//                     </div>
//                 </div>
//             </div>
//         </div>`);
// };

// const buildDomainSelector = () => {
//     console.log("Building domain selector");
//     $("#domain-selector").append(`
//         <div class="row">
//         <div class="input-group mb-3 btn-group dropup">
//             <label class="input-group-text" for="domaininput">Domain</label>
//             <select class="form-select" id="domaininput">
//                 <option value="all" selected>All</option>
//                 <option value="sm">Social Media</option>
//                 <option value="va">Voice Assistants</option>
//                 <option value="vr">Virtual Reality</option>
//             </select>
//         </div>
//     </div>`);
// };

// const buildAspectSelector = () => {
//     console.log("Building aspect selector");
//     $("#aspect-selector").append(`
//         <div class="row">
//             <div class="input-group mb-3 btn-group dropup">
//                 <label class="input-group-text" for="aspectinput">Aspect</label>
//                 <select class="form-select" id="aspectinput">
//                     <option value="All" selected="">All</option>
//                     <option value="undefined">undefined</option>
//                 </select>
//             </div>
//         </div>`);
// };

// const buildShuffleButton = () => {
//     console.log("Building shuffle button");
//     $("#shuffle-button").append(`
//         <div class="row">
//             <div class="col-12">
//                 <button id="shuffle-btn" class="btn btn-light btn-block" data-bs-toggle="tooltip" data-bs-placement="top" title="Shuffle">
//                     <i class="fas fa-sync-alt"></i>
//                 </button>
//             </div>
//         </div>`);
// };

// const buildSearchBar = () => {
//     console.log("Building search bar");
//     $("#search-bar").append(`
//         <div class="row">
//             <div class="col-12">
//                 <input id="search" type="text" class="form-control" placeholder="Search terms (≥2 chars)" aria-label="Search terms (≥3 chars)" aria-describedby="basic-addon1">
//             </div>
//         </div>`);
// };

// const buildBookMarkBar = () => {
//     console.log("Building bookmark bar");
//     $("#bookmark-bar").append(`
//         <div class="col-12">
//             <div class="row">
//                 <div class="col-12">
//                     <div class="progress my-3" style="height:20px">
//                         <div id="accepted-bar" class="progress-bar progress-bar-striped bg-danger progress-bar-animated" role="progressbar" style="width: 50%" aria-valuenow="10" aria-valuemin="0" aria-valuemax="100"></div>
//                         <div id="rejected-bar" class="progress-bar progress-bar-striped bg-warning progress-bar-animated" role="progressbar" style="width: 50%" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100"></div>
//                     </div>
//                 </div>
//             </div>


//             <div class="accordion" id="accordionExample">
//                 <div class="accordion-item">
//                   <h2 class="accordion-header" id="headingTwo">
//                     <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
//                       <span style="color: #c62828">
//                         <i class="fas fa-bookmark"></i>
//                       </span> &nbsp; Bookmarked Articles &nbsp; <span id="accepted-count" class="badge rounded-pill bg-dark">0</span>
//                     </button>
//                   </h2>
//                   <div id="collapseTwo" class="accordion-collapse collapse" aria-labelledby="headingTwo" data-bs-parent="#accordionExample">
//                     <div id="accepted-block" class="accordion-body">
//                       <strong>This is the second item's accordion body.</strong> It is hidden by default, until the collapse plugin adds the appropriate classes that we use to style each element. These classes control the overall appearance, as well as the showing and hiding via CSS transitions. You can modify any of this with custom CSS or overriding our default variables. It's also worth noting that just about any HTML can go within the <code>.accordion-body</code>, though the transition does limit overflow.
//                     </div>
//                   </div>
//                 </div>

//                 <div class="accordion-item">
//                   <h2 class="accordion-header" id="headingThree">
//                     <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseThree" aria-expanded="false" aria-controls="collapseThree">
//                       <span style="color: #ff9800">
//                         <i class="fas fa-times-circle"></i>
//                       </span> &nbsp; Removed from my view &nbsp; <span id="rejected-count" class="badge rounded-pill bg-dark">0</span>
//                     </button>
//                   </h2>
//                   <div id="collapseThree" class="accordion-collapse collapse" aria-labelledby="headingThree" data-bs-parent="#accordionExample">
//                     <div id="rejected-block" class="accordion-body">
//                       <strong>This is the third item's accordion body.</strong> It is hidden by default, until the collapse plugin adds the appropriate classes that we use to style each element. These classes control the overall appearance, as well as the showing and hiding via CSS transitions. You can modify any of this with custom CSS or overriding our default variables. It's also worth noting that just about any HTML can go within the <code>.accordion-body</code>, though the transition does limit overflow.
//                     </div>
//                   </div>
//                 </div>
//             </div>
//         </div>`);
// };

// $(document).ready(() => {
//     // buildHomepageLogo();
//     // buildHompageNavbar();
//     buildBookMarkBar(); 
//     buildDomainSelector();
//     buildAspectSelector();
//     buildShuffleButton();
//     buildSearchBar();
// });