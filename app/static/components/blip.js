// // declare data file path
// SM_Label = 'Social Media';
// VA_Label = 'Virtual Assistant';
// VR_Label = 'Virtual Reality';

// FILE_DICT = {
//     'sm': '/static/data/new_sm_summs1.csv',
//     'va': '/static/data/new_va_summs1.csv',
//     'vr': '/static/data/new_vr_summs1.csv',
//     // 'all': '/static/data/overall.csv'
//     'all': '/static/data/merged.csv'
// }

// let mainTech = "";

// const aspect_colors = {
//   "Economy" : "rgba(102, 194, 165, 0.4)",
//   "Equality & Justice" : "rgba(252, 141, 98, 0.4)",
//   "Health & Wellbeing" : "rgba(141, 160, 203, 0.4)",
//   "Information, Discourse & Governance" : "rgba(231, 138, 195, 0.4)",
//   "Politics" : "rgba(166, 216, 84, 0.4)",
//   "Power" : "rgba(255, 217, 47, 0.4)",
//   "Security & Privacy" : "rgba(229, 196, 148, 0.4)",
//   "Social Norms & Relationships" : "rgba(179, 179, 179, 0.4)",
//   "User Experience & Entertainment" : "rgba(76, 175, 80, 0.4)",
//   "Environment & Sustainability" : "rgba(123, 123, 231, 0.4)",
// }

// var name_dict = {
//     "economy": "Economy",
//     "equality & justice": "Equality & Justice",
//     "health & well-being": "Health & Wellbeing",
//     "health & wellbeing": "Health & Wellbeing",
//     "information, discourse & governance": "Information, Discourse & Governance",
//     "access to information & discourse": "Information, Discourse & Governance",
//     "politics": "Politics",
//     "power": "Power",
//     "security & privacy": "Security & Privacy",
//     "social norms & relationship": "Social Norms & Relationships",
//     "user experience": "User Experience & Entertainment",
//     "environment & sustainability": "Environment & Sustainability",
//     "power dynamics": "Power",
//     "Navigation": "Health & Wellbeing",
//     'Economy': "Economy",
//     'Equality & Justice': "Equality & Justice",
//     'Health & Wellbeing': "Health & Wellbeing",
//     'Information, Discourse & Governance': "Information, Discourse & Governance",
//     'Politics': "Politics",
//     'Power': "Power",
//     'Security & Privacy': "Security & Privacy",
//     'Social Norms & Relationships': "Social Norms & Relationships",
//     'User Experience & Entertainment': "User Experience & Entertainment",
//     'Environment & Sustainability': "Environment & Sustainability"
// }


// // declare variables
// let data = [];
// let maindata = [];
// let accepted = [], rejected = [];  


// // find the current tech sector from the url
// const getUrlParameter = (sParam) => {
//     var sPageURL = window.location.search.substring(1),
//         sURLVariables = sPageURL.split('&'),
//         sParameterName,
//         i;

//     for (i = 0; i < sURLVariables.length; i++) {
//         sParameterName = sURLVariables[i].split('=');

//         if (sParameterName[0] === sParam) {
//             return sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
//         }
//     }
//     return false;
// };


// const loadD3Data = async (filePath) => {
//     try {
//         const data = await d3.csv(filePath);
//         return data;
//     } catch (error) {
//         console.log(error);
//         throw error;
//     }
// }


// const loadData = async (tech) => {
//     if(tech === 'sm') {
//         return await loadD3Data(SM_FILE);
//     } else if (tech === 'vr') {
//         return await loadD3Data(VR_FILE);
//     } else if (tech === 'va') {
//         return await loadD3Data(VA_FILE);
//     }
// }


// const loadHeader = (tech) => {
//     if(tech === 'sm') {
//         $('#domainlabel').text(SM_Label);
//     } else if (tech === 'vr') {
//         $('#domainlabel').text(VR_Label);
//     } else if (tech === 'va') {
//         $('#domainlabel').text(VA_Label);
//     }
// }


// const loadAspect = () => {
//     // render initial color options
//     $('#aspectinput').html('<option value="All" selected>All</option>')
//     $.each(aspect_colors, function(index, value) {
//         $('#aspectinput').append($("<option />").val(index).text(index));
//     });
// }

// const loadCards = (data) => {
//     // clear html setup
//     $("#allcards").html('');
//     $('#accepted-block').html('')
//     $('#rejected-block').html('')

//     datalen = data.length
//     accelen = accepted.length
//     rejelen = rejected.length
//     $("#accepted-bar").css('width', accelen / datalen * 100 + '%')
//     $("#rejected-bar").css('width', rejelen / datalen * 100 + '%')
//     $("#accepted-count").text(accelen)
//     $("#rejected-count").text(rejelen)

//     data.forEach(function(d) {
//         if (accepted.includes(d.index)) {
//             accepted_color = '#ffcdd2'
//             like_color = '#c62828'
//             $('#accepted-block').append(`
//               <div class="card shadow-sm mb-2 p-0 accepted-card">
//                 <div class="card-body">
//                   ` + d.title + `
//                 </div>  
//               </div>
//             `)         
//           } else {
//             accepted_color = '#f5f5f5'
//             like_color = '#999'
//           }

//           if (rejected.includes(d.index)) {
//             $('#rejected-block').append(`
//               <div class="card shadow-sm mb-2 p-0 accepted-card">
//                 <div class="card-body">
//                   ` + d.title + `
//                 </div>  
//               </div>
//             `)
//           } else {
//             let cardText = "";
//             console.log(mainTech);
//             if(mainTech === "all" || mainTech === "") {
//                 cardText = "<p class='card-text'><strong>[" + d.sector + "]</strong>: " + d.gpt_summary + "</p>";
//             } else{
//                 cardText = "<p class='card-text'>" + d.gpt_summary + "</p>";
//             }

//             $("#allcards").append(`
//                 <div id="card-` + d.index + `" class="col-3 mb-3" >
//                     <div id="cardhead" class="card-header" style="background-color:` + aspect_colors[name_dict[d.label]] + `">
//                     <div class="justify-content-between">
//                         <div>` + name_dict[d.label] + `</div>

//                     </div>
//                     </div>
//                         <div class="card-body">` +
//                         cardText +
//                         `<a style="text-decoration:none;" href="` + d.url + `" target="_blank"><h6 class="card-title">` + d.title + `</h6></a>
//                         <div class="d-flex justify-content-between">
//                         <div>
//                             <button id="accept-` + d.index + `" onClick="accept_option(this.id)" class="btn btn-sm accept-btn" style="color: ` + like_color + `">
//                                 <i class="fas fa-bookmark"></i>
//                             </button>
//                             <button id="reject-` + d.index + `" onClick="reject_option(this.id)" class="btn btn-sm reject-btn" style="color: #ff9800">
//                                 <i class="fas fa-times-circle"></i>
//                             </button>
//                         </div>
//                         <div>
//                             <img src="/static/images/logos/` + d.magazine + `.png" height="15">
                            
//                         </div>
                            
//                         </div>
//                             </div>
//                     </div>
//                 </div>
//             `);
//         }
//     });

//     var msnry = new Masonry('#allcards');
//     msnry.layout();
// }

// const onChange = (timeout) => {
//     wto = setTimeout(function() {
//         let text = $("#search").val();
//         let aspect = $("#aspectinput").val();
//         let texbool = true;
//         let aspbool = true;
//         let newdata = [];
        
//         data.forEach(function(d) {
//             if (aspect != "All") {
//                 aspbool = d.label.toLowerCase().includes(aspect.toLowerCase())
//             }
//             if (text.length >= 3) {
//                 texbool = d.gpt_summary.toLowerCase().includes(text.toLowerCase())
//             }
//             if (aspbool && texbool) {
//               newdata.push(d);
//             }
//         });

//         loadCards(newdata);
//         }, timeout); 
// }

// const shuffleCards = (data) => {
//     data = d3.shuffle(data);
//     newLst = [];
//     constraintSet = [];
//     for(let i = 0; i < data.length; i++) {
//       if(constraintSet.includes(data[i].label)) {
//         newLst.push(data[i]);
//       } else {
//         newLst.unshift(data[i]);
//         constraintSet.push(data[i].label);
//       }
//     }
//     return newLst;
// }

// // function for accepting and rejecting bookmarks
// const accept_option = (elem) => {
//     elemid = elem.split('-')[1]
//     if (accepted.includes(elemid)) {
//       accepted = accepted.filter(x => x !== elemid);
//     } else {
//       accepted.push(elemid)
//     }
    
//     loadCards(data);
// }

// const reject_option = (elem) => {
//     elemid = elem.split('-')[1]
//     rejected.push(elemid)
//     if (accepted.includes(elemid)) {
//       accepted = accepted.filter(x => x !== elemid);
//     }
    
//     $("#card-" + elemid).css('z-index', 100)
//     $("#card-" + elemid).animate({opacity: '0', left: 3000, top: 500}, 500, function() {
//         loadCards(data);
//     });
// }

// function searchArticles() {
//     // Send the article data to the server using an AJAX request
//     $.ajax({
//         type: "POST",
//         // url: "http://localhost:8000/search",
//         url: "104.197.248.47:80/search",
//         contentType: "application/json",
//         data: JSON.stringify({"query": $("#search").val()}),
//         success: function(response) {
//             console.log(response);

//             d3.csv("static/data/temp_search.csv").then(function(dt){
//                 data = dt;
//                 maindata = dt;
//             }).then(function(){
//                 loadCards(maindata);
//             });
//         },
//         error: function() {
//             alert("An error occurred. Please try again.");
//         }
//     });
// }

// $(document).ready(function() {
//     // let tech = getUrlParameter('tech');
//     tech = "all"
//     loadHeader(tech);
//     loadAspect();
//     mainTech = tech;

//     d3.csv(FILE_DICT[tech]).then(function(dt){
//         data = dt;
//         maindata = dt;
//     }).then(function(){
//         loadCards(shuffleCards(maindata));
//     });

//     // $("#search").on('input', function(e){
//     //     // onChange(500);
//     //     // 
//     // });
//     $("#search").bind('enterKey', searchArticles);
//     $("#search").keyup(function(e){
//         if(e.keyCode == 13) {
//             $("#search").trigger("enterKey");
//         }
//     });

  
//     $("#aspectinput").on('input', function(e){
//         onChange(0);
//     });
    
//     $('#shuffle-btn').on('click', function(e) {
//         loadCards(shuffleCards(maindata));
//     });

//     $('#domaininput').on('input', function(e) {
//         let domain = $("#domaininput").val();
//         mainTech = domain;
//         d3.csv(FILE_DICT[domain]).then(function(dt){
//             data = dt;
//             maindata = dt;
//         }).then(function(){
//             loadCards(shuffleCards(maindata));
//         });
//     })
    
// });