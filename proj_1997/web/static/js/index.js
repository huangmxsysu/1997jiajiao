$(document).ready(function() {
    let get_sliders = function(selector) {
        let result = [];
        $(selector).find(".item").each(function(n, el) {
            result.push({
                image: $(el).find("img").attr("src"),
                content: $(el).find(".content").text()
            });
        });
        // $(selector).remove(".item");
        return result;
    }

    let start_slider = function(selector, sliders) {
        let delay = $(selector).find("input[name='delay']").val();
        let idx = 0;
        $(selector).backstretch(sliders[idx].image);
        $(selector).find(".sub-des").text(sliders[idx].content);

        setInterval(function() {
            idx++;
            if(idx == sliders.length) {
                idx = 0;
            }
            // $(selector).fadeOut();
            $(selector).backstretch(sliders[idx].image);
            $(selector).find(".sub-des").text(sliders[idx].content);
            // $(selector).fadeIn("slow");
        }, delay);
    }

    let reset_height_div = function(selector, w_div_h) {
        let width = $(selector).width();
        $(selector).height(width / w_div_h);
    }

    reset_height_div('div.slider', 16/9);
    let sliders = get_sliders("div.slider");
    // console.log(sliders);
    start_slider("div.slider", sliders);

    $(window).resize(function() {
        console.log('qqq');
        reset_height_div('div.slider', 16/9);
    });
})