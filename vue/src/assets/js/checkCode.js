function check_syntax(code, result_cb) {
  //Example error for guideline
  var error_list = [{
    line_no: null,
    column_no_start: null,
    column_no_stop: null,
    fragment: null,
    message: null,
    severity: null
  }];

  //Push and replace errors
  function check(data) {
    //Clear array.
    error_list = [{
      line_no: null,
      column_no_start: null,
      column_no_stop: null,
      fragment: null,
      message: null,
      severity: null
    }]; //Check if pylint output is empty.
    if (data == null) {
      result_cb(error_list);
    } else {
      var data_length = 0;
      if (data != null) {
        data_length = Object.keys(data).length;
      }
      for (var x = 0; x < data_length; x += 1) {
        if (data[x] == null) {
          continue
        }
        number = data[x].line
        code = data[x].code
        codeinfo = data[x].error_info
        severity = code[0]
        moreinfo = data[x].message
        message = data[x].error

        //Set severity to necessary parameters
        if (severity == "E" || severity == "e") {
          severity = "error";
          severity_color = "red";
        } else if (severity == "W" || severity == "w") {
          severity = "warning";
          severity_color = "yellow";
        }
        //Push to error list
        error_list.push({
          line_no: number,
          column_no_start: null,
          column_no_stop: null,
          fragment: null,
          message: message,
          severity: severity
        });


      }
      result_cb(error_list);
    }
  }

  //AJAX call to pylint
  $.post('/check_code', {
    text: code
  }, function (data) {
    current_text = data;
    check(current_text);
    return false;
    }, 'json');

}
