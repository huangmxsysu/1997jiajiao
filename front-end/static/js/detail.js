$(document).ready(function() {
    $("body").backstretch("./static/img/blackboard.jpg");
    
    $(".time:not(.active)").click(function() {
        $(".time.active").removeClass("active");
        $(this).addClass("active");
    });

    $(".start").click(function() {
        if (!$(".time.active").length) {
            swal("", "请先选择一个时段", "info");
            return false;
        }


        swal({
            html: '<div class="ui grid">\
            <div class="ui row">\
            <div class="column fluid"><small>新用户需要填写姓名和地址哦，老用户我们已经保存了地址，不需更改就直接验证就好啦~</small></div>\
            </div>\
            <div class="ui row">\
            <div class="column four wide">手机号码</div>\
            <div class="column seven wide">\
            <div class="ui input mini fluid phone">\
            <input type="text">\
            </div>\
            </div>\
            <div class="column four wide">\
            <a href="#">发送验证码</a>\
            </div>\
            </div>\
            <div class="ui row">\
            <div class="column four wide">真实姓名</div>\
            <div class="column seven wide">\
            <div class="ui input mini fluid name">\
            <input type="text">\
            </div>\
            </div>\
            </div>\
            <div class="ui row">\
            <div class="column four wide">辅导地址</div>\
            <div class="column eleven wide">\
            <div class="ui input mini fluid address">\
            <input type="text">\
            </div>\
            </div>\
            </div>\
            <div class="ui row">\
            <div class="column four wide">验证码</div>\
            <div class="column six wide">\
            <div class="ui input mini fluid code">\
            <input type="text">\
            </div>\
            </div>\
            </div>\
            </div>',
            preConfirm: function() {
                return new Promise(function(resolve) {
                    resolve([
                        $('.input.phone').val(),
                        $('.input.name').val(),
                        $('.input.address').val(),
                        $('.input.code').val(),
                    ]);
                })
            }
        }).then(function(result) {
            // swal(JSON.stringify(result));
            swal("预定成功", "工作人员会尽快联系您", "success");
        }).catch(swal.noop)
    })
})