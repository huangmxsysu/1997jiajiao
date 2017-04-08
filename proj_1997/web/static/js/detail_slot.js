$(document).ready(function() {
  $("#new-slot").click(function() {
    let row = $('<div class="ui row slot">\
      <div class="five wide column">\
      <div class="ui input fluid">\
      <input type="text">\
      </div>\
      </div>\
      <div class="four wide column">\
      <button class="ui button red basic delete">删除</button>\
      </div>\
      </div>');
    row.find("button.delete").click(function() {
      $(row).remove();
    })
    $(".grid.slots").append(row);
  });

  $("button.delete").on("click", function() {
    $(this).parents(".row.slot").remove();
  });

  let send_modi = function(qqq) {
    $.ajax({
      url: "/admin/d",
      type: "POST",
      dataType: "json",
      contentType: 'application/x-www-form-urlencoded; charset=utf-8',
      cache: false,
      data: {
        id: $("#slot-id").val(),
        slots: JSON.stringify(qqq),
      },
      success: function(data) {
        if(!data.code) {
          location.reload();
        } else {
          swal('网络错误');
        }
      }
    });
  }

  $("button.save").click(function() {
    let qqq = [];
    $(".row.slot").each(function(n, el) {
      let v = $(el).find("input").val();
      if(v.length) {
        qqq.push(v);
      }
    });
    console.log(qqq);
    send_modi(qqq);
  });
});