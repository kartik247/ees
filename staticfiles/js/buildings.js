$(function(){
    $("#tab2").addClass('sidebar__item--selected');

    $("#addbgl").click(function() {
        $("#bglform").append('<tr><td><div class="form-group__text"><input type="text" placeholder="Specify name"></div></td><td><div class="form-group__text"><input type="number" placeholder="Floor count"></div></td><td></td></tr>');
    });

    $("#save").click(function() {
        var bglnames=[];
        $('#bglform tr td:nth-child(1) div input').each( function(){
           //add item to array
           bglnames.push( $(this).val() );
        });
        //console.log(bglnames);

        var flrcnt=[];
        $('#bglform tr td:nth-child(2) div input').each( function(){
           //add item to array
           flrcnt.push( $(this).val() );
        });
        //console.log(flrcnt);

        bgljson = {"items":[]};
        $.each( bglnames, function(i, item){
            bgljson.items.push(
                {"name": bglnames[i], "cnt": flrcnt[i]}
            );
        });
        console.log(bgljson);
        var datatosend = JSON.stringify(bgljson);
        //datatosend = JSON.parse(bgljson);
        console.log(datatosend);

        $.ajax({
            "type": "POST",
            "url": "/collector/savebuildingdata/",
            "data":  {'bgljson': datatosend, csrfmiddlewaretoken: '{{ csrf_token }}'},
            "success": function(response) {
               // console.log(response['lastid']);
                if(response.hasOwnProperty('errormsg')){
                  //  console.log("yes error");
                    var errormsg = response.errormsg;
                    alert(errormsg);
                }
                else{
                    //location.reload(true);
                    //$('#modal_loader').addClass('hide');
                    //window.location.reload(true);
                }
            }
        });

    });
});