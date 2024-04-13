// For Future Requirement
var message_list = []
$.ajax({
    url: "/get-messages",
    type: "POST",
    success: function (resp) {
        let count_val = 0
        for (var item in resp) {
            count_val = count_val + 1
        }
        let count_final = ""
        if (count_val > 5) {
            count_final = count_val - 5
        }
        else if (count_val <= 5) {
            count_final = 0
        }
        if (count_final == 0) {
            document.getElementsByClassName("showless").style.display = 'none'
            document.getElementsByClassName("showmore").style.display = 'none'
        }
        else {
            $(".showless").addClass("toblock")
        }
        for (var item in resp) {
            var to_message = "There is any problem in getting messages"
            if (resp[item]['importance'] == 'Login') {
                to_message = `Anyone has been login to your ID on <b>${resp[item]['message'].split(",")[1]}</b>`
            }
            else if (resp[item]['importance'] == 'Leave Class') {
                to_message = `You have been leaved the <b>${resp[item]['message'].split(",")[0]}</b> on <b>${resp[item]['message'].split(",")[1]}</b>`
            }
            else if (resp[item]['importance'] == 'Class Joined') {
                to_message = `You have been joined the <b>${resp[item]['message'].split(",")[0]}</b> on <b>${resp[item]['message'].split(",")[1]}</b>`
            }
            else if (resp[item]['importance'] == 'Test') {
                to_message = `Your <b>${resp[item]['message'].split(",")[0]}</b> Test has been schedule for the date <b>${resp[item]['message'].split(",")[1]}</b>`
            }
            else if (resp[item]['importance'] == 'Assignment') {
                to_message = `Your <b>${resp[item]['message'].split(",")[0]}</b> Assignment has been schedule for the date <b>${resp[item]['message'].split(",")[1]}</b>`
            }
            else if (resp[item]['importance'] == 'Cancelled') {
                to_message = `Your <b>${resp[item]['message'].split(",")[0]}</b> <b>${resp[item]['message'].split(",")[1]}</b> has been <b>cancelled</b>`
            }
            else if (resp[item]['importance'] == 'Date Changed') {
                to_message = `Your <b>${resp[item]['message'].split(",")[0]}</b> <b>${resp[item]['message'].split(",")[1]}</b> has been <b>changed to ${resp[item]['message'].split(",")[2]}</b>`
            }
            else if (resp[item]['importance'] == 'Password') {
                to_message = `Your <b>account</b> password has been changed on <b>${resp[item]['message'].split(",")[1]}</b>`
            }
            else if (resp[item]['importance'] == 'Missed') {
                to_message = `You have been <b>missed</b> the class <b>${resp[item]['message'].split(",")[0]}</b>`
            }
            else if (resp[item]['importance'] == 'Running') {
                to_message = `<b>${resp[item]['message'].split(",")[0]}</b> is<b> running </b>now.`
            }
            let item_top = `
                <tr id="${resp[item]['sno']}">
                    <td>${count_val}</td>
                    <td>${resp[item]['message'].split(",")[0]}</td>
                    <td>${to_message}</td>
                </tr>`
            $("#messages").prepend(item_top)
            if (count_val > 5) {
                message_list.push(resp[item]['sno'])
                $(`#${resp[item]['sno']}`).addClass("toblock")
                // document.getElementsByClassName("showmore").style.display = 'none'
            }
            else {

            }
            count_val = count_val - 1

        }
        message_list.reverse()

    },
    error: function () {
        alert("this is lert")
    }

})
