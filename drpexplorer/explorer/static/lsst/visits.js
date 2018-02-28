function getvisitinfo(thevisit) {
    $.get(`/visit/` + thevisit, function (visinfo) {
        var mydiv = document.getElementById("VisitInfoDiv");
        mydiv.innerHTML = visinfo;
    });
}
function getconfiginfo(theconfig) {
    $.get(`/config/` + theconfig, function (cfginfo) { 
        var mydiv = document.getElementById("ConfigInfoDiv");
        mydiv.innerHTML = cfginfo;
    });
}
function getschemainfo(theschema) {
    $.get(`/schema/` + theschema, function (schinfo) { 
        var mydiv = document.getElementById("SchemaInfoDiv");
        mydiv.innerHTML = schinfo;
    });
}