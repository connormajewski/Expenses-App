var menuDrop = document.getElementById("menu-drop");

var dropdownList = document.getElementById("dropdown-list");

function menuChange(x) {

    x.classList.toggle("change")

    if(menuDrop.style.height === "35%") {

      menuDrop.style.height = "0%"

      dropdownList.style.display = "none"

    }

    else {

      menuDrop.style.height = "35%"

      dropdownList.style.display = "block"

    }

}


function formValidation() {

    var form = document.getElementById("transaction");

    form.submit();

}