$(document).ready(function () {
    console.log("ready!");
});

function callAjax() {
    if (filled) {
        $("#mainTable").fadeOut(1000);
        $("#mainTable").innerHTML = "";
        $("#mainTable").fadeIn(1000);
    }

    var main_skills = $("#mainSkills").val();
    var additional_skills = $("#additionalSkills").val();
    var all_skills = main_skills.split(',').concat(additional_skills.split(','));
    all_skills = all_skills.map(function (e) {
        e = e.trim();
        return e;
    });
    all_skills = all_skills.join('+');

    console.log(all_skills);
    $("#spinner").css("visibility", "visible");
    $.ajax({
        url: "http://127.0.0.1:5000/reverse_search",
        data: {
            skills: all_skills
        },
        success: function (result) {
            if(result===""){
                notFound();
            }
            var result_arr = JSON.parse(result);
            result_arr.forEach(element => {
                addRow(element);
            });

        }
    });
};

function notFound(){
    row = `<tr>
            <td align="left">No results found</td>
            </tr>`
}

function craftRow(skill, value) {
    row = `<tr>
            <td align="left">${skill}</td>
            <td align="center">
                <div class="container">
                    <div class="row">
                        <div class="col-10 mt-1">
                            <div class="progress">
                                <div class="progress-bar" role="progressbar"
                                    style="width: ${value}%; background-color: #e1b794;" aria-valuenow="${value}"
                                    aria-valuemin="0" aria-valuemax="100">
                                </div>
                            </div>
                        </div>
                        <div class="col-1">
                            ${value}%
                        </div>
                    </div>
                </div>
            </td>
        </tr>`
    return row;
}