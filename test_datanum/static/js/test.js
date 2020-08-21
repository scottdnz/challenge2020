$(document).ready(function() {

    let VettingPage = {

        fillCMTable: function(data) {
            let cm = data["construction_materials"];
            let constructionTypeNames = Object.keys(cm);
            constructionTypeNames.sort();

            // Each block looks like:
            /*
             <div class="jtilex col-md-2">
                <h3>Foundations</h3>
                <ul id="cd_cm_" class="ui-selectable">
                    <li id="1" class="ui-selectee">Concrete</li>
                    <li id="20" class="ui-selectee">Concrete Piles</li>
                    <li id="70" class="ui-selectee">Driven Piles</li>
                    <li id="9" class="ui-selectee">Masonry</li>
                    <li id="72" class="ui-selectee">Polystyrene Block System</li>
                    <li id="74" class="ui-selectee">Specific Engineer Design Foundations</li>
                    <li id="23" class="ui-selectee">Steel Piles</li>
                    <li id="21" class="ui-selectee">Timber Piles</li>
                </ul>
            </div>
            */

            for (let i = 0; i < constructionTypeNames.length; i++) {

                let currentCTypeName = constructionTypeNames[i];

                let uList = document.createElement("ul");
                uList.className = "ui-selectable";

                for (let j = 0; j < cm[currentCTypeName].length; j++) {

                    let currentCm = cm[currentCTypeName][j];

                    let textVal = document.createTextNode(currentCm["Name"]);

                    let listItem = document.createElement("li");
                    listItem.className = "ui-selectee";
                    listItem.setAttribute("id", currentCm["ID"]);
                    listItem.appendChild(textVal);

                    uList.appendChild(listItem);
                }

                let headingVal = document.createTextNode(currentCTypeName);
                let heading = document.createElement("h3");
                heading.appendChild(headingVal);

                let cTypeSection = document.createElement("div");
                cTypeSection.className = "jtilex col-md-2";

                cTypeSection.appendChild(heading);

                cTypeSection.appendChild(uList);

                $("#construction_material_container").append(cTypeSection);
            }

            $(".ui-selectee").click(function() {
                $(this).toggleClass("ui-selected");
            });
        };


        fillVetTable: function(data, staticDir) {
            /*
             <tr data-row-number="1" id="l_85280">
                <td class="mr" id="q_65099">
                    <span class="pull-right question-badges" style=
                    "padding: 2px 8px;"><span id="200472_2578_65099"></span></span>
                    <b id="t_65099">Application Form:</b> Has the application form
                    been properly completed?

                    <br> <i>
                    <img src="{% static 'img/icons/lightbulb.png' %}" style="cursor: default;">
                    <span style="color: #0066FF; font-size: 14px">
                    If Title is not yet available a subdivision scheme plan is requ
                    </span>
                    </i>

                    <div class="ref" id="ref_65099"></div>
                    <div class="hl"></div>
                </td>
                <td class="rh">
                    <img alt="Yes" id="s_p_65099" src=
                    "{%%20static%20'img/yes.png'%20%}">
                    <img alt="No" id="s_f_65099"
                    src="{%%20static%20'img/no_off.png'%20%}">
                    <img alt="N/A" id=
                    "s_u_65099" src="{%%20static%20'img/na_off.png'%20%}">
                    <img alt=
                    "Write Notes" id="notes_65099" src=
                    "{%%20static%20'img/notes.png'%20%}">
                </td>
            </tr>
            */

            let questions = data["vetting_questions"];
            let jobIds = Object.keys(questions);
            jobIds.sort();

            for (let i = 0; i < jobIds.length; i++) {

                let currentJobId = jobIds[i];

                for (let j = 0; j < questions[currentJobId].length; j++) {
                    let currentQuestion = questions[currentJobId][j];

                    let qRow = document.createElement("tr");
                    qRow.setAttribute("data-row-number", String(++j));
                    qRow.setAttribute("id", "l_" + String(currentQuestion["criteriaLId"]));

                    // Cell 1
                    let qCell = document.createElement("td");
                    qCell.className = "mr";
                    qCell.setAttribute("id", "q_" + String(currentQuestion["qID"]));

                    let spanner = document.createElement("span");
                    spanner.className = "pull-right question-badges";
                    spanner.setAttribute("style", "padding: 2px 8px;");

                    let bolded = document.createElement("div");
                    bolded.setAttribute("id", "t_" + String(currentQuestion["qID"]));
                    bolded.innerHTML = "<b>" + currentQuestion["Title"] + ": </b>" + currentQuestion["Question"] ;

                    qCell.appendChild(spanner);
                    qCell.appendChild(bolded);

                    // Cell 2
                    let aCell = document.createElement("td");
                    aCell.className = "rh";

                    let img1 = document.createElement("img");
                    img1.setAttribute("id", "s_p_" + currentQuestion["qID"]);
                    img1.setAttribute("src", staticDir + "img/yes.png");

                    let img2 = document.createElement("img");
                    img2.setAttribute("id", "s_f_" + currentQuestion["qID"]);
                    img2.setAttribute("src", staticDir + "img/no_off.png");

                    let img3 = document.createElement("img");
                    img3.setAttribute("id", "s_u_" + currentQuestion["qID"]);
                    img3.setAttribute("src", staticDir + "img/na_off.png");

                    let img4 = document.createElement("img");
                    img4.setAttribute("id", "notes_" + currentQuestion["qID"]);
                    img4.setAttribute("src", staticDir + "img/notes.png");

                    aCell.appendChild(img1);
                    aCell.appendChild(img2);
                    aCell.appendChild(img3);
                    aCell.appendChild(img4);

                    qRow.appendChild(qCell);
                    qRow.appendChild(aCell);

                    $("#qtable").append(qRow);
                }
            }

        };

        preselectBoxes: function(data) {
            console.log(data);
            for (let i = 0; i < data["question_ids"].length; i++) {
                let $elem = $('#s_u_' + data["question_ids"][i]);
                let currentImgPath = $elem.attr("src");
                let newImgPath = currentImgPath.replace("_off", "_on");

                $elem.attr("src", newImgPath);
            }
        };


        // Save construction details button
        $("#cd_saveform").click(function() {
            let cmIdsSelected = [];
            $("ul.ui-selectable > .ui-selected").each(function() {
                cmIdsSelected.push($(this).attr("id"));
            });

            $('#JPO').popup('show');

            $.ajax({
                method: "POST",
                url: "/main/handle-construction-material-inputs",
                data: {"cm_ids": cmIdsSelected},
                success: function(data) {
                    preselectBoxes(data);
                },
                dataType: "json"
            });
        });


        initialise: function(staticDir, jobId) {

            $.ajax({
                url: "/main/get-construction-materials",
                data: [],
                success: function(data) {
                    fillCMTable(data);
                },
                dataType: "json"
            });

            $.ajax({
                url: "/main/get-vetting-questions?jid=" + jobId,
                data: [],
                success: function(data) {
                    fillVetTable(data, staticDir);
                },
                dataType: "json"
            });

            $('#JPO').popup({opacity: 0.8});

	        $('#JPO').popup('hide');
        }
    };

	let staticDir = "/static/";
	let jobId = $("#qtable").attr("data-jid");

	VettingPage.initialise(staticDir, jobId);

});
