$(document).ready(function() {
    window.center_to_margin = function(child, par) {
        $(child).css({
            "margin-top": ($(par).height() - $(child).height()) / 2
        });
    }
    window.center_to_padding = function(child, par) {
        $(child).css({
            "padding-top": ($(par).height() - $(child).height()) / 2
        });
    }
})