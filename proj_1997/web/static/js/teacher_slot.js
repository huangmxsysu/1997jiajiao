$(document).ready(function() {
    let search_teacher = function() {
        // $("tr.teacher").show();
        let k = $("input.search").val();
        // console.log(k);
        if(!k.length) {
            return true;
        }
        $("tr.teacher").each(function(n, el) {
            if($(el).find("td.name").text().indexOf(k) == -1 && 
                $(el).find("td.slots").text().indexOf(k) == -1 && 
                $(el).find("td.other").text().indexOf(k) == -1) {
                $(el).fadeOut("fast");
            } else {
                $(el).fadeIn();
            }
        });
    }

    $("button.search").click(search_teacher);
    $("input.search").keyup(search_teacher);

    $("table.sortable").tablesort();
});