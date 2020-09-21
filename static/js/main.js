const menuBtn = document.querySelector('.menu-btn');
const wrapper = document.querySelector('#wrapper');
let menuOpen = true;

menuBtn.addEventListener('click', () => {
    if (!menuOpen) {
        menuBtn.classList.add('open');
        wrapper.classList.remove('toggled');
        menuOpen = true;
    }
    else{
        menuBtn.classList.remove('open');
        wrapper.classList.add('toggled');
        menuOpen = false;
    }
})

// =============================================================================
// loading food data from the database
// =============================================================================

let foodData = []

document.querySelector('#search-food-button').addEventListener('click', (e)=> {
  let searchItem  = document.querySelector('#food-search-box');
  if (searchItem.value.length == 0) {
    searchItem.style.border = "3px solid rgba(222,100,0,0.7)";
    document.querySelector('#food-item-holder').innerHTML = "Please Enter foodname";
    document.querySelector('#projector').innerHTML = "Please Enter foodname";
  }
  else {
    searchItem.style.border = "3px solid #69BDBB";
    const ENDPOINT = "/api/data/food/?search="+searchItem.value;
    // make an ajax call to the rest-api
    $.ajax({
      method: "GET",
      url: ENDPOINT,
      success: function(data){
        if (data.length == 0) {
          document.querySelector('#food-item-holder').innerHTML = "No item found";
          document.querySelector('#projector').innerHTML = "";
        }
        else{
          foodData = data;
          displayData();
        }
      },
      error: function(error_data){
        console.log(error_data)
      },
    })
  }
})

let item = null;

// dislay method is responsible for displaying the API fetched food data
let displayData = () => {
  // query selector for container holding recieved food items from API
  let parent = document.querySelector('#food-item-holder');
  // setting value of container to null so that it won't append new values into previous values
  parent.innerHTML = "";
  let projector=document.querySelector('#projector');
  projector.innerHTML = "";
  foodData.forEach((element)=>{
    let childNode = document.createElement('li');
    let textnode = document.createTextNode(element.product_name);
    childNode.appendChild(textnode);
    childNode.addEventListener('click', (e)=>{
      item = element;
      // setting background color of all child nodes to white
      for (let i=0;i<parent.childNodes.length; i++){
        parent.childNodes[i].style.backgroundColor = "#fff";
      }
      // now assigning new color to the clicked item
      e.currentTarget.style.backgroundColor = "#adf0ee";
      projector.innerHTML = element.product_name;
      projector.append(createDiv(element));
      calServingSize(element.serving_size);
    });
    parent.appendChild(childNode);
  });
};

// creting projection div to display the content of the selected item
let createDiv = (item)=>{
  const SEARCH_LIST = {'serving_size': 'Serving Size','sugars_100g':'Sugar/100g', 'fat_100g':'Fat/100g', 'carbohydrates_100g':'Carbohydrates/100g', 'fiber_100g':'Fiber/100g', 'proteins_100g':'Protein/100g', 'salt_100g':'Salt/100g', 'sodium_100g':'Sodium/100g'};
  let table = document.createElement('table');
  table.setAttribute('class', 'table table-striped table-hover');
  for(const [key, value] of Object.entries(item)){
    if (key in SEARCH_LIST) {
      let tr = document.createElement('tr');
      let td1 = document.createElement('td');
      let data = document.createTextNode(SEARCH_LIST[key]);
      td1.appendChild(data);

      let td2 = document.createElement('td');
      data = document.createTextNode(value);
      td2.appendChild(data);

      tr.appendChild(td1);
      tr.appendChild(td2);
      table.appendChild(tr);
    }
  }
  return table;
};

// cart contains the objects of selected food
let cart = []
const Food = {
  "serve size": null,
  "food": null
};

// adding item to cart and displaying on cartview
document.querySelector(".projection button").addEventListener('click', ()=>{
  // declaring the regular expression to be searched
  let re = /\d+/;
  // fetch numeric item based on regular expression
  // numericValue = parseInt(re.exec(item.serving_size));
  let food = Object.create(Food);
  food["serve size"] = parseInt(re.exec(item.serving_size));
  food["food"] = Object.assign({}, item);
  cart.push(food);
  if (cart.length > 0) {
    document.querySelector('#record-nutrition').disabled = false;
  }
  document.querySelector('#cart-view ul').innerHTML = "";
  for(let counter=0; counter < cart.length; counter++){
    // console.log(cart[counter]);
    updateCart(cart[counter]["food"]);
  }

  // update nutrition intake banner
  nutritionCalculator();
});

let nutritionCalculator = ()=>{
  let serveSize = 0, carbs = 0, fat = 0, protein = 0;
  let fooditem = null;
  for (let counter = 0; counter < cart.length; counter++){
    let re = /\d+/;
    // fetch numeric item based on regular expression
    numericValue = parseInt(re.exec(item.serving_size));
    serveSize = numericValue/cart[counter]["serve size"];
    carbs = carbs + parseFloat(cart[counter]["food"]["carbohydrates_100g"]);
    protein = protein +parseFloat(cart[counter]["food"]["proteins_100g"]);
    fat = fat + parseFloat(cart[counter]["food"]["fat_100g"]);
  }
  document.querySelector("#nutrition-board").innerHTML = `Total nutrition intake </br>carbs ${carbs} g | protein ${protein} g | sugar ${fat} g`;
};

let updateCart = (element)=>{
  listItem = document.createElement('li');
  delButton = document.createElement('button');
  delButton.innerHTML = "Delete";
  delButton.classList.add('t2b-btn-delete');
  listItem.appendChild(document.createTextNode(element.product_name));
  listItem.appendChild(delButton);
  document.querySelector('#cart-view ul').appendChild(listItem);
  delButton.addEventListener('click', (e)=> {
    // find the index of the current node in the parent list
    indexOfItemToDelete = Array.from(e.currentTarget.parentNode.parentNode.children).indexOf(e.currentTarget.parentNode);
    e.currentTarget.parentNode.remove();
    cart.splice(indexOfItemToDelete, 1);
    nutritionCalculator();
    if(cart.length == 0){
      document.querySelector('#record-nutrition').disabled = true;
    }
  });
}

// record button functionality onclick
document.querySelector('#record-nutrition').addEventListener('click',()=>{
  // creating hidden input field to store the ids of the selected food items
  inputField = document.createElement('input');
  inputField.setAttribute("name", "foodItems")
  inputField.setAttribute("type","text");
  inputField.hidden = true;
  let val = "";
  // adding values to a string with a space character in between them
  for (let counter=0; counter<cart.length; counter++){
    val = val + cart[counter]["food"].id + " ";
  }
  // removing the last white space from the newly created string
  val = val.substring(0, val.length-1);
  inputField.setAttribute('value', val);

  let serveSizeVal = "";
  // adding values to a string with a space character in between them
  for (let counter=0; counter<cart.length; counter++){
    serveSizeVal = serveSizeVal + cart[counter]["serve size"] + " ";
  }
  serveSizeVal = serveSizeVal.substring(0, val.length-1);

  form = document.querySelector('#nutritionIntakeForm');
  form.appendChild(inputField);
  if (document.querySelector('#datetimepicker1 .datetimepicker-input').value === ''){
    let error = document.createElement('p');
    error.append(document.createTextNode('**please select date first.'));
    error.setAttribute('color','red');
    error.setAttribute('id','error-tag');
    document.querySelector('#nutritionIntakeForm').appendChild(error);
  }
  else {
    if(form.elements['serveSize'] === ''){
      form.elements['serveSize'].value = 1;
    }
    if (cart.length) {
      form.elements['serveSize'].value = serveSizeVal;
      form.submit();
    }
    else{
      let error = document.createElement('p');
      error.append(document.createTextNode('**You have not selected any food item'));
      error.setAttribute('color','red');
      error.setAttribute('id','error-tag');
      document.querySelector('#nutritionIntakeForm').appendChild(error);
    }
  }
})

function totalNutrition() {
  let carbs = sugar = fat = protein = 0;
  for(let counter=0;counter<cart.length;counter++){
    carbs += cart[counter].carbohydrates_100g;
    sugar += cart[counter].sugars_100g;
    fat += cart[counter].fat_100g;
    protein += cart[counter].proteins_100g;
  }
  console.log(cabs + "KJ | " + sugar + "mg | ");
}

//==============================================================
//==== display the serving in the serving size input field =====
//==============================================================
let calServingSize = (serveSize) => {
  // fetch input field using query
  node = document.querySelector("input[name='serveSize']");
  // fetch unit measure using queryselector
  unitNode = document.querySelector('#units');
  // declaring the regular expression to be searched
  let re = /\d+/;
  // fetch numeric item based on regular expression
  numericValue = parseInt(re.exec(serveSize));
  if (serveSize.length === 0){
    node.value = 1;
  }
  else if(serveSize.match('g')){
    unitNode.innerHTML = " g";
    node.value = ""+numericValue;
  }
  else if(serveSize.match('ml') || serveSize.match('m')){
    unitNode.innerHTML = " ml";
    node.value = ""+numericValue;
  }
  else{
    unitNode.innerHTML = " qty";
    node.value = ""+numericValue;
  }
};

function setDashboard(data){
  currentData = data[data.length-1];
  nodeList = document.querySelectorAll('.card-text-header');
  valueList = document.querySelectorAll('.card-text-value');
  blockquoteList = document.querySelectorAll('.card-blockquotes');
  nodeList[0].firstChild.nodeValue = "2-h plasma glucose on ("+currentData.timestamp+")";
  nodeList[1].firstChild.nodeValue = "Fasting plasma glucose on ("+currentData.timestamp+")";
  nodeList[2].firstChild.nodeValue = "HbA1c on ("+currentData.timestamp+")";
  valueList[0].firstChild.nodeValue = currentData['h2_plasma_glucose']+" mmol/L";
  if (currentData['h2_plasma_glucose'] <= 11.1) {
    blockquoteList[0].firstChild.nodeValue = "No Risk: it's under 11.1 mmol/L";
  }else{
    blockquoteList[0].firstChild.nodeValue = "Risk: it's above 11.1 mmol/L";
  }
  valueList[1].firstChild.nodeValue = currentData['fasting_plasma_glucose']+" mmol/L";
  if(currentData['fasting_plasma_glucose'] < 7.0){
    blockquoteList[1].firstChild.nodeValue = "No Risk: it's under 7.0 mmol/L";
  }else{
    blockquoteList[1].firstChild.nodeValue = "Risk: it's above 7.0 mmol/L";
  }
  valueList[2].firstChild.nodeValue = currentData['hbA1c']+"%";
  if(currentData['hbA1c'] < 5.7){
    blockquoteList[2].firstChild.nodeValue = "No Risk: it's under 5.7 mmol/L";
  }else if(currentData['hbA1c'] >= 5.7 && currentData['hbA1c'] <= 6.4){
    blockquoteList[2].firstChild.nodeValue = "At Risk: it's between 5.7 and 6.4 mmol/L";
  }else{
    blockquoteList[2].firstChild.nodeValue = "High Risk: it's above 6.5 mmol/L";
  }
};

// loading data from medical db
function loadMedicalData(){
  const ENDPOINT = '/api/data/medical';
  let currentData = [];
  $.ajax ({
    method: "GET",
    url: ENDPOINT,
    success: function(data) {
      setDashboard(data);
    },
    error: function(error_data) {
      console.log("error")
      console.log(error_data)
    }
  });
}


function loadDashBoard(){
  // load medical data and poplate it
  loadMedicalData();
};

// =============================================================================
// ++++++++++++++++  H I S T O R Y - F I L E  ++++++++++++++++++++++++++++++++++
// =============================================================================

function createMedicalHistory(data) {
  const keys = Object.keys(data[0]);
  const ALIASKEYS = {"timestamp":"Date", "h2_plasma_glucose": "H2 Plasma Glucose", "fasting_plasma_glucose":"Fasting Plasma Glucose", "hbA1c":"HbA1c"};
  let parent = document.querySelector('#medical');
  let table = document.createElement('table');
  let tableBody = document.createElement('tbody');

  for (let i = 0; i < data.length; i++){

    let row = document.createElement('tr');

    if (i==0){
      let tableHeadRow = document.createElement('tr');;
      for (let i=0;i<keys.length;i++){
        let th = document.createElement('th');
        let thText = document.createTextNode(ALIASKEYS[keys[i]]);
        th.appendChild(thText);
        tableHeadRow.appendChild(th);
      }
      tableBody.appendChild(tableHeadRow);
    }

    for (let j=0;j<keys.length;j++){
        let cell = document.createElement('td');
        let cellText = document.createTextNode(data[i][keys[j]]);
        cell.appendChild(cellText);
        row.appendChild(cell);
    }
    tableBody.appendChild(row);
  }
  tableBody.setAttribute('class','w-100');
  table.appendChild(tableBody);
  table.setAttribute("class","table table-striped");
  parent.appendChild(table);
}

function createNutritionHistory(data) {
  let foodItemInfo = {};
  const ALIASKEYS = {"timestamp":"Date", "food_item": "Food Name", "server_size":"Serving Size"};
  const KEYS = Object.keys(ALIASKEYS);
  let parent = document.querySelector('#nutrition');
  let table = document.createElement('table');
  let tableBody = document.createElement('tbody');

  for (let i = 0; i < data.length; i++){

    let row = document.createElement('tr');
    if (i==0){
      let tableHeadRow = document.createElement('tr');;
      for (let j=0;j<KEYS.length;j++){
        let th = document.createElement('th');
        let thText = document.createTextNode(KEYS[j]);
        th.appendChild(thText);
        tableHeadRow.appendChild(th);
      }
      let th = document.createElement('th');
      th.appendChild(document.createTextNode("Nutrition"));
      tableHeadRow.appendChild(th);
      tableBody.appendChild(tableHeadRow);
    }

    for (let j=0;j<KEYS.length;j++){
        let cell = document.createElement('td');
        let cellText = document.createTextNode(data[i][KEYS[j]]);
        cell.appendChild(cellText);
        row.appendChild(cell);
    }
    let cell = document.createElement('td');
    let ENDPOINT = '/api/data/food/?search='+data[i]['food'];
    $.ajax ({
      method: "GET",
      url: ENDPOINT,
      success: function(data) {
        console.log(data);
        cell.appendChild(document.createTextNode("Carbohydrates: " + data[0].carbohydrates_100g + "\nSugar: " + data[0].sugars_100g + "\nProtein: " + data[0].proteins_100g));
        row.appendChild(cell);
      },
      error: function(error_data) {
        console.log("error")
        console.log(error_data)
      }
    });
    tableBody.appendChild(row);
  }
  tableBody.setAttribute('class','w-100');
  table.appendChild(tableBody);
  table.setAttribute("class","table table-striped");
  parent.appendChild(table);
}

function loadHistoryData(ep_url, callback){
  const ENDPOINT = ep_url;
  $.ajax ({
    method: "GET",
    url: ENDPOINT,
    success: function(data) {
      callback(data)
    },
    error: function(error_data) {
      console.log("error")
      console.log(error_data)
    }
  });
}

function loadHistory() {
  loadHistoryData('/api/data/medical', createMedicalHistory);
  loadHistoryData('/api/data/nutrition', createNutritionHistory);
}
