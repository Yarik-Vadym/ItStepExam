function updateElement() {
        $.ajax({
            url: "",
            success: function(data) {
                for (const [key, value] of Object.entries(data)) {
                    var resault_price = '#' + value.html_tag.price;
                    var resault_name = '#' + value.html_tag.name;
                    var resault_volume = '#' + value.html_tag.volume;
                    var resault_procent_change = '#' + value.html_tag.procent_change;
                    var resault_quote_volume = '#' + value.html_tag.quote_volume;
                    $(resault_price).html(value.price);
                    $(resault_name).html(value.name);
                    $(resault_volume).html(value.volume + ' ' + key);
                    $(resault_procent_change).html(value.procent_change);
                    $(resault_quote_volume).html(value.quote_volume);
                }
            }
        });
    }

    setInterval(updateElement, 1000 * 3); // Call updateElement every 3 minutes
