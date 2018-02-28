function getvisitinfo(thevisit) {
    $.getJSON(`/visit/` + thevisit, function (visinfo) { 
        var mydiv = document.getElementById("VisitInfoDiv");
        mydiv.append(visitinfo);
    })
}
              
function getconfiginfo(thevisit) {
    $.getJSON(`/visit/` + thevisit, function (visinfo) { 
        var mydiv = document.getElementById("ConfigInfoDiv");
        mydiv.append(visitinfo);
    })
}
              