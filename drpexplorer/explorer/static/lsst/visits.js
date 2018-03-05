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
function loadmyfile() {
    var myfile = document.getElementById("filetoload").value;
    $.getJSON(`/makelink/` + myfile, function (mylink) { JS9.Load(mylink['link'], {scale: 'log', zoom: 'to fit'}) });
}