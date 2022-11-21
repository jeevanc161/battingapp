$(function () {
    var start = moment().subtract(29, "days");
    var end = moment();

    function cb(start, end) {
        var date_range = start.format("MMMM D, YYYY") + " - " + end.format("MMMM D, YYYY")
        console.log(date_range)

        $("#reportrange span").html(
            start.format("MMMM D, YYYY") + " - " + end.format("MMMM D, YYYY")
            
        );


      //   $.ajax({
      //   url: dashboard_url,

      //   data: {
      //     'start_date':  start.format("MMMM D, YYYY"),
      //     'end_date ' : end.format("MMMM D, YYYY"),
      //   },
      //   dataType: 'json', 

      //   success: function (data) {
      //     alert(data)
      //   },
      //   error: function (res) {
      //    alert(res.status);                                                                                                                          
      //  }
      // });



    }


    $("#reportrange").daterangepicker(
        {
            startDate: start,
            endDate: end,
            ranges: {
                Today: [moment(), moment()],
                Yesterday: [
                    moment().subtract(1, "days"),
                    moment().subtract(1, "days"),
                ],
                "Last 7 Days": [moment().subtract(6, "days"), moment()],
                "Last 30 Days": [moment().subtract(29, "days"), moment()],
                "This Month": [
                    moment().startOf("month"),
                    moment().endOf("month"),
                ],
                "Last Month": [
                    moment().subtract(1, "month").startOf("month"),
                    moment().subtract(1, "month").endOf("month"),
                ],
            },
        },
        cb
    );

    cb(start, end);
});


