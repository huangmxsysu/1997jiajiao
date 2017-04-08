$(document).ready(function() {

  let search_rsv = function() {
    // $("tr.teacher").show();
    let k = $("input.search").val();
    // console.log(k);
    if (!k.length) {
      $("tr.rsv").show();
      return true;
    }
    $("tr.rsv").each(function(n, el) {
      if ($(el).find("td.teacher-name").text().indexOf(k) == -1 &&
        $(el).find("td.slots").text().indexOf(k) == -1 &&
        $(el).find("td.guest-name").text().indexOf(k) == -1 &&
        $(el).find("td.guest-phone-num").text().indexOf(k) == -1 &&
        $(el).find("td.guest-address").text().indexOf(k) == -1 &&
        $(el).find("td.ctime").text().indexOf(k) == -1 &&
        $(el).find("td.status").text().indexOf(k) == -1) {
        $(el).fadeOut("fast");
      } else {
        $(el).fadeIn();
      }
    });
  }

  $("button.search").click(search_rsv);
  $("input.search").keyup(search_rsv);

  $("table.sortable").tablesort();

  // tab menu
  $('.tabular.menu .item').click(function() {
    $(".tabular.menu .item.active").removeClass('active');
    $(this).addClass('active');
    let status = $(this).text().trim();
    if (status === '全部') {
      $("tr.rsv").show();
      return true;
    }
    $("tr.rsv").each(function(n, el) {
      if ($(el).find("td.status").text().trim() != status) {
        $(el).fadeOut("fast");
      } else {
        $(el).fadeIn();
      }
    });
  });

  // set buttons
  let send_rsv_status = function(id, status) {
    $.ajax({
      url: "/admin/r/status",
      type: "POST",
      dataType: "json",
      contentType: 'application/x-www-form-urlencoded; charset=utf-8',
      cache: false,
      data: {
        "id": id,
        "status": status,
      },
      success: function(data) {
        if (data.code) {
          swal("网络错误", "", "info");
        } else {
          swal("修改成功", "", "success");
        }
      },
      error: function() {
        swal("Oh...", "", "error");
      }
    });
  }

  $("button.set-succeed").click(function() {
    let id = $(this).attr('rsv-id');
    send_rsv_status(id, 1);
    $(this).parents('tr.rsv').children('td.status').text('成功');
  });

  $("button.set-expired").click(function() {
    let id = $(this).attr('rsv-id');
    send_rsv_status(id, 2);
    $(this).parents('tr.rsv').children('td.status').text('失效');
  });
});