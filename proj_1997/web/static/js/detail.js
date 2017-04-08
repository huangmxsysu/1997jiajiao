$(document).ready(function() {
  $("body").backstretch("./static/img/blackboard.jpg");

  $(".time").click(function() {
    // $(".time.active").removeClass("active");
    $(this).toggleClass("active");
  });

  $("a.start").click(function() {
    if(!$(".time.active").length) {
      swal("请选择至少一个时段", "", "info");
      return false;
    }
    $(".row.reservation").show();
  });

  let set_warning_msg = function(msgs) {
    $(".warning > .list").empty("li");
    if (!msgs.length) {
      $("form.reservation").removeClass("warning");
      return;
    }
    $("form.reservation").addClass("warning");
    $(msgs).each(function(n, el) {
      $(".warning > .list").append("<li>" + el + "</li>");
    });
  }

  let check_phone_num = function(num) {
    let partten = /^1[0-9]\d{9}$/;
    let fl = false;
    if (partten.test(num)) {
      return true;
    } else {
      return false;
    }
  }

  let count_down_btn = function(t) {
    if (t === 0) {
      $("#send-code").removeClass("disabled");
      $("#send-code").text("发送验证码");
    } else {
      $("#send-code").text(t + "秒后重新发送");
      setTimeout(function() {
        count_down_btn(t - 1);
      }, 1000);
    }
  }

  let send_msg_to = function(phone_num) {
    $("#send-code").addClass("disabled");

    $.ajax({
      url: "/scode",
      type: "POST",
      dataType: "json",
      contentType: 'application/x-www-form-urlencoded; charset=utf-8',
      cache: false,
      data: {
        "phone_num": phone_num,
      },
      success: function(data) {
        if(data.code === 202) {
          count_down_btn(120 - data.delta);
        } else if(data.code) {
          swal('','发送验证码失败，请稍后再试。','info');
        } else {
          count_down_btn(120);
        }
      }
    });
  }

  let check_form_valid = function() {
    let msgs = [],
    phone_num = $("input[name='phone-num']").val();
    if(!$(".time.active").length) {
      msgs.push("请选择至少一个时段");
    }
    if (!phone_num.length) {
      msgs.push("请填写 手机号");
    } else if (!check_phone_num(phone_num)) {
      msgs.push("手机号格式不正确，应为11位数字");
    }
    if (!$("input[name='name']").val().length) {
      msgs.push("请填写 您的姓名");
    }
    if (!$("textarea[name='address']").val().length) {
      msgs.push("请填写 辅导地址");
    }
    if (!$("input[name='code']").val().length) {
      msgs.push("请填写 手机验证码");
    }
    set_warning_msg(msgs);

    return msgs.length === 0;
  }

  $("#send-code").click(function() {
    let msgs = [],
    phone_num = $("input[name='phone-num']").val();
    console.log(!phone_num.length);
    if (!phone_num.length) {
      msgs.push("请填写手机号");
    } else if (!check_phone_num(phone_num)) {
      msgs.push("手机号格式不正确，应为11位数字");
    } else {
      send_msg_to(phone_num);
    }

    set_warning_msg(msgs);
  });

  $("form.reservation input, form.reservation textarea").focusout(check_form_valid);

  let send_reservation = function() {
    let time_slot = [];
    $(".time.active").each(function(n, el) {
      time_slot.push($(el).text());
    });

    $.ajax({
      url: "/newrsv",
      type: "POST",
      dataType: "json",
      contentType: 'application/x-www-form-urlencoded; charset=utf-8',
      cache: false,
      data: {
        "id": $("input[name='teacher-id']").val(),
        "phone_num": $("input[name='phone-num']").val(),
        "name": $("input[name='name']").val(),
        "address": $("textarea[name='address']").val(),
        "code": $("input[name='code']").val(),
        "time_slot": JSON.stringify(time_slot),
      },
      success: function(data) {
        if(data.code) {
          set_warning_msg(data.msgs);
        } else {
          swal("预约成功", "我们的工作人员会尽快联系您，请保持电话畅通", "success");
        }
      },
      error: function() {
        swal("Oh...", "", "error");
      }
    });
  }

  $("#send-rsv").click(function() {
    if(check_form_valid()) {
      send_reservation();
    }
  });

});