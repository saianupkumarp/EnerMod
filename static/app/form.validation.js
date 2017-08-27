function validate(cols, model, sm, fnname) {
    var valid = true
    var msg="<ul class='list'>"
    if (model==0){
        msg+="<li>Please select a Model</li>"
        valid= false
    }
    if (sm==0){
        msg+="<li>Please select a Sub-Model</li>"
        valid= false
    }
    if (fnname==0){
        msg+="<li>Please select a Function</li>"
        valid= false
    }
    if (cols==0){
        msg+="<li>Please select atleast one Column</li>"
        valid= false
    }
    
    if (!valid)
        $(".ui.error.message").css("display", "block")
    else 
        $(".ui.error.message").css("display", "none")
    errMsg.innerHTML=msg+"</ul>"
    return valid
}