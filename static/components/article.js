const getResultCard = (url, domain, response) => {
    if(!response["title_relevant"]) {
        return $(`
        <div class="alert alert-warning" role="alert">
            Sorry, but the <strong>title</strong> of the article doesn't seem relevant to the topic of undesirable consequences in this domain. (Note that the decision is generated by GPT-3.)
        </div>
        `)
    } else if(!response["content_relevant"]) {
        return $(`
            <div class="alert alert-warning" role="alert">
               Sorry, but the <strong>content</strong> of the article doesn't seem relevant to the topic of undesirable consequences in this domain. (Note that the decision is generated by GPT-3.)
            </div>
        `)
    } 

    return $(`
        <div id="card-trial" class="col-12 mb-3" >
            <div class="card shadow uccards" style="background-color:` + card_colors[response.aspect] + `">
                <div id="cardhead" class="card-header" style="background-color:` + aspect_colors[response.aspect] + `">
                <div>
                Aspect: ` + response.aspect + `
                </div>
            </div>
            <div class="card-body">
                <p class="card-text"><strong>Summary</strong>: ` + response.summary + ` (Note that the summary is generated by GPT-3.)</p>
                <a style="text-decoration:none;" href="` + url  + `" target="_blank"><h6 class="card-title">` + response.title + `</h6></a>
            </div>
        </div>
        <br>
        <div class="alert alert-success" role="alert">
            Please note that this card will <strong>NOT</strong> be automatically added to the database. However, we have received the input about this article and will use it to improve the catalog upon moderation. The information is received anonymously.
        </div>
        `);
}

$(document).ready(function() {
    // When the user clicks the button, open the modal
    $("#articleBtn").on("click", function(){
        $("#articleModal").css("display", "block");
    });

    // When the user clicks on <span> (x), close the modal
    function closeModal() {
        $("#results").html("");
        $("#articleModal").css("display", "none");
    }

    // When the user clicks the Submit button, submit the article to the server and display the results
    function submitArticle() {
        // Validate the URL using a regular expression
        if (!/^(ftp|http|https):\/\/[^ "]+$/.test($("#url").val())) {
            alert("Invalid URL format");
            return;
        }

        // Show loading spinner
        $("#results").html("").append($("<div>").addClass("loader"));
        
        console.log($("#domain").val());
        console.log($("#url").val());
        // Send the article data to the server using an AJAX request
        $.ajax({
            type: "POST",
            url: "http://localhost:8000/request",
            contentType: "application/json",
            data: JSON.stringify({"url": $("#url").val(), "domain": $("#domain").val()}),
            success: function(response) {
                $("#results .loader").remove();
                $("#results").html("").append(getResultCard($("#url").val(), $("#domain").val(), response));
            },
            error: function() {
                alert("An error occurred. Please try again.");
            }
        });
    }

    $("#submitButton").on("click", submitArticle);

    // Attach event handlers
    $(".close").on("click", closeModal);

    $(window).click(function(event) {
        if ($(event.target).is($("#articleModal"))) {
            closeModal();
        }
    });
});