function createTabele(tablebody, datatime, objectData) {
  var newRowTr = document.createElement("tr");
  var newColTd1_data = document.createElement("td");
  var newColTd2_travelStart = document.createElement("td");
  var newColTd3_travelEnd = document.createElement("td");
  var newColTd4_workStart = document.createElement("td");
  var newColTd5_workEnd = document.createElement("td");
  var newColTd6_standardTime = document.createElement("td");
  var newColTd7_projectMachine = document.createElement("td");
  var newColTd8_netzVorgang = document.createElement("td");
  var newColTd9_link = document.createElement("td");

  newRowTr.appendChild(newColTd1_data);
  newRowTr.appendChild(newColTd2_travelStart);
  newRowTr.appendChild(newColTd3_travelEnd);
  newRowTr.appendChild(newColTd4_workStart);
  newRowTr.appendChild(newColTd5_workEnd);
  newRowTr.appendChild(newColTd6_standardTime);
  newRowTr.appendChild(newColTd7_projectMachine);
  newRowTr.appendChild(newColTd8_netzVorgang);
  newRowTr.appendChild(newColTd9_link);

  if (datatime === objectData.date) {
    newColTd1_data.innerText = datatime;
    newColTd2_travelStart.innerText = objectData.travel_start;
    newColTd3_travelEnd.innerText = objectData.travel_end;
    newColTd4_workStart.innerText = objectData.work_start;
    newColTd5_workEnd.innerText = objectData.work_end;
    newColTd6_standardTime.innerText = objectData.workimes_standard__description;
    newColTd7_projectMachine.innerText = objectData.project_machine;
    newColTd8_netzVorgang.innerText = objectData.netzplan_vorgang;
    newColTd9_link.innerText = "link";
  }
  else {
    newColTd1_data.innerText = datatime;
    newColTd2_travelStart.innerText = "--";
    newColTd3_travelEnd.innerText = "--"
    newColTd4_workStart.innerText = "--";
    newColTd5_workEnd.innerText = "--";
    newColTd6_standardTime.innerText = "--";
    newColTd7_projectMachine.innerText = "--";
    newColTd8_netzVorgang.innerText = "--";
    newColTd9_link.innerText = "link";
  }

  tablebody.appendChild(newRowTr);
}
var htbody = document.querySelector("tbody[id=id_week_overview_js]");

var hListData = JSON.parse(document.getElementById("list_data").textContent);
var hObjectData = JSON.parse(document.getElementById("object_data").textContent);

console.log(hListData, hObjectData);

var j = 0;
for (let i = 0; i < hListData.length; ++i) {
  createTabele(htbody, hListData[i], hObjectData[j]);
  if (hListData[i] === hObjectData[j].date) {
    j++;
  }
}