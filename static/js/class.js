var add_list = []
var classes_values_for_classes = ""
var url_for_classes = ""
var role_user = `{{current_user.role}}`
if (role_user == "Student") {
    url_for_classes = "/get-student-classes"
    $("#class_join").on("click", function (e) {
        window.location.href = "/join-class"
    })
}
else {
    url_for_classes = "/get-teacher-classes"
    $("#class_create").on("click", function (e) {
        window.location.href = "/create-class"
    })
}

// Side Class 

$.ajax({
    url: url_for_classes,
    type: "POST",
    success: function (resp) {
        if (resp != 'Problem') {
            classes_values_for_classes = resp
            for (item in classes_values_for_classes) {
                var vaaa_class_value = ""
                var to_vlass_name_text = ""
                if (role_user == 'Student') {
                    var real_text = classes_values_for_classes[item]['class_name'].trim()
                    var length_of_text = classes_values_for_classes[item]['class_name'].trim().length
                    if (length_of_text > 20) {
                        to_vlass_name_text = real_text.substr(0, 18) + "...."
                    }
                    else {
                        to_vlass_name_text = real_text
                    }
                }
                else {
                    var real_text = classes_values_for_classes[item]['class_name'].trim()
                    var length_of_text = (classes_values_for_classes[item]['class_name'].trim() + classes_values_for_classes[item]['class_standard']).length
                    if (length_of_text > 20) {
                        to_vlass_name_text = real_text.substr(0, 15) + "...." + classes_values_for_classes[item]['class_standard']
                    }
                    else {
                        to_vlass_name_text = real_text + classes_values_for_classes[item]['class_standard']
                    }

                }

                vaaa_class_value = `<div class="submenu collapsed" id="${classes_values_for_classes[item]['classid']}"">
                <a class="nav-link" href="/class/${classes_values_for_classes[item]['classid']}/">
                    <div class="nav-link-icon ">
                                <i-feather class="icon" style="width: 1rem !important;"><svg
                                        xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"
                                        class="feather feather-book-open">
                                        <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
                                        <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
                                    </svg></i-feather>
                            </div>
                    ${to_vlass_name_text}
                                </a>
                            </div >`
                $("#classes_content").append(vaaa_class_value)
            }
        }
        else {
            var vaaa_class_value = `<div class="submenu collapsed" id="${classes_values_for_classes[item]['classid']}"">
                <a class="nav-link">
                    <div class="nav-link-icon ">
                                <i-feather class="icon" style="width: 1rem !important;"><svg
                                        xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"
                                        class="feather feather-book-open">
                                        <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
                                        <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
                                    </svg></i-feather>
                            </div>Problem In getting Classes</a>
                            </div >`
            $("#classes_content").append(vaaa_class_value)
        }
    },
    error: function () {
        alert("Problem in getting classes")
    }
})
