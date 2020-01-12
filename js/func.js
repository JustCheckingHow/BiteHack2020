function notFound() {
    row = `<tr>
            <td align="left">No results found</td>
            </tr>`
    $("#barChart").remove();
    $("#spinner").remove();

    $("#mainTable").fadeIn(1000);

    $('#mainTable tr:last').after(row);
}



function onReady() {
    console.log("ready!");

    $('form input').keydown(function (e) {
        if (e.keyCode == 13) {
            e.preventDefault();
            callAjax();
            return false;
        }
    });
}

function craftRow(skill, value) {
    row = `<tr class="clickable-row" onclick='onSkillClick("${skill}")'>
            <td align="left" id="skillName">${skill}</td>
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